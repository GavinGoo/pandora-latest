import hashlib
import json
import random
import re
import time
import uuid
import base64
import hashlib
import traceback
from os import getenv
from binascii import hexlify
from datetime import datetime, timedelta, timezone

import ua_generator
from curl_cffi import requests
from certifi import where

from .utils import Console
from .env import navigator_key, document_key, window_key, cores, memorys, screens, timeLayout

session = requests.Session()

def __auth_generator(auth_list):
    while True:
        for auth in auth_list:
            yield auth

oai_proxy_str = getenv("OAI_PROXY", None)
if oai_proxy_str:
    oai_proxy_url_list = oai_proxy_str.split(',')
    oai_proxy_url_iter = __auth_generator(oai_proxy_url_list)
ua = ua_generator.generate(device='mobile', browser='safari', platform='ios')
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
OAI_Device_ID = str(uuid.uuid4())
req_kwargs = {
    # 'proxies': {
    #     'http': proxy,
    #     'https': proxy,
    # } if proxy else None,
    'verify': where(),
    'timeout': 60,
    # 'allow_redirects': False,
    # 'impersonate': 'safari17_0',
    # 'impersonate': 'chrome110',
    'impersonate': 'safari17_2_ios',
    # 'http_version': 1,
}

host_url = "https://chatgpt.com"
headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'oai-device-id': OAI_Device_ID,
            'oai-language': 'en-US',
            'origin': host_url,
            'priority': 'u=1, i',
            'referer': f'{host_url}/',
            'sec-ch-ua': ua.ch.brands,
            'sec-ch-ua-mobile': ua.ch.mobile,
            'sec-ch-ua-platform': ua.ch.platform,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent
        }

oai_script = "https://chatgpt.com/backend-api/sentinel/sdk.js"
oai_dpl = ""
dpl_time = 0



def get_dpl():
    global oai_script, oai_dpl, dpl_time, req_kwargs, headers
    if oai_proxy_str:
        oai_proxy = next(oai_proxy_url_iter)
        req_kwargs['proxies'] = {
            'http': oai_proxy,
            'https': oai_proxy,
        }
        Console.success(f"OAI Pow Using proxy: {oai_proxy}")

    headers['oai-device-id'] = str(uuid.uuid4())
    Console.success(f"oai-device-id: {headers['oai-device-id']}")

    if int(time.time()) - dpl_time < 86400:
        return True

    try:
        r = session.get(f"{host_url}/", headers=headers, **req_kwargs)
        if r.status_code == 200:
            match = re.search(r'data-build="([^"]+)"', r.text[:150])
            if match:
                data_build = match.group(1)
                oai_dpl = data_build
                dpl_time = int(time.time())
                Console.warn(f"Found dpl: {oai_dpl}")
            
                return True
        else:
            Console.error(f"Failed to get dpl from webpage: {r.status_code}")
    except Exception as e:
        error_detail = traceback.format_exc()
        Console.debug(error_detail)
        Console.warn(f"Failed to get dpl: {e}")

def get_time():
    #timeLayout = "%a %b %d %Y %H:%M:%S"
    now = datetime.now(timezone(timedelta(hours=+8)))
    return now.strftime(timeLayout) + " GMT+0800 (Singapore Standard Time)"

def get_js_heap_size_limit():
    _memory = random.choice(memorys) - 1
    total_memory = _memory * 1024 * 1024 * 1024  # GB -> B
    heap_size_limit = total_memory * 0.15

    return int(heap_size_limit + random.randint(-100 * 1024 * 1024, 500 * 1024 * 1024))

def get_config():
    #_core = random.choice(cores)
    _screen = random.choice(screens)
    _navigator_key = random.choice(navigator_key)
    _document_key = random.choice(document_key)
    _window_key = random.choice(window_key)
    
    config = [
        _screen,
        get_time(),
        get_js_heap_size_limit(),
        random.random(),
        user_agent,
        oai_dpl,
        "en-US",
        "en-US,en",
        random.random(),
        _navigator_key,
        _document_key,
        _window_key,
        time.perf_counter(),
        str(uuid.uuid4()),
        '',
        #_core,
        12,
        round(time.time(), 1)
    ]

    return config


def get_pow(payload, access_token):
    r_headers = headers.copy()
    r_headers['Authorization'] = f"Bearer {access_token}"
    # Console.warn(r_headers)
    # url = "https://chatgpt.com/backend-api/sentinel/chat-requirements"
    r = session.post(f"{host_url}/backend-api/sentinel/chat-requirements", headers=r_headers, json=payload, **req_kwargs)
    if r.status_code == 200:
        # Console.warn(f"Got pow data: {r.text}")
        resp = r.json()
        Console.success('get_pow')
        turnstile = resp.get('turnstile', {})
        turnstile_required = turnstile.get('required')
        if turnstile_required:
            Console.debug('Turnstile is required')

        pow = resp.get('proofofwork', {})
        pow_required = pow.get('required')
        proof_token = resp.get('token')
        # Console.success(f"Proof token: {proof_token}")
        Console.success("Get Proof token Succeeded")
        if pow_required:
            Console.debug('Proof of work is required')
            return pow.get('seed'), pow.get('difficulty'), proof_token
        
    else:
        Console.error(f"Failed to get pow: {r.status_code}")


def proof_of_work(seed, diff, config):
    diff_len = len(diff) // 2
    hasher = hashlib.sha3_512()
    
    for i in range(100000):
        config[3] = i
        config_encode = json.dumps(config).encode('utf-8')
        base = base64.standard_b64encode(config_encode).decode('utf-8')
        hasher.update((seed + base).encode('utf-8'))
        hash = hasher.digest()
        hasher = hashlib.sha3_512()  # 重置hasher
        if hexlify(hash[:diff_len]).decode('utf-8') <= diff:
            return "gAAAAAB" + base
        
    return ("gAAAAABwQ8Lk5FbGpA2NcR9dShT6gYjU7VxZ4D" + 
            base64.standard_b64encode(json.dumps(seed).encode('utf-8')).decode('utf-8'))


def get_requirements_token_prefix(config):
    p = proof_of_work(format(random.random()), "0fffff", config)
    return 'gAAAAAC' + p


def get_requirements_token(access_token, only_proof_token=False):
    get_dpl()
    env_config = get_config()
    p = get_requirements_token_prefix(env_config)
    pow_data = {'p': 'gAAAAAC' + p}

    seed, diff, proof_token = get_pow(pow_data, access_token)
    if only_proof_token:
        return proof_token
    
    Console.success(f"seed: {seed}, diff: {diff}")
    proof_of_work_result = proof_of_work(seed, diff, env_config)

    return proof_of_work_result



def get_voice_url(access_token, voice_mode="standard"):
    proof_token = get_requirements_token(access_token, only_proof_token=True)
    if not proof_token:
        Console.error("Failed to get proof token")
        return None
    
    headers = {
        "content-type": "application/json",
        "user-agent": user_agent,
        "authorization": "Bearer {}".format(access_token),
    }

    payload_advanced = {"parent_message_id":"root",
                "voice":"ember",
                "language_code":"auto",
                "voice_session_id":str(uuid.uuid4()),
                "timezone_offset_min":-480,
                "voice_mode":"advanced",
                "model_slug":"auto",
                # "model_slug":"gpt-4o",
                "model_slug_advanced":"auto",
                # "model_slug_advanced":"gpt-4o",
                "chatreq_token":proof_token,
                # "chatreq_token":"default",
    }

    payload_standard = {
        "voice": "cove",
        "voice_mode": "standard",
        "parent_message_id": str(uuid.uuid4()),
        "model_slug": "auto",
        "voice_training_allowed": False,
        "enable_message_streaming": False,
        "language": "zh",
        "video_training_allowed": False,
        "voice_session_id": str(uuid.uuid4())
    }

    # data = payload_advanced if getenv("VOICE_MODE", None) == "advanced" else payload_standard
    resp = session.post("https://chatgpt.com/voice/get_token", headers=headers, json=payload_standard if voice_mode == "standard" else payload_advanced, **req_kwargs)
    status_code = resp.status_code
    if status_code != 200:
        Console.error(f"Failed to get voice token: {status_code}")
        return None
    
    Console.success(f"OAI Voice Mode: {voice_mode}")
    voice_data = resp.json()
    wss_url = getenv("VOICE_WSS_URL", voice_data["url"])
    livekit_url = "https://meet.livekit.io/custom?liveKitUrl={}&token={}#{}".format(
        wss_url, voice_data["token"], voice_data["e2ee_key"]
    )

    return livekit_url