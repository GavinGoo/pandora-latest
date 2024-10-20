<br />

<p align="center">
  <h3 align="center">潘多拉Web · PandoraWeb</h3>
  <p align="center">
    复活吧 我的Pandora
  </p>
  <p align="center">感谢原作者: 
      <a target="_blank" href="https://github.com/wozulong">Zhile(始皇)</a>
        源码在
      <a target="_blank" href="https://github.com/GavinGoo/pandora-web/tree/master">Master</a>
      分支
  </p>
</p>



## 一睹为快

![login_new](https://github.com/GavinGoo/pandora-web/blob/dev/doc/images/login_new.jpg)

![chat_new](https://github.com/GavinGoo/pandora-web/blob/dev/doc/images/chat_new.jpg)

![login_old](https://github.com/GavinGoo/pandora-web/blob/dev/doc/images/login_old.png)

![PandoraNeverDie](https://github.com/GavinGoo/pandora-web/blob/dev/doc/images/PandoraNeverDie.png)





## 相关特性

- 两套UI任君选择，随意搭配
- 支持设置站点密码
- 支持隔离用户对话(隔离码长度不少于四位)
- 支持老Pandora式的无密码直接访问(见后文配置说明)
- API对话自动保存
- 重定向3.5/4模型
- 携带历史对话(可单独对模型设定、可设置当历史消息数量大于设定数量时，自动携带第一组历史对话)
- 模型`Auth`轮询
- 单独指定模型的网络代理
- 设定内置Prompt
- 隐藏(假删除)对话(默认,可更改)
- 仅 ~~OAI(仅支持3.5/4o模型)~~ /API模式或二者共存运行
- 文生图模型可调用其他文本模型以生成/优化你的绘图Prompt
- 对于某些以二进制文件(Blob对象)作为响应的文生图模型(比如Cloudflare AI)，自动保存并转为url输出(若使用了CDN服务，请注意**流量消耗**)
- 文件上传(支持以Base64编码/Url携带(需公网)、支持类型/大小限制)
- ~~(3月24日)可以本地网络环境使用`Access Token`进行3.5对话，详见后文`更新日志0324`部分~~ (能力有限 不再支持 抱歉)



**API模型支持：**

- 支持3.5免登的[aurora项目](https://github.com/aurora-develop/aurora)
- COP2GPT
- DALL·E
- ChatGLM 4V
- ChatGLM 4
- [kimi-free-api项目](https://github.com/LLM-Red-Team/kimi-free-api)
- [glm-free-api项目](https://github.com/LLM-Red-Team/glm-free-api)(请将`slug`参数配置为`glm-free-api`)
- [emohaa-free-api项目](https://github.com/LLM-Red-Team/emohaa-free-api)
- Gemini Pro
- Gemini Pro Vision
- Cloudflare AI文本模型(**4月1日开始收费**)
- Cloudflare AI文生图模型(`stable-diffusion-xl-base-1.0`, `dreamshaper-8-lcm`, `stable-diffusion-xl-lightning`)(**4月1日开始收费**)
- 某个连夜改成每月仅免费50条消息的模型
- 其他OpenAI标准输出模型





## 配置说明

### 程序参数：

> 20241020：因能力有限，不再支持OAI相关代理，也请无视相关变量/参数，在此表示抱歉

```
--email: 您的 OpenAI 邮箱。
--password: 您的 OpenAI 密码(不建议直接设置密码，可仅配置Email然后在终端输入密码)。
--mfa: 您的 OpenAI MFA认证码。
--proxy_api: OpenAI 前端的代理地址。
--login_url: 获取Access Token的地址。
--site_password: 网站密码。如果以server模式启动，必须设置此项。
-p/--proxy: 使用代理。格式为 protocol://user:pass@ip:port。
--gpt4: 从 "api.json" 文件中选择 GPT-4 的请求模型。
--gpt35: 从 "api.json" 文件中选择 GPT-3.5 的请求模型。
--history_count: 为 API 携带的历史消息数量。默认为4。
--best_history: 当历史消息数量大于设定数量时，自动携带第一组历史对话。
--true_del: 【真正】从数据库中删除对话，而非将其设为隐藏(is_visible=0)。
-l/--local: 仅在本地运行，不使用 OAI 服务。
--timeout: 请求超时，默认60s，单位(秒)。
--oai_only: 仅使用 OAI 服务。
-t/--token_file: 指定Access Token文件。
--tokens_file: 指定一个存放多Access Token的文件路径。
--config_dir: 指定配置目录存放Access Token的access_token.dat文件、API配置文件api.json、本地对话数据库文件local_conversation.db、以二进制文件(Blob对象)作为响应的文生图模型图片保存目录text2img、登录会话目录sessions(默认跟随系统,docker则位于/data)
-s/--server: 作为一个代理服务器启动。格式为 ip:port，默认为 0.0.0.0:8008。
--threads: server模式的线程数，默认为8。
-a/--api: 使用gpt-3.5-turbo 聊天 API。注意：OpenAI 将会向您收费。
--login_local: 使用本地环境登录，你可能需要一个合适的代理IP以避免账号被风控！
-v/--verbose: 显示调试信息，且出错时打印异常堆栈信息，供查错使用。
--old_login: 使用老Pandora登陆页面。
--old_chat: 使用老Pandora聊天页面。
--file_size: 限制上传文件的大小。单位：MB。
--type_whitelist: 限制上传文件的后缀名(白名单)，以英文逗号","分隔。
--type_blacklist: 限制上传文件的后缀名(黑名单)，以英文逗号","分隔。
--file_access: 是否允许外网直接访问文件(如果对话希望以url携带文件，则需要True启用)。默认：False。
--device_id: 官方OAI3.5对话时请求头参数"Oai-Device-Id", 若不配置则从用户浏览器的请求头中获取。多人共享【建议配置】。
--debug: 打印发送消息的请求体(前500字符)与收到的第一条响应。
-i/--isolate: 隔离对话模式(隔离码长度不少于四位)。
--isolate_master: 管理员隔离码。此隔离码允许管理者查看所有隔离对话。
```



### 环境变量：

> 20241020：因能力有限，不再支持OAI相关代理，也请无视相关变量/参数，在此表示抱歉

1. `OPENAI_EMAIL`, `OPENAI_PASSWORD`,`OPENAI_MFA_CODE`: OAI账密相关(**不建议**直接设置密码，可仅配置Email然后在终端输入密码)。
2. `OPENAI_API_PREFIX`: OpenAI 前端的代理地址。
3. `OPENAI_LOGIN_URL`: 获取`Access Token`的地址。
4. `PANDORA_ACCESS_TOKEN`:  指定`Access Token`文件。
5. `PANDORA_TOKENS_FILE`: 指定一个存放多`Access Token`的文件路径。
6. `USER_CONFIG_DIR`: 指定配置目录存放`Access Token`的`access_token.dat`文件、API配置文件`api.json`、本地对话数据库文件`local_conversation.db`、以二进制文件(Blob对象)作为响应的文生图模型图片保存目录`text2img`、登录会话目录`sessions`(默认跟随系统，docker则位于/data)
7. `PANDORA_SERVER`: 以`http`服务方式启动，格式：`ip:port`，默认：`0.0.0.0:8008`。
8. `PANDORA_SITE_PASSWORD`: 站点密码，如果以server模式启动该值为必填。
9. `OPENAI_MFA_CODE`: OpenAI 的MFA认证码，可以通过命令行参数 `--mfa` 设置。
10. `PANDORA_PROXY`: 代理地址，可以通过命令行参数 `--proxy` 设置。
11. `PANDORA_GPT4_MODEL`: 从 "api.json" 文件中选择`GPT-4`模型。
12. `PANDORA_GPT35_MODEL`: 从 "api.json" 文件中选择`GPT-3.5`模型。
13. `PANDORA_HISTORY_COUNT`: 设置历史消息的数量，默认为`4`。
14. `PANDORA_BEST_HISTORY`: 当历史消息数量大于设定数量时，自动携带第一组历史对话。
15. `PANDORA_TRUE_DELETE`: **真正从数据库中**删除对话，而非将其设为隐藏(is_visible=0)。
16. `PANDORA_LOCAL_OPTION`: 仅API模式，不使用 OAI 服务。
17. `PANDORA_TIMEOUT`: 请求超时，默认`60`s，单位(秒)。
18. `PANDORA_OAI_ONLY`: 仅使用 OAI 服务。
19. `PANDORA_OLD_LOGIN`: 使用老Pandora登陆页面。
20. `PANDORA_OLD_CHAT`: 使用老Pandora聊天页面。
21. `PANDORA_FILE_SIZE`: 限制上传文件的大小。单位：MB。
22. `PANDORA_TYPE_WHITELIST`: 限制上传文件的后缀名(白名单)，以英文逗号","分隔。
23. `PANDORA_TYPE_BLACKLIST`: 限制上传文件的后缀名(黑名单)，以英文逗号","分隔。
24. `PANDORA_FILE_ACCESS`: 是否允许外网直接访问文件(如果对话希望以url携带文件，则需要True启用)。默认：`False`。
25. `OPENAI_DEVICE_ID`: 官方OAI3.5对话时请求头参数"Oai-Device-Id", 若不配置则从用户浏览器的请求头中获取。多人共享**建议配置**。
26. `PANDORA_API`: 使用`gpt-3.5-turbo`API请求，**你可能需要向`OpenAI`支付费用**。
27. `PANDORA_LOGIN_LOCAL`: 使用本地环境登录，**你可能需要一个合适的代理IP以避免账号被风控！**
28. `PANDORA_VERBOSE`: 显示调试信息，且出错时打印异常堆栈信息，供查错使用。
29. `PANDORA_THREADS`: server模式的线程数，默认为`8`。
30. `PANDORA_CLOUD`: Pandora Cloud模式(原参数，不知还可用否?)。
31. `PANDORA_SERVERLESS`: vercel部署请启用，将`api.json`指向项目根目录的`data`文件夹(请不要将密钥直接填写到文件)
32. `PANDORA_DEBUG`: 可设置`True`以打印发送消息的请求体(前500字符)与收到的第一条响应
33. `PANDORA_ISOLATION`: 可设置`True`以启用隔离对话模式(隔离码长度不少于四位)。
34. `PANDORA_ISOLATION_MASTERCODE`: 管理员隔离码。此隔离码允许管理者查看所有隔离对话。

> 使用Docker仅配置环境变量即可，无视上述`程序参数`。
>
> 如果想实现老Pandora无登录功能点开即用，将`--site_password`/`PANDORA_SITE_PASSWORD`设置为`I_KNOW_THE_RISKS_AND_STILL_NO_SITE_PASSWORD`即可(这可能是个危险设置，请注意)。



### API配置：

使用`api.json`文件配置，默认位于用户配置目录，可通过环境变量`USER_CONFIG_DIR`或程序参数`config_dir`设置

> 默认用户配置目录：
>
> Mac OS X: same as user_data_dir (Python appdirs模块的说明)
> Unix: ~/.config/Pandora-ChatGPT # or in $XDG_CONFIG_HOME, if defined
> Win : C:\Users\\`<User Name>`\AppData\Local\Pandora-ChatGPT\Pandora-ChatGPT
>
> 无论是否设置，启动时都会把路径打印出来

以下是参考模板：

```json
{
    "glm-4v": {
        "slug": "glm-4v",
        "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "auth": "<智谱AI Token>",
        "title": "ChatGLM-4V",
        "description": "ChatGLM-4V",
        "upload": true,
        "file_base64": true,
        "history_count": 10,
        "max_tokens": 8191 
    },
    "kimi": {
        "slug": "kimi",
        "url": "http://172.17.0.1:8000/v1/chat/completions",
        "auth": "<Your Refresh Token>",
        "title": "Kimi",
        "description": "Kimi",
        "upload": true,
        "max_tokens": 8191 
    },
    "coze": {
        "slug": "coze",
        "url": "<Coze-Discord-Proxy Url>",
        "auth": "<Coze-Discord-Proxy AUTH>",
        "title": "Coze(可联网)",
        "description": "https://coze.com",
        "max_tokens": 8191 
    },
    "glm-4": {
        "slug": "glm-4",
        "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "auth": "<智谱AI Token>",
        "title": "ChatGLM-4",
        "description": "ChatGLM-4",
        "max_tokens": 8191 
    },
    "cogview-3": {
        "slug": "cogview-3",
        "url": "https://open.bigmodel.cn/api/paas/v4/images/generations",
        "auth": "<智谱AI Token>",
        "title": "CogView(文生图|收费)",
        "description": "刚开始没留意这玩意不是消耗token额度，现在倒欠3块大洋还没还",
        "max_tokens": 8191 
    },
    "gemini-pro": {
        "slug": "gemini-pro",
        "url": "https://generativelanguage.googleapis.com/v1/models/gemini-pro:streamGenerateContent?key=<Your Google AI Key>",
        "title": "Gemini-Pro",
        "description": "Gemini-Pro",
        "max_tokens": 8191 
    },
    "llama-2-7b-chat-fp16": {
        "slug": "llama-2-7b-chat-fp16",
        "url": "https://api.cloudflare.com/client/v4/accounts/<Your Cloudflare Account ID>/ai/run/@cf/meta/llama-2-7b-chat-fp16",
        "auth": "<Your Cloudflare AI Key>",
        "title": "llama-2-7b-chat-fp16",
        "description": "llama-2-7b-chat-fp16",
        "max_tokens": 8191 
    },
    "stable-diffusion-xl-base-1.0": {
        "slug": "stable-diffusion-xl-base-1.0",
        "url": "https://api.cloudflare.com/client/v4/accounts/<Your Cloudflare Account ID>/ai/run",
        "image_model": "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        "prompt_model": "glm-4",
        "prompt": "You are a professional ai prompt generator, now please seriously realize the scene and atmosphere of the text and generate an AI drawing prompt about '<Prompt>', please don't show any Chinese, if there is any Chinese, it will be automatically translated to English. Finally, you can output the main content of the prompt directly.",
        "auth": "<Your Cloudflare AI Key>",
        "title": "cfai(文生图)",
        "description": "cfai(文生图)",
        "max_tokens": 8191 
    },
    "gpt-4": {
        "slug": "gpt-4",
        "url": "<Your API Url>",
        "auth": ["鸡", "你", "太", "美"],
        "prompt": "You use the GPT-4 version of OpenAI’s GPT models.Respond in the following locale: zh-cn.",
        "title": "GPT-4",
        "description": "GPT-4",
        "max_tokens": 8191 
    }
}
```

> 参数说明：
>
> `键值`: 可为同模型不同来源而作区分
>
> `slug`: 请求时的模型名 ~~(请与键值保持一致)~~
>
> `url`: 模型请求的url
>
> `auth`: 模型请求的验证头(智谱家的与某模型会自动处理(`slug`需包含关键词比如`glm`)，直接填入你的Key即可)无则不写`auth`这个键，比如Gemini。**轮询**请参照`gpt-4`模型填写
>
> `proxy`: 指定该模型使用的网络代理(**优先级最高**)(如果使用Docker且网络模式非host,指向本机时请使用`172.17/18.0.1`或内网IP)，可设置为`""`意味着该模型不走代理
>
> `prompt`: 你的内置Prompt
>
> `title`: 前端页面上的模型显示名称
>
> `description`: 老Pandora页面上的模型描述
>
> `history_count`: 设置历史消息的数量，优先级最高
>
> `upload`: `true` 启用文件上传，如需以Url携带请配置`file_access`参数/`PANDORA_FILE_ACCESS`环境变量为`True`
>
> `file_base64`: `true` 文件以Base64编码
>
> `max_tokens`: (不知道啥玩意，官方有我也就顺便带上了)
>
> 特殊参数：
>
> `prompt_model`: 指定**文本模型**生成/优化绘图Prompt(使用**非流式**请求)，此时`prompt`支持使用"`<Prompt>`"作为原Prompt的占位符，当占位符不存在时则自动将原Prompt追加到文末(如果文生图模型非Cloudflare AI 即url非`"https://api.cloudflare.com/client/v4/accounts/<Your Cloudflare Account ID>/ai/run"`，则不支持Cloudflare AI的文本模型)
>
> `image_model`: 仅由用于Cloudflare AI文生图模型，填入`Model ID`。格式：`"@cf/***/<model>"`，参见：`"https://developers.cloudflare.com/workers-ai/models/<model>"`





## 如何运行

- 本地运行

  Python版本最好在`3.8`及以上(我的版本为3.10.0)

  进入项目根目录，运行：

  ```
  # 安装依赖
  pip install --no-cache-dir -r requirements.txt
  
  # 0324使用OAI服务(先将Access Token填入access_token.dat文件)：
  ## 如果不希望API模型走代理，可在api.json文件中为每个模型配置: "proxy":""
  python -m src.pandora.launcher -s \
  --proxy_api https://chat.openai.com \
  -p <你的网络代理地址> \
  --device_id <OAI官方前端发送对话的请求头参数"Oai-Device-Id"> \
  --site_password <Your Site Password> \
  --history_count 10 \
  --best_history
  
  # 启用OAI服务：
  python -m src.pandora.launcher -s --email <Your OAI Email> --proxy_api <Your OAI Service Proxy Endpoint> --login_url <Get Access Token Url> --site_password <Your Site Password> --history_count 10
  
  # 仅API模式：
  python -m src.pandora.launcher -s -l --site_password <Your Site Password>
  ```
  
  > 后台运行：`nohup python -m src.pandora.launcher -s -l --site_password <Your Site Password> &`
  
  
  
- Docker Hub 运行

  ```
  docker pull ghcr.io/gavingoo/pandora-web:dev
  ```

  ```
  # 0324使用OAI服务(先将Access Token填入access_token.dat文件)：
  ## 如果不希望API模型走代理，可在api.json文件中为每个模型配置: "proxy":""
  docker run -d -p 8008:8008 --restart=unless-stopped --name pandoraweb \
  -e PANDORA_SERVER=0.0.0.0:8008 \
  -e PANDORA_SITE_PASSWORD=<Your Site Password> \
  -e OPENAI_API_PREFIX=https://chat.openai.com \
  -e OPENAI_DEVICE_ID=<OAI官方前端发送对话的请求头参数"Oai-Device-Id"> \
  -e PANDORA_PROXY=<你的网络代理地址> \
  -e PANDORA_HISTORY_COUNT=10 \
  -e PANDORA_BEST_HISTORY=True \
  -v $PWD/pandora_web_data:/data \
  ghcr.io/gavingoo/pandora-web:dev
  
  # 仅API模式：
  docker run -d -p 8008:8008 --restart=unless-stopped --name pandoraweb \
  -e PANDORA_SERVER=0.0.0.0:8008 \
  -e PANDORA_SITE_PASSWORD=<Your Site Password> \
  -e PANDORA_HISTORY_COUNT=10 \
  -e PANDORA_BEST_HISTORY=True \
  -e PANDORA_LOCAL_OPTION=True \
  -v $PWD/pandora_web_data:/data \
  ghcr.io/gavingoo/pandora-web:dev
  	
  # 启用OAI服务：
  docker run -d -p 8008:8008 --restart=unless-stopped --name pandoraweb \
  -e PANDORA_SERVER=0.0.0.0:8008 \
  -e PANDORA_SITE_PASSWORD=<Your Site Password> \
  -e OPENAI_EMAIL=<Your OAI Email> \
  -e OPENAI_PASSWORD=<Your OAI Password> \
  -e OPENAI_API_PREFIX=<Your OAI Service Proxy Endpoint> \
  -e OPENAI_LOGIN_URL=<Get Access Token Url> \
  -e PANDORA_HISTORY_COUNT=10 \
  -e PANDORA_BEST_HISTORY=True \
  -v $PWD/pandora_web_data:/data \
  ghcr.io/gavingoo/pandora-web:dev
  ```

  

- Docker 编译运行

  ```
  git clone -b dev https://github.com/GavinGoo/pandora-web.git
  cd pandora-web
  docker build -t pandoraweb .
  ```

  

- Nginx 反向代理配置
  
  ```
    location / {
            proxy_http_version 	1.1;
            proxy_pass 		http://IP:Port;
            proxy_set_header	Connection		"";
            proxy_set_header   	Host			$http_host;
            proxy_set_header 	X-Forwarded-Proto 	$scheme;
            proxy_set_header   	X-Real-IP          	$remote_addr;
            proxy_set_header   	X-Forwarded-For    	$proxy_add_x_forwarded_for;
  
            proxy_buffering off;
            proxy_cache off;
            chunked_transfer_encoding on;
            tcp_nopush on;
            tcp_nodelay on;
        		
            send_timeout 600;
            proxy_connect_timeout 600;
            proxy_send_timeout 600;
            proxy_read_timeout 600;
            proxy_headers_hash_max_size 51200;
            proxy_headers_hash_bucket_size 6400;
    }
  ```



## 其他说明

* 本二改项目是站在原作者[Zhile](https://github.com/wozulong)与其他巨人的肩膀之上，感谢！！
* 感谢[EmccK](https://github.com/EmccK)、Lin Goo佬友对本项目的帮助

* 本人的代码水平太过糟糕，在此表示抱歉

* 最近这段时间除非重要Bug外可能实在没空维护



## 更新日志

### 0601 (请务必更新！！)：

- **fix 重大安全漏洞：未登录的情况下依然可以访问API，导致对话接口被转API**

### 0516：

- 支持OAI `GPT-4o`模型
  - 非仅API模式 或 未指定前端GPT-4的实际请求模型时，请在模型列表中选择第一项：`GPT-4`。
  - 无论账号是否支持`GPT-4o`模型/被风控暂不可见，都会强行请求。但实际具体是否为GPT-4o回答**视乎于OAI官方**。如果账号本身不支持`GPT-4o`模型(**从来没出现过动态模式**)，则回答必然是3.5。如果次数消耗完后，回答也必然是3.5。
  - 经测试，若账号**被风控**暂不可见(在官网表现为**只有3.5可选，动态模式消失，模型接口也只有3.5**)，回答依然可以是`GPT-4o`。
  - 当同时启用OAI与API模式时，若**API模型**刚好存在**完全同名**的`gpt-4o`模型，前端模型列表与对话保存将显示为`gpt-4o-api`，请求对话时会自动替换回`gpt-4o`，无需担心。
- 补全隔离模式下 OAI对话的删除与标题重命名功能
  - 之前忘记了，非常抱歉🙏🏼
- 隔离模式下使用设定的管理员隔离码进入，可查看隐藏对话(标题前带🔒标志)
- 由于个人能力问题，暂时无法实现文件上传，非常抱歉🙏🏼

### 0507：

- 修复OAI 3.5对话
- 修复可能导致隔离对话失败的问题
- 修复仅OAI模式无法启动的问题

### 0505：

- 支持隔离用户对话(Isolation Code)(隔离码长度不少于四位)
  - 使用`-i/--isolate`参数或设置环境变量`PANDORA_ISOLATION=True`以启用
- Chat页面替换了更实用的Prompt(逻辑强化、文章复述与分析、翻译、论文润色)
  - 逻辑强化：Take a deep breath and think step by step...  [来源](https://linux.do/t/topic/68360?u=manager)
  - 文章复述与分析：利用5W2H分析法对文章进行深入的解读和总结。[来源](https://linux.do/t/topic/68360?u=manager)
  - 翻译：英译中, 直译再意译。
  - 论文润色：论文润色写作, 并要求重复率低于10%。[来源](https://linux.do/t/topic/29874/2?u=manager)
- 模型选择列表的子菜单"Alpha Models"替换为"Other Models"

### 0412：

- 修复使用[aurora项目](https://github.com/aurora-develop/aurora)时对话异常
- 修复不显示重新生成的对话
- 修复触发`BEST_HISTORY`时出错

### 0404：

- 修复老潘多拉UI的对话问题
- 更好的错误日志输出
- 由于官方3.5又从ws改回sse，因此不再请求`register-websocket`接口

### 0401：

- 新增支持官方API、DALL·E
- 修复当请求出错后重新请求，错误地触发了新建对话(表现为出现重复标题的对话但无法打开)的问题

### 0328：

- 修复当启用OAI服务时若请求`register-websocket`报错429，由于直接返回了响应(OAI的报错页)导致泄露(代理)IP的**严重安全问题**，请**公网搭建**的佬友务必更新，同时在此致歉 !
- 修复多轮对话可能出现报错`sqlite3.OperationalError: no such table: conversations_file`并导致异常的BUG

### 0324：

- 修复对话列表无法加载58条之后的记录
- 修复OAI3.5对话
  - 需要使用本地网络环境(可设置代理)，将参数`proxy_api`/环境变量`OPENAI_API_PREFIX`配置为`https://chat.openai.com`，把`Access Token`填入/更新到用户配置目录(即`api.json`所在目录)下的`access_token.dat`文件。
  - **强烈建议**传入请求头参数"Oai-Device-Id"
  - 请务必注意**环境风控**，**仅**建议使用**无价值账号**
- 支持文件上传(以Base64编码/Url携带(需公网)、支持类型/大小限制)
- 支持[kimi-free-api](https://github.com/LLM-Red-Team/kimi-free-api)、[glm-free-api](https://github.com/LLM-Red-Team/glm-free-api)、[emohaa-free-api](https://github.com/LLM-Red-Team/emohaa-free-api)项目
- 前端直接显示接口报错内容
- 将GPT4叽里呱啦的模型说明改为"Be more powerful"，简洁有力
- 去掉"Upgrade plan"按钮
- 尝试支持Vercel部署(还未测试)
