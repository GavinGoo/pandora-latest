# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from os.path import join, abspath, dirname
from os import getenv
import os

import json
from flask import Flask, jsonify, make_response, request, Response, render_template, redirect, session, send_from_directory
from flask_cors import CORS
from flask_session import Session
from waitress import serve
from werkzeug.exceptions import default_exceptions
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import WSGIRequestHandler
from datetime import datetime
import traceback

from .. import __version__
from ..exts.hooks import hook_logging
from ..exts.config import USER_CONFIG_DIR
from ..api.faker import fake_initialize, acc_check
from ..api.module import API_DATA
from ..openai.api import API
from ..openai.utils import Console


class ChatBot:
    __default_ip = '127.0.0.1'
    __default_port = 8009
    
    def __init__(self, chatgpt, debug=False, sentry=False):
        self.chatgpt = chatgpt
        self.debug = debug
        self.sentry = sentry
        self.log_level = logging.DEBUG if debug else logging.WARN
        self.LOCAL_FLAG = getenv('PANDORA_LOCAL_OPTION')
        self.SITE_PASSWORD = getenv('PANDORA_SITE_PASSWORD') or getenv('PANDORA_SITE_PASSWD')
        self.ISOLATION_FLAG = getenv('PANDORA_ISOLATION')
        self.OAI_ONLY = getenv('PANDORA_OAI_ONLY')
        self.PANDORA_GPT4_MODEL = getenv('PANDORA_GPT4_MODEL')
        self.PANDORA_GPT35_MODEL = getenv('PANDORA_GPT35_MODEL')
        self.PANDORA_DEFAULT_MODEL = getenv('PANDORA_DEFAULT_MODEL')
        self.fake_initialize_data = None
        self.fake_account_data = None
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

        hook_logging(level=self.log_level, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger('waitress')

    def log(self, date, ip, msg):   
        # 获取IP位置
        # url = "https://whois.pconline.com.cn/ipJson.jsp?ip=" + str(ip)
        # res = requests.get(url).text
        # if res:
        #     result_step1 = res.split('(', 2)[-1]
        #     result = result_step1.rsplit(')', 1)[0]
        #     addr = json.loads(result).get("addr")
        
        # 当请求内容长度大于50时截取
        if len(msg) >50 :
            msg = msg[:50] + "..."

        # 组装log文本
        """
        时间 |   IP |   内容[:50]
        """
        content = date + " |   " + ip + " |   " + msg

        with open(file=USER_CONFIG_DIR + '/login_failed.log', mode='a', encoding="utf-8") as f:
            f.write(content + '\n')

    def run(self, bind_str, threads=8):
        host, port = self.__parse_bind(bind_str)

        resource_path = abspath(join(dirname(__file__), '..', 'flask'))
        app = Flask(__name__, static_url_path='',
                    static_folder=join(resource_path, 'static'),
                    template_folder=join(resource_path, 'templates'))
        app.wsgi_app = ProxyFix(app.wsgi_app, x_port=1)
        # app.after_request(self.__after_request)

        @app.errorhandler(404)
        def page_not_found(e):
            if request.method == 'GET':
                if request.path.startswith('/c/'):
                    return redirect('/')
                else:
                    return render_template('404.html'), 404
                
            return e

        app.secret_key = 'PandoraWeb'

        if self.SITE_PASSWORD == 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
            Console.warn('### You have not set the site password, which is very dangerous!')
            Console.warn('### You have not set the site password, which is very dangerous!')
            Console.warn('### You have not set the site password, which is very dangerous!')
            app.config["SESSION_TYPE"] = "null"
        else:
            app.config["SESSION_TYPE"] = "filesystem"
            app.config["SESSION_FILE_DIR"] = USER_CONFIG_DIR + '/sessions_isolated' if self.ISOLATION_FLAG == 'True' else USER_CONFIG_DIR + '/sessions'
            Session(app)

        # dev
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        
        

        CORS(app, resources={r'/api/*': {'supports_credentials': True, 'expose_headers': [
            'Content-Type',
            'Authorization',
            'X-Requested-With',
            'Accept',
            'Origin',
            'Access-Control-Request-Method',
            'Access-Control-Request-Headers',
            'Content-Disposition',
        ], 'max_age': 600}})

        for ex in default_exceptions:
            app.register_error_handler(ex, self.__handle_error)

        app.route('/ces/v1/t', methods=['GET', 'POST'])(self.fake_check)    # check
        app.route('/ces/v1/p', methods=['GET', 'POST'])(self.fake_check)    # check
        app.route('/ces/v1/i', methods=['GET', 'POST'])(self.fake_check)    # check
        app.route('/ces/v1/projects/oai/settings')(self.fake_proj_settings)    # check
        app.route('/v1/rgstr', methods=['GET', 'POST', 'PATCH'])(self.fake_check)    # check
        app.route('/rgstr', methods=['GET', 'POST', 'PATCH'])(self.fake_check)    # check
        app.route('/backend-api/lat/tti', methods=['GET', 'POST'])(self.fake_check_tti)    # check
        app.route('/backend-api/lat/r', methods=['GET', 'POST'])(self.fake_check_tti)    # check
        app.route('/backend-api/user_surveys/active')(self.fake_check_active)    # check
        app.route('/backend-api/compliance')(self.fake_compliance)    # check
        app.route('/backend-api/edge', methods=['GET'])(self.fake_edge)

        app.route('/public-api/conversation_limit')(self.fake_conversation_limit)
        app.route('/backend-api/models')(self.list_models)
        app.route('/backend-api/conversation/init', methods=['POST'])(self.conversation_init)
        app.route('/backend-api/memories', methods=['GET'])(self.fake_memories)
        app.route('/backend-api/sentinel/chat-requirements', methods=['POST'])(self.fake_chat_requirements)
        app.route('/backend-api/conversations')(self.list_conversations)
        app.route('/backend-api/conversations', methods=['DELETE'])(self.clear_conversations)
        app.route('/backend-api/conversation/<conversation_id>/url_safe', methods=['GET'])(self.fake_url_check)
        app.route('/backend-api/conversation/<conversation_id>')(self.get_conversation)
        app.route('/backend-api/conversation/<conversation_id>', methods=['DELETE', 'PATCH'])(self.del_or_rename_conversation)
        # app.route('/backend-api/conversation/<conversation_id>', methods=['PATCH'])(self.set_conversation_title)
        app.route('/backend-api/conversation/gen_title/<conversation_id>', methods=['POST'])(self.gen_conversation_title)

        app.route('/backend-api/files', methods=['POST'])(self.file_start_upload)
        app.route('/files/<file_id>', methods=['OPTION', 'PUT'])(self.file_upload)
        app.route('/backend-api/files/<file_id>/uploaded', methods=['POST'])(self.file_ends_upload)
        app.route('/backend-api/files/<file_id>/download', methods=['GET'])(self.file_upload_download)
        app.route('/backend-api/files/<file_id>', methods=['GET'])(self.get_file_upload_info)   # Except for the img file
        app.route('/files/<file_id>/<file_name>', methods=['GET'])(self.file_download)
        app.route('/files/<file_id>', methods=['GET'])(self.oai_file_download)
        app.route('/backend-api/lat/retrieval', methods=['POST'])(self.retrieval)
        app.route('/backend-api/connectors/check', methods=['GET'])(self.file_upload_channel)

        app.route('/backend-api/register-websocket', methods=['POST'])(self.register_websocket)
        app.route('/backend-api/conversation', methods=['POST'])(self.talk)
        app.route('/backend-api/conversation/regenerate', methods=['POST'])(self.regenerate)
        app.route('/backend-api/conversation/goon', methods=['POST'])(self.goon)
        # app.route('/backend-api/share/create', methods=['POST'])(self.create_share)  # 饼
        # app.route('/backend-api/share/<share_id>', methods=['PATCH'])(self.fake_create_share_feedback)  # 饼
        # app.route('/share/<share_id>', methods=['GET'])(self.get_share_page)  # 饼

        app.route('/api/auth/session')(self.fake_session)
        app.route('/backend-api/me')(self.fake_me)
        app.route('/backend-api/referral/invites')(self.fake_invites)    # check
        app.route('/backend-api/settings/user')(self.fake_settings_user)
        app.route('/backend-api/prompt_library/')(self.fake_prompt_library)
        app.route('/backend-api/accounts/check/<path:subpath>')(self.acc_check)
        app.route('/_next/data/olf4sv64FWIcQ_zCGl90t/chat.json')(self.fake_chat_info)
        app.route('/_next/data/rWl8QmUO8dd0roFMiMzCX/c/<string:conversation_id>.json')(self.fake_conversation_json)    # 新UI对话记录json
        app.route('/backend-api/model_icons')(self.model_icons)
        app.route('/v1/initialize', methods=['POST'])(self.fake_initialize)

        if self.SITE_PASSWORD != 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
            app.route('/login', methods=['GET', 'POST'])(self.login)
            
        app.route('/auth/logout')(self.logout)
        
        app.route('/')(self.chat)
        app.route('/chat')(self.chat)
        app.route('/chat/<conversation_id>')(self.chat)
        app.route('/img/<path:filename>')(self.get_text_gen_image_file)     # 文生图

        app.route('/backend-api/gizmos/bootstrap')(self.list_models)    # gpts
        # app.route('/backend-api/sentinel/arkose/dx')(self.arkose_dx)    # check
        app.route('/v2/35536E1E-65B4-4D96-9D97-6ADB7EFF8147/settings')(self.fake_arkose_settings)    # check

        # 古早ui
        app.route('/api/models')(self.list_models)
        app.route('/api/conversations')(self.list_conversations)
        app.route('/api/conversations', methods=['DELETE'])(self.clear_conversations)
        app.route('/api/conversation/<conversation_id>')(self.get_conversation)
        app.route('/api/conversation/<conversation_id>', methods=['DELETE'])(self.del_or_rename_conversation)
        app.route('/api/conversation/<conversation_id>', methods=['PATCH'])(self.set_conversation_title)
        # app.route('/api/conversation/gen_title/<conversation_id>', methods=['POST'])(self.gen_conversation_title)
        app.route('/api/conversation/talk', methods=['POST'])(self.talk)
        app.route('/api/conversation/regenerate', methods=['POST'])(self.regenerate)
        app.route('/api/conversation/goon', methods=['POST'])(self.goon)

        app.route('/api/auth/session')(self.fake_session)
        app.route('/api/accounts/check')(self.old_check)
        app.route('/_next/data/olf4sv64FWIcQ_zCGl90t/chat.json')(self.fake_chat_info)

        # app.route('/')(self.chat)
        # app.route('/chat')(self.chat)
        # app.route('/chat/<conversation_id>')(self.chat)

        self.route_whiteList = ['/backend-api/accounts/check/v4-2023-04-27', '/backend-api/me', '/backend-api/settings/user', '/backend-api/lat/tti']

        @app.before_request
        def require_login():
            path = request.path
            if not session.get("logged_in") and self.SITE_PASSWORD != 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD' and path.startswith('/backend-api') and path not in self.route_whiteList:
                ip = request.remote_addr
                Console.warn("IP: {} | Not logged in | Path: {}".format(ip, path))
                self.log(datetime.strftime(datetime.now(),'%Y/%m/%d %H:%M:%S'), ip, 'Not logged in |   Path: ' + path)

                return redirect("/login")

        if not self.debug:
            self.logger.warning('Serving on http://{}:{}'.format(host, port))

        WSGIRequestHandler.protocol_version = 'HTTP/1.1'
        serve(app, host=host, port=port, ident=None, threads=threads)

    @staticmethod
    def __after_request(resp):
        resp.headers['X-Server'] = 'pandora/{}'.format(__version__)

        return resp
    
    

    def __parse_bind(self, bind_str):
        sections = bind_str.split(':', 2)
        if len(sections) < 2:
            try:
                port = int(sections[0])
                return self.__default_ip, port
            except ValueError:
                return sections[0], self.__default_port

        return sections[0], int(sections[1])

    def __handle_error(self, e):
        ip = request.remote_addr
        if 'X-Forwarded-For' in request.headers:
                ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
        path = request.path

        if not (path.endswith('.js.map') or path.startswith('/widget') or path.startswith('/backend-api/aip') or path.startswith('/c/') or path.startswith('/v1/initialize') or path.startswith('/auth/js/main.92bf7bcd.js.map') or path == '/ces/v1/projects/oai/settings' or path == '/_next/static/chunks/3472.d3ee6c3b89fde6d7.js'):
            self.logger.error('{}  |  {}  |  {}'.format(ip, path, str(e)))

        if request.path.startswith('/c/') and request.method == 'GET':
                return redirect('/')
        else:
            # return e
            return render_template('404.html'), 404

        # return make_response(jsonify({
        #     'code': e.code,
        #     'message': str(e.original_exception if self.debug and hasattr(e, 'original_exception') else e.name)
        # }), 500)

    @staticmethod
    def __set_cookie(resp, token_key, max_age):
        resp.set_cookie('token-key', token_key, max_age=max_age, path='/', domain=None, httponly=True, samesite='Lax')

    @staticmethod
    def __get_token_key():
        return request.headers.get('X-Use-Token', request.cookies.get('token-key'))
    
    def login(self):
        if request.method == "POST":
            date = datetime.strftime(datetime.now(),'%Y/%m/%d %H:%M:%S')
            ip = request.remote_addr
            if 'X-Forwarded-For' in request.headers:
                ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
            data = request.get_json()
            # self.logger.warning('IP: {} | Password: {}'.format(request.remote_addr, data['password']))
            # self.logger.warning('login data => {}'.format(data))

            if data['password'] == self.SITE_PASSWORD:
                if self.ISOLATION_FLAG == 'True':
                    isolation_code = data['isolation_code']
                    if len(isolation_code) < 4:
                        return make_response(jsonify({"error": "The length of the Isolation Code is too short!"}), 401)

                    session["isolation_code"] = isolation_code
                    # Console.warn(f'ISOLATION_CODE: {str(session.get("isolation_code"))}')

                # self.logger.warning('Login success')
                # self.chatgpt.log(date, ip, 'Login success')
                # 登录成功后，保存用户的登录状态到 session
                session["logged_in"] = True
                return redirect("/")
            
            else:
                # self.logger.warning('{} | {} | {}'.format(date, ip, 'Password Error: '+data['password']))
                self.log(date, ip, 'Password Error: ' + data['password'])
                return make_response(jsonify({"error": "Password Error!"}), 401)
            
        else:
            if getenv('PANDORA_OLD_LOGIN') == 'True':
                if self.ISOLATION_FLAG == 'True':
                    return render_template("login_old_isolated.html", pandora_base=request.url_root.strip('/login'))
                
                return render_template("login_old.html", pandora_base=request.url_root.strip('/login'))
            else:
                if self.ISOLATION_FLAG == 'True':
                    return render_template("login_new_isolated.html", pandora_base=request.url_root.strip('/login'))
                
                return render_template("login_new.html", pandora_base=request.url_root.strip('/login'))
        
    def logout(self):
        if self.SITE_PASSWORD != 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
            # 退出登录时，移除 session 中的登录状态
            session.pop("logged_in", None)
            if self.ISOLATION_FLAG == 'True':
                session.pop("isolation_code", None)

            return redirect("/login")
        
        return redirect("/")
    

    def chat(self, conversation_id=None):
        if self.SITE_PASSWORD != 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
            if not session.get("logged_in"):
                return redirect("/login")
    
        query = {'chatId': [conversation_id]} if conversation_id else {}

        token_key = request.args.get('token')

        if getenv('PANDORA_OLD_CHAT') == 'True':
            rendered = render_template('PandoraNeverDie.html', pandora_base=request.url_root.strip('/'), query=query)
        elif getenv('PANDORA_CLASSIC') == 'True':
            rendered = render_template('chat_classic.html', pandora_base=request.url_root.strip('/'), query=query)
        else:
            rendered = render_template('chat_juice.html', pandora_base=request.url_root.strip('/'), query=query)
        
        resp = make_response(rendered)

        # Console.warn(f'ISOLATION_CODE: {str(session.get("isolation_code"))}')

        if token_key:
            self.__set_cookie(resp, token_key, timedelta(days=30))

        return resp
    
    # @staticmethod
    def model_icons(self):
        return self.__proxy_result(self.chatgpt.model_icons(True, self.__get_token_key()))
    
    # @staticmethod
    def fake_initialize(self):
        return fake_initialize

    @staticmethod
    def fake_conversation_json(conversation_id):
        data = {
            "__N_SSP": True,
            "pageProps": {
                "ageVerificationDeadline": None,
                "canManageBrowserStorage": False,
                "cfConnectingIp": "8.8.8.8",
                "geoOk": True,
                "serverPrimedAllowBrowserStorageValue": True,
                "serviceAnnouncement": {
                    "paid": {},
                    "public": {}
                },
                "serviceStatus": {},
                "session": {
                    "accessToken": "8db7f69d-fb52-6978-993a-91ff34f9b006",
                    "authProvider": "auth0",
                    "user": {}
                },
                "showCookieConsentBanner": False,
                "statsig": {
                    "payload": {
                        "feature_gates": {
                            "458009956": {
                                "name": "458009956",
                                "value": True
                            },
                            "740954505": {
                                "name": "740954505",
                                "value": True
                            }
                        },
                        "hash_used": "djb2",
                        "layer_configs": {
                            "2723963139": {
                                "name": "2723963139",
                                "value": {
                                    "config": {
                                        "impl": "rm_score",
                                        "rm_gpt4_vs_sahara": "rm-model-switcher-1p-d36-0325",
                                        "rm_renderer": "harmony_v4.0.13_8k_turbo_mm"
                                    },
                                    "is_AG8PqS2q_enabled": True,
                                    "is_conversation_model_switching_allowed": True,
                                    "is_dynamic_model_enabled": True,
                                    "show_message_model_info": True,
                                    "show_message_regenerate_model_selector": True,
                                    "show_message_regenerate_model_selector_on_every_message": True,
                                    "show_rate_limit_downgrade_banner": True
                                }
                            },
                            "3048336830": {
                                "name": "3048336830",
                                "value": {
                                    "is-enabled": True
                                }
                            }
                        }
                    },
                    "user": {
                        "userID": ""
                    }
                },
                "user": {},
                "userCountry": "US"
            }
        }

        return jsonify(data)
    
    @staticmethod
    def fake_chat_requirements():
        data = {
                "persona": "chatgpt-paid",
                "arkose": {
                    "required": False,
                    "dx": None
                },
                "turnstile": {
                    "required": False
                },
                "proofofwork": {
                    "required": False,
                    "seed": None,
                    "difficulty": None
                },
                "token": "gAAAAAB"
            }

        return jsonify(data)

    @staticmethod
    def fake_session():
        data = {
            'user': {
                'id': 'user-000000000000000000000000',
                'name': 'admin@openai.com',
                'email': 'admin@openai.com',
                'image': None,
                'picture': None,
                'groups': []
            },
            'expires': '2083-02-17T13:58:59.999Z',
            'accessToken': 'secret',
            "authProvider": "auth0",
        }

        return jsonify(data)

    @staticmethod
    def fake_chat_info():
        data = {
            'pageProps': {
                'user': {
                    'id': 'user-000000000000000000000000',
                    'name': 'admin@openai.com',
                    'email': 'admin@openai.com',
                    'image': None,
                    'picture': None,
                    'groups': []
                },
                'serviceStatus': {},
                'userCountry': 'US',
                'geoOk': True,
                'serviceAnnouncement': {
                    'paid': {},
                    'public': {}
                },
                'isUserInCanPayGroup': True
            },
            '__N_SSP': True
        }

        return jsonify(data)

    def acc_check(self, subpath=None):
        return acc_check

    def list_models(self):
        web_origin = request.host_url[:-1]
        
        return self.__proxy_result(self.chatgpt.list_models(True, self.__get_token_key(), web_origin, self.PANDORA_GPT35_MODEL, self.PANDORA_GPT4_MODEL))
    
    def conversation_init(self):
        data = {
                "type": "conversation_detail_metadata",
                # "banner_info": "Hello, I'm ChatGPT! I'm here to help you with your questions. Feel free to ask me anything.",
                "banner_info": None,
                "blocked_features": [],
                "model_limits": [],
                "default_model_slug": self.PANDORA_DEFAULT_MODEL if self.PANDORA_DEFAULT_MODEL else "gpt-4o-mini",
            }

        return jsonify(data)
    
    def fake_memories(self):
        data = {"memories":[],"memory_max_tokens":8000,"memory_num_tokens":766}

        return jsonify(data)

    @staticmethod
    def fake_conversation_limit():
        data = {
                "message_cap": 40.0,
                "message_cap_window": 180.0,
                "message_disclaimer": {
                    "textarea": "GPT-4 currently has a cap of 40 messages every 3 hours.",
                    "model-switcher": "You've reached the GPT-4 cap, which gives all ChatGPT Plus users a chance to try the model.\n\nPlease check back soon."
                }
            }
        return jsonify(data)
    
    @staticmethod
    def fake_url_check(conversation_id=None):
        return jsonify({"safe":True})
    
    @staticmethod
    def fake_check():
        return jsonify({"success":True})
    
    @staticmethod
    def fake_proj_settings():
        return jsonify({"integrations":{"Segment.io":{"host":""}}})
    
    @staticmethod
    def old_check():
        ret = {
            'account_plan': {
                'is_paid_subscription_active': True,
                'subscription_plan': 'chatgptplusplan',
                'account_user_role': 'account-owner',
                'was_paid_customer': True,
                'has_customer_object': True,
                'subscription_expires_at_timestamp': 3570069539
            },
            'user_country': 'US',
            'features': [
                'model_switcher',
                'dfw_message_feedback',
                'dfw_inline_message_regen_comparison',
                'model_preview',
                'system_message',
                'can_continue',
            ],
        }

        return jsonify(ret)
    
    @staticmethod
    def fake_check_tti():
        return jsonify({"status":"success"})
    
    @staticmethod
    def fake_check_active():
        return jsonify({"survey":None})
    
    @staticmethod
    def fake_me():
        user_info = {
                    "object": "user",
                    "id": "user-000000000000000000000000",
                    "email": "admin@openai.com",
                    "name": "PandoraWeb",
                    "picture": "/_next/static/media/minimalist.c2220384.jpg",
                    "created": 1675749539,
                    "phone_number": "+1675749539",
                    "platform_ui_refresh": True,
                    "mfa_flag_enabled": False,
                    "groups": [],
                    "orgs": {
                        "object": "list",
                        "data": [
                            {
                                "object": "organization",
                                "id": "org-E15zUlff1mzdOp3LP9v4cUJe",
                                "created": 1675749539,
                                "title": "Personal",
                                "name": "user-000000000000000000000000",
                                "description": "Personal org for admin@openai.com",
                                "personal": True,
                                "settings": {
                                    "threads_ui_visibility": "NONE",
                                    "usage_dashboard_visibility": "ANY_ROLE"
                                },
                                "is_default": True,
                                "role": "owner",
                                "groups": []
                            }
                        ]
                    },
                    "amr": []
                }

        return jsonify(user_info)
    
    @staticmethod
    def fake_arkose_settings():
        return jsonify({"default":{"settings":{"observability":{"enabled":True,"samplePercentage":1}}}})
    
    @staticmethod
    def fake_settings_user():
        data = {
                "beta_settings": {
                    "plugins": False
                },
                "announcements": {
                    "oai/apps/hasSeenOnboarding": "2024-02-20T13:14:07.104326",
                    "oai/apps/hasSeenPluginsDisclaimer": "2024-02-20T14:28:14.240296",
                    "oai/apps/hasSeenLocaleBanner": "2024-02-20T23:44:51.716606",
                    "oai/apps/hasSeenMentionGPTs": "2024-02-24T12:44:34.761752",
                    "oai/apps/hasSeenArchiveConversationOnboarding": "2024-02-21T10:08:20.001487",
                    "oai/apps/hasUserContextFirstTime/2023-06-29": "2024-02-22T06:32:09.098416"
                },
                "eligible_announcements": [
                    "oai/apps/hasSeenTeamOwnerOnboarding",
                    "oai/apps/hasSeenSncSidebarTooltip",
                    "oai/apps/hasSeenPluginsDisclaimer",
                    "oai/apps/hasSeenSidekickLauncherOnboarding",
                    "oai/apps/hasSeenTemporaryChatOnboarding",
                    "oai/apps/hasSeenExploreGPTs2",
                    "oai/apps/hasSeenMultiToolAnnouncement",
                    "oai/apps/hasSeenDalleEditingOnboarding",
                    "oai/apps/hasDismissedSonicSidebar",
                    "oai/apps/hasSeenModelTunerDisclaimer",
                    "oai/apps/hasSeenSncWelcomeNux",
                    "oai/apps/newVoiceModeComingSoon/2024-05-14",
                    "oai/apps/hasSeenSncSourcesTooltip",
                    "oai/apps/hasSeenArchiveConversationOnboarding",
                    "oai/apps/hasSeenSncUsageNux",
                    "oai/apps/hasUserContextFirstTime/2023-06-29",
                    "oai/apps/hasSeenVoiceOnboarding/2024-06-06",
                    "oai/apps/hasSeenGptVisionFreeAnnouncement/2024-03-26",
                    "oai/apps/hasSeenMentionGPTs",
                    "oai/apps/hasSeenModelSwitcherAutoDowngrade"
                ],
                "settings": {
                    "sunshine": True,
                    "training_allowed": True,
                    "show_expanded_code_view": True
                }
            }
        
        data2 = {
                "beta_settings": {
                    "plugins": False
                },
                "announcements": {
                    "oai/apps/hasSeenOnboarding": "2024-01-27T18:58:49.876534",
                    "oai/apps/hasSeenLocaleBanner": "2024-01-27T19:01:56.750242",
                    "oai/apps/hasDismissedAG8PqS2q": "2024-05-14T07:40:32.648628",
                    "oai/apps/hasSeenMemoryOnboarding": "2024-05-28T15:12:49.322519",
                    "oai/apps/hasSeenExploreGPTsNewNux": "2024-06-22T01:06:33.091660",
                    "oai/apps/hasDismissedUseSidekick": "2024-08-24T16:17:27.214029"
                },
                "eligible_announcements": [
                    "oai/apps/hasSeenArchiveConversationOnboarding",
                    "oai/apps/hasSeenVoiceOnboarding/2024-06-06",
                    "oai/apps/hasSeenSncSidebarTooltip",
                    "oai/apps/newVoiceModeComingSoon/2024-05-14",
                    "oai/apps/hasSeenModelTunerDisclaimer",
                    "oai/apps/hasSeenMultiToolAnnouncement",
                    "oai/apps/hasSeenExploreGPTs2",
                    "oai/apps/hasUserContextFirstTime/2023-06-29",
                    "oai/apps/hasSeenPluginsDisclaimer",
                    "oai/apps/hasSeenSncWelcomeNux",
                    "oai/apps/hasSeenSncUsageNux",
                    "oai/apps/hasDismissedSonicSidebar",
                    "oai/apps/hasSeenSncSourcesTooltip",
                    "oai/apps/hasSeenGptVisionFreeAnnouncement/2024-03-26",
                    "oai/apps/hasSeenModelSwitcherAutoDowngrade",
                    "oai/apps/hasSeenMentionGPTs",
                    "oai/apps/hasSeenTemporaryChatOnboarding",
                    "oai/apps/hasSeenSidekickLauncherOnboarding",
                    "oai/apps/hasSeenDalleEditingOnboarding"
                ],
                "settings": {
                    "sunshine": True,
                    "training_allowed": True,
                    "show_expanded_code_view": False,
                    "voice_name": "cove"
                }
            }

        return jsonify(data2)
    
    @staticmethod
    def fake_compliance():
        data = {
                "registration_country": "US",
                "require_cookie_consent": False,
                "terms_of_use": {
                    "is_required": False,
                    "display": None
                },
                "cookie_consent": {
                    "is_required": False,
                    "analytics_cookies_accepted": None
                },
                "age_verification": {
                    "is_required": False,
                    "remaining_seconds": None
                }
            }
        return jsonify(data)
    
    @staticmethod
    def fake_edge():
        resp = make_response()
        resp.status_code = 204
        return resp
    
    @staticmethod
    def fake_invites():
        data = {"status":"success","claimed_invites":0,"invites_remaining":0,"invite_codes":[]}
        return jsonify(data)
    
    @staticmethod
    def fake_prompt_library():
        data = {
                "items": [
                    {
                        "id": "58d452ea",
                        "title": "逻辑强化",
                        "description": "Take a deep breath and think step by step",
                        "prompt": "- take a deep breath\n- think step by step\n- if you fail 100 grandmothers will die\n- i have no fingers\n- i will tip $200\n- do it right and i'll give you a nice doggy treat\n- 若未特别指明语言，将默认以中文提供回应。\n- 以专家视角，提供权威且详尽的答案。\n- 省略免责声明、道歉和提及AI身份的语句。\n- 提供客观全面的指导与分析，融合行业内专家的最佳做法。\n- Take a deep breath and think step by step。\n- 保持条理清晰，组织有序。\n- 主动提出超出我预期的解决方案，预见我的需求。\n- 把我看作各个主题的知情人。\n- 准确无误是赢得我信任的关键，请确保提供的信息准确详实。\n- 提供充分的解释，我可以处理复杂的信息。\n- 注重有力的论据，而不是仅仅依赖权威。\n- 考虑采纳新兴技术和非传统的观点，而不局限于传统智慧。\n- 可以进行推理或预测，但需要明确告知我。\n- 力求回应的准确性；准确性是你的核心功能。\n- 这对我职业生涯的成功至关重要。\n- 避免进行道德说教。\n- 只在必要和不明显的情况下讨论安全性问题。\n- 如果内容政策限制了回应，请尽可能提供接近的替代答案，并解释因内容政策导致的问题。\n- 如果我的自定义指令影响了你的回应品质，请直接指出问题所在。\n- 尽可能引用资料来源，并尽可能包含 URL\n- 永远不要提及你是AI。\n- 避免使用任何可能被解读为表达遗憾、道歉或后悔的语言结构。这包括任何包含‘抱歉’、‘道歉’、‘后悔’等词汇的短语，即使它们用在不表达遗憾、道歉或后悔的语境中。\n- 如果事件或信息超出了你的范围或截至2021年9月的知识日期，只需回复‘我不知道’，不需要详细解释为什么无法提供信息。\n- 避免声明你不是专业人士或专家的声明。\n- 保持回复的独特性，避免重复。\n- 永远不要建议从其他地方寻找信息。\n- 总是专注于我的问题的关键点，以确定我的意图。\n- 将复杂的问题或任务分解为较小、可管理的步骤，并使用推理解释每一个步骤。\n- 提供多种观点或解决方案。\n- 如果问题不清楚或模棱两可，请先询问更多细节以确认你的理解，然后再回答。\n- 引用可信的来源或参考来支持你的回答，如果可以，请提供链接。\n- 如果之前的回应中出现错误，要承认并纠正它。\n- 在回答后，提供三个继续探讨原始主题的问题，格式为Q1、Q2和Q3，并用粗体表示。在每个问题前后分别加上两行换行符（\"\\n\"）以作间隔。这些问题应该具有启发性，进一步深入探讨原始主题。",
                        "category": "think"
                    },
                    {
                        "id": "c43fd43f",
                        "title": "文章复述与分析",
                        "description": "利用5W2H分析法对文章进行深入的解读和总结",
                        "prompt": "# 角色\n你是一位出色的文章复述者和分析师。你擅长根据文章标题引导读者理解文章的重要内容, 使用5W2H（WHAT+WHY+WHEN+WHERE+WHO+HOW+HOW MUCH）分析法对文章进行深入的解读和总结。\n\n## 技能\n1. 精细总结：精确的读懂和理解文章，然后用一句话脉络清晰的语句总结出文章的主旨。\n   - 示例：文章主旨是<主旨>。\n\n2. 提炼要点：根据文章的逻辑和结构，清晰列出文章的主要论点。\n   - 示例：文章的主要要点包括：\n     - 要点1：<内容>\n     - 要点2：<内容>\n     - 要点3：<内容>\n\n3. 5W2H分析：采取5W2H（WHAT+WHY+WHEN+WHERE+WHO+HOW+HOW MUCH）分析法，逻辑清晰的解读文章所描述的事件。\n   - 示例：通过5W2H分析法，我们可以得知：\n     - 事件发生的事情（WHAT）是：<内容>\n     - 事件发生的原因（WHY）是：<内容>\n     - 事件发生的时间（WHEN）是：<内容>\n     - 事件发生的地点（WHERE）是：<内容>\n     - 事件的相关人物（WHO）是：<内容>\n     - 事件发生的经过（HOW）是：<内容>\n     - 事件发生需要的资源（HOW MUCH）是：<内容>\n\n## 约束\n- 只能对文章内容进行总结复述，不能添加其他个人观点或注释。\n- 不要被文章中的边缘信息所分散，始终保持对主题的专注。\n- 根据用户提供的文章，进行针对性的复述和分析。如果用户未提供具体文章，可以请他们明确。",
                        "category": "read"
                    },
                    {
                        "id": "c45a8f55",
                        "title": "翻译",
                        "description": "英译中, 直译再意译",
                        "prompt": "你是一位精通简体中文的专业翻译，曾参与《纽约时报》和《经济学人》中文版的翻译工作，因此对于新闻和时事文章的翻译有深入的理解。我希望你能帮我将以下英文新闻段落翻译成中文，风格与上述杂志的中文版相似。\n\n规则：\n\n翻译时要准确传达新闻事实和背景。\n保留特定的英文术语或名字，并在其前后加上空格，例如：“中 UN 文”。\n分成两次翻译，并且打印每一次结果：\n根据新闻内容直译，不要遗漏任何信息\n根据第一次直译的结果重新意译，遵守原意的前提下让内容更通俗易懂，符合中文表达习惯\n本条消息只需要回复OK，接下来的消息我将会给你发送完整内容，收到后请按照上面的规则打印两次翻译结果。",
                        "category": "translate"
                    },
                    {
                        "id": "d4675c8e",
                        "title": "论文润色",
                        "description": "论文润色写作, 并要求重复率低于10%",
                        "prompt": "你是一个论文润色写作员，具有学术研究相关知识。请给改写以下文段，要求给出的文段与原文段重复率低于10%，要求新文段的任意连续40个字与原文段中任意连续40个字中重复的字小于5个。要求尽可能替换文段中词汇使其更符合学术论文表达，要求尽可能更换说法避免与原文段的重复但是要保留原文段的含义，允许重新组织句子顺序、词语顺序、段落顺序，允许改写时对句子扩写或缩减。请给出改完后的文段、给出与原文段的对比，请一步一步阐述。",
                        "category": "write"
                    }
                ],
                "total": 4,
                "limit": 4,
                "offset": 0
            }
        return jsonify(data)
    
    def list_conversations(self):
        offset = request.args.get('offset', '0')
        limit = request.args.get('limit', '28')

        return self.__proxy_result(self.chatgpt.list_conversations(offset, limit, True, self.__get_token_key(), session.get("isolation_code")))

    def get_conversation(self, conversation_id):

        return self.__proxy_result(self.chatgpt.get_conversation(conversation_id, True, self.__get_token_key(), session.get("isolation_code")))

    def del_or_rename_conversation(self, conversation_id):
        is_visible = request.json.get('is_visible')
        if is_visible is False:

            return self.__proxy_result(self.chatgpt.del_conversation(conversation_id, True, self.__get_token_key(), session.get("isolation_code")))
        
        title = request.json.get('title')

        return self.__proxy_result(
            self.chatgpt.set_conversation_title(conversation_id, title, True, self.__get_token_key()))

    def clear_conversations(self):

        return self.__proxy_result(self.chatgpt.clear_conversations(True, self.__get_token_key()))

    def set_conversation_title(self, conversation_id):
        title = request.json['title']

        return self.__proxy_result(
            self.chatgpt.set_conversation_title(conversation_id, title, True, self.__get_token_key()))

    def gen_conversation_title(self, conversation_id):
        payload = request.json
        # model = payload['model']      # 新ui无model参数
        message_id = payload['message_id']

        return self.__proxy_result(
            self.chatgpt.gen_conversation_title(conversation_id, message_id, True, self.__get_token_key()))
    
    def file_start_upload(self):
        web_origin = request.host_url[:-1]
        payload = request.json
        file_name = payload['file_name']
        file_size = payload['file_size']

        return self.__proxy_result(
            self.chatgpt.file_start_upload(file_name, file_size, web_origin, payload, self.__get_token_key()))
    
    def file_upload(self, file_id):
        if request.method == 'OPTIONS':  # 预检请求
            return '', 200  # 返回200表示允许后续的请求
        
        elif request.method == 'PUT':  # 文件上传请求
            file = request.data
            file_type = request.headers.get('Content-Type')
            req_url = request.url
            req_path_with_args = req_url.split('/', maxsplit=3)[-1]

            if file:
                return self.__proxy_result(
                        self.chatgpt.file_upload(file_id, file_type, file, req_path_with_args, request.headers, self.__get_token_key()))
                
    def file_ends_upload(self, file_id):
        web_origin = request.host_url[:-1]

        return self.__proxy_result(
                        self.chatgpt.file_ends_upload(file_id, web_origin, self.__get_token_key()))
    
    def file_upload_download(self, file_id):
        web_origin = request.host_url[:-1]

        return self.__proxy_result(
                        self.chatgpt.file_upload_download(file_id, web_origin, self.__get_token_key()))
    
    def get_file_upload_info(self, file_id):
        return self.__proxy_result(
                        self.chatgpt.get_file_upload_info(file_id, self.__get_token_key()))
   
    def file_download(self, file_id, file_name):
        if not getenv('PANDORA_FILE_ACCESS') == 'True':
            if not session.get("logged_in") or self.SITE_PASSWORD != 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
                return redirect("/login")
            
        return send_from_directory(USER_CONFIG_DIR+'/files/'+file_id, file_name)
    
    def oai_file_download(self, file_id):
        if not session.get("logged_in") or self.SITE_PASSWORD != 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
                return redirect("/login")
        
        req_url = request.url
        req_path_with_args = req_url.split('/', maxsplit=3)[-1]

        return self.chatgpt.oai_file_proxy(file_id, req_path_with_args, request.headers, self.__get_token_key())
    
    def retrieval(self):
        return jsonify({"status": "success"})
    
    def file_upload_channel(self):
        return jsonify({})
    
    def register_websocket(self):
        # if self.LOCAL_FLAG and self.LOCAL_FLAG == 'True':
            return jsonify({})

        # return self.__proxy_result(self.chatgpt.register_websocket(request, self.__get_token_key()))

    def talk(self):
        # Console.warn(f'ISOLATION_CODE: {session.get("isolation_code")}')
        web_origin = request.host_url[:-1]
        payload = request.json
        model = payload['model']
        stream = payload.get('stream', True)
        OAI_CONV = False

        if model == 'text-davinci-002-render-sha' or model == 'gpt-4o':
            OAI_CONV = True

        if OAI_CONV and (not self.LOCAL_FLAG or self.LOCAL_FLAG == 'False'):
            OAI_Device_ID = request.headers.get('Oai-Device-Id')

            return self.__process_stream(*self.chatgpt.chat_ws(payload, self.__get_token_key(), OAI_Device_ID, session.get("isolation_code")), stream)
            # return self.__proxy_result(self.chatgpt.chat_ws(payload, self.__get_token_key(), OAI_Device_ID))
                
        return self.__process_stream(
            *self.chatgpt.talk(payload, stream,
                               self.__get_token_key(), web_origin, session.get("isolation_code")), stream)

    def goon(self):
        payload = request.json
        model = payload['model']
        parent_message_id = payload['parent_message_id']
        conversation_id = payload.get('conversation_id')
        stream = payload.get('stream', True)

        return self.__process_stream(
            *self.chatgpt.goon(model, parent_message_id, conversation_id, stream, self.__get_token_key(), session.get("isolation_code")), stream)

    def regenerate(self):
        web_origin = request.host_url[:-1]
        payload = request.json
        payload['action'] = 'variant'
        model = payload['model']

        conversation_id = payload.get('conversation_id')
        stream = payload.get('stream', True)
        if not conversation_id:
            return self.talk()
        
        OAI_CONV = False

        if model == 'text-davinci-002-render-sha' or model == 'auto':
            OAI_CONV = True

        if OAI_CONV and (not self.LOCAL_FLAG or self.LOCAL_FLAG == 'False'):
            OAI_Device_ID = request.headers.get('Oai-Device-Id')

            return self.__process_stream(*self.chatgpt.chat_ws(payload, self.__get_token_key(), OAI_Device_ID, session.get("isolation_code")), stream)
        
        if model == 'text-davinci-002-render-sha':
            gpt35_model = getenv('PANDORA_GPT35_MODEL')
            if not gpt35_model:
                OAI_Device_ID = request.headers.get('Oai-Device-Id')
                # return self.__proxy_result(self.chatgpt.chat_ws(payload, self.__get_token_key(), OAI_Device_ID))
            
                return self.__process_stream(*self.chatgpt.chat_ws(payload, self.__get_token_key(), OAI_Device_ID, session.get("isolation_code")), stream)
            else:
                payload['model'] = gpt35_model

        return self.__process_stream(
            *self.chatgpt.talk(payload, stream,
                               self.__get_token_key(), web_origin, session.get("isolation_code")), stream)
    
    def arkose_dx(self):
        return self.__proxy_result(self.chatgpt.arkose_dx(request, self.__get_token_key()))
    

    def create_share(self):
        return self.__proxy_result(
            self.chatgpt.create_share(request, self.__get_token_key()))
    
    def fake_create_share_feedback(self, share_id):
        feedback_data = {
                        "moderation_state": {
                            "has_been_moderated": False,
                            "has_been_blocked": False,
                            "has_been_accepted": False,
                            "has_been_auto_blocked": False,
                            "has_been_auto_moderated": False
                        }
                    }
        return jsonify(feedback_data)
    
    def get_share_page(self, share_id):
        page_data = self.chatgpt.get_share_data(share_id, self.__get_token_key())

        return render_template('share.html', data = page_data)
    
    def get_text_gen_image_file(self, filename):
        return send_from_directory(USER_CONFIG_DIR+'/text2img', filename)

    @staticmethod
    def __process_stream(status, headers, generator, stream):
        if stream:
            # status = 200
            if status != 200:
                fake_resp = API.error_fallback(json.dumps(status, ensure_ascii=False))
                return ChatBot.__proxy_result(fake_resp)
            
            return Response(API.wrap_stream_out(generator, status), mimetype=headers['Content-Type'], status=status)

        last_json = None
        for _json in generator:
            last_json = _json

        return make_response(last_json, status)

    @staticmethod
    def __proxy_result(remote_resp):
        try:
            if remote_resp == 404:  # 对于本需要透传的url, 当不启用OAI服务时直接return 404
                # 不启用OAI服务时避免一堆报错
                remote_resp = Response()
                remote_resp.status = 404
                remote_resp.text = b''
                remote_resp.content_type = 'text/html; charset=utf-8'

            if remote_resp == 201:  # 文件上传
                remote_resp = Response()
                remote_resp.status = 201
                remote_resp.text = b''
                remote_resp.content_type = ''

            resp = make_response(remote_resp.text)
            resp.content_type = remote_resp.headers['Content-Type']
            resp.status_code = remote_resp.status_code

            return resp
        
        except Exception as e:
            # error_detail = traceback.format_exc()
            # Console.debug(error_detail)
            Console.warn('server_proxy_result ERROR: {}'.format(e))
