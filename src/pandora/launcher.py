# -*- coding: utf-8 -*-

import argparse
import os
from os import getenv
import traceback
import sys
import datetime

from loguru import logger
from rich.prompt import Prompt, Confirm

from . import __version__
from .bots.legacy import ChatBot as ChatBotLegacy
from .bots.server import ChatBot as ChatBotServer
from .exts.config import USER_CONFIG_DIR, default_api_prefix
from .exts.hooks import hook_except_handle
from .exts.token import check_access_token_out
from .openai.api import ChatGPT
from .openai.auth import Auth0
from .openai.utils import Console

if 'nt' == os.name:
    import pyreadline3 as readline
else:
    import readline

    readline.set_completer_delims('')
    readline.set_auto_history(False)

__show_verbose = False

def read_access_token(token_file):
    with open(token_file, 'r') as f:
        return f.read().strip()


def save_access_token(access_token):
    token_file = os.path.join(USER_CONFIG_DIR, 'access_token.dat')

    if not os.path.exists(USER_CONFIG_DIR):
        os.makedirs(USER_CONFIG_DIR)

    with open(token_file, 'w') as f:
        f.write(access_token)

    if __show_verbose:
        Console.debug_b('\nThe access token has been saved to the file:')
        Console.debug(token_file)
        print()


def confirm_access_token(token_file=None, silence=False, api=False, email=None, password=None, mfa=None):
    app_token_file = os.path.join(USER_CONFIG_DIR, 'access_token.dat')

    app_token_file_exists = os.path.isfile(app_token_file)
    if app_token_file_exists and __show_verbose:
        Console.debug_b('Found access token file: ', end='')
        Console.debug(app_token_file)

    if token_file:
        if not os.path.isfile(token_file):
            raise Exception('Error: {} is not a file.'.format(token_file))

        access_token = read_access_token(token_file)
        if os.path.isfile(app_token_file) and access_token == read_access_token(app_token_file):
            return access_token, False

        return access_token, True

    if app_token_file_exists:
        confirm = 'y' if silence else Prompt.ask('A saved access token has been detected. Do you want to use it?',
                                                 choices=['y', 'n', 'del'], default='y')
        if 'y' == confirm:
            token_file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(app_token_file))
            days_diff = (datetime.datetime.now() - token_file_modified_time).days
            if days_diff >= 8:
                Console.warn('### The access token file has been used for {} days, we should update access token!\n'.format(days_diff))

                if not email or not password:
                    if not password and not silence:
                        password = Prompt.ask('  Password', password=True)
                    else:
                        Console.warn('### Invalid email or password. Abandoned update.')
                        return read_access_token(app_token_file), False

                ## ask Error in docker: Exception occurred in file /usr/local/lib/python3.9/site-packages/rich/console.py at line 2123: EOF when reading a line
                # email = getenv('OPENAI_EMAIL') or Prompt.ask('  Email')
                # password = getenv('OPENAI_PASSWORD') or Prompt.ask('  Password', password=True)
                # # mfa = getenv('OPENAI_MFA_CODE') or Prompt.ask('  MFA Code(Optional if not set)')
                # mfa = getenv('OPENAI_MFA_CODE') or None
                    
                Console.warn('### Do login, please wait...')
                access_token = Auth0(email, password, getenv('PROXY'), mfa=mfa).auth()

                if not access_token.startswith('eyJ'):
                    Console.error('### Failed to get access token, please try again.')
                    access_token = read_access_token(app_token_file)    # 兜底
                
            else:
                Console.warn('### The access token file has been used for {} days.\n'.format(days_diff))
                access_token = read_access_token(app_token_file)

            if not check_access_token_out(access_token, api):
                os.remove(app_token_file)
                return None, True

            return access_token, False
        
        elif 'del' == confirm:
            os.remove(app_token_file)

    return None, True


def parse_access_tokens(tokens_file, api=False):
    if not os.path.isfile(tokens_file):
        raise Exception('Error: {} is not a file.'.format(tokens_file))

    import json
    with open(tokens_file, 'r') as f:
        tokens = json.load(f)

    valid_tokens = {}
    for key, value in tokens.items():
        if not check_access_token_out(value, api=api):
            Console.error('### Access token id: {}'.format(key))
            continue
        valid_tokens[key] = value

    if not valid_tokens:
        Console.error('### No valid access tokens.')
        return None

    return valid_tokens


def main():
    global __show_verbose

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--email',
        help='Your openai email',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--password',
        help='Your openai password',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--mfa',
        help='Your openai mfa',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--proxy_api',
        help='Proxy for openai frontend',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--login_url',
        help='Login to get access token',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--site_password',
        help='Website password. Note: If u start as a proxy server, should be set it.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-p',
        '--proxy',
        help='Use a proxy. Format: protocol://user:pass@ip:port',
        required=False,
        type=str,
        default=getenv("PANDORA_PROXY"),
    )
    parser.add_argument(
        '--gpt4',
        help='Select gpt4 model from the file "api.json". Default: gpt-4',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--gpt35',
        help='Select gpt3.5 model from the file "api.json". Note: Default value depends on OpenAI.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--default_model',
        help='Select your default model from the file "api.json".',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--history_count',
        help='Number of history messages carried for api, default: 4',
        required=False,
        type=str,
        default='4',
    )
    parser.add_argument(
        '--best_history',
        help='Automatically carries the first pair of history conversations when the total number of history messages is greater than the set number of carried history messages.',
        action='store_true',
    )
    parser.add_argument(
        '--true_del',
        help='Actually delete the conversation instead of setting it hidden (is_visible=0).',
        action='store_true',
    )
    parser.add_argument(
        '-l',
        '--local',
        help='Running locally only, not use OAI service.',
        action='store_true',
    )
    parser.add_argument(
        '--timeout',
        help='Request timeout. Default: 60 Unit: seconds',
        required=False,
        type=str,
        default='60',
    )
    parser.add_argument(
        '--oai_only',
        help='Only OAI service.',
        action='store_true',
    )
    parser.add_argument(
        '-t',
        '--token_file',
        help='Specify an access token file and login with your access token.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--tokens_file',
        help='Specify an access tokens json file.',
        required=False,
        type=str,
        default=None,
        nargs='?',
        const='token',
    )
    parser.add_argument(
        '--config_dir',
        help='User Config Dir, default: System determined.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-s',
        '--server',
        help='Start as a proxy server. Format: ip:port, default: 0.0.0.0:8008',
        required=False,
        type=str,
        default=getenv("PANDORA_SERVER"),
        action='store',
        nargs='?',
        const='0.0.0.0:8008',
    )
    parser.add_argument(
        '--threads',
        help='Define the number of server workers, default: 8',
        required=False,
        type=int,
        default=8,
    )
    parser.add_argument(
        '-a',
        '--api',
        help='Use gpt-3.5-turbo chat api. Note: OpenAI will bill you.',
        action='store_true',
    )
    parser.add_argument(
        '--login_local',
        help='Login locally. Pay attention to the risk control of the login ip!',
        action='store_true',
    )   # 原'-l'/'--local'
    parser.add_argument(
        '-v',
        '--verbose',
        help='Show exception traceback.',
        action='store_true',
    )
    parser.add_argument(
        '--old_login',
        help='Use the old login page',
        action='store_true',
    )
    parser.add_argument(
        '--old_chat',
        help='Use the old chat page',
        action='store_true',
    )
    parser.add_argument(
        '--classic',
        help='Use the classic chat page',
        action='store_true',
    )
    parser.add_argument(
        '--file_size',
        help='Limit upload file size. Unit: MB(Integer)',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--type_whitelist',
        help='Limit upload file type as whitelist.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--type_blacklist',
        help='Limit upload file type as blacklist.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--file_access',
        help='Uploaded file is accessible on the Internet. Default: False',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--device_id',
        help='OAI Device ID for OAI service.',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '--debug',
        help='Prints the request body(first 500 characters) of the message sent with the first response received.',
        action='store_true',
    )

    parser.add_argument(
        '-i',
        '--isolate',
        help='Isolated user conversation(Isolation Mode).',
        action='store_true',
    )

    parser.add_argument(
        '--isolate_master',
        help='This isolation code allows manager to view all user conversations.',
        required=False,
        type=str,
        default=None,
    )

    parser.add_argument(
        '--oai_proxy',
        help='Proxy OAI.',
        required=False,
        type=str,
        default=None,
    )

    parser.add_argument(
        '--oai_voice',
        help='Enable OAI Voice.',
        action='store_true',
    )

    parser.add_argument(
        '--voice_wssurl',
        help='Replace OAI Voice WSS Url.',
        required=False,
        type=str,
        default=None,
    )
    
    args, _ = parser.parse_known_args()
    __show_verbose = args.verbose

    os.environ['PANDORA_HISTORY_COUNT'] = args.history_count

    api_prefix = getenv('OPENAI_API_PREFIX')
    login_url = getenv('OPENAI_LOGIN_URL')
    email = getenv('OPENAI_EMAIL')
    password = getenv('OPENAI_PASSWORD')
    site_password = getenv('PANDORA_SITE_PASSWD') or getenv('PANDORA_SITE_PASSWORD')
    user_config_dir = getenv('USER_CONFIG_DIR')

    if not api_prefix:
        if args.proxy_api:
            # if args.proxy_api == 'https://chat.openai.com' and not args.device_id:
            #     raise Exception('You are using the official OAI service but No args.device_id or env.OPENAI_DEVICE_ID !')
            os.environ['OPENAI_API_PREFIX'] = args.proxy_api
        elif not args.local:
            raise Exception('No args.proxy_api or env.OPENAI_API_PREFIX !')
        else:
            if not os.path.exists(USER_CONFIG_DIR + '/api.json'):
                raise Exception(f'You had enabled local mode, but no "api.json" file found in user config dir({USER_CONFIG_DIR})!')
        
    if not login_url:
        if args.login_url:
            os.environ['OPENAI_LOGIN_URL'] = args.login_url
        # elif not args.local or getenv('PANDORA_LOCAL_OPTION'):
        #     raise Exception('No args.login_url or env.OPENAI_LOGIN_URL !')
        
    if not email:
        if args.email:
            os.environ['OPENAI_EMAIL'] = args.email
        # elif not args.local or getenv('PANDORA_LOCAL_OPTION'):
        #     raise Exception('No args.email or env.OPENAI_EMAIL !')
        
    if not user_config_dir:
        if args.config_dir:
            os.environ['USER_CONFIG_DIR'] = args.config_dir
        
    # if not password:
    #     if args.password:
    #         os.environ['OPENAI_PASSWORD'] = args.password
    #     elif not args.local:
    #         raise Exception('No args.password or env.OPENAI_PASSWORD !')
        
    if args.server:
        if not site_password:
            if args.site_password:
                os.environ['PANDORA_SITE_PASSWORD'] = args.site_password
            else:
                raise Exception('No args.site_password or env.PANDORA_SITE_PASSWORD !')
        
    if args.password:
        os.environ['OPENAI_PASSWORD'] = args.password

    if args.mfa:
        os.environ['OPENAI_MFA_CODE'] = args.mfa

    if args.proxy:
        os.environ['PANDORA_PROXY'] = args.proxy

    if args.gpt4:
        os.environ['PANDORA_GPT4_MODEL'] = args.gpt4

    if args.gpt35:
        os.environ['PANDORA_GPT35_MODEL'] = args.gpt35

    if args.default_model:
        os.environ['PANDORA_DEFAULT_MODEL'] = args.default_model

    if args.best_history:
        os.environ['PANDORA_BEST_HISTORY'] = 'True'

    if args.local:
        os.environ['PANDORA_LOCAL_OPTION'] = 'True'

    if args.oai_only:
        os.environ['PANDORA_OAI_ONLY'] = 'True'

    if args.old_login:
        os.environ['PANDORA_OLD_LOGIN'] = 'True'

    if args.old_chat:
        os.environ['PANDORA_OLD_CHAT'] = 'True'

    if args.classic:
        os.environ['PANDORA_CLASSIC'] = 'True'

    if args.file_size:
        os.environ['PANDORA_FILE_SIZE'] = args.file_size

    if args.type_whitelist:
        os.environ['PANDORA_TYPE_WHITELIST'] = args.type_whitelist

    if args.type_blacklist:
        os.environ['PANDORA_TYPE_BLACKLIST'] = args.type_blacklist

    if args.file_access:
        os.environ['PANDORA_FILE_ACCESS'] = args.file_access

    if args.true_del:
        os.environ['PANDORA_TRUE_DELETE'] = 'True'

    if args.timeout != '60':
        os.environ['PANDORA_TIMEOUT'] = args.timeout

    if args.device_id:
        os.environ['OPENAI_DEVICE_ID'] = args.device_id

    if args.debug:
        os.environ['PANDORA_DEBUG'] = 'True'

    if args.isolate:
        if getenv('PANDORA_SITE_PASSWORD') == 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
            raise Exception('You have not set the site password, Unable to enable Isolation Mode!')
        
        os.environ['PANDORA_ISOLATION'] = 'True'

    if args.isolate_master:
        os.environ['PANDORA_ISOLATION_MASTERCODE'] = args.isolate_master

    if args.oai_proxy:
        os.environ['OAI_PROXY'] = args.oai_proxy

    if args.oai_voice:
        os.environ['OAI_VOICE'] = 'True'

    if args.voice_wssurl:
        os.environ['VOICE_WSS_URL'] = args.voice_wssurl

    
    Console.debug_b(
        '''
            Pandora - A command-line interface to ChatGPT
            Original Github: https://github.com/zhile-io/pandora
            Original author: https://github.com/wozulong
            Secondary dev: https://github.com/GavinGoo/pandora-web/tree/dev
            Get access token: {}
            Version: {}'''.format(login_url or args.login_url, __version__), end=''
    )

    Console.debug_b(''', Mode: {}, Engine: {}
        '''.format('server' if args.server else 'cli', 'turbo' if args.api else 'free'), end='')
    
    Console.debug_b('    Support OAI: {}'.format('False' if args.local else 'True'), end='\n\n')

    if getenv('PANDORA_SITE_PASSWORD') == 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
        Console.warn('### You have not set the site password, which is very dangerous!')
        Console.warn('### You have not set the site password, which is very dangerous!')
        Console.warn('### You have not set the site password, which is very dangerous!', end='\n\n')
    
    Console.warn('Your Arguments:')
    for arg, value in vars(args).items():
        if arg == 'password' and value is not None:
            value = '******'
        if arg == 'config_dir' and not value:
            value = USER_CONFIG_DIR
        if arg == 'file_size' and value:
            value = value + ' MB'
        if arg == 'file_access' and value != 'True':
            value = 'False'
        Console.debug_b(f"{arg}: {value}")
        if arg == 'site_password' and value == 'I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD':
            Console.warn(arg+': ### NO_SITE_PASSWORD_IS_A_DANGEROUS_SETTING!')
        if arg == 'proxy_api' and value == 'https://chat.openai.com':
            Console.warn('### Please be sure to pay attention to the environmental risk control, and ONLY recommend the use of non-valuable account!')
    Console.warn('')

    if args.api:
        try:
            from .openai.token import gpt_num_tokens
            from .migrations.migrate import do_migrate

            do_migrate()
        except (ImportError, ModuleNotFoundError):
            Console.error_bh('### You need `pip install Pandora-ChatGPT[api]` to support API mode.')
            return

    access_tokens = parse_access_tokens(args.tokens_file, args.api) if args.tokens_file else None

    if not access_tokens and not args.local:
        access_token, need_save = confirm_access_token(args.token_file, args.server, args.api, args.email, args.password, args.mfa)
        if not access_token:
            # Console.info_b('Please enter your email and password to log in ChatGPT!')
            if not args.login_local:
                Console.warn('We login via {}'.format(getenv('OPENAI_API_PREFIX')))

            email = args.email  # or Prompt.ask('  Email')
            password = args.password
            # if password is None:
            #     Prompt.ask('  Password', password=True)
            #     os.environ['OPENAI_PASSWORD'] = password
            # mfa = getenv('OPENAI_MFA_CODE') or Prompt.ask('  MFA Code(Optional if not set)')
            mfa = args.mfa
            if email and password:
                Console.warn('### Do login, please wait...')
                access_token = Auth0(email, password, args.proxy, mfa=mfa).auth(args.login_local)

                if not check_access_token_out(access_token, args.api):
                    return

                if need_save:
                    if args.server or Confirm.ask('Do you want to save your access token for the next login?', default=True):
                        save_access_token(access_token)

        access_tokens = {'default': access_token}

    else:
        access_tokens = {'default': None}

    if args.api:
        from .turbo.chat import TurboGPT

        chatgpt = TurboGPT(access_tokens, args.proxy)
    else:
        chatgpt = ChatGPT(access_tokens, args.proxy, int(args.timeout), args.local, args.oai_only, args.debug, args.isolate)

    if args.server or getenv("PANDORA_SERVER"):
        return ChatBotServer(chatgpt, args.verbose).run(args.server or getenv("PANDORA_SERVER"), args.threads or int(getenv("PANDORA_THREADS", 8)))

    ChatBotLegacy(chatgpt).run()


def run():
    hook_except_handle()

    try:
        main()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = traceback.extract_tb(exc_traceback)

        filename = traceback_details[-1].filename
        line_num = traceback_details[-1].lineno
        print(f"Exception occurred in file {filename} at line {line_num}: {e}")
        Console.error_bh('### Error occurred: ' + str(e))
        Console.error_bh(f'### Exception occurred in file {filename} at line {line_num}: {e}')

        if __show_verbose:
            logger.exception('Exception occurred.')


if __name__ == '__main__':
    run()
