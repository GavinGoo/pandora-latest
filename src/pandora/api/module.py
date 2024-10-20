from ..api.database import convs_database
# convs_database_cursor
from ..exts.config import USER_CONFIG_DIR
from ..openai.utils import Console

from datetime import datetime
from dateutil.tz import tzutc
from dateutil.parser import parse
import time
import os
from os.path import join
from os import getenv
import os
import json
from requests.models import Response
import jwt
import traceback

API_CONFIG_FILE = (USER_CONFIG_DIR + '/api.json') if not getenv('PANDORA_SERVERLESS') else join(os.path.dirname(os.path.abspath(__file__)), '../../../data/api.json')
API_DATA = []
API_AUTH_DATA = {}
UPLOAD_TYPE_WHITELIST = []
UPLOAD_TYPE_BLACKLIST = []


class LocalConversation:
    global API_DATA
    global API_AUTH_DATA
    global API_CONFIG_FILE
    global UPLOAD_TYPE_WHITELIST
    global UPLOAD_TYPE_BLACKLIST
    global ISOLATION_FLAG
    global ISOLATION_MASTER_CODE

    if os.path.exists(API_CONFIG_FILE):
        with open(API_CONFIG_FILE, 'r', encoding='utf-8') as f:
            API_DATA = json.load(f)

        def __auth_generator(auth_list):
            while True:
                for auth in auth_list:
                    yield auth

        # Console.warn('Your API Config:')
        for alias in API_DATA.keys():
            item = API_DATA[alias]

            if item['url'].find('<Your Google AI Key>') != -1:
                item['url'] = item['url'].replace('<Your Google AI Key>', getenv('GOOGLE_KEY'))

            if item['url'].find('<Your Cloudflare Account ID>') != -1:
                item['url'] = item['url'].replace('<Your Cloudflare Account ID>', getenv('CF_ID'))

            if item['url'].find('<REPLACE>') != -1:
                item['url'] = item['url'].replace('<REPLACE>', getenv(alias+'_REPLACE'))

            os.environ[alias + '_URL'] = item['url']
            # Console.debug_b('{}  |  URL  |  {}'.format(slug, item['url']))
            if item.get('auth'):
                # os.environ[slug + '_AUTH'] = item['auth']
                # Console.debug_b('{}  |  AUTH  |  {}'.format(slug, item['auth'] if not isinstance(item['auth'], list) else ', '.join(item['auth'])))

                if isinstance(item['auth'], list):
                    API_AUTH_DATA[alias] = __auth_generator(item['auth'])
                else:
                    API_AUTH_DATA[alias] = __auth_generator([item['auth']])

            elif getenv(alias+'_AUTH'):
                auth = getenv(alias+'_AUTH')
                if auth:
                    auth_list = auth.split(',')
                    API_AUTH_DATA[alias] = __auth_generator(auth_list)
        

    @staticmethod
    def initialize_database():
        global ISOLATION_FLAG
        global ISOLATION_MASTER_CODE

        ISOLATION_FLAG = getenv('PANDORA_ISOLATION')
        ISOLATION_MASTER_CODE = getenv('PANDORA_ISOLATION_MASTERCODE')

        convs_database_cursor = convs_database.cursor()

        if ISOLATION_FLAG == 'True':
            # Console.warn('Isolation Mode: ON')
            convs_database_cursor.execute('''
                CREATE TABLE IF NOT EXISTS list_conversations_isolated (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    create_time TEXT NOT NULL,
                    update_time TEXT NOT NULL,
                    isolation_code TEXT NOT NULL,
                    visible BOOLEAN DEFAULT 1
                )
            ''')  
        else:
            convs_database_cursor.execute('''
                CREATE TABLE IF NOT EXISTS list_conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    create_time TEXT NOT NULL,
                    update_time TEXT NOT NULL,
                    visible BOOLEAN DEFAULT 1
                )
            ''')
        convs_database.commit()
        convs_database_cursor.close()

    @staticmethod
    def get_url(model):
        url = getenv(model + '_URL')

        if url == None:
            Console.warn(f"get '{model}' models url failed!")
        
        return url

    @staticmethod
    def get_auth(model):
        auth_iter = API_AUTH_DATA.get(model)
        if auth_iter:
            return next(auth_iter)
        
        return None
        
    # @staticmethod
    # def get_selfapi_auth(model):
    #     return getenv(model + '_AUTH')

    @staticmethod
    def glm_generate_token(apikey: str, exp_seconds: int):
        try:
            id, secret = apikey.split(".")
        except Exception as e:
            Console.error("invalid apikey", e)
            return None

        payload = {
            "api_key": id,
            "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
            "timestamp": int(round(time.time() * 1000)),
        }

        return jwt.encode(
            payload,
            secret,
            algorithm="HS256",
            headers={"alg": "HS256", "sign_type": "SIGN"},
        )

    @staticmethod
    def create_conversation(id, title, time, isolation_code=None):
        try:
            title = title[:40] if title else 'New Chat'

            convs_database_cursor = convs_database.cursor()

            if ISOLATION_FLAG == 'True':
                convs_database_cursor.execute("INSERT INTO list_conversations_isolated (id, title, create_time, update_time, isolation_code, visible) VALUES (?, ?, ?, ?, ?, ?)",
                    (id, title, str(time), str(time), isolation_code, 1)
                )
            else:
                convs_database_cursor.execute("INSERT INTO list_conversations (id, title, create_time, update_time, visible) VALUES (?, ?, ?, ?, ?)",
                    (id, title, str(time), str(time), 1)
                )
            
            convs_database.commit()
            convs_database_cursor.close()

        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('create_conversation FAILED: {}'.format(e))

    @staticmethod
    def save_conversation(conversation_id, message_id, content, role, time, model, action):
        try:
            dt = datetime.fromisoformat(time.replace("+08:00", "+00:00").replace("Z", "+00:00"))
            local_time = dt.strftime('%Y-%m-%d %H:%M:%S')

            convs_database_cursor = convs_database.cursor()
            convs_database_cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT NOT NULL,
                    message_id TEXT NOT NULL PRIMARY KEY,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    model TEXT,
                    create_time TEXT NOT NULL,
                    local_time TEXT
                )
            ''')    # 此处的id为conversation_id

            if not (action == 'variant' and role == 'user'):
                convs_database_cursor.execute("INSERT INTO conversations (id, message_id, role, message, model, create_time, local_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (conversation_id, message_id, role, content, model, str(time), str(local_time)))
            
            convs_database_cursor.execute(f"UPDATE {'list_conversations_isolated' if ISOLATION_FLAG=='True' else 'list_conversations'} SET update_time = ? WHERE id = ?",
                (str(time), conversation_id)
            )
            
            convs_database.commit()
            convs_database_cursor.close()

        except Exception as e:
            error_detail = traceback.format_exc()
            Console.debug(error_detail)
            Console.warn('save_conversation FAILED: {}'.format(e))


    @staticmethod
    def del_conversation(conversation_id, DELETE_FLAG=False, isolation_code=None):
        convs_database_cursor = convs_database.cursor()

        if getenv('PANDORA_TRUE_DELETE') == 'True' or DELETE_FLAG or isolation_code == ISOLATION_MASTER_CODE:
            convs_database_cursor.execute(f"DELETE FROM {'list_conversations_isolated' if ISOLATION_FLAG=='True' else 'list_conversations'} WHERE id=?", (conversation_id,))
            convs_database_cursor.execute("DELETE FROM conversations WHERE id=?", (conversation_id,))

        else:
            convs_database_cursor.execute(f"UPDATE {'list_conversations_isolated' if ISOLATION_FLAG=='True' else 'list_conversations'} SET visible = ? WHERE id=?;",(0, conversation_id))

        convs_database.commit()
        convs_database_cursor.close()

        return LocalConversation.fake_resp(fake_data=json.dumps({"success":True}))

    @staticmethod
    def rename_conversation(title, conversation_id):
        convs_database_cursor = convs_database.cursor()

        convs_database_cursor.execute(f"UPDATE {'list_conversations_isolated' if ISOLATION_FLAG=='True' else 'list_conversations'} SET title = ? WHERE id=?;",(title, conversation_id))

        convs_database.commit()
        convs_database_cursor.close()

        return LocalConversation.fake_resp(fake_data=json.dumps({"success":True}))

    @staticmethod
    def list_conversations(offset, limit, isolation_code=None):
        convs_database_cursor = convs_database.cursor()
        
        try:
            if ISOLATION_FLAG == 'True' and isolation_code:
                # Console.warn(f'isolation_code: {isolation_code}')
                if isolation_code == ISOLATION_MASTER_CODE:
                    convs_total = convs_database_cursor.execute("SELECT COUNT(id) FROM list_conversations_isolated").fetchone()[0]
                else:
                    convs_total = convs_database_cursor.execute("SELECT COUNT(id) FROM list_conversations_isolated WHERE isolation_code=? AND visible=1", (isolation_code,)).fetchone()[0]
            else:
                convs_total = convs_database_cursor.execute("SELECT COUNT(id) FROM list_conversations WHERE visible=1").fetchone()[0]
        except Exception as e:
            convs_total = 0
            Console.warn(str(e))

        try:
            if ISOLATION_FLAG == 'True' and isolation_code:
                if isolation_code == ISOLATION_MASTER_CODE:
                    convs_data = convs_database_cursor.execute("SELECT * FROM list_conversations_isolated ORDER BY update_time DESC LIMIT ?, ?", (offset, limit)).fetchall()
                else:
                    convs_data = convs_database_cursor.execute("SELECT * FROM list_conversations_isolated WHERE isolation_code=? AND visible=1 ORDER BY update_time DESC LIMIT ?, ?", (isolation_code, offset, limit)).fetchall()
            else:
                convs_data = convs_database_cursor.execute("SELECT * FROM list_conversations WHERE visible=1 ORDER BY update_time DESC LIMIT ?, ?", (offset, limit)).fetchall()
        except Exception as e:
            Console.warn(str(e))

            convs_database_cursor.close()
            return None
        
        convs_database_cursor.close()

        convs_dict = [dict(zip([column[0] for column in convs_database_cursor.description], row)) for row in convs_data]
        # Console.debug_b('对话列表计数: '+str(len(convs_dict)))
        data = {'list_data': convs_dict, 'total': convs_total}
        # list = json.dumps(convs_dict, ensure_ascii=False)

        # Console.debug_b('Read local conversation dict: ')
        # for item in convs_dict:
        #     # print(item)
        #     self.logger.info(item)

        # Console.debug_b('list_json: ')
        # print(convs_dict)

        return data

    @staticmethod
    def check_conversation_exist(conversation_id, isolation_code=None):
        convs_database_cursor = convs_database.cursor()

        try:
            # if ISOLATION_FLAG == 'True' and isolation_code:
            #     conversation_info = convs_database_cursor.execute("SELECT id FROM list_conversations_isolated WHERE id=? AND isolation_code=? AND visible=1", (conversation_id, isolation_code)).fetchone()
            # else:
            #     conversation_info = convs_database_cursor.execute("SELECT id FROM list_conversations WHERE id=? AND visible=1", (conversation_id,)).fetchone()

            # conversation_info = convs_database_cursor.execute(f"SELECT id FROM {'list_conversations_isolated' if ISOLATION_FLAG=='True' else 'list_conversations'} WHERE id=? AND visible=1", (conversation_id,)).fetchone()

            EXIT_FLAG = convs_database_cursor.execute(f"SELECT id FROM conversations WHERE id=?", (conversation_id,)).fetchone()

            convs_database_cursor.close()

            if EXIT_FLAG:
                return True
            else:
                return False
        
        except Exception as e:
            Console.warn(f'check_conversation_exist ERROR: {str(e)}')

            convs_database_cursor.close()
            return None

    @staticmethod
    def get_conversation(conversation_id, isolation_code=None, share=False):
        convs_database_cursor = convs_database.cursor()

        # if ISOLATION_FLAG == 'True' and isolation_code:
        #     list_conversation_info = convs_database_cursor.execute("SELECT * FROM list_conversations_isolated WHERE id=? AND isolation_code=? AND visible=1", (conversation_id, isolation_code)).fetchone()
        # else:
        #     list_conversation_info = convs_database_cursor.execute("SELECT * FROM list_conversations WHERE id=? AND visible=1", (conversation_id,)).fetchone()

        list_conversation_info = convs_database_cursor.execute(f"SELECT * FROM {'list_conversations_isolated' if ISOLATION_FLAG=='True' else 'list_conversations'} WHERE id=?", (conversation_id,)).fetchone()
        
        
        if list_conversation_info:
            # Console.warn(f'Conversation ID: {conversation_id}  ||  Title: {list_conversation_info[1]}')
            conversation_data = convs_database_cursor.execute("SELECT * FROM conversations WHERE id=?", (conversation_id,)).fetchall()

            if conversation_data:
                title = list_conversation_info[1]
                create_time = list_conversation_info[2]
                update_time = list_conversation_info[3]

                # Console.debug_b('组装对话: title={}, create_time={}, update_time={}'.format(title, create_time, update_time))
                create_time_unix = parse(create_time).timestamp()
                update_time_unix = parse(update_time).timestamp()
                base = {
                    "title": title,
                    "create_time": create_time_unix,
                    "update_time": update_time_unix,
                    "mapping": {
                                "123456": {
                                    "id": "123456",
                                    "message": {
                                        "id": "123456",
                                        "author": {
                                            "role": "system",
                                            "name": None,
                                            "metadata": {}
                                        },
                                        "create_time": None,
                                        "update_time": None,
                                        "content": {
                                            "content_type": "text",
                                            "parts": [
                                                ""
                                            ]
                                        },
                                        "status": "finished_successfully",
                                        "end_turn": True,
                                        "weight": 0.0,
                                        "metadata": {
                                            "is_visually_hidden_from_conversation": True
                                        },
                                        "recipient": "all"
                                    },
                                    "parent": "654321",
                                    "children": [
                                        conversation_data[0][1]
                                    ]
                                },
                                "654321": {
                                    "id": "654321",
                                    "message": None,
                                    "parent": None,
                                    "children": [
                                        "123456"
                                    ]
                                }
                    },
                    "moderation_results": [],
                    "current_node": conversation_data[-1][1],
                    "plugin_ids": None,
                    "conversation_id": conversation_id,
                    "conversation_template_id": None,
                    "gizmo_id": None,
                    "is_archived": False,
                    "safe_urls": []
                }

                NEXT_IS_USER = True
                last_user_msgid = None
                for i, item in enumerate(conversation_data):
                    message_id = item[1]
                    role = item[2]
                    message = item[3]
                    # parts = item[3]
                    model = item[4]
                    message_create_time = item[5]
                    message_create_time_unix = parse(message_create_time).timestamp()
                    parent = "123456" if i == 0 else conversation_data[i-1][1]

                    try:
                        children = conversation_data[i+1][1]
                    except IndexError:
                        children = None

                    # Console.debug_b('组装对话: \nmessage_id: {}, role: {}, message: {}, model: {}, message_create_time: {}, parent: {}, children: {}'
                    #                 .format(message_id, role, message, model, message_create_time, parent, children))
                    
                    mapping_item = {
                            "id": message_id,
                            "message": {
                                "id": message_id,
                                "author": {
                                    "role": role,
                                    "name": None,
                                    "metadata": {}
                                },
                                "create_time": message_create_time_unix,
                                "update_time": None,
                                "content": {
                                    "content_type": "text",
                                    "parts": [message]
                                },
                                "status": "finished_successfully",
                                "end_turn": True,
                                "weight": 1.0,
                                "metadata": {},
                                "recipient": "all"
                            },
                            "parent": "123456" if i == 0 else parent,
                            "children": []
                    }

                    parts, attachments = LocalConversation.get_conversations_attachments(message_id)
                    if attachments:
                        # Console.debug_b(f'get_conversation: {message_id} attachments: {str(attachments)}')
                        mapping_item['message']['metadata']['attachments'] = attachments
                        mapping_item['message']['content']['parts'] = parts

                    if children:
                        mapping_item['children'].append(children)

                    if role == 'user':
                        NEXT_IS_USER = False
                        last_user_msgid = message_id
                        mapping_item['message']['metadata']['request_id'] = "Pandora-SIN"
                        mapping_item['message']['metadata']['timestamp_'] = "absolute"
                        mapping_item['message']['metadata']['message_type'] = None

                    if role == 'assistant':
                        if NEXT_IS_USER:
                            mapping_item['parent'] = last_user_msgid
                            mapping_item['message']['metadata']['parent_id'] = last_user_msgid

                            if isinstance(base['mapping'][list(base['mapping'].keys())[-2]]['children'], list):
                                base['mapping'][last_user_msgid]['children'].append(message_id)
                                base['mapping'][list(base['mapping'].keys())[-1]]['children'] = []

                        else:
                            mapping_item['message']['metadata']['parent_id'] = parent
                        
                        NEXT_IS_USER = True
                        mapping_item['message']['metadata']['finish_details'] = {"type": "stop", "stop_tokens": [100260]}
                        mapping_item['message']['metadata']['citations'] = []
                        mapping_item['message']['metadata']['gizmo_id'] = None
                        mapping_item['message']['metadata']['is_complete'] = True
                        mapping_item['message']['metadata']['message_type'] = None
                        mapping_item['message']['metadata']['model_slug'] = model
                        # mapping_item['message']['metadata']['parent_id'] = parent
                        mapping_item['message']['metadata']['request_id'] = "Pandora-SIN"
                        mapping_item['message']['metadata']['timestamp_'] = "absolute"

                    base['mapping'][message_id] = mapping_item
                    
                if share:
                    convs_database_cursor.close()
                    
                    return {"title": base["title"], "create_time": base["create_time"], "update_time": base["update_time"], "conversation_id": base["conversation_id"], "mapping": base["mapping"]}

                conv = LocalConversation.fake_resp(fake_data=json.dumps(base, ensure_ascii=False))

                convs_database_cursor.close()
                return conv
            
            else:
                convs_database_cursor.close()
                return None
        
        convs_database_cursor.close()
        return None

    @staticmethod
    def get_history_conversation(conversation_id, model_history_count=None):
            history_count = str(model_history_count) if model_history_count else getenv('PANDORA_HISTORY_COUNT')
            
            convs_database_cursor = convs_database.cursor()
            history_data = convs_database_cursor.execute(
                """
                SELECT message_id, role, message 
                FROM (
                    SELECT * 
                    FROM (
                        SELECT * 
                        FROM conversations 
                        WHERE id=? 
                        ORDER BY create_time DESC 
                        LIMIT ?
                    ) 
                    ORDER BY create_time ASC
                )
                """, 
                (conversation_id, history_count,)
            ).fetchall()
            history_dict = [dict(zip([column[0] for column in convs_database_cursor.description], row)) for row in history_data]

            if getenv('PANDORA_BEST_HISTORY'):
                history_total = int(convs_database_cursor.execute("SELECT COUNT(message_id) FROM conversations WHERE id=?", (conversation_id,)).fetchone()[0])

                if int(history_count) < history_total:
                    first_history_data = convs_database_cursor.execute("SELECT message_id, role, message FROM conversations WHERE id=? ORDER BY create_time ASC LIMIT 1", (conversation_id,)).fetchall()
                    first_history_dict = [dict(zip([column[0] for column in convs_database_cursor.description], row)) for row in first_history_data]

                    if getenv('PANDORA_DEBUG'):
                        Console.debug(f'Because of PANDORA_BEST_HISTORY, add first history message: {str(first_history_dict[0])}')

                    history_dict.insert(0, first_history_dict[0])

            # history_json = json.dumps(history_dict, ensure_ascii=False)
            # Console.debug_b('携带历史对话: {}'.format(history_json))

            convs_database_cursor.close()
            return history_dict

    @staticmethod
    def get_conv_share_data(conversation_id):
        conv_data = LocalConversation.get_conversation(conversation_id, share=True)
        if conv_data is None:
            return
        
        model_slug = "text-davinci-002-render-sha"
        model_max_tokens = 8191
        model_title = "Default (GPT-3.5)"
        model_description = "Our fastest model, great for most everyday tasks."

        for k, v in conv_data['mapping'].items():
            if v['message'] is not None:
                if v['message']['author']['role'] == 'user':
                    v['message']['metadata']['shared_conversation_id'] = conversation_id

                if v['message']['author']['role'] == 'assistant':
                    model_slug = v['message']['metadata']['model_slug']


        if model_slug != "text-davinci-002-render-sha":
            with open(API_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    API_DATA = json.load(f)

                    for alias in API_DATA.keys():
                        item = API_DATA[alias]
                        model_title = item['title']
                        model_description = item['description']
                        model_max_tokens = item['max_tokens']
        
        serverResponse = {
            "type": "data",
            "data": {
                "title": conv_data["title"],
                "create_time": conv_data["create_time"],
                "update_time": conv_data["update_time"],
                "mapping": conv_data["mapping"][::-1],
                "moderation_results": [],
                "current_node": next(iter(conv_data["mapping"][::-1])),
                "conversation_id": conversation_id,
                "is_archived": False,
                "safe_urls": [],
                "is_public": True,
                "linear_conversation": [conv_data["mapping"]],
                "has_user_editable_context": False,
                "continue_conversation_url": '/share/' + conversation_id,
                "model": {
                    "slug": model_slug,
                    "max_tokens": model_max_tokens,
                    "title": model_title,
                    "description": model_description,
                    "tags": ["gpt3.5"]
                },
                "moderation_state": {
                    "has_been_moderated": False,
                    "has_been_blocked": False,
                    "has_been_accepted": False,
                    "has_been_auto_blocked": False,
                    "has_been_auto_moderated": False
                }
            }
        }
        
        return serverResponse

    @staticmethod
    def fake_resp(origin_resp=None, fake_data=None):
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

            return fake_resp

    async def save_image_file(resp, web_origin, msg_id, img_type):
        resource_path = USER_CONFIG_DIR + '/text2img'

        if not os.path.exists(resource_path):
            os.makedirs(resource_path)
            
        file_name = msg_id + '.' + img_type
        file_path = join(resource_path, file_name)

        try:
            resp_content = '![img]({})'.format(web_origin + '/img/' +file_name)
        except:
            resp_content = '{}'.format('/img/' +file_name)
        # Console.debug_b('file_path: {}'.format(file_path))

        with open(file_path, 'wb') as f:
            # async for chunk in resp.aiter_bytes():  # httpx
            async for chunk in resp.aiter_content():
                f.write(chunk)

        return resp_content
    

    @staticmethod
    def create_file_upload(file_id, file_name, file_size, create_time):
        convs_database_cursor = convs_database.cursor()

        # convs_database_cursor.execute("DROP TABLE IF EXISTS files_upload")
        # convs_database.commit()

        convs_database_cursor.execute('''
            CREATE TABLE IF NOT EXISTS files_upload (
                file_id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_type TEXT,
                create_time TEXT NOT NULL
            )
        ''')


        convs_database_cursor.execute("INSERT INTO files_upload (file_id, file_name, file_size, create_time) VALUES (?, ?, ?, ?)",
            (file_id, file_name, file_size, create_time)
        )
        
        convs_database.commit()
        convs_database_cursor.close()

    @staticmethod
    def get_file_upload_info(file_id):
        convs_database_cursor = convs_database.cursor()
        file_name, file_size, file_type, create_time = convs_database_cursor.execute("SELECT file_name, file_size, file_type, create_time FROM files_upload WHERE file_id=?", (file_id,)).fetchone()

        convs_database_cursor.close()
        return file_name, int(file_size), file_type, create_time
    
    @staticmethod
    def get_file_upload_type(file_id):
        convs_database_cursor = convs_database.cursor()
        file_name, file_type = convs_database_cursor.execute("SELECT file_name, file_type FROM files_upload WHERE file_id=?", (file_id,)).fetchone()

        convs_database_cursor.close()
        return file_name, file_type
    
    @staticmethod
    def update_file_upload_type(file_id, file_type):
        convs_database_cursor = convs_database.cursor()
        convs_database_cursor.execute("UPDATE files_upload SET file_type = ? WHERE file_id=?;",(file_type, file_id))

        convs_database.commit()
        convs_database_cursor.close()
    
    def save_file_upload(file_id, file_type, file):
        LocalConversation.update_file_upload_type(file_id, file_type)

        resource_path = USER_CONFIG_DIR + '/files/' + file_id

        if not os.path.exists(resource_path):
            os.makedirs(resource_path)
            
        file_name, file_size, file_type, create_time = LocalConversation.get_file_upload_info(file_id)
        file_path = join(resource_path, file_name)

        with open(file_path, 'wb') as f:
            # async for chunk in resp.aiter_bytes():  # httpx
            # for chunk in file:
            f.write(file)

        return

    @staticmethod
    def save_conversations_file(message_id, conversation_id, parts, attachments, file_path, file_type):
        convs_database_cursor = convs_database.cursor()
        # convs_database_cursor.execute("DROP TABLE IF EXISTS conversations_file")
        # convs_database.commit()

        convs_database_cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations_file (
                message_id TEXT NOT NULL PRIMARY KEY,
                conversation_id TEXT,
                parts TEXT,
                attachments TEXT NOT NULL,
                file_path TEXT,
                file_type TEXT
            )
        ''')
        try:
            convs_database_cursor.execute("INSERT INTO conversations_file (message_id, conversation_id, parts, attachments, file_path, file_type) VALUES (?, ?, ?, ?, ?, ?)",
                (message_id, conversation_id, parts, attachments, file_path, file_type)
            )

            convs_database.commit()
            convs_database_cursor.close()
        except Exception as e:
            Console.warn(str(e))
            convs_database_cursor.close()
        
    @staticmethod
    def get_conversations_attachments(message_id):
        try:
            convs_database_cursor = convs_database.cursor()
            parts_str, attachments_str = convs_database_cursor.execute("SELECT parts, attachments FROM conversations_file WHERE message_id=?", (message_id,)).fetchone()
            # Console.warn(f'message_id: {message_id}\nparts: {parts_str}\nattachments: {attachments_str}')

            if attachments_str:
                attachments = eval(attachments_str)
                parts = eval(parts_str)
                
                convs_database_cursor.close()
                return parts, attachments
            
            convs_database_cursor.close()
            return None, None
        except:
            return None, None
        
    @staticmethod
    def get_history_conversation_attachments(conversation_id):
        convs_database_cursor = convs_database.cursor()

        try:
            convs_data = convs_database_cursor.execute("SELECT message_id, file_path, file_type FROM conversations_file WHERE conversation_id=?", (conversation_id,)).fetchall()
            if convs_data:
                convs_dict = {}
                for row in convs_data:
                    message_id = row[0]
                    file_path = row[1]
                    file_type = row[2]

                    if convs_dict.get(message_id):
                        convs_dict[message_id].append({'file_path': file_path, 'file_type': file_type})
                    else:
                        convs_dict[message_id] = [{'file_path': file_path, 'file_type': file_type}]

                convs_database_cursor.close()
                return convs_dict
            
            convs_database_cursor.close()
            return None
        
        except Exception as e:
            ee = str(e)
            if 'no such table' not in ee:
                Console.warn(f'API.module: get_history_conversation_attachments ERROR: {str(e)}')
                
            convs_database_cursor.close()
            return None
        
