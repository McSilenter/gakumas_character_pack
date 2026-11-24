# 学マス角色扩展包（gakumas_character_pack）

给 [eidolon-sc](https://github.com/Sallyn0225/eidolon-sc) 用的扩展包：在你已有的 eidolon-sc 旁边另起一套实例，里面是《学园偶像大师》初星学園的 14 位偶像。

- 不改 eidolon-sc 的任何文件。扩展包拿你本机的 eidolon-sc 源码，在构建镜像时打上自己的补丁。
- 学マス实例有自己的数据库和角色目录，和你的 283 实例互不相干，可以同时开着。

> **状态：制作中。** 14 位的角色配置已经写好，并通过了后端自带的配置校验；还没有完整地构建、启动和试聊过。没有 Fish Audio 音色，语音和通话暂时用不了。

## 需要
- 一份 eidolon-sc 仓库（已经能正常部署 283 实例的那份），以及它根目录的 `.env`。
- Docker Desktop，或 Docker Engine + Compose v2.24 以上。

## 安装
1. 把这个仓库下载或克隆到任意位置。
2. 复制 `.env.example` 为 `.env`，把 `EIDOLON_SC_DIR` 填成你本机 eidolon-sc 仓库的路径。
3. 在本目录运行：
   ```
   docker compose up -d --build
   ```
4. 打开 `http://localhost:3001`。端口可以用 `.env` 里的 `GAKUMAS_PORT` 改。

模型、语音等密钥直接读 eidolon-sc 根目录的 `.env`。想给学マス实例单独设置哪一项，就写进本目录的 `.env`，同名的以这里为准。

## 它是怎么工作的
| 部分 | 做什么 |
|---|---|
| `overlay/patches/backend.json`、`frontend.json` | 构建镜像时，对 eidolon-sc 源码的副本做逐条文字替换。每条原文都必须精确命中，否则构建失败。 |
| `overlay/*.Dockerfile` | 用 eidolon-sc 的 `backend/`、`frontend/` 作为构建上下文，先打补丁，再照原项目的步骤构建。 |
| `overlay/upstream.lock` | 记录扩展包测试过的原项目 Dockerfile。原项目改了 Dockerfile 时拒绝构建，提醒维护者核对。 |
| `characters-init` 服务 | 每次启动时组装角色目录：先复制 eidolon-sc 的通用清单（礼物、饮品、工作、地点、酒吧、信的配乐），按 `overlay/patches/characters.json` 改掉其中 283 的说法，地点池去掉 283 的圣地标注，最后放上 `characters/` 里的学マス角色。 |
| `characters/` | 学マス自己的东西：角色配置、人设（sheets）、角色资料（facts）、头像、世界设定（`world.json`、`world-setting.md`）。 |
| `tools/world_sync/` | 重新同步学マス现实中的唱片、歌曲和演出，写进 `characters/world.json`。 |

补丁改了什么：
- **世界设定**：读 `characters/world-setting.md`，代替原项目写死的“事务所的组合和成员”那一段。
- **各处提示词**：“《偶像大师 闪耀色彩》283 事务所”改成“《学园偶像大师》初星学園”，制作人是プロデューサー科的学生。
- **酒吧**：店名「VA-gakumas」，IF 设定不变。
- **前端**：站点标题和免责声明、没有组合的偶像那一组叫「初星学園」、去掉群聊入口（学マス实例不开群聊）。
- **登录 Cookie**：改名为 `gakumas_session`，和 283 实例开在同一台机器上时互不登出。

## eidolon-sc 更新以后
重新运行 `docker compose up -d --build`。

如果构建或启动时出现「[学マス扩展包] 补丁失败」，说明原项目改到了补丁要替换的地方，需要更新扩展包的补丁清单。扩展包测试过的原项目版本写在 `overlay/upstream.lock` 里。

## 世界设定
- 每位偶像的经历以她自己的亲爱度剧情为准，她只认自己的制作人。
- `world-setting.md` 只写各条线一致的东西：学园、职员、宿舍、班级、生徒会、大赛制度、校外势力。
- 现实中的公演（包括名字里带『H.I.F』的）和学园里的同名大赛不是一回事。

数据来源和同步规则见 `tools/world_sync/README.md`。

## 还没完成
- **音色**：`characters/characters.toml` 里每位的 `voice_id` 都空着。配好以后运行 `docker compose exec backend eidolon reading draft` 补上读音的音素，再运行 `eidolon greeting upload` 合成落地页的招呼。
- **剧情库**：扩展包不带剧情（版权原因，不放进仓库）。见下面「剧情库」。

## 剧情库
剧情不在仓库里，需要你本机自己有一份学マス剧情的 CSV。格式和 SCTranslationData 的一样：`id,name,text,trans` 四列，最后一行 `info` 写剧本编号，例如 `adv_dear_ttmr_001`。
1. 在 `.env` 里把 `GAKUMAS_CORPUS_DIR` 设成这个目录，它会挂载为容器里的 `/corpus`。
2. 启动后运行一次：
   ```
   docker compose exec backend eidolon story import-csv /corpus
   ```
导入时按剧本编号分类：亲爱度、P 卡、S 卡、培育、活动、主线，其余算"其他剧情"。

## 角色配置的依据
- 礼物、酒吧口味：写在各人 `characters/facts/<id>.sources.md` 的「喜欢的礼物」「酒吧口味」两节。礼物只收剧情或官方资料里有依据的；酒吧口味没有剧情依据的标「人设推断」。
- 印象色、年龄、生日：取自游戏数据（vertesan/gakumasu-diff），见同一文件的「印象色核实」。
- 照片 tag、外貌：照片 tag 取 Danbooru 的角色 tag。外貌取单人图里出现最多的发色、发型和瞳色，并对照了头像。
- 中文名（`name_zh`）是国内社区常用的译名，请按需要校对。

## 声明
非官方的粉丝作品，与《学园偶像大师》的版权方和官方没有任何关系。仓库不含剧情原文；人设和资料里引用的台词只是简短的片段。
