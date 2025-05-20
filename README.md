<h1 align="center">JM PDF Plugin</h1>

<div align="center">

一个基于**LangBot**的漫画下载插件🧩

将你想看的漫画转换为PDF，上传到QQ群聊/QQ私信中

**支持缓存**，**指定章节下载**，**文案匹配**，**定时撤回**，**关键词搜索**，**白名单管理**✨

</div>

<div align="center">

![Status](https://img.shields.io/badge/状态-开发中-green)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![Contributors](https://img.shields.io/github/contributors/AmethystTim/JM-PDF-plugin.svg?style=flat&label=贡献者&color=red)
![forks](https://img.shields.io/github/forks/AmethystTim/JM-PDF-plugin.svg?style=flat&label=分支数)
![stars](https://img.shields.io/github/stars/AmethystTim/JM-PDF-plugin?style=flat&label=星标数&color=yellow)
![issues](https://img.shields.io/github/issues/AmethystTim/JM-PDF-plugin?&color=green)

</div>

<hr>

## ✨  插件特性

|功能描述|实现情况|
|:-:|:-:|
|漫画转PDF|✅|
|指定章节转换|✅|
|匹配文案对应jmID|✅|
|定时撤回|✅|
|缓存漫画|✅|
|关键词搜索|✅|
|白名单管理|✅|
|指令管理|✅|
|定时撤回|✅|
|获取分类/排行榜|✅|

---

## ⚙️ 插件架构

```
JM-PDF-plugin/
│
├── cells/                # 独立模块
│   ├── apicaller.py      # 消息平台API调用模块
│   ├── argsparser.py     # 参数解析模块
│   ├── controller.py     # 访问控制模块
│   ├── converter.py      # 转换器模块
│   └── downloader.py     # 下载器模块
│
├── utils/                # 实用工具模块
│   ├── cacheclener.py    # 缓存清理模块
│   ├── filehandler.py    # 文件处理模块
│   ├── searchhandler.py  # 站内搜索模块
│   └── rankhandler.py    # 排行榜模块
│
├── handlers/             # 指令处理模块
│   ├── jmmanga.py        # 处理漫画下载
│   ├── jmsearch.py       # 处理漫画搜索
│   ├── jmclear.py        # 处理缓存清理
│   └── jmrank.py         # 处理排行榜查询
│
├── config.yml            # JM下载配置文件
├── commands.yml          # 指令管理配置文件
├── docker.yml            # docker补丁配置文件
│
├── main.py               # 插件主程序入口
├── requirements.txt      # 依赖列表
│
└── README.md             # 项目说明文档
```

## 🧭 使用方法

### 1. 插件安装

#### 方法一：管理员账号安装

配置完成 [LangBot](https://github.com/RockChinQ/LangBot) 主程序后使用管理员账号向机器人发送命令即可安装：

```
!plugin get https://github.com/AmethystTim/JM-PDF-plugin.git
```
或查看详细的[安装说明](https://docs.langbot.app/insight/guide)

#### 方法二：git安装（推荐）

进入`Langbot`的`plugins`目录，使用`git`克隆仓库：

```
git clone https://github.com/AmethystTim/JM-PDF-plugin.git
```

#### 方法三：插件市场安装

访问`Langbot webui`（默认为`127.0.0.1:5300`），进入**插件市场**，搜索`JM-PDF-plugin`进行安装

---

### 2. 网络配置

请根据你的消息平台进行网络配置

#### 2.1 NapCat配置

- 访问`NapCat`消息平台的webui（默认为`http://127.0.0.1:6099`）
- 在**网络配置**栏目中新建**HTTP服务器**
- 主机填写为`127.0.0.1`，端口填写为`3000`

<div align="center">

<img src="./images/napcat_1.png" width="60%">

</div>

> [!Warning]
>
> 请勿在网络配置中填写**token**，确保**token**一栏为空


#### 2.2 Lagrange配置

- 在`appsettings.json`中修改`Implementations`部分
- 新增`"Type": "HTTP"`一项，具体配置参考如下：

```json
"Implementations": [
    {
        "Type": "ReverseWebSocket",
        "Host": "127.0.0.1",
        "Port": 2280,
        "Suffix": "/ws",
        "ReconnectInterval": 5000,
        "HeartBeatInterval": 5000,
        "AccessToken": ""
    },
    {
        "Type": "Http",
        "Host": "127.0.0.1",
        "Port": 3000,
        "AccessToken": ""
    }
]
```

> [!Note]
> 
> 目前Lagrange不支持**在私聊中发送PDF文件**，为体验所有功能，推荐使用NapCat消息平台

#### 2.3 LLOneBot配置

- 在注入版QQ中打开设置，进入LLOneBot栏目，进行网络配置
- 启用HTTP服务，并将HTTP服务监听端口设置为`3000`

<div align="center">

<img src="./images/llonebot_1.png" width="80%">

</div>

> [!Tip]
> 
> 网络配置完成后可以使用`curl 127.0.0.1:3000`测试是否连通，出现
> ```
> StatusCode        : 200
> StatusDescription : OK
> Content           : xxx is running/xxx 已启动
> ```
> 则说明网络配置成功
> 
> 若发生端口冲突，请将端口修改为其他值，比如`3001`，同时将`main.py`文件
> ```
> self.msg_platform = MsgPlatform(port=3000)
> ```
> 一行的端口`3000`修改为新端口值

---

### 3. 偏好配置

> [!Note]
> 
> 由于LangBot v4.0之后采用清单文件来注册插件，所以此后的配置编写会在webui上进行
> 
> 目前作者正在努力适配，LangBot v3.x的用户仍然使用配置文件进行配置

#### 3.1 下载配置 config.yml

- `dir_rule`部分：修改`base_dir`为你想存储漫画的目录，若使用Docker部署LangBot，请参考注释说明
- `client`部分：若均无法访问可尝试用“**#**”注释掉`client`所有部分，使用默认配置的域名列表
- `download`部分：一般情况下可忽略
- `plugins`部分：大部分漫画都可以在**无登录状态下**访问/下载，但是有些漫画需要登录才可以查看，若有需要可以配置你的账号信息

```yaml
# Github Actions 下载脚本配置
version: '2.0'

################################################
# 特别注意：                            
# 如果你是使用Docker部署LangBot的用户，请按照以下步骤修改配置文件：
#
# 将dir_rule中的base_dir一项修改为LangBot容器内的可达路径
#
# 根据LangBot的挂载配置，你目前可以在这两个目录下选择你想存储PDF的位置
#    - /app/data
#    - /app/plugins 
#
# 例如："/app/plugins/JM-PDF-plugin/downloads/"
################################################

dir_rule:
  base_dir: "C:\\Users\\Hello\\Desktop\\downloads" # 漫画/PDF的存储目录（注意转义字符的使用）
  rule: Bd_Aid_Pindex

# 域名配置，若均无法访问可尝试用“#”注释client所有部分，以使用默认配置的域名列表
client:
  impl: api
  domain:
    api:
      - www.cdnmhws.cc
      - www.cdnuc.vip
      - www.cdnmhwscc.vip
      - www.cdnblackmyth.club

# 下载配置，无需关注
download:
  cache: true # 如果要下载的文件在磁盘上已存在，不用再下一遍了吧？
  image:
    decode: true # JM的原图是混淆过的，要不要还原？
    suffix: .jpg # 把图片都转为.jpg格式
  threading:
    # batch_count: 章节的批量下载图片线程数
    batch_count: 45

# jmcomic包插件项配置，非必需配置
plugins:
  after_init:
    - plugin: login # 登录插件，以下载某些需要登录才能下载的漫画，需要配置登录信息
      kwargs:
        username: your_username # 用户名
        password: your_password # 密码
```
> [!warning]
>
> 如果使用**MacOS**部署NapCat，需要将`base_dir`一项修改为`NapCat`的缓存目录
> 
> ```
> /Users/<your_username>/Library/Containers/com.tencent.qq/Data/.config/QQ/NapCat/temp
> ```
>
> 否则无法进行PDF文件的发送

---

#### 3.2 指令管理 commands.yml

- `whitelist`部分：若要启用群聊白名单，请将`enabled`设置为`true`，并填入需要加入白名单的群聊id
- `commands`部分：为了防止意外触发某些指令炸群，请根据你的实际需求禁用/激活指令，若要禁用某指令，请将对应值由`true`修改为`false`
- 以上配置需要**重载插件**/**重启bot**后才会生效

```yaml
# 插件指令管理

# 白名单机制，启用后仅允许白名单群聊/用户使用指令
whitelist: 
  # 是否启用白名单
  enabled: false
  # 白名单群聊/用户id
  groups: [
    114514,
  ]
  users: [
    1919810,
  ]

# 指令管理列表，若需禁用某指令，则将其对应值由true修改为false
commands: [
  # 指令：/jm [jmID] [chapter]
  "/jm [ID] [CHAPTER]": true,
  # 指令：/jm search [keyword]
  "/jm search [KEYWORD]": true,
  # 指令： 清除缓存
  "/jm clear": true,
  # 指令：文案匹配
  "[text]": false,
]
```

#### 3.3 Docker相关配置 docker.yml

针对使用`Docker`部署`Langbot`的用户的配置，若不是使用`Docker`部署LangBot的用户，请**忽略此项配置**

- `docker_cfg`部分：修改`enabled`为`true`
- `host_base_dir`部分：修改为宿主机上PDF的实际存储目录

```yaml
################################################
# 特别注意：                            
# 如果你是使用Docker部署LangBot的用户，请按照以下步骤修改配置文件：
# 修改docker_cfg配置项
# - 将enabeld设置为true
# - 将host_base_dir修改为宿主机上PDF的实际存储目录
#
# 例如: "C:\\Users\\Hello\\Desktop\\downloads"
################################################

docker_cfg: # 非Docker部署LangBot用户请无视此项
  enabled: false # 是否使用Docker部署LangBot
  host_base_dir: "C:\\Users\\Hello\\Desktop\\downloads" # 宿主机上PDF的实际存储目录（注意转义字符的使用）
```

---

## ❓ 常见问题

|Q|A|
|-|-|
|漫画下载失败|1. 检查网络配置，推荐添加网络代理<br>2. 检查`jmcomic`包是否为最新版本，建议`pip install -U jmcomic`后重启bot（issue [#23](https://github.com/AmethystTim/JM-PDF-plugin/issues/23)）<br>3. 在`config.yml`内`client`的`domain`一项中添加可用域名或将`client`全部注释掉以使用默认域名列表|
|与`langbot`内置AI对话冲突|issue [#4](https://github.com/AmethystTim/JM-PDF-plugin/issues/4)|
|控制台报错：无效的`apikey`|非插件报错，可能是LangBot的`provider.json`配置有误|

> 有其他问题欢迎提issue或在交流群讨论

---

## 🤖 指令

|指令|说明|参数|备注|
|-|-|-|-|
|`/jm (help)`|查看帮助信息|-|可选参数：`help`|
|`/jm [jmID] [chapter]`|下载漫画指定章节|`jmID` `chapter`|`chapter`：指定章节，若不指定默认转换第一章|
|`/jm search [keyword]`|搜索漫画|`keyword`|`keyword`：搜索关键字|
|`/jm rank [duration]`|查询排行榜|`duration`|`duration`：排行榜时间范围，可选值：`week`，`month`，若不指定默认为`week`|
|`/jm clear`|清除缓存漫画与转化的PDF|-|-|

---

## 📸 效果展示

### 单章节漫画

<details>

<summary>展开查看</summary>

<div align="center">

<img src="./images/readme_singlechap1.png" width="65%">

</div>

</details>

### 多章节漫画

<details>

<summary>展开查看</summary>

<div align="center">

<img src="./images/readme_multichap1.png" width="65%">

</div>

<div align="center">

<img src="./images/readme_multichap2.png" width="65%">

</div>

</details>

### 文案匹配

<details>

<summary>展开查看</summary>

<div align="center">

<img src="./images/readme_match.png" width="65%">

</div>

</details>

### 搜索漫画

<details>

<summary>展开查看</summary>

<div align="center">

<img src="./images/readme_search.png" width="50%">

<img src="./images/readme_searchresult.png" width="55%">

</div>

</details>

### 排行榜查询

<details>

<summary>展开查看</summary>

<div align="center">

<img src="./images/readme_rank.png" width="50%">

<img src="./images/readme_rankresult.png" width="55%">

</div>

</details>

---

## 📜 参考项目

- **Python API for JMComic**：[JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) by [hect0x7](https://github.com/hect0x7)
- **图像转PDF**：[image2pdf](https://github.com/salikx/image2pdf) by [salikx](https://github.com/salikx)

## 🥳 贡献者

<a href="https://github.comAmethystTim/JM-PDF-plugin/graphs/contributors">
  <img alt="contributors" src="https://contrib.rocks/image?repo=AmethystTim/JM-PDF-plugin"/>
</a>

## ⭐ Star Trend

如果你觉得这个插件还不错，欢迎给我们一个star！🥰

[![Stargazers over time](https://starchart.cc/AmethystTim/JM-PDF-plugin.svg?variant=adaptive)](https://starchart.cc/AmethystTim/JM-PDF-plugin)