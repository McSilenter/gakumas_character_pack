# 学マス角色扩展包（gakumas_character_pack）

给 [eidolon-sc](https://github.com/Sallyn0225/eidolon-sc) 用的扩展包：在你已有的 eidolon-sc 旁边另起一套实例，里面是《学园偶像大师》初星学園的 14 位偶像。

- 不改 eidolon-sc 的任何文件。扩展包拿你本机的 eidolon-sc 源码，在构建镜像时打上自己的补丁。
- 学マス实例有自己的数据库和角色目录，和你的 283 实例互不相干，可以同时开着。

## 需要
- 一份 eidolon-sc 仓库（已经能正常部署 283 实例的那份），以及它根目录的 `.env`（没有这个文件时，启动会直接报找不到它）。扩展包对着原项目 main 测试，版本见 `overlay/upstream.lock`；自己改过的分支（fork）不保证能打上补丁。
- Docker Desktop，或 Docker Engine + Compose v2.24 以上。

## 安装
1. 把这个仓库下载或克隆到任意位置。
2. 复制 `.env.example` 为 `.env`，把 `EIDOLON_SC_DIR` 填成你本机 eidolon-sc 仓库的路径。
3. 在本目录运行：
   ```
   docker compose up -d --build
   ```
4. 打开 `http://localhost:3001`。端口可以用 `.env` 里的 `GAKUMAS_PORT` 改。

**登录**：和你的 283 实例用同一套登录设置（见下面的「继承」）。原项目没有免登录：
- 只在本机、局域网或 Tailscale 里用时，最简单的是在本目录的 `.env` 里加一行 `EIDOLON_DEV_LOGIN=1`，登录页会出现一个输入框，填个名字就能进（同一个名字就是同一个用户）。它让任何能打开网页的人冒充任何用户，所以只在自己的网络里用。
- 已经给 283 实例配了 GitHub、Google 登录（OAuth）时，学マス实例也能用，但 OAuth 应用的回调地址要加上学マス实例的地址，见下面的「继承」。

模型、语音等密钥直接读 eidolon-sc 根目录的 `.env`。想给学マス实例单独设置哪一项，就写进本目录的 `.env`，同名的以这里为准。

> **登录和部署的设置也会一起继承。** 扩展包是给本机或局域网、Tailscale 里用的：`EIDOLON_DOMAIN` 不设时，从这些地址打开都能登录。
> 如果你的 283 实例是公开部署（`.env` 里设了 `EIDOLON_DOMAIN`），学マス实例也会拿到同一个域名，登录会出问题。这时请在本目录的 `.env` 里写一行 `EIDOLON_DOMAIN=`（留空）只在本机用；或者给它另配一个域名和反向代理（扩展包不带），OAuth 回调地址相应改成 `https://<新域名>/api/auth/<provider>/callback`。
> 另外，设了 `EIDOLON_DOMAIN` 时，`EIDOLON_DEV_LOGIN` 不能开，否则后端不会启动。

**语音**：14 位都配了 Fish Audio 上公开的音色（`characters/characters.toml` 的 `voice_id`），用你自己的 `FISH_AUDIO_API_KEY` 就能用。

## 它是怎么工作的
| 部分 | 做什么 |
|---|---|
| `overlay/patches/backend.json`、`frontend.json` | 构建镜像时，对 eidolon-sc 源码的副本做逐条文字替换。每条原文都必须精确命中，否则构建失败。 |
| `overlay/*.Dockerfile` | 用 eidolon-sc 的 `backend/`、`frontend/` 作为构建上下文，先打补丁，再照原项目的步骤构建。 |
| `overlay/upstream.lock` | 记录扩展包测试过的原项目 Dockerfile。原项目改了 Dockerfile 时拒绝构建，提醒维护者核对。 |
| `characters-init` 服务 | 每次启动时组装角色目录：先复制 eidolon-sc 的通用清单（礼物、饮品、工作、地点、酒吧、信的配乐），按 `overlay/patches/characters.json` 改掉其中 283 的说法，地点池去掉 283 的圣地标注，最后放上 `characters/` 里的学マス角色。 |
| `characters/` | 学マス自己的东西：角色配置、人设（sheets）、角色资料（facts）、头像、世界设定（`world.json`、`world-setting.md`）。 |
| `tools/world_sync/` | 重新同步学マス现实中的唱片、歌曲和演出，写进 `characters/world.json`。 |
| `story-sync.sh`、`tools/story_sync/` | 同步剧情库：下载剧情来源、转换成 CSV、导入后端。见下面「剧情库」。 |

补丁改了什么：
- **世界设定**：读 `characters/world-setting.md`，代替原项目写死的“事务所的组合和成员”那一段。
- **各处提示词**：“《偶像大师 闪耀色彩》283 事务所”改成“《学园偶像大师》初星学園”，制作人是プロデューサー科的学生。
- **酒吧**：店名「VA-gakumas」（门口的像素招牌只有 56 像素宽，写作「VA-学マス」），IF 设定不变。第一次进店的教程是原项目写死的，仍由はづき来教调酒。
- **日历**：14 位偶像两周一轮，每周 7 位（原项目是 28 位四周一轮）。按四周一轮时每周只有三四位，凑不够一周的工作量，日历会抽不出来。
- **登录 Cookie**：改名为 `gakumas_session`，和 283 实例开在同一台机器上时互不登出。

## eidolon-sc 更新以后
重新运行 `docker compose up -d --build`。

如果构建或启动时出现「[学マス扩展包] 补丁失败」，说明原项目改到了补丁要替换的地方，需要更新扩展包的补丁清单。扩展包测试过的原项目版本写在 `overlay/upstream.lock` 里。

扩展包更新之前想先用上：另外克隆一份 eidolon-sc，切到 `upstream.lock` 里的提交，再把本目录 `.env` 的 `EIDOLON_SC_DIR` 指向这一份。你原来那份 eidolon-sc 和 283 实例不受影响。
```
git clone https://github.com/Sallyn0225/eidolon-sc.git eidolon-sc-for-gakumas
cd eidolon-sc-for-gakumas
git checkout <upstream.lock 里 tested_commit 的提交号>
```
这份克隆里也要有 `.env`（可以复制原来那份），因为模型、语音的密钥是从 `EIDOLON_SC_DIR` 下的 `.env` 读的。

## 世界设定
- 每位偶像的经历以她自己的亲爱度剧情为准，她只认自己的制作人。
- `world-setting.md` 只写各条线一致的东西：学园、职员、宿舍、班级、生徒会、大赛制度、校外势力。
- 现实中的公演（包括名字里带『H.I.F』的）和学园里的同名大赛不是一回事。

数据来源和同步规则见 `tools/world_sync/README.md`。

## 剧情库
导入剧情库以后，偶像能回忆她自己出场过的剧情。和 Eidolon-SC 一样，**剧情不随仓库分发**（来源没有明确的许可证，见原项目的 ADR-0003），仓库里只有同步工具：你自己运行一次，它从公开的来源下载、转换，再导入你自己的实例。

需要：实例已经在运行（`docker compose up -d`）；`.env` 里有向量化服务的 key（和原项目一样，默认 `SILICONFLOW_API_KEY`），导入时要给每段剧情做向量；能访问 GitHub。

在本目录运行（Windows 用 Git Bash）：
```
./story-sync.sh
tail -f logs/story-sync.log   # 另开一个终端看进度
```
它做三件事：
1. 下载三份来源到 `corpus/sources/`：
   - [chinosk6/GakumasTranslationData](https://github.com/chinosk6/GakumasTranslationData) 的发布版：中文译文和中文卡名、话名；
   - [DreamGallery/Campus-adv-txts](https://github.com/DreamGallery/Campus-adv-txts)：游戏的日文原版剧本和说话人；
   - [vertesan/gakumasu-diff](https://github.com/vertesan/gakumasu-diff) 里的几张表：日文的卡名、话名。
2. 转换成剧情 CSV，放在 `corpus/csv/`：日文原文和说话人以原版为准，中文取译文，两版逐句对齐；人名原作是日文的保持日文；失败结局不收；还没有译文的新剧情只有日文。转换报告在 `corpus/convert-report.txt`。
3. 在后端容器里运行 `eidolon story import-csv /corpus/csv` 导入。导入时按剧本编号分类：亲爱度、P 卡、S 卡、培育、活动、主线，其余算「其他剧情」。

第一次同步要下载约 70 MB，给约 3600 个剧本（5400 段文本）做向量，实测一共 8 分钟左右（看网络和向量化服务的速度）。导入结束时会列出每位偶像的剧情目录；也可能有几条「标题像失败结局，但不在失败结局的规则里，已照常导入」的注意，那是原项目按标题里的「败」字做的提醒，学マス的「将失败化为动力」「绝对不败的力量」这类标题会被提到，照常导入了，不用管。
中途中断（关掉终端、断网、向量化出错）也没关系，重新运行会接着做。之后每次运行，三份来源都没更新时什么也不下载、不转换；有更新时只下载变了的那份，导入时也只处理新增和改过的剧情。

访问 GitHub 要代理时，在本目录的 `.env` 里填 `GAKUMAS_SYNC_PROXY`（只给剧情同步用，不影响后端；容器里访问本机的代理写 `host.docker.internal`，例如 `http://host.docker.internal:7890`）。想固定在某个版本的来源时，填 `GAKUMAS_GTD_TAG`、`GAKUMAS_ADV_REF`、`GAKUMAS_MASTER_REF`，见 `.env.example`。剧情目录默认是本目录下的 `corpus/`，可以用 `GAKUMAS_CORPUS_DIR` 改到别处。

### 每周自动同步
来源更新以后（新活动、新卡、新译文），每周运行一次就能跟上。

- **Linux**：用 cron。`crontab -e`，加一行（路径换成本目录的实际位置；这里是每周一 4:17）：
  ```
  17 4 * * 1 /home/you/gakumas_character_pack/story-sync.sh
  ```
  运行 cron 的用户要能执行 `docker compose`，并且对本目录有写权限。
- **Windows**：用任务计划程序。在命令提示符里运行一次（路径换成实际位置；Git 装在别处时也改掉 `bash.exe` 的路径，例如 `D:\Program Files\Git\bin\bash.exe`。要写 Git 自带的这个完整路径，单写 `bash` 会找到 Windows 自带的 WSL，跑不了这个脚本）：
  ```
  schtasks /Create /TN gakumas-story-sync /SC WEEKLY /D MON /ST 04:17 /TR "\"C:\Program Files\Git\bin\bash.exe\" -c /d/path/to/gakumas_character_pack/story-sync.sh"
  ```
  任务只在你登录 Windows、Docker Desktop 开着的时候运行；错过的那一周不会补跑，下周照常。想立刻试一次：`schtasks /Run /TN gakumas-story-sync`。不想要了：`schtasks /Delete /TN gakumas-story-sync`。

脚本自己把输出写进 `logs/story-sync.log`，每次以「开始同步学マス剧情库」开头、以「结束：退出码 N（含义）」结尾。看最近几次的结果：
```
grep '结束：' logs/story-sync.log | tail
```

| 退出码 | 含义 | 要做什么 |
|---|---|---|
| 0 | 完全成功（来源都没更新时也是 0） | 不用管 |
| 1 | 导入出错：缺少向量化服务的 key，或向量化中断 | 看日志里的错误；向量化中断时重新运行即可继续 |
| 2 | 下载或转换出错（网络、来源的目录结构变了），这次导入的是上次转换的那一份 | 偶尔一次不用管；连续几周都是 2 时看日志 |
| 3 | 下载或转换出错，而且还没有可导入的剧情 | 看日志：多半是连不上 GitHub，填 `GAKUMAS_SYNC_PROXY` |
| 4 | 后端容器没有运行，或无法运行 `docker compose` | `docker compose up -d` |
| 5 | 上一次同步还没结束，这次没有运行 | 不用管 |

## 角色配置的依据
- 礼物、酒吧口味：写在各人 `characters/facts/<id>.sources.md` 的「喜欢的礼物」「酒吧口味」两节。礼物只收剧情或官方资料里有依据的；酒吧口味没有剧情依据的标「人设推断」。
- 印象色、年龄、生日：取自游戏数据（vertesan/gakumasu-diff），见同一文件的「印象色核实」。
- 照片 tag、外貌：照片 tag 取 Danbooru 的角色 tag。外貌取单人图里出现最多的发色、发型和瞳色，并对照了头像。
- 中文名（`name_zh`）是国内社区常用的译名，请按需要校对。

## 许可
以 AGPL-3.0-or-later 发布，和 Eidolon-SC 相同。头像、音色、引用的台词不受 AGPL 约束，详见 [LICENSING.md](LICENSING.md)。

## 致谢
- [Eidolon-SC](https://github.com/Sallyn0225/eidolon-sc)：扩展包所扩展的原项目
- [GakumasTranslationData](https://github.com/chinosk6/GakumasTranslationData)（chinosk6）：剧情的中文译文和中文卡名、话名
- [Campus-adv-txts](https://github.com/DreamGallery/Campus-adv-txts)（DreamGallery）：剧情的日文原版剧本和说话人
- [gakumasu-diff](https://github.com/vertesan/gakumasu-diff)（vertesan）：游戏数据表，日文卡名、话名，以及偶像的印象色、年龄和生日
- [ふじわらはじめ](https://fujiwarahaji.me/)：唱片的曲目和演唱者、演出的曲目单
- [im@sparql](https://sparql.crssnky.xyz/imas/)：偶像的读音和 CV
- [Fish Audio](https://fish.audio/)：语音合成，以及 Fish Audio 上公开的音色和它们的作者

## 声明
非官方的粉丝作品，与《学园偶像大师》的版权方和官方没有任何关系。仓库不含剧情原文；人设和资料里引用的台词只是简短的片段。

头像取自官方图片，Fish Audio 音色是用游戏语音训练的，它们的版权都属于版权方。请只在个人、非商业的范围内使用；版权方要求时会删除。
