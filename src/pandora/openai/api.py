# -*- coding: utf-8 -*-

import asyncio
import json
import queue as block_queue
import threading
from requests.models import Response

# import httpx
# import requests
from curl_cffi import requests
from certifi import where

from .. import __version__
from ..exts.config import default_api_prefix
from .utils import Console
import logging
from ..exts.hooks import hook_logging
from ..exts.config import USER_CONFIG_DIR
from .pow import get_requirements_token, get_voice_url

from os import getenv
import os
import json
from datetime import datetime
from dateutil.tz import tzutc
import uuid
import time
import urllib.parse
from urllib.parse import quote
import base64
import hashlib
from binascii import hexlify
import traceback
import random
from dateutil.tz import tzlocal
from bs4 import BeautifulSoup   # func get_origin_share_data

if getenv('PANDORA_ISOLATION') == 'True' or (os.path.exists(USER_CONFIG_DIR + '/api.json') and getenv('PANDORA_OAI_ONLY') != 'True'):
    from ..transactions.module import LocalConversation
    from ..transactions.module import API_CONFIG_FILE, API_DATA


class API:
    def __init__(self, proxy, ca_bundle, req_timeout=60, LOCAL_OP=False, OAI_ONLY=False, PANDORA_DEBUG=False, ISOLATION_FLAG=False):
        # self.proxy = proxy    # httpx
        self.proxy = {
                        'http': proxy,
                        'https': proxy,
                    }if proxy else None
        self.ca_bundle = ca_bundle
        self.web_origin = ''
        self.LOCAL_OP = LOCAL_OP
        self.OAI_ONLY = OAI_ONLY
        self.req_timeout = req_timeout
        self.PANDORA_DEBUG = PANDORA_DEBUG
        self.ISOLATION_FLAG = ISOLATION_FLAG

        # curl_cffi
        if 'nt' == os.name:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    @staticmethod
    def error_fallback(content):
        resp = Response()
        resp.headers = {'Content-Type': 'text/event-stream;charset=UTF-8'}
        resp.status_code = 200

        if 'Failed to connect' in content and 'port' in content:
            content = 'Internal Error!'

        if isinstance(content, (dict, list)):
            content = json.dumps(content, ensure_ascii=False)

        error_content = 'System Error: \n' + content
        Console.warn(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + '{}'.format(error_content))
        msg_id = str(uuid.uuid4())
        create_time = int(time.time())
        fake_json = {"message": {"id": msg_id, "author": {"role": "assistant", "name": None, "metadata": {}}, "create_time": create_time, "update_time": None, "content": {"content_type": "text", "parts": [error_content]}, "status": "in_progress", "end_turn": None, "weight": 1.0, "metadata": {"citations": [], "gizmo_id": None, "message_type": "next", "parent_id": ""}, "recipient": "all"}, "error": error_content}

        resp_content = b'data: ' + json.dumps(fake_json, ensure_ascii=False).encode('utf-8') + b'\n\n' + b'data: [DONE]\n\n'
        resp._content = resp_content

        return resp
                    
    @staticmethod
    def wrap_stream_out(generator, status):
        if status != 200:
            for line in generator:
                yield json.dumps(line)

            return

        for line in generator:
            yield b'data: ' + json.dumps(line).encode('utf-8') + b'\n\n'

        yield b'data: [DONE]\n\n'


    async def __process_sse(self, resp, conversation_id=None, message_id=None, model=None, action=None, prompt=None, isolation_code=None):
        if resp.status_code != 200:
            Console.warn(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + f'Model: {model} | Status_Code: {str(resp.status_code)}')
            Console.warn(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + f'Resp: {str(resp.text)}')
            yield await self.__process_sse_except(resp)
            return
        
        BLOB_FLAGE = False
        headers_data = dict(resp.headers)
        # Console.debug_b('resp_headers_data: {}'.format(headers_data))
        if headers_data['content-type'].startswith('image/'):    # gan, cf返回的键名是小写
            BLOB_FLAGE = True
            img_type = headers_data['content-type'].split('/')[1]

        # 保证Headers: 'Content-Type':'text/event-stream;charset=UTF-8'
        # 否则如果直接透传，当某些API的响应头部'Content-Type'为json时，前端无法解析为SSE
        headers_data['Content-Type'] = 'text/event-stream;charset=UTF-8'
        headers_data['Transfer-Encoding'] = 'chunked'

        yield resp.status_code
        # yield resp.headers
        yield headers_data

        # Console.debug_b('__process_sse:status_code: {}'.format(resp.status_code))
        # Console.debug_b('__process_sse:headers: {}'.format(resp.headers))

        resp_content = ''
        yield_msg = ''
        official_title = ''
        create_time = None
        msg_id = None
        original_conv_id = conversation_id
        index = 0
        # SAVE_ASSISTANT_MSG = False
        msg_id = str(uuid.uuid4())
        create_time = int(time.time())

        if model == 'gpt-4o' and not self.LOCAL_OP and not self.OAI_ONLY: # 0516: 同时启用OAI与API模式时避免与OAI模型冲突
            if API_DATA and API_DATA.get(model):
                model = 'gpt-4o-api'

        SHOW_RESP_MSG = False  # dev

        if not BLOB_FLAGE:
            async for utf8_line in resp.aiter_lines():
                if isinstance(utf8_line, bytes):
                    utf8_line = utf8_line.decode('utf-8')

                # dev
                # Console.warn(utf8_line)
                
                # debug mode
                if not SHOW_RESP_MSG and self.PANDORA_DEBUG:
                    Console.warn(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + '{}'.format(utf8_line))
                    SHOW_RESP_MSG = True

                # 适配Real-Coze-API
                if '{"content"' == utf8_line[0:10] or b'{"content"' == utf8_line[0:10]:
                    for i in utf8_line.split('}'):
                        if i:
                            stream_data = json.loads(i + '}')
                            resp_content = stream_data['content']
                            # Console.debug_h('Coze => {}'.format(resp_content))
                            
                # 适配智谱CogView
                if '{"created"' == utf8_line[0:10] and 'cogview' in model:
                    resp_data = json.loads(utf8_line)
                    # resp_content = resp_data['url']
                    resp_content = '![img]({})'.format(resp_data['data'][0]['url'])

                if 'data: [DONE]' == utf8_line[0:12] or 'data: [DONE]' == utf8_line:
                    continue

                if 'data: ' in utf8_line[0:6]:
                    json_data = json.loads(utf8_line[6:])

                    # 适配3.5
                    if conversation_id is None and json_data.get('conversation_id'):
                        conversation_id = json_data['conversation_id']

                    # Official Title
                    if json_data.get('title'):
                        official_title = json_data.get('title')

                        # 创建隔离OAI对话
                        if not original_conv_id and self.ISOLATION_FLAG and isolation_code:
                            if self.OAI_ONLY or (API_DATA and API_DATA.get(model) is None):
                                Console.warn('OAI隔离模式, 创建对话')
                                LocalConversation.create_conversation(conversation_id, official_title, datetime.now(tzutc()).isoformat(), isolation_code)

                    # 0412: 为避免一些OAI接口返回重复id, 因此改为自主生成
                    # if json_data.get('id'):
                    #     msg_id = json_data['id']

                    if json_data.get('message'):
                        if json_data['message'].get('id'):
                            previous_msg_id = msg_id
                            msg_id = json_data['message']['id']

                        if json_data['message'].get('create_time'):
                            create_time = json_data['message']['create_time']
                    
                    if json_data.get('created'):
                        create_time = json_data['created']

                    if json_data.get('create_time'):
                        create_time = json_data['create_time']

                    # 适配cloudflare ai
                    if 'data: {"response":' == utf8_line[0:18]:
                        resp_content += json_data['response']

                    else:
                        if json_data.get('choices'):
                            if json_data['choices'][0].get('message'):
                                _resp_content = json_data['choices'][0]['message']['content']

                                if _resp_content:
                                    resp_content = _resp_content

                            if json_data['choices'][0].get('delta'):  # 适配GLM
                                try:
                                    _resp_content = json_data['choices'][0]['delta']['content']

                                    if _resp_content:
                                        resp_content += _resp_content
                                except KeyError:
                                    continue

                        # 适配3.5
                        elif json_data.get('message'):
                            if json_data['message'].get('content'):
                                if json_data['message']['content'].get('parts'):
                                    if not original_conv_id:
                                        ## 新对话
                                        if previous_msg_id == msg_id:
                                            resp_content = json_data['message']['content']['parts'][0]
                                    else:
                                        resp_content = json_data['message']['content']['parts'][0]

                # 适配Gemini
                if '"text": ' == utf8_line[12:20] and 'gemini' in model:
                    text_json = json.loads('{' + utf8_line[12:] + '}')
                    resp_content += text_json['text']

                # 适配Double
                if 'double' in model:
                    resp_content += utf8_line

                # 适配DALL·E
                if 'dall' in model:
                    if '      "revised_prompt": ' in utf8_line[0:25]:
                        resp_content += utf8_line[25:-2]

                    if '      "url": ' in utf8_line[0:14]:
                        resp_content += '![img]({})'.format(utf8_line[14:-1])

                
                if resp_content:
                    for char in resp_content[index:]:
                        yield_msg += char
                        fake_json = {"message": {"id": msg_id, "author": {"role": "assistant", "name": None, "metadata": {}}, "create_time": create_time, "update_time": None, "content": {"content_type": "text", "parts": [yield_msg]}, "status": "in_progress", "end_turn": None, "weight": 1.0, "metadata": {"citations": [], "gizmo_id": None, "message_type": "next", "model_slug": model, "parent_id": ""}, "recipient": "all"}, "conversation_id": conversation_id, "error": None}
                        index += 1

                        yield fake_json

        else:
            resp_content = await LocalConversation.save_image_file(resp, self.web_origin, msg_id, img_type)

            fake_json = {"message": {"id": msg_id, "author": {"role": "assistant", "name": None, "metadata": {}}, "create_time": create_time, "update_time": None, "content": {"content_type": "text", "parts": [resp_content]}, "status": "in_progress", "end_turn": None, "weight": 1.0, "metadata": {"citations": [], "gizmo_id": None, "message_type": "next", "model_slug": model, "parent_id": ""}, "recipient": "all"}, "conversation_id": conversation_id, "error": None}

            yield fake_json

        # Console.debug_b("End of assistant's answer, save assistant conversation.")

        if os.path.exists(USER_CONFIG_DIR + '/api.json') and not self.OAI_ONLY:
            if API_DATA.get(model):
                LocalConversation.save_conversation(conversation_id, msg_id, resp_content, 'assistant', datetime.now(tzutc()).isoformat(), model, action)
        
        # 创建隔离OAI对话(当无title生成时的兜底策略)
        if not original_conv_id and self.ISOLATION_FLAG and isolation_code:
            if self.OAI_ONLY or (API_DATA and API_DATA.get(model) is None):
                if not official_title:
                    official_title = prompt
                    Console.warn('OAI隔离模式, 创建对话(无title生成)')
                    LocalConversation.create_conversation(conversation_id, prompt, datetime.now(tzutc()).isoformat(), isolation_code)
  
    async def __process_sse_origin(self, resp):
        yield resp.status_code
        yield resp.headers

        if resp.status_code != 200:
            yield await self.__process_sse_except(resp)
            return

        async for utf8_line in resp.aiter_lines():
            if 'data: [DONE]' == utf8_line[0:12]:
                break

            if 'data: {"message":' == utf8_line[0:17] or 'data: {"id":' == utf8_line[0:12]:
                yield json.loads(utf8_line[6:])

    @staticmethod
    async def __process_sse_except(resp):
        result = b''
        # async for line in resp.aiter_bytes(): # httpx
        async for line in resp.aiter_lines():
            result += line

        return json.loads(result.decode('utf-8'))

    @staticmethod
    def __generate_wrap(queue, thread, event):
        while True:
            try:
                item = queue.get()
                if item is None:
                    break

                yield item
            except BaseException as e:
                event.set()
                thread.join()

                if isinstance(e, GeneratorExit):
                    raise e

    # async def _do_request_sse_httpx(self, url, headers, data, queue, event, conversation_id=None, message_id=None, model=None, action=None, prompt=None):
    #     try: 
    #         proxy = API_DATA[model].get('proxy')
    #     except KeyError:
    #         proxy = None

    #     async with httpx.AsyncClient(verify=self.ca_bundle, proxies=proxy if proxy else self.proxy) as client:
    #         async with client.stream('POST', url, json=data, headers=headers, timeout=600) as resp:
    #             async for line in self.__process_sse(resp, conversation_id, message_id, model, action, prompt):
    #                 queue.put(line)

    #                 if event.is_set():
    #                     await client.aclose()
    #                     break

    #             queue.put(None)

    async def _do_request_sse(self, url, headers, data, queue, event, conversation_id=None, message_id=None, model=None, action=None, prompt=None, isolation_code=None):
        proxy = None
        if os.path.exists(USER_CONFIG_DIR + '/api.json') and not getenv('PANDORA_OAI_ONLY'):
            if API_DATA.get(model):
                proxy_url = API_DATA[model].get('proxy')
                proxy = {
                            "http": proxy_url,
                            "https": proxy_url,
                        }if 'proxy' in API_DATA[model] else None
        try:
            async with requests.AsyncSession(verify=self.ca_bundle, proxies=proxy if proxy else self.proxy, impersonate='chrome110') as client:
                async with client.stream('POST', url, json=data, headers=headers, timeout=60 if not self.req_timeout else self.req_timeout, http_version=1) as resp:
                    async for line in self.__process_sse(resp, conversation_id, message_id, model, action, prompt, isolation_code):
                        queue.put(line)

                        if event.is_set():
                            # await client.aclose()     # httpx
                            await client.close()
                            break

                    queue.put(None)

        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('_do_request_sse FAILED: {}'.format(e))

            return self.error_fallback('Internal Error!') 

    def _request_sse(self, url, headers, data, conversation_id=None, message_id=None, model=None, action=None, prompt=None, isolation_code=None):
        if self.PANDORA_DEBUG:
            data_str = json.dumps(data, ensure_ascii=False)[:500]
            Console.debug(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + 'data: {}'.format(data_str)) # dev

        queue, e = block_queue.Queue(), threading.Event()
        t = threading.Thread(target=asyncio.run, args=(self._do_request_sse(url, headers, data, queue, e, conversation_id, message_id, model, action, prompt, isolation_code),))
        t.start()

        return queue.get(), queue.get(), self.__generate_wrap(queue, t, e)



class ChatGPT(API):
    def __init__(self, access_tokens: dict, proxy=None, req_timeout=60, LOCAL_OP=False, OAI_ONLY=False, PANDORA_DEBUG=False, ISOLATION_FLAG=False):
        self.access_tokens = access_tokens
        self.access_token_key_list = list(access_tokens)
        self.default_token_key = self.access_token_key_list[0]
        self.session = requests.Session()
        self.req_kwargs = {
            'proxies': {
                'http': proxy,
                'https': proxy,
            } if proxy else None,
            'verify': where(),
            'timeout': req_timeout,
            'allow_redirects': False,
            'impersonate': 'chrome110',
        }

        access_token_file = os.path.join(USER_CONFIG_DIR, 'access_token.dat')
        access_token_file_exists = os.path.isfile(access_token_file)
        if access_token_file_exists:
            with open(access_token_file, 'r', encoding='utf-8') as f:
                self.access_token_key_list = [line.strip() for line in f.readlines()]
                Console.success(f'Access Token Count: {len(self.access_token_key_list)}')
        if self.access_token_key_list:
            def __auth_generator(auth_list):
                while True:
                    for auth in auth_list:
                        yield auth
            self.access_token_key_iter = __auth_generator(self.access_token_key_list)

        # self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
        #                   'Pandora/{} Safari/537.36'.format(__version__)
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        self.FILE_SIZE_LIMIT = int(getenv('PANDORA_FILE_SIZE')) if getenv('PANDORA_FILE_SIZE') else None
        self.OAI_Device_ID = uuid.uuid4()
        PANDORA_TYPE_WHITELIST = getenv('PANDORA_TYPE_WHITELIST')
        PANDORA_TYPE_BLACKLIST = getenv('PANDORA_TYPE_BLACKLIST')
        self.UPLOAD_TYPE_WHITELIST = []
        self.UPLOAD_TYPE_BLACKLIST = []
        self.MODELS_LIST = []
        self.MODELS_ICONS = []
        self.VOICE_STATUS = getenv('OAI_VOICE', 'False')
        
        # if getenv('PANDORA_OAI_ONLY') != 'True' or self.ISOLATION_FLAG == 'True':
        #     LocalConversation.initialize_database()

        if ISOLATION_FLAG or not OAI_ONLY:
            global API_DATA
            # Console.warn('Initialize LocalConversation Database')
            LocalConversation.initialize_database()
            API_DATA = LocalConversation.initialize_model()

        if PANDORA_TYPE_WHITELIST:
            self.UPLOAD_TYPE_WHITELIST = PANDORA_TYPE_WHITELIST.split(',')
            # Console.warn(f"PANDORA_TYPE_WHITELIST: {self.UPLOAD_TYPE_WHITELIST}")

        if PANDORA_TYPE_BLACKLIST:
            self.UPLOAD_TYPE_BLACKLIST = PANDORA_TYPE_BLACKLIST.split(',')
            # Console.warn(f"PANDORA_TYPE_BLACKLIST: {self.UPLOAD_TYPE_BLACKLIST}")

        self.log_level = logging.INFO
        hook_logging(level=self.log_level, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger('waitress')

        super().__init__(proxy, self.req_kwargs['verify'], req_timeout, LOCAL_OP, OAI_ONLY, PANDORA_DEBUG, ISOLATION_FLAG)

        if self.req_timeout:
            self.req_kwargs['timeout'] = self.req_timeout

    def __get_headers(self, token_key=None, OAI_Device_ID=None):
        # return {
        #     'Authorization': 'Bearer ' + self.get_access_token(token_key),
        #     'User-Agent': self.user_agent,
        #     'Content-Type': 'application/json',
        # }

        if getenv('OPENAI_DEVICE_ID'):
            OAI_Device_ID = getenv('OPENAI_DEVICE_ID')

        if not OAI_Device_ID:
            OAI_Device_ID = self.OAI_Device_ID

        headers = {
                    "Accept":"*/*",
                    "Accept-Encoding":"gzip, deflate, br, zstd",
                    "Accept-Language":"en-US,en;q=0.9",
                    "Authorization":'Bearer ' + self.get_access_token(token_key),
                    "Cache-Control":"no-cache",
                    "Content-Type":"application/json",
                    "Oai-Device-Id":str(OAI_Device_ID),
                    "Oai-Language":"en-US",
                    # "Origin":"https://chatgpt.com",
                    "Pragma":"no-cache",
                    "Sec-Ch-Ua":'"Google Chrome";v="110", "Not:A-Brand";v="8", "Chromium";v="110"',
                    "Sec-Ch-Ua-Mobile":"?0",
                    "Sec-Ch-Ua-Platform":'"Windows"',
                    "Sec-Fetch-Dest":"empty",
                    "Sec-Fetch-Mode":"cors",
                    "Sec-Fetch-Site":"same-origin",
                    "User-Agent":self.user_agent
        }

        return headers

    @staticmethod
    def __get_api_prefix():
        return getenv('OPENAI_API_PREFIX', default_api_prefix())
    
    def __get_api_req_kwargs(self, model):
        req_kwargs = self.req_kwargs
        proxy_url = API_DATA[model].get('proxy')
        proxy = {
                    "http": proxy_url,
                    "https": proxy_url,
                }if 'proxy' in API_DATA[model] else None
        
        if proxy:
            req_kwargs['proxies'] = proxy

        return req_kwargs

    def fake_resp(self, origin_resp=None, fake_data=None):
        fake_resp = Response()
        # Console.debug_b('fake_data: {}'.format(fake_data))
        fake_resp._content = fake_data.encode('utf-8')

        if origin_resp:
            fake_resp.headers = origin_resp.headers
            fake_resp.status_code = origin_resp.status_code
        else:
            fake_resp.headers = {'Content-Type': 'application/json'}
            fake_resp.status_code = 200

        fake_resp.encoding = 'utf-8'

        # Console.debug_b('fake_resp: ')
        # print(fake_resp.json())

        return fake_resp

    def get_access_token(self, token_key=None):
        return self.access_tokens[token_key or self.default_token_key]

    def refresh_model(self, token_key=None):
        global API_DATA

        try:
            API_DATA = LocalConversation.initialize_model()

            # 清空缓存
            self.MODELS_LIST = None
            self.MODELS_ICONS = None

            # Console.warn(API_DATA.keys())
            return self.fake_resp(fake_data=json.dumps({"msg": "Succeeded"}, ensure_ascii=False))

        except Exception as e:
            return self.fake_resp(fake_data=json.dumps({"msg": f"Failed: {str(e)}"}, ensure_ascii=False))
    
    def double_generate_token(self, model, double_api_key):
        url = 'https://api.double.bot/api/auth/refresh'
        headers = {'Authorization': 'Bearer ' + double_api_key, 'User-Agent': self.user_agent}

        resp = self.session.post(url=url, headers=headers, **self.__get_api_req_kwargs(model))

        if resp.status_code == 200:
            access_token = resp.json().get('access_token')

            return access_token
        
        else:
            raise Exception('Double generate token failed: ' + self.__get_error(resp.text))

    def list_token_keys(self):
        return self.access_token_key_list

    def model_icons(self, raw=False, token=None):
        # if self.MODELS_ICONS:
        #     return self.fake_resp(fake_data=json.dumps(self.MODELS_ICONS, ensure_ascii=False))

        if not self.MODELS_ICONS and (not self.OAI_ONLY and API_DATA):
            self.MODELS_ICONS = {}
            icons = {
                'best': {
                    "icon_filled_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 36 36\" fill=\"none\" width=\"32\" height=\"32\"><path fill=\"currentColor\" d=\"m7.358 14.641 5.056-5.055A2 2 0 0 1 13.828 9h8.343a2 2 0 0 1 1.414.586l5.056 5.055a2 2 0 0 1 .055 2.771l-9.226 9.996a2 2 0 0 1-2.94 0l-9.227-9.996a2 2 0 0 1 .055-2.77Zm6.86-1.939-.426 1.281a2.07 2.07 0 0 1-1.31 1.31l-1.28.426a.296.296 0 0 0 0 .561l1.28.428a2.07 2.07 0 0 1 1.31 1.309l.427 1.28c.09.27.471.27.56 0l.428-1.28a2.07 2.07 0 0 1 1.309-1.31l1.281-.427a.296.296 0 0 0 0-.56l-1.281-.428a2.07 2.07 0 0 1-1.309-1.309l-.427-1.28a.296.296 0 0 0-.561 0z\"></path></svg>",

                    "icon_outline_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 36 36\" fill=\"none\" width=\"32\" height=\"32\"><path fill=\"currentColor\" d=\"m7.358 14.641 5.056-5.055A2 2 0 0 1 13.828 9h8.343a2 2 0 0 1 1.414.586l5.056 5.055a2 2 0 0 1 .055 2.771l-9.226 9.996a2 2 0 0 1-2.94 0l-9.227-9.996a2 2 0 0 1 .055-2.77Zm6.86-1.939-.426 1.281a2.07 2.07 0 0 1-1.31 1.31l-1.28.426a.296.296 0 0 0 0 .561l1.28.428a2.07 2.07 0 0 1 1.31 1.309l.427 1.28c.09.27.471.27.56 0l.428-1.28a2.07 2.07 0 0 1 1.309-1.31l1.281-.427a.296.296 0 0 0 0-.56l-1.281-.428a2.07 2.07 0 0 1-1.309-1.309l-.427-1.28a.296.296 0 0 0-.561 0z\"></path></svg>"
                },
                'stars': {
                    "icon_filled_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M19.92.897a.447.447 0 0 0-.89-.001c-.12 1.051-.433 1.773-.922 2.262-.49.49-1.21.801-2.262.923a.447.447 0 0 0 0 .888c1.035.117 1.772.43 2.274.922.499.49.817 1.21.91 2.251a.447.447 0 0 0 .89 0c.09-1.024.407-1.76.91-2.263.502-.502 1.238-.82 2.261-.908a.447.447 0 0 0 .001-.891c-1.04-.093-1.76-.411-2.25-.91-.493-.502-.806-1.24-.923-2.273ZM11.993 3.82a1.15 1.15 0 0 0-2.285-.002c-.312 2.704-1.115 4.559-2.373 5.817-1.258 1.258-3.113 2.06-5.817 2.373a1.15 1.15 0 0 0 .003 2.285c2.658.3 4.555 1.104 5.845 2.37 1.283 1.26 2.1 3.112 2.338 5.789a1.15 1.15 0 0 0 2.292-.003c.227-2.631 1.045-4.525 2.336-5.817 1.292-1.291 3.186-2.109 5.817-2.336a1.15 1.15 0 0 0 .003-2.291c-2.677-.238-4.529-1.056-5.789-2.34-1.266-1.29-2.07-3.186-2.37-5.844Z\"/></svg>",

                    "icon_outline_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M19.898.855a.4.4 0 0 0-.795 0c-.123 1.064-.44 1.802-.943 2.305-.503.503-1.241.82-2.306.943a.4.4 0 0 0 .001.794c1.047.119 1.801.436 2.317.942.512.504.836 1.241.93 2.296a.4.4 0 0 0 .796 0c.09-1.038.413-1.792.93-2.308.515-.516 1.269-.839 2.306-.928a.4.4 0 0 0 .001-.797c-1.055-.094-1.792-.418-2.296-.93-.506-.516-.823-1.27-.941-2.317Z\"/><path fill=\"currentColor\" d=\"M12.001 1.5a1 1 0 0 1 .993.887c.313 2.77 1.153 4.775 2.5 6.146 1.34 1.366 3.3 2.223 6.095 2.47a1 1 0 0 1-.003 1.993c-2.747.238-4.75 1.094-6.123 2.467-1.373 1.374-2.229 3.376-2.467 6.123a1 1 0 0 1-1.992.003c-.248-2.795-1.105-4.754-2.47-6.095-1.372-1.347-3.376-2.187-6.147-2.5a1 1 0 0 1-.002-1.987c2.818-.325 4.779-1.165 6.118-2.504 1.339-1.34 2.179-3.3 2.504-6.118A1 1 0 0 1 12 1.5ZM6.725 11.998c1.234.503 2.309 1.184 3.21 2.069.877.861 1.56 1.888 2.063 3.076.5-1.187 1.18-2.223 2.051-3.094.871-.87 1.907-1.55 3.094-2.05-1.188-.503-2.215-1.187-3.076-2.064-.885-.901-1.566-1.976-2.069-3.21-.505 1.235-1.19 2.3-2.081 3.192-.891.89-1.957 1.576-3.192 2.082Z\"/></svg>"
                },
                'star': {
                    "icon_filled_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M12.001 1.75c.496 0 .913.373.969.866.306 2.705 1.126 4.66 2.44 6 1.31 1.333 3.223 2.17 5.95 2.412a.976.976 0 0 1-.002 1.945c-2.682.232-4.637 1.067-5.977 2.408-1.34 1.34-2.176 3.295-2.408 5.977a.976.976 0 0 1-1.945.002c-.243-2.727-1.08-4.64-2.412-5.95-1.34-1.314-3.295-2.134-6-2.44a.976.976 0 0 1-.002-1.94c2.75-.317 4.665-1.137 5.972-2.444 1.307-1.307 2.127-3.221 2.444-5.972a.976.976 0 0 1 .971-.864Z\"/></svg>",

                    "icon_outline_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M12.001 1.5a1 1 0 0 1 .993.887c.313 2.77 1.153 4.775 2.5 6.146 1.34 1.366 3.3 2.223 6.095 2.47a1 1 0 0 1-.003 1.993c-2.747.238-4.75 1.094-6.123 2.467-1.373 1.374-2.229 3.376-2.467 6.123a1 1 0 0 1-1.992.003c-.248-2.795-1.105-4.754-2.47-6.095-1.372-1.347-3.376-2.187-6.147-2.5a1 1 0 0 1-.002-1.987c2.818-.325 4.779-1.165 6.118-2.504 1.339-1.34 2.179-3.3 2.504-6.118A1 1 0 0 1 12 1.5ZM6.725 11.998c1.234.503 2.309 1.184 3.21 2.069.877.861 1.56 1.888 2.063 3.076.5-1.187 1.18-2.223 2.051-3.094.871-.87 1.907-1.55 3.094-2.05-1.188-.503-2.215-1.187-3.076-2.064-.885-.901-1.566-1.976-2.069-3.21-.505 1.235-1.19 2.3-2.081 3.192-.891.89-1.957 1.576-3.192 2.082Z\"/></svg>"
                },
                'faster': {
                    "icon_filled_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M12.566 2.11c1.003-1.188 2.93-.252 2.615 1.271L14.227 8h5.697c1.276 0 1.97 1.492 1.146 2.467L11.434 21.89c-1.003 1.19-2.93.253-2.615-1.27L9.772 16H4.076c-1.276 0-1.97-1.492-1.147-2.467L12.565 2.11Z\" clip-rule=\"evenodd\"/></svg>",
                    
                    "icon_outline_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M13.091 4.246 4.682 14H11a1 1 0 0 1 .973 1.23l-1.064 4.524L19.318 10H13a1 1 0 0 1-.973-1.229l1.064-4.525Zm-.848-2.08c1.195-1.386 3.448-.238 3.029 1.544L14.262 8h5.056c1.711 0 2.632 2.01 1.514 3.306l-9.075 10.528c-1.195 1.386-3.448.238-3.029-1.544L9.738 16H4.681c-1.711 0-2.632-2.01-1.514-3.306l9.075-10.527Z\"/></svg>"
                }
            }

            for alias in API_DATA.keys():
                item = API_DATA[alias]
                icon_type = item.get('icon', 'stars')
                self.MODELS_ICONS[alias] = icons.get(icon_type, 'stars')

        return self.fake_resp(fake_data=json.dumps(self.MODELS_ICONS, ensure_ascii=False))

    
    def list_models(self, raw=False, token=None, web_origin=None, gpt35_model=None, gpt4_model=None):
        self.web_origin = web_origin
        OAI_FLAG = False
        global API_DATA

        if self.MODELS_LIST:
            # Console.debug('MODELS_LIST 缓存')

            return self.fake_resp(fake_data=json.dumps(self.MODELS_LIST, ensure_ascii=False))

        else:
            if getenv('PANDORA_OLD_CHAT') != 'True' and getenv('PANDORA_CLASSIC') != 'True':
                NEW_CHAT_PAGE = True
            else:
                NEW_CHAT_PAGE = False

            result = {
                "models": [],
                "categories": [
                    {
                        "category": "gpt_3.5",
                        "human_category_name": "GPT-3.5",
                        "subscription_level": "free",
                        "default_model": gpt35_model if gpt35_model else "text-davinci-002-render-sha",
                        "code_interpreter_model": gpt35_model if gpt35_model else "text-davinci-002-render-sha-code-interpreter",
                        "plugins_model": gpt35_model if gpt35_model else "text-davinci-002-render-sha-plugins"
                    },
                    {
                        "category": "gpt_4",
                        "human_category_name": "GPT-4",
                        "subscription_level": "free",
                        "default_model": gpt4_model if gpt4_model else ("gpt-4o" if not self.LOCAL_OP else "gpt-4"),
                        "plugins_model": gpt4_model if gpt4_model else ("gpt-4o" if not self.LOCAL_OP else "gpt-4")
                    }
                ] if not NEW_CHAT_PAGE else []
            }

            if not gpt35_model or OAI_FLAG:
                result['models'].append({
                    "slug": "text-davinci-002-render-sha",
                    "max_tokens": 8191,
                    "title": "Default (GPT-3.5)",
                    "description": "Our fastest model, great for most everyday tasks.",
                    "tags": [
                        "gpt3.5"
                    ],
                    "capabilities": {},
                    "product_features": {}
                })

            # if OAI_GPT4O_FLAG:
            if not self.LOCAL_OP:
                result['models'].append({
                    "slug": "gpt-4o",
                    "max_tokens": 8191,
                    "title": "GPT-4o",
                    "description": "Newest and most advanced model",
                    # "enabled_tools": [
                    #     "tools",
                    #     "tools2"
                    # ],
                    "tags": [
                        "gpt3.5"
                    ],
                    "capabilities": {},
                    # "product_features": {"attachments":{"type":"retrieval","accepted_mime_types":["text/javascript","text/x-c","text/x-c++","application/msword","application/vnd.openxmlformats-officedocument.presentationml.presentation","text/plain","text/x-sh","application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/x-latext","text/x-php","application/pdf","application/json","text/x-script.python","text/x-ruby","text/html","text/x-tex","text/x-typescript","text/x-java","text/x-csharp","text/markdown"],"image_mime_types":["image/gif","image/webp","image/png","image/jpeg"],"can_accept_all_mime_types":True}} if self.OAI_ONLY else {}
                    "product_features": {}
                })


            if not self.OAI_ONLY and API_DATA:
                for alias in API_DATA.keys():
                    item = API_DATA[alias]
                    title = item['title']
                    slug = 'gpt-4o-api' if item['slug'] == 'gpt-4o' and not self.LOCAL_OP else alias
                    description = item['description']
                    max_tokens = item['max_tokens']

                    if NEW_CHAT_PAGE:
                        category_json = {
                            "category": slug,
                            "human_category_name": title,
                            "human_category_short_name": title,
                            "color": "#00BCE5",
                            "icon": "stars",
                            "icon_outline_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M19.898.855a.4.4 0 0 0-.795 0c-.123 1.064-.44 1.802-.943 2.305-.503.503-1.241.82-2.306.943a.4.4 0 0 0 .001.794c1.047.119 1.801.436 2.317.942.512.504.836 1.241.93 2.296a.4.4 0 0 0 .796 0c.09-1.038.413-1.792.93-2.308.515-.516 1.269-.839 2.306-.928a.4.4 0 0 0 .001-.797c-1.055-.094-1.792-.418-2.296-.93-.506-.516-.823-1.27-.941-2.317Z\"/><path fill=\"currentColor\" d=\"M12.001 1.5a1 1 0 0 1 .993.887c.313 2.77 1.153 4.775 2.5 6.146 1.34 1.366 3.3 2.223 6.095 2.47a1 1 0 0 1-.003 1.993c-2.747.238-4.75 1.094-6.123 2.467-1.373 1.374-2.229 3.376-2.467 6.123a1 1 0 0 1-1.992.003c-.248-2.795-1.105-4.754-2.47-6.095-1.372-1.347-3.376-2.187-6.147-2.5a1 1 0 0 1-.002-1.987c2.818-.325 4.779-1.165 6.118-2.504 1.339-1.34 2.179-3.3 2.504-6.118A1 1 0 0 1 12 1.5ZM6.725 11.998c1.234.503 2.309 1.184 3.21 2.069.877.861 1.56 1.888 2.063 3.076.5-1.187 1.18-2.223 2.051-3.094.871-.87 1.907-1.55 3.094-2.05-1.188-.503-2.215-1.187-3.076-2.064-.885-.901-1.566-1.976-2.069-3.21-.505 1.235-1.19 2.3-2.081 3.192-.891.89-1.957 1.576-3.192 2.082Z\"/></svg>",
                            "icon_filled_src": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" d=\"M19.92.897a.447.447 0 0 0-.89-.001c-.12 1.051-.433 1.773-.922 2.262-.49.49-1.21.801-2.262.923a.447.447 0 0 0 0 .888c1.035.117 1.772.43 2.274.922.499.49.817 1.21.91 2.251a.447.447 0 0 0 .89 0c.09-1.024.407-1.76.91-2.263.502-.502 1.238-.82 2.261-.908a.447.447 0 0 0 .001-.891c-1.04-.093-1.76-.411-2.25-.91-.493-.502-.806-1.24-.923-2.273ZM11.993 3.82a1.15 1.15 0 0 0-2.285-.002c-.312 2.704-1.115 4.559-2.373 5.817-1.258 1.258-3.113 2.06-5.817 2.373a1.15 1.15 0 0 0 .003 2.285c2.658.3 4.555 1.104 5.845 2.37 1.283 1.26 2.1 3.112 2.338 5.789a1.15 1.15 0 0 0 2.292-.003c.227-2.631 1.045-4.525 2.336-5.817 1.292-1.291 3.186-2.109 5.817-2.336a1.15 1.15 0 0 0 .003-2.291c-2.677-.238-4.529-1.056-5.789-2.34-1.266-1.29-2.07-3.186-2.37-5.844Z\"/></svg>",
                            "subscription_level": "plus",
                            "default_model": slug,
                            "code_interpreter_model": slug,
                            "plugins_model": slug,
                            "short_explainer": description,
                            "tagline": description
                        }

                        result['categories'].append(category_json)

                    model_json = {
                        "capabilities": {},
                        "description": description,
                        "enabled_tools": [
                            "tools",
                            "tools2"
                        ],
                        "max_tokens": max_tokens,
                        "product_features": {},
                        "slug": slug,
                        "tags": [
                            "gpt3.5"
                        ],
                        "title": title
                    }

                    if item.get('upload'):
                        if item['upload'] == 'only_image':
                            model_json['product_features'] = {
                                "attachments": {
                                    "type": "retrieval",
                                    "image_mime_types": [
                                        "image/png",
                                        "image/gif",
                                        "image/webp",
                                        "image/jpeg"
                                    ],
                                    "can_accept_all_mime_types": False
                                }
                            }

                        if item['upload'] == 'true' or item['upload'] == True:
                            model_json['product_features'] = {
                                "attachments": {
                                    "type": "retrieval",
                                    "accepted_mime_types": [
                                        "text/html",
                                        "application/msword",
                                        "text/x-csharp",
                                        "text/x-sh",
                                        "text/markdown",
                                        "application/pdf",
                                        "text/javascript",
                                        "text/x-java",
                                        "text/x-ruby",
                                        "text/x-script.python",
                                        "text/x-php",
                                        "application/json",
                                        "application/x-latext",
                                        "text/x-c",
                                        "text/x-c++",
                                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        "text/x-tex",
                                        "text/plain",
                                        "text/x-typescript",
                                        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                    ],
                                    "image_mime_types": [
                                        "image/png",
                                        "image/gif",
                                        "image/webp",
                                        "image/jpeg"
                                    ],
                                    "can_accept_all_mime_types": True
                                }
                            }


                    result['models'].append(model_json)

            result['categories'].reverse()
            self.MODELS_LIST = result

            return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))

    def list_conversations(self, offset, limit, raw=False, token=None, isolation_code=None):
        OAI_ERROR_FLAG = False
        if not self.LOCAL_OP and not self.ISOLATION_FLAG:
            # url = '{}/api/conversations?offset={}&limit={}'.format(self.__get_api_prefix(), offset, limit)
            url = '{}/backend-api/conversations?offset={}&limit={}&order=updated'.format(self.__get_api_prefix(), offset, limit)
            try:
                resp = self.session.get(url=url, headers=self.__get_headers(token), **self.req_kwargs)

                if resp.status_code == 200:
                    result = resp.json()

                    if self.OAI_ONLY:
                        return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))
                else:
                    Console.warn(f'list_conversations: resp.status_code={str(resp.status_code)}')
                    Console.warn(f'list_conversations: resp.text={str(resp.text)}')
                    OAI_ERROR_FLAG = True

            except Exception as e:
                error_detail = traceback.format_exc()
                Console.debug(error_detail)
                Console.warn('list_conversations FAILED: {}'.format(e))
                OAI_ERROR_FLAG = True

                if self.OAI_ONLY:
                    return

        if self.LOCAL_OP or self.ISOLATION_FLAG or OAI_ERROR_FLAG == True:
            result = {
                'has_missing_conversations': False,
                'items': [],
                'limit': int(limit),
                'offset': int(offset),
                'total': 0,
            }

        convs_data = LocalConversation.list_conversations(offset, limit, isolation_code)
        # Console.debug_b('Local conversation list: {}'.format(convs_data))
        if convs_data:
            convs_data_total = convs_data['total']

            if convs_data.get('list_data'):
                for item in convs_data['list_data']:
                    # if item['visible'] == 1 or item['visible'] == '1':    # 0516: MasterCode可查看已隐藏的对话
                        id = item['id']
                        title = item['title'] if item['visible'] == 1 or item['visible'] == '1' else '🔒'+item['title']
                        create_time = item['create_time']
                        update_time = item['update_time']

                        final_item = {
                            "id": id,
                            "title": title,
                            "create_time": create_time,
                            "update_time": update_time,
                            "mapping": None,
                            "current_node": None,
                            "conversation_template_id": None,
                            "gizmo_id": None,
                            "is_archived": False,
                            "workspace_id": None
                        }

                        # final_item_json = json.dumps(final_item, ensure_ascii=False)
                        result['items'].append(final_item)

                # 对话列表按更新时间'update_time'倒序重新排序
                result['items'] = sorted(result['items'], key=lambda item: item['update_time'], reverse=True)

                if not self.LOCAL_OP and not self.ISOLATION_FLAG and OAI_ERROR_FLAG == False:
                    result['total'] = convs_data_total if convs_data_total > result['total'] else result['total']

                    return self.fake_resp(resp, json.dumps(result, ensure_ascii=False))
                    # return self.fake_resp(resp, result)
                else:
                    # from datetime import timezone
                    # now = datetime.now(timezone.utc).isoformat()
                    ## 当获取oai对话列表失败时, 在对话列表中插入警告项
                    # warning_item = {
                    #         "id": "warning",
                    #         "title": "!!! Get oai convs list failed !!!",
                    #         "create_time": now,
                    #         "update_time": now,
                    #         "mapping": None,
                    #         "current_node": None,
                    #         "conversation_template_id": None,
                    #         "gizmo_id": None,
                    #         "is_archived": False,
                    #         "workspace_id": None
                    #     }
                    # result['items'].insert(0, warning_item)

                    result['total'] = convs_data_total

                    return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))
                
        return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))

    def register_websocket(self, request, token=None):
        if self.LOCAL_OP:
            return 404
        
        try:
            url = '{}/backend-api/register-websocket'.format(self.__get_api_prefix())
            data = request.data
            headers = self.__get_headers(token)

            if url.startswith('https://chat.openai.com') or url.startswith('https://chatgpt.com'):
                headers['Origin'] = 'https://chatgpt.com'
            
            resp = self.session.post(url=url, headers=self.__get_headers(token), data=data, **self.req_kwargs)

            if resp.status_code == 200:
                Console.warn('register_websocket SUCCESS')
                return resp
            else:
                Console.warn('register_websocket FAILED: Status_Code={} | Content_Type={}'.format(str(resp.status_code), resp.headers.get('Content-Type')))
                return 404
                
        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('register_websocket FAILED: {}'.format(e))
            return 404
    
    def arkose_dx(self, request, token=None):
        url = '{}/backend-api/sentinel/arkose/dx'.format(self.__get_api_prefix())
        data = request.data
        resp = self.session.post(url=url, headers=self.__get_headers(token), data=data, **self.req_kwargs)

        return resp

    def get_conversation(self, conversation_id, raw=False, token=None, isolation_code=None):
        # if self.ISOLATION_FLAG or os.path.exists(API_CONFIG_FILE) or not self.OAI_ONLY:
        if self.ISOLATION_FLAG or not self.OAI_ONLY:
            # conversation_info = LocalConversation.check_conversation_exist(conversation_id, isolation_code)
            # if conversation_info:
            #     return LocalConversation.get_conversation(conversation_id, isolation_code)
            
            # 不检查对话是否存在, 直接请求对话详情. 2024-05-05
            conversation_detail = LocalConversation.get_conversation(conversation_id, isolation_code)
            if conversation_detail:
                return conversation_detail

        # url = '{}/api/conversation/{}'.format(self.__get_api_prefix(), conversation_id)
        url = '{}/backend-api/conversation/{}'.format(self.__get_api_prefix(), conversation_id)
        resp = self.session.get(url=url, headers=self.__get_headers(token), **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('get conversation failed: ' + self.__get_error(resp))

        return resp.json()

    # 新ui已无清空对话功能
    def clear_conversations(self, raw=False, token=None):
        data = {
            'is_visible': False,
        }

        url = '{}/backend-api/conversations'.format(self.__get_api_prefix())
        resp = self.session.patch(url=url, headers=self.__get_headers(token), json=data, **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('clear conversations failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'success' not in result:
            raise Exception('clear conversations failed: ' + resp.text)

        return result['success']

    def del_conversation(self, conversation_id, raw=False, token=None, isolation_code=None):
        if self.LOCAL_OP:
            return LocalConversation.del_conversation(conversation_id, False, isolation_code)
        
        if self.ISOLATION_FLAG or not self.OAI_ONLY:
            if not self.LOCAL_OP or self.ISOLATION_FLAG:
                EXIT_FLAG = LocalConversation.check_conversation_exist(conversation_id)

                if EXIT_FLAG:
                    return LocalConversation.del_conversation(conversation_id, False, isolation_code)
                else:
                    LocalConversation.del_conversation(conversation_id, True)   # 0516: 完全删除OAI对话, 无视是否隐藏对话式删除

        data = {
            'is_visible': False,
        }

        return self.__update_conversation(conversation_id, data, raw, token)

    def gen_conversation_title(self, conversation_id, message_id, raw=False, token=None):
        if self.LOCAL_OP:
            return 404
        
        url = '{}/backend-api/conversation/gen_title/{}'.format(self.__get_api_prefix(), conversation_id)
        data = {
            'message_id': message_id,
        }
        resp = self.session.post(url=url, headers=self.__get_headers(token), json=data, **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('gen title failed: ' + self.__get_error(resp))

        result = resp.json()

        if self.OAI_ONLY:
            return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))

        if 'title' not in result:
            raise Exception('gen title failed: ' + resp.text)

        return result['title']

    def set_conversation_title(self, conversation_id, title, raw=False, token=None):
        if self.LOCAL_OP:
            return LocalConversation.rename_conversation(title, conversation_id)
        
        if self.ISOLATION_FLAG or not self.OAI_ONLY:
            if not self.LOCAL_OP or self.ISOLATION_FLAG:
                EXIT_FLAG = LocalConversation.check_conversation_exist(conversation_id)

                if EXIT_FLAG:
                    return LocalConversation.rename_conversation(title, conversation_id)
                else:
                    LocalConversation.rename_conversation(title, conversation_id)
            
        data = {
            'title': title,
        }

        return self.__update_conversation(conversation_id, data, raw, token)
    
    
    def file_start_upload(self, file_name, file_size, web_origin=None, payload=None, token=None):
        if self.OAI_ONLY:
            url = '{}/backend-api/files'.format(self.__get_api_prefix())
            resp = self.session.post(url=url, headers=self.__get_headers(token), json=payload, **self.req_kwargs)

            if resp.status_code == 200:
                Console.warn('file_start_upload SUCCESS')
                result = resp.json()
                Console.warn('file_start_upload result: {}'.format(result))
                upload_url = result.get('upload_url')
                fake_upload_url = web_origin + '/files/' + upload_url.split('/', maxsplit=3)[-1]
                result['upload_url'] = fake_upload_url

                return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))
            
            else:
                Console.warn('file_start_upload FAILED: ' + self.__get_error(resp))
                return self.fake_resp(fake_data=json.dumps({'code': resp.status_code, 'message':'file_start_upload failed!'}))


        file_type = file_name.split('.')[-1].lower()
        # Console.warn('file_type: {}'.format(file_type))
        if self.UPLOAD_TYPE_WHITELIST and file_type not in self.UPLOAD_TYPE_WHITELIST:
            return self.fake_resp(fake_data=json.dumps({'code': 403, 'message':'File type not supported!'}))
        
        if self.UPLOAD_TYPE_BLACKLIST and file_type in self.UPLOAD_TYPE_BLACKLIST:
            return self.fake_resp(fake_data=json.dumps({'code': 403, 'message':'File type not supported!'}))

        if self.FILE_SIZE_LIMIT:
            try:
                file_size_MB = int(file_size) / 1024 / 1024
                if file_size_MB > self.FILE_SIZE_LIMIT:
                    return self.fake_resp(fake_data=json.dumps({'code': 403, 'message':'File size exceeds the limit!'}))
                
            except Exception as e:
                error_detail = traceback.format_exc()
                Console.debug(error_detail)
                Console.warn('file_upload FAILED: {}'.format(e))

                return self.fake_resp(fake_data=json.dumps({f'code': 403, 'message':'file_start_upload FAILED: {e}'}))

        file_id = 'file-' + str(uuid.uuid4()).replace('-', '')
        LocalConversation.create_file_upload(file_id, file_name, file_size, datetime.now(tzutc()).isoformat())

        data = {
            "status": "success",
            "upload_url": (web_origin if web_origin else self.web_origin) + '/files/' + file_id,
            "file_id": file_id
        }

        return self.fake_resp(fake_data=json.dumps(data, ensure_ascii=False))
    
    def file_upload(self, file_id, file_type, file, req_path_with_args, original_headers, token=None):
        if self.OAI_ONLY:
            url = 'https://files.oaiusercontent.com/{}'.format(req_path_with_args)
            op_header = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Access-Control-Request-Headers': 'content-type,x-ms-blob-type,x-ms-version',
                'Headers': '',
                'Access-Control-Request-Method': 'PUT',
                'Cache-Control': 'no-cache',
                'Origin': 'https://chatgpt.com',
                'Pragma': 'no-cache',
                'Priority': 'u=1, i',
                'Referer': 'https://chatgpt.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': self.user_agent
            }
            Console.warn(url)
            op_resp = self.session.options(url=url, headers=op_header, **self.req_kwargs)

            if op_resp.status_code == 200:
                Console.warn('file_upload_options SUCCESS')
                # return 201

            else:
                Console.warn('file_upload_options FAILED: ' + self.__get_error(op_resp))
                error_response = Response()
                error_response.status_code = op_resp.status_code
                error_response._content = op_resp.content
                error_response.headers = {'Content-Type': op_resp.headers.get('Content-Type')}

                return error_response

            put_header = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                # 'Authorization': 'Bearer ' + self.get_access_token(token),
                'Cache-Control': 'no-cache',
                'Content-Type': file_type,
                'Origin': 'https://chatgpt.com',
                'Pragma': 'no-cache',
                'Priority': 'u=1, i',
                'Referer': 'https://chatgpt.com/',
                'Sec-Ch-Ua': self.user_agent,
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': self.user_agent,
                'X-Ms-Blob-Type': 'BlockBlob',
                'X-Ms-Version': '2020-04-08'
            }
            Console.debug(put_header)

            put_resp = self.session.put(url=url, headers=put_header, data=file, **self.req_kwargs)

            if put_resp.status_code == 200 or put_resp.status_code == 201:
                Console.warn('file_upload_put SUCCESS')
                return 201

            else:
                Console.warn('file_upload_put FAILED: ' + self.__get_error(put_resp))
                error_response = Response()
                error_response.status_code = put_resp.status_code
                error_response._content = put_resp.content
                error_response.headers = {'Content-Type': op_resp.headers.get('Content-Type')}

                return error_response


        if self.FILE_SIZE_LIMIT:
            try:
                file_size_MB = int(len(file)) / 1024 / 1024
                if file_size_MB > self.FILE_SIZE_LIMIT:
                    return self.fake_resp(fake_data=json.dumps({'code': 500, 'message':'File size exceeds the limit!'}))
                
            except Exception as e:
                error_detail = traceback.format_exc()
                Console.debug(error_detail)
                Console.warn('file_upload FAILED: {}'.format(e))

                return self.fake_resp(fake_data=json.dumps({f'code': 500, 'message':'file_upload FAILED: {e}'}))
            
        # Console.warn('file_size: {}'.format(len(file)))
        LocalConversation.save_file_upload(file_id, file_type, file)

        return 201
    
    def file_ends_upload(self, file_id, web_origin, token=None):
        if self.OAI_ONLY:
            url = '{}/backend-api/files/{}/uploaded'.format(self.__get_api_prefix(), file_id)
            resp = self.session.post(url=url, headers=self.__get_headers(token), json={}, **self.req_kwargs)

            if resp.status_code == 200:
                Console.warn('file_ends_upload SUCCESS')
                result = resp.json()
                Console.warn('file_ends_upload result: {}'.format(result))
                download_url = result.get('download_url')
                fake_download_url = web_origin + '/files/' + download_url.split('/', maxsplit=3)[-1]
                result['download_url'] = fake_download_url

                return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))
            
            else:
                Console.warn('file_ends_upload FAILED: ' + self.__get_error(resp))
                return self.fake_resp(fake_data=json.dumps({'code': resp.status_code, 'message':'file_ends_upload failed!'}))


        file_name, file_size, file_type, create_time = LocalConversation.get_file_upload_info(file_id)

        data = {
            "status": "success",
            "download_url": (web_origin if web_origin else self.web_origin) + '/files/' + file_id+'/' + file_name,
            "metadata": None,
            "file_name": file_name,
            "creation_time": create_time
        }

        return self.fake_resp(fake_data=json.dumps(data, ensure_ascii=False))
    
    def file_upload_download(self, file_id, web_origin, token=None):
        if self.OAI_ONLY:
            url = '{}/backend-api/files/{}/download'.format(self.__get_api_prefix(), file_id)
            resp = self.session.post(url=url, headers=self.__get_headers(token), json={}, **self.req_kwargs)

            if resp.status_code == 200:
                Console.warn('file_upload_download SUCCESS')
                result = resp.json()
                Console.warn('file_upload_download result: {}'.format(result))
                download_url = result.get('download_url')
                fake_download_url = web_origin + '/files/' + download_url.split('/', maxsplit=3)[-1]
                result['download_url'] = fake_download_url

                return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))
            
            else:
                Console.warn('file_upload_download FAILED: ' + self.__get_error(resp))
                return self.fake_resp(fake_data=json.dumps({'code': resp.status_code, 'message':'file_upload_download failed!'}))

        file_name, file_size, file_type, create_time = LocalConversation.get_file_upload_info(file_id)

        data = {
            "status": "success",
            "download_url": (web_origin if web_origin else self.web_origin) + '/files/' + file_id+'/' + file_name,
            "metadata": {},
            "file_name": file_name,
            "creation_time": create_time
        }

        return self.fake_resp(fake_data=json.dumps(data, ensure_ascii=False))
    
    def get_file_upload_info(self, file_id, token=None):
        if self.OAI_ONLY:
            url = '{}/backend-api/files/{}'.format(self.__get_api_prefix(), file_id)
            resp = self.session.post(url=url, headers=self.__get_headers(token), json={}, **self.req_kwargs)

            if resp.status_code == 200:
                Console.warn('get_file_upload_info SUCCESS')
                result = resp.json()

                return self.fake_resp(fake_data=json.dumps(result, ensure_ascii=False))
            
            else:
                Console.warn('file_upload_download FAILED: ' + self.__get_error(resp))
                return self.fake_resp(fake_data=json.dumps({'code': resp.status_code, 'message':'file_upload_download failed!'}))

        file_name, file_size, file_type, create_time = LocalConversation.get_file_upload_info(file_id)

        file_name, file_size, file_type, create_time = LocalConversation.get_file_upload_info(file_id)

        data = {
            "id": file_id,
            "name": file_name,
            "creation_time": create_time.split('T')[0],
            "state": "ready",
            "ready_time": create_time.split('+00:00')[0],
            "size": file_size,
            "metadata": {
                "retrieval": {
                    "status": "success",
                    "file_size_tokens": 500
                }
            },
            "use_case": "my_files",
            "retrieval_index_status": "success",
            "file_size_tokens": 500,
            "variants": None
        }

        return self.fake_resp(fake_data=json.dumps(data, ensure_ascii=False))
    

    def oai_file_proxy(self, file_id, req_path_with_args, original_headers, token=None):
        url = 'https://files.oaiusercontent.com//{}'.format(req_path_with_args)
        header = {
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization':'Bearer ' + self.get_access_token(token),
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Priority': 'u=1, i',
                'Referer': 'https://chatgpt.com/',
                'Sec-Ch-Ua': self.user_agent,
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': "Windows",
                'Sec-Fetch-Dest': 'image',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': self.user_agent,
            }
        
        resp = self.session.get(url=url, headers=header, **self.req_kwargs)
        if resp.status_code == 200:
            Console.warn('oai_file_proxy SUCCESS')
            return Response(resp.content, mimetype=resp.headers['Content-Type'])
        
        else:
            Console.warn('oai_file_proxy FAILED: ' + self.__get_error(resp))
            return Response(resp.text, status=resp.status_code)


    # def talk(self, prompt, model, message_id, parent_message_id, conversation_id=None, stream=True, token=None):
    def talk(self, payload, stream=True, token=None, web_origin=None, isolation_code=None):
        if web_origin:
            self.web_origin = web_origin

        if payload.get('messages'):
            action = payload['action']
            parts = payload['messages'][0]['content']['parts']
            content = str(parts[0]) if len(parts) == 1 else str(parts[-1])
            model = payload['model']
            message_id = payload['messages'][0]['id']
        else:
            payload['action'] = 'next'
            action = 'next'
            parts = payload['prompt']
            content = str(parts)
            model = payload['model']
            message_id = payload['message_id']

        if model == 'gpt-4o-api':
            model = 'gpt-4o'
        
        conversation_id = payload.get('conversation_id')
        parent_message_id = payload['parent_message_id']

        data = {
            'action': action if action else 'next',
            'messages': [
                {
                    'id': message_id,
                    'role': 'user',
                    'author': {
                        'role': 'user',
                    },
                    'content': {
                        'content_type': 'text',
                        'parts': parts if isinstance(parts, list) else [parts],
                    },
                    'metadata': payload['messages'][0].get('metadata', {}) if payload.get('messages') else {},
                }
            ],
            'model': model,
            'parent_message_id': parent_message_id,
        }

        if conversation_id:
            data['conversation_id'] = conversation_id

        return self.__request_conversation(data, token, isolation_code)

    def oai_voice_status(self, token=None):
        data = {"status": True if self.VOICE_STATUS == 'True' else False}
        return self.fake_resp(fake_data=json.dumps(data, ensure_ascii=False))

    def oai_voice(self, model, token=None):
        if self.access_token_key_list and len(self.access_token_key_list) >=1:
            try:
                acccess_token = next(self.access_token_key_iter)
                Console.success(f'oai_voice get access_token[-10:]: {acccess_token[-10:]}')

                voice_mode = 'standard'
                if 'gpt-4' in model:
                    if 'gpt-4o' not in model:
                        voice_mode = 'advanced'
                else:
                    voice_mode = 'standard'

                voice_url = get_voice_url(acccess_token, voice_mode)
                data = {"url": voice_url}

            except Exception as e:
                error_detail = traceback.format_exc()
                Console.debug(error_detail)
                Console.warn('oai_voice FAILED: {}'.format(e))
                data = {"url": None}

        else:
            data = {"url": None}

        return self.fake_resp(fake_data=json.dumps(data, ensure_ascii=False))

    
    def __proof_token(self, seed, diff):
        fake_config = self.__chat_requirements(GET_FAKE_CONFIG=True)
        diff_len = len(diff) // 2
        hasher = hashlib.sha3_512()
        
        for i in range(100000):
            fake_config[3] = i
            config_encode = json.dumps(fake_config).encode('utf-8')
            base = base64.standard_b64encode(config_encode).decode('utf-8')
            hasher.update((seed + base).encode('utf-8'))
            hash = hasher.digest()
            hasher = hashlib.sha3_512()  # 重置hasher
            if hexlify(hash[:diff_len]).decode('utf-8') <= diff:
                return "gAAAAAB" + base
            
        return ("gAAAAABwQ8Lk5FbGpA2NcR9dShT6gYjU7VxZ4D" + 
                base64.standard_b64encode(json.dumps(seed).encode('utf-8')).decode('utf-8'))
    
    def __chat_requirements(self, token=None, OAI_Device_ID=None, GET_FAKE_CONFIG=False):
        headers=self.__get_headers(token, OAI_Device_ID)
        headers['Dnt'] = '1'
        headers['Origin'] = 'https://chatgpt.com'

        cores = [8, 12, 16, 24]
        screens = [3000, 4000, 6000]
        random.seed(int(time.time() * 1e9))
        core = random.choice(cores)
        screen = random.choice(screens)
        now = datetime.now(tzlocal())
        timeLayout = "%a %b %d %Y %H:%M:%S %Z"
        parse_time = now.strftime(timeLayout)
        fake_config = [
            core + screen,
            parse_time,
            4294705152,
            0,
            self.user_agent,
            "https://cdn.oaistatic.com/_next/static/2E3kyHMTDQPAokpbyfwns/_ssgManifest.js?dpl=ebab7301ae39fe916a5e1ce6d894b31921d5d573",
            "dpl=ebab7301ae39fe916a5e1ce6d894b31921d5d573",
            "zh-CN",
            "zh-CN, zh"
        ]

        if GET_FAKE_CONFIG:
            return fake_config

        fake_config_encode = json.dumps(fake_config).encode()
        fake_data_base64_string = base64.b64encode(fake_config_encode).decode()
        fake_data = {'p': 'gAAAAAC' + fake_data_base64_string} 

        url = 'https://chatgpt.com/backend-api/sentinel/chat-requirements'
        resp = self.session.post(url=url, headers=headers, json=fake_data, **self.req_kwargs)

        if resp.status_code == 200:
            resp_data = resp.json()
            # Console.warn(resp_data)
            fallback_data = {'Openai-Sentinel-Chat-Requirements-Token': resp_data['token']}

            if resp_data.get('proofofwork'):
                if resp_data['proofofwork']['required'] == True:
                    seed = resp_data['proofofwork']['seed']
                    diff = resp_data['proofofwork']['difficulty']
                    proff_token = self.__proof_token(seed, diff)
                    fallback_data['Openai-Sentinel-Proof-Token'] = proff_token
                
            return fallback_data

        else:
            Console.warn('chat_requirements FAILED: resp.status_code={}'.format(resp.status_code))
            Console.warn('chat_requirements FAILED: {}'.format(resp.text))

        return resp.json()['token']

    def chat_ws(self, payload, token=None, OAI_Device_ID=None, isolation_code=None):
        if self.LOCAL_OP:
            return API.error_fallback('OAI not supported!')

        try:
            url = '{}/backend-api/conversation'.format(self.__get_api_prefix())
            # url = 'https://chatgpt.com/backend-api/conversation'
            headers = self.__get_headers(token, OAI_Device_ID)
            headers['Dnt'] = '1'

            if url.startswith('https://chat.openai.com') or url.startswith('https://chatgpt.com'):
                chat_requirements_data = self.__chat_requirements(token, OAI_Device_ID)
                headers['Openai-Sentinel-Chat-Requirements-Token'] = chat_requirements_data['Openai-Sentinel-Chat-Requirements-Token']
                if chat_requirements_data.get('Openai-Sentinel-Proof-Token'):
                    headers['Openai-Sentinel-Proof-Token'] = chat_requirements_data['Openai-Sentinel-Proof-Token']
            # Console.warn('chat_ws:headers SUCCESS')

            headers['Accept'] = 'text/event-stream'
            model = payload['model']
            if model == 'auto':
                payload['model'] = 'gpt-4o'

            # resp = self.session.post(url=url, headers=headers, json=payload, **self.req_kwargs)

            # if resp.status_code == 200:
            #     Console.warn('chat_ws SUCCESS')
            #     return resp
            # else:
            #     Console.warn('chat_ws SUCCESS')
            #     Console.warn('chat_ws FAILED: Status_Code={} | Content_Type={}'.format(str(resp.status_code), resp.headers.get('Content-Type')))
            #     Console.warn('chat_ws FAILED: {}'.format(resp.text))
            
            # return API.error_fallback(resp.text)
                
            if payload.get('messages'):
                action = payload['action']
                parts = payload['messages'][0]['content']['parts']
                content = str(parts[0]) if len(parts) == 1 else str(parts[-1])
                model = payload['model']
                # model = 'auto'
                message_id = payload['messages'][0]['id']

            else:
                payload['action'] = 'next'
                action = 'next'
                parts = payload['prompt']
                content = payload['prompt']
                model = payload['model']
                message_id = payload['message_id']

            parent_message_id = payload['parent_message_id']

            data = {
                    'action': action if action else 'next',
                    'messages': [
                        {
                            'id': message_id,
                            'role': 'user',
                            'author': {
                                'role': 'user',
                            },
                            'content': {
                                'content_type': 'text',
                                'parts': parts if isinstance(parts, list) else [parts],
                            },
                            'metadata': payload['messages'][0].get('metadata', {}) if payload.get('messages') else {},
                        }
                    ],
                    'model': model,
                    'parent_message_id': parent_message_id,
                }
        
            conversation_id = payload.get('conversation_id')

            if conversation_id:
                data['conversation_id'] = conversation_id

            return self._request_sse(url, headers, data, conversation_id, message_id, model, action, content, isolation_code)
        
        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('chat_ws FAILED: {}'.format(e))

            return API.error_fallback('Error: {}'.format(e))
    
    def get_text_gen_img_prompt(self, content, url, prompt_model, gen_img_model=None):
        auth = LocalConversation.get_auth(prompt_model)
        origin_prompt = API_DATA[gen_img_model].get('prompt')
        # Console.debug_b('prompt_model: {} | prompt_model_auth: {} | gen_img_model: {}'.format(prompt_model, auth, gen_img_model))
        
        if origin_prompt:
            prompt_content = origin_prompt.replace('<Prompt>', content)

            if origin_prompt == prompt_content:
                prompt_content += content

        else:
            prompt_content = content

        prompt_data = { "messages": [{ "role": "user", "content": prompt_content }]}
        headers = {'User-Agent': self.user_agent, 'Content-Type': 'application/json'}

        if not prompt_model.startswith('@cf'):
            prompt_data['model'] = prompt_model

            if 'glm' in prompt_model and prompt_model != 'glm-free-api':
                auth = LocalConversation.glm_generate_token(auth, 3600)

            if 'double' in prompt_model:
                double_api_key = auth
                auth = self.double_generate_token(prompt_model, double_api_key)
                headers['double-version'] = '2024-03-04'

                prompt_data['api_key'] = double_api_key
                prompt_data['chat_model'] = 'GPT4 Turbo' if 'GPT' in prompt_model or 'gpt' in prompt_model else 'Claude 3 (Opus)'
                del prompt_data['model']

                for item in prompt_data['messages']:
                    if item.get('content'):
                        item['message'] = item['content']
                        del item['content']

                    if item['role'] == 'user':
                        item['codeContexts'] = []

            if 'gemini' in prompt_model:
                headers = {'User-Agent': self.user_agent, 'Content-Type': 'application/json'}
                prompt_data = {"contents":[]}

                if prompt:
                    prompt_data['contents'].append({"role": "system", "parts": [{"text": prompt}]})

                prompt_data['contents'].append({"role": "user", "parts": [{"text": prompt_content}]})

        if auth:
            headers['Authorization'] = 'Bearer ' + auth

        # Console.debug_b('get_text_gen_img_prompt=>url: {}'.format(url))
        # Console.debug_b('get_text_gen_img_prompt=>headers: {}'.format(headers))
        prompt_resp = self.session.post(url=url, headers=headers, json=prompt_data, **self.__get_api_req_kwargs(prompt_model))

        if prompt_resp.status_code == 200:
            prompt_data = prompt_resp.json()
            prompt = ''

            if prompt_data.get('result'):   # Cloudflare AI
                prompt = prompt_data['result']['response']
            elif prompt_data.get('choices'):
                prompt = prompt_data['choices'][0]['message']['content']

            # Console.debug_b('get_text_gen_img_prompt: {}'.format(prompt))

            return prompt
        else:
            Console.warn('get_text_gen_img_prompt FAILED: {}'.format(prompt_resp.text))
            return None
    
    # 已废弃
    def cfai_text_gen_img(self, payload, token=None):
        content = str(payload['messages'][0]['content']['parts'][0])
        model = payload['model']
        base_url = LocalConversation.get_url(model) if not LocalConversation.get_url(model).endswith('/') else LocalConversation.get_url(model)[:-1]
        img_url = base_url + '/' + API_DATA[model].get('image_model')
        auth = LocalConversation.get_auth(model)
        headers = {'Authorization': 'Bearer ' + auth, 'User-Agent': self.user_agent, 'Content-Type': 'application/json'}
        fake_data = {"prompt": content}

        if API_DATA[model].get('prompt_model'):
            prompt_url = base_url + '/' + API_DATA[model].get('prompt_model')
            # prompt_data = { "messages": [{ "role": "user", "content": "你是专业的ai prompt生成师，现在请你认真体悟文字的场景与氛围并生成关于'{}'的AI drawing prompt，言简意骇，请不要出现任何中文，如有中文则自动翻译至英语。最后直接输出prompt的主要内容即可".format(content) }]}
            prompt_data = { "messages": [{ "role": "user", "content": "You are a professional ai prompt generator, now please seriously realize the scene and atmosphere of the text and generate an AI drawing prompt about '{}', please don't show any Chinese, if there is any Chinese, it will be automatically translated to English. Finally, you can output the main content of the prompt directly.".format(content) }]}
            prompt_resp = self.session.post(url=prompt_url, headers=headers, json=prompt_data, **self.__get_api_req_kwargs(model))

            if prompt_resp.status_code == 200:
                prompt = prompt_resp.json()['result']['response']
                fake_data = {"prompt": prompt}

        resp = self.session.post(url=img_url, headers=headers, json=fake_data, **self.__get_api_req_kwargs(model))

        return resp

    def goon(self, model, parent_message_id, conversation_id, stream=True, token=None, isolation_code=None):
        data = {
            'action': 'continue',
            'conversation_id': conversation_id,
            'model': model,
            'parent_message_id': parent_message_id,
        }

        return self.__request_conversation(data, token, isolation_code)

    def regenerate_reply(self, prompt, model, conversation_id, message_id, parent_message_id, stream=True, token=None, isolation_code=None):
        if model == 'gpt-4o-api':
            model = 'gpt-4o'

        data = {
            'action': 'variant',
            'messages': [
                {
                    'id': message_id,
                    'role': 'user',
                    'author': {
                        'role': 'user',
                    },
                    'content': {
                        'content_type': 'text',
                        'parts': [prompt],
                    },
                }
            ],
            'model': model,
            'conversation_id': conversation_id,
            'parent_message_id': parent_message_id,
        }

        return self.__request_conversation(data, token, isolation_code)
    

    def create_share(self, request, token=None):
        host = request.host_url
        payload = request.json
        conversation_id = payload['conversation_id']
        current_node_id = payload['current_node_id']
        is_anonymous = payload['is_anonymous']
        resp_data = {
                    "share_id": "",
                    "share_url": "",
                    "title": "",
                    "is_public": True,
                    "is_visible": True,
                    "is_anonymous": is_anonymous,
                    "highlighted_message_id": None,
                    "current_node_id": current_node_id,
                    "already_exists": True,
                    "moderation_state": {
                        "has_been_moderated": False,
                        "has_been_blocked": False,
                        "has_been_accepted": False,
                        "has_been_auto_blocked": False,
                        "has_been_auto_moderated": False
                    }
            }
        title = LocalConversation.check_conversation_exist(conversation_id)
        # Console.debug_b('create_share: {}'.format(title))
        if title:
            is_anonymous = payload['is_anonymous']
            current_node_id = payload['current_node_id']
            resp_data['share_id'] = conversation_id
            resp_data['share_url'] = host + "share/" + conversation_id
            resp_data['title'] = title[0]

            return self.fake_resp(fake_data=json.dumps(resp_data, ensure_ascii=False))
        
        if self.LOCAL_OP:
            return 404
        
        url = '{}/backend-api/share/create'.format(self.__get_api_prefix())
        resp = self.session.post(url=url, headers=self.__get_headers(token), json=payload, **self.req_kwargs)
        if resp.status_code == 200:
            resp_data = resp.json()
            share_url = host + "share/" + resp_data['share_id']
            resp_data['share_url'] = share_url

            return self.fake_resp(fake_data=json.dumps(resp_data, ensure_ascii=False))
        
        return resp
    
    def get_origin_share_data(self, share_id, token=None):
        url = '{}/share/{}'.format(self.__get_api_prefix(), share_id)
        resp = self.session.get(url=url, headers=self.__get_headers(token), **self.req_kwargs)
        if resp.status_code == 200:
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            scripts = soup.find_all('script')  # 找到所有的脚本
            for script in scripts:
                if script.get('id') == '__NEXT_DATA__':
                    json_text = script.string
                    origin_share_data = json.loads(json_text)
                    Console.debug_b('origin_share_data: {}'.format(origin_share_data))
                    serverResponse_data = origin_share_data['props']['pageProps']['serverResponse']
                    serverResponse_data['continue_conversation_url'] = serverResponse_data['continue_conversation_url'].split('https://chat.openai.com')[1]     # 去掉oai的host, 最后在server.py-get_share_page再添加host

                    return serverResponse_data
        else:
            raise Exception('get_origin_share_data failed: \n' + self.__get_error(resp) + '\n' + str(resp.status_code))

        # return resp
            

    def get_share_data(self, share_id, token=None):
        script_json = {'It has been deleted by GavinGoo.'}

        conv_share_data = LocalConversation.get_conv_share_data(share_id)
        if conv_share_data:
            script_json['props']['pageProps']['serverResponse'] = conv_share_data
            script_json['query']['shareParams'][0] = conv_share_data['data']['conversation_id']

        elif not self.LOCAL_OP:
            origin_conv_share_data = self.get_origin_share_data(share_id, token)
            # 待修改
            script_json['props']['pageProps']['serverResponse'] = origin_conv_share_data
            script_json['query']['shareParams'][0] = origin_conv_share_data['data']['conversation_id']

        return script_json
    

    def __file_to_base64(self, file_path):
        if file_path.startswith('/files/'):
            file_path = USER_CONFIG_DIR + file_path

        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
            else:
                Console.warn('file_to_base64 FAILED: No such file: {}'.format(file_path))
                
        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('file_to_base64 FAILED: {}'.format(e))
            return file_path
        
    def __file_to_base64url(self, file_path):
        if file_path.startswith('/files/'):
            file_path = USER_CONFIG_DIR + file_path

        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    base64_url_data = base64.urlsafe_b64encode(f.read()).decode()
                    safe_encoded = urllib.parse.quote_plus(base64_url_data)

                    return safe_encoded
            else:
                Console.warn('file_to_base64url FAILED: No such file: {}'.format(file_path))
                
        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('file_to_base64url FAILED: {}'.format(e))
            return file_path
    
    def __gemini_msg_withfile(self, file_path, file_type):
        if file_type.startswith('image'):
            file_path = USER_CONFIG_DIR + file_path
            file_base64 = self.__file_to_base64(file_path)

            return {'inline_data': {'mime_type': file_type, 'data': file_base64}}
        else:
            return None

    def __request_conversation(self, data, token=None, isolation_code=None):
        model_alias = data['model']
        if model_alias in API_DATA:
            # Console.warn('Request conversation: {}'.format(data['messages'][0]))
            if data.get('messages'):
                action = data['action']
                parts = data['messages'][0]['content']['parts']
                attachments = data['messages'][0]['metadata'].get('attachments')
                content = str(parts[0]) if len(parts) == 1 else str(parts[-1])
                # model = data['model']
                message_id = data['messages'][0]['id']
            else:
                action = data.get('action')
                parts = data['prompt']
                content = str(parts)
                # model = API_DATA[model].get('slug')
                # model = data['model']
                message_id = data['message_id']
                attachments = None
            
            model = model_alias  # 0521: 暂代
            conversation_id = data.get('conversation_id')
            prompt_model = API_DATA[model].get('prompt_model')
            prompt = API_DATA[model].get('prompt')

            # url = LocalConversation.get_url(model)
            url = API_DATA[model_alias].get('url')
            auth = LocalConversation.get_auth(model)
            headers = {'User-Agent': self.user_agent, 'Content-Type': 'application/json'}
            history_list = []
            fake_data = {
                "messages": [],
                "model": API_DATA[model].get('slug'),
                "stream": True,
            } if 'gemini' not in model else {"contents":[]}
            # Console.warn('{} | {}'.format(model, auth))
            # Console.debug_b(f'发送消息: {content}')

            if ('glm' in model or 'cogview' in model) and model != 'glm-free-api':
                auth = LocalConversation.glm_generate_token(auth, 3600)
                # Console.debug_b('生成的GLM_Token: {}'.format(auth))

            if 'emohaa' in model:
                del fake_data['model']

            if 'kimi' in model:
                # del fake_data['model']
                fake_data['use_search'] = True

            if 'double' in model:
                double_api_key = auth
                auth = self.double_generate_token(model, double_api_key)
                # Console.debug_b('生成的Double_Token: {}'.format(auth))

            if auth:
                headers['Authorization'] = 'Bearer ' + auth

            if prompt and not prompt_model:
                if 'double' in model:
                    fake_data['messages'].append({"role": "user", "message": prompt})
                    fake_data['messages'].append({"role":"assistant","message":"Ok, I get it."})

                else:
                    fake_data['messages'].append({"role": "system", "content": prompt})

            ## 插入历史消息
            ## 2024-10-22: 不携带历史文件
            ### DALL·E不插入历史消息
            if data.get('conversation_id') and 'dall-e' not in model:
                history_list = LocalConversation.get_history_conversation(conversation_id, API_DATA[model].get('history_count'))
                # history_attaches_list = LocalConversation.get_history_conversation_attachments(conversation_id)

                for item in history_list:
                    # history_message_id = item['message_id']
                    # if history_attaches_list and history_message_id in history_attaches_list:   # 历史消息带附件
                    #     if 'gemini' not in model:
                    #         file_msg = {
                    #             "role": item['role'],
                    #             "content": [
                    #                 {'type': 'text', 'text': item['message']}
                    #             ]
                    #         }
                    #     else:
                    #         file_msg = {"parts": [{"text": item['message']}]}

                        # for attach in history_attaches_list[history_message_id]:
                        #     file_type = attach['file_type']
                        #     file_path = attach['file_path']
                            
                        #     if 'gemini' not in model:
                        #         if API_DATA[model].get('file_base64') and (API_DATA[model].get('file_base64') == 'true' or API_DATA[model].get('file_base64') == True):
                        #             if 'glm' in model:
                        #                 file_url = self.__file_to_base64(file_path)
                        #             else:
                        #                 file_url = f'data:{file_type};base64,' + self.__file_to_base64(file_path)

                        #         elif API_DATA[model].get('file_base64url') and (API_DATA[model].get('file_base64url') == 'true' or API_DATA[model].get('file_base64url') == True):
                        #             file_url = self.__file_to_base64url(file_path)

                        #         else:
                        #             file_url = quote((self.web_origin + file_path) if not file_path.startswith('http') else file_path, safe='/:')

                        #         # file_msg['content'].append({"type": file_type, file_type+'_url' if file_type == 'file' else file_type: {'url': file_url}})

                        #         file_msg['content'].append({"type": 'image_url' if file_type.startswith('image') else 'file', 'image_url' if file_type.startswith('image') else 'file_url': {'url': file_url}})

                        #         if 'kimi' in model:
                        #             fake_data['use_search'] = False # Kimi模型带附件不能联网搜索

                        #     else:
                        #         # Gemini处理逻辑
                        #         gemini_file_msg = self.__gemini_msg_withfile(file_path, file_type)
                        #         if gemini_file_msg:
                        #             file_msg['parts'].append(gemini_file_msg)
                        #         else:
                        #             file_msg['role'] = "user" if item['role'] == 'user' else "model"

                        # fake_data['messages' if 'gemini' not in model else 'contents'].append(file_msg)

                    # else:
                        if 'gemini' not in model:
                            fake_data['messages'].append({"role": item['role'], "content": item['message']})
                        else:
                            fake_data['contents'].append({"role": "user" if item['role'] == 'user' else "model", "parts": [{"text": item['message']}]})

            elif action != 'variant':
                if not data.get('conversation_id'):
                    # Console.debug_b('No conversation_id, create and save user conversation.')
                    if API_DATA[model].get('getConvIDUrl'):
                        getConvIDUrl = API_DATA[model].get('getConvIDUrl')
                        get_conversation_id = self.session.get(url=getConvIDUrl, headers=headers, **self.req_kwargs)
                        if get_conversation_id.status_code == 200:
                            conversation_id = get_conversation_id.json()['conversation_id']
                    else: 
                        conversation_id = str(uuid.uuid4())
                    LocalConversation.create_conversation(conversation_id, content, datetime.now(tzutc()).isoformat(), isolation_code)
                
            LocalConversation.save_conversation(conversation_id, message_id, content, 'user', datetime.now(tzutc()).isoformat(), model, action)

            ###########            
            
            ## 发送新消息
            ### 带附件
            if attachments:
                if 'gemini' not in model:
                    file_msg = {
                        "role": "user",
                        "content": [
                            {'type': 'text', 'text': content}
                        ]
                    }
                else:
                    file_msg = {"parts": [{"text": content}]}

                for item in attachments:
                    file_path = '/files/' + str(item['id']) + '/' + str(item['name'])
                    file_mimeType = item.get('mimeType') or item.get('mime_type')
                    # file_type = "image_url" if file_mimeType.startswith('image') else "file"
                    file_type = file_mimeType

                    if action != 'variant':
                        LocalConversation.save_conversations_file(message_id, conversation_id, str(parts), str(attachments), file_path, file_type)
                        # dev
                        # LocalConversation.save_conversations_file(message_id, conversation_id, str(parts), str(attachments), file_url, file_type)
                        # Console.debug_b(f'保存file对话:\n parts: {str(parts)} \nattachments: {str(attachments)}\n')

                    if 'gemini' in model:
                        gemini_file_msg = self.__gemini_msg_withfile(file_path, file_type)
                        if gemini_file_msg:
                            file_msg['parts'].append(gemini_file_msg)

                    else:
                        if API_DATA[model].get('file_base64') and (API_DATA[model].get('file_base64') == 'true' or API_DATA[model].get('file_base64') == True):
                            if 'glm' in model:
                                file_url = self.__file_to_base64(file_path)
                            else:
                                file_url = f'data:{file_mimeType};base64,' + self.__file_to_base64(file_path)

                        elif API_DATA[model].get('file_base64url') and (API_DATA[model].get('file_base64url') == 'true' or API_DATA[model].get('file_base64url') == True):
                            file_url = self.__file_to_base64url(file_path)

                        else:
                            file_url = quote(self.web_origin + file_path, safe='/:')

                        # file_msg['content'].append({"type": file_type, file_type+'_url' if file_type == 'file' else file_type: {'url': file_url}})
                        file_msg['content'].append({"type": 'image_url' if file_type.startswith('image') else 'file', 'image_url' if file_type.startswith('image') else 'file_url': {'url': file_url}})
                        # Console.warn({"type": 'image_url' if file_type.startswith('image') else 'file', 'image_url' if file_type.startswith('image') else 'file_url': {'url': file_path}})

                    if 'kimi' in model:
                        fake_data['use_search'] = False

                fake_data['messages' if 'gemini' not in model else 'contents'].append(file_msg)

                # Console.debug('New Message | message_id: {} | content: {} | url: {}'.format(message_id, content, fake_data['messages'][-1]['content'][1]['image_url']['url'][:10]))   # dev

            else:
                # 调用其他模型优化生图Prompt
                if prompt and prompt_model:
                    if prompt_model.startswith('@cf'):
                        prompt_url = base_url + '/' + prompt_model
                    else:
                        prompt_url = LocalConversation.get_url(prompt_model)

                    prompt = self.get_text_gen_img_prompt(content, prompt_url, model if prompt_model.startswith('@cf') else prompt_model, model)

                    if prompt:
                        content = prompt

                # 适配Cloudflare AI: text_gen_img
                if model == 'stable-diffusion-xl-base-1.0' or model == 'dreamshaper-8-lcm' or model == 'stable-diffusion-xl-lightning':
                    # base_url = LocalConversation.get_url(model) if not LocalConversation.get_url(model).endswith('/') else LocalConversation.get_url(model)[:-1]
                    base_url = API_DATA[model_alias].get('url') if not API_DATA[model_alias].get('url').endswith('/') else API_DATA[model_alias].get('url')[:-1]
                    img_url = base_url + '/' + API_DATA[model].get('image_model')
                    gen_img_data = {"prompt": content}

                    return self._request_sse(img_url, headers, gen_img_data, conversation_id, message_id, model, action, content)

                # 适配DALL·E
                if 'dall' in model:
                    fake_data = {
                        "model": model,
                        "prompt": content,
                        "n": 1,
                    }

                    return self._request_sse(url, headers, fake_data, conversation_id, message_id, model, action, content)

                # 适配Gemini
                if 'gemini' in model:
                    headers = {'User-Agent': self.user_agent, 'Content-Type': 'application/json'}

                    if prompt:
                        if history_list:
                            if fake_data['contents'][0]['role'] != 'system':
                                fake_data['contents'][0] = {"role": "system", "parts": [{"text": prompt}]}
                        else:
                            fake_data['contents'].append({"role": "system", "parts": [{"text": prompt}]})

                    fake_data['contents'].append({"role": "user", "parts": [{"text": content}]})
                    # Console.debug_b(fake_data)
                    return self._request_sse(url, headers, fake_data, conversation_id, message_id, model, action, content)
                
                # # 适配coze-real-api   # R.I.P
                # if model == 'coze-cra' or model == 'coze-real-api':
                #     fake_data = []
                #     if history_list:
                #         for item in history_list:
                #             fake_data.append({"role": 2 if item['role'] == 'user' else 1, "content": item['message']})
                #     fake_data.append({"role": 2, "content": content})

                #     return self._request_sse(url, headers, fake_data, conversation_id, message_id, model, action, content)
                
                # 适配智谱AI文生图
                if 'cogview' in model:
                    fake_data = {"model": "cogview-3", "prompt": content}

                    return self._request_sse(url, headers, fake_data, conversation_id, message_id, model, action, content)
                
                # 适配Double(需重新处理请求体)
                if 'double' in model:
                    headers['double-version'] = '2024-03-04'
                    fake_data['api_key'] = double_api_key
                    fake_data['chat_model'] = 'GPT4 Turbo' if 'GPT' in model or 'gpt' in model else 'Claude 3 (Opus)'
                    del fake_data['model']

                    for item in fake_data['messages']:
                        if item.get('content'):
                            item['message'] = item['content']
                            del item['content']

                        if item['role'] == 'user':
                            item['codeContexts'] = []   # user对话需要带上codeContexts, 否则报错

                fake_data['messages'].append({"role": "user", "content": content})
                

            return self._request_sse(url, headers, fake_data, conversation_id, message_id, model, action, content)

        # if talk:
        #     headers['Openai-Sentinel-Chat-Requirements-Token'] = self.__chat_requirements(token)

        # return self._request_sse(url=url, headers=headers, data=data)

    def __update_conversation(self, conversation_id, data, raw=False, token=None):
        if self.ISOLATION_FLAG:
            if 'is_visible' in data.keys():
                LocalConversation.del_conversation(conversation_id)

            if 'title' in data.keys():
                title = data['title']
                LocalConversation.rename_conversation(title, conversation_id)

        url = '{}/backend-api/conversation/{}'.format(self.__get_api_prefix(), conversation_id)
        # url = '{}/backend-api/conversation/{}'.format(self.__get_api_prefix(), conversation_id)
        resp = self.session.patch(url=url, headers=self.__get_headers(token), json=data, **self.req_kwargs)

        if raw:
            return resp

        if resp.status_code != 200:
            raise Exception('update conversation failed: ' + self.__get_error(resp))

        result = resp.json()
        if 'success' not in result:
            raise Exception('update conversation failed: ' + resp.text)

        return result['success']

    @staticmethod
    def __get_error(resp):
        try:
            return str(resp.json()['detail'])
        except:
            return resp.text


class ChatCompletion(API):
    def __init__(self, proxy=None):
        self.session = requests.Session()
        self.req_kwargs = {
            'proxies': {
                'http': proxy,
                'https': proxy,
            } if proxy else None,
            'verify': where(),
            'timeout': 60 if not self.req_timeout else self.req_timeout,
            'allow_redirects': False,
        }

        self.user_agent = 'pandora/{}'.format(__version__)

        super().__init__(proxy, self.req_kwargs['verify'])

    def __get_headers(self, api_key):
        return {
            'Authorization': 'Bearer ' + api_key,
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
        }

    def request(self, api_key, model, messages, stream=True, **kwargs):
        data = {
            'model': model,
            'messages': messages,
            **kwargs,
            'stream': stream,
        }

        return self.__request_conversation(api_key, data, stream)

    def __request_conversation(self, api_key, data, stream):
        default = default_api_prefix()

        if api_key.startswith('fk-') or api_key.startswith('pk-'):
            prefix = default
        else:
            prefix = getenv('OPENAI_API_PREFIX', default)
        url = '{}/v1/chat/completions'.format(prefix)

        if stream:
            headers = {**self.__get_headers(api_key), 'Accept': 'text/event-stream'}
            return self._request_sse(url=url, headers=headers, data=data)

        resp = self.session.post(url=url, headers=self.__get_headers(api_key), json=data, **self.req_kwargs)

        def __generate_wrap():
            yield resp.json()

        return resp.status_code, resp.headers, __generate_wrap()
