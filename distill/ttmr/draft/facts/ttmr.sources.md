月村手毬 角色资料（facts/ttmr.md）和人设（sheets/ttmr.md）的出处。只是整理记录，不被程序读取。
剧情来源：corpus/gakumas/csv 下按剧本转出的 CSV（日文原文 text 列，取自 Campus-adv-txts；中文 trans 列取自 GakumasTranslationData）。写法为「剧本 stem 行号」，stem 和 CSV 路径的对应见 corpus/gakumas/distill/ttmr/index.tsv。逐篇笔记在 distill/ttmr/notes/<stem>.md，按世界线分组的提炼在 distill/ttmr/digest/。用户确认过的说话人、冲突和未交代的事见 distill/ttmr/conflicts.md（下文写作 conflicts 编号）。
说话人：她本人的标签只有「手毬」；「？？？」0041（event_007_main-01）、「聞き覚えのある声」0003、0004（adv_dear_hmsz_029）也是她；「一同」齐声按 ichido-judgement.md 判定（算她的 96 条）。回想、转述、再现、演戏、歌词、括号心声在笔记里都已标出，资料里不当成她当场说的话。

## 统计（人设的「自称」「口癖」「对他人的称呼」的依据）
corpus/gakumas/distill/ttmr/stats.md（line_stats.py）：她的台词 6206 行、475 篇。「私」951 行；对制作人「プロデューサー」339、「あなた」189；「てもいいよ」16 行，是其他人的 26.5 倍；「……」41.8%（他人 33.1%）；括号心声 4.7%（他人 2.1%）。别人怎么叫她、她怎么叫别人的次数也见 stats.md；美鈴叫她「まりちゃん」统计脚本没有收（只数了姓名写法），出处见下。

## 档案 / 基本信息
- 官网学園名簿 https://gakuen.idolmaster-official.jp/idol/temari/ （2026-10-30 取，存为 distill-work/ref/official-temari.html）：年龄、血型、生日、星座、身高、体重、三围、惯用手、出身地、兴趣、特技、CV、标语「夢？いいえ、必ず達成する目標です。」、介绍文。
- vertesan/gakumasu-diff@fc6afb8b CharacterDetail.yaml（characterId: ttmr）：同上各项一致，另有学年「1年生」和游戏内简介（Introduction）；CharacterColor.yaml：mainColor 27B4EB。这两个文件不在 corpus/gakumas/master-jp 里，存于 distill-work/ref/master-dl/（附 SOURCE.txt）。
- 印象色是蓝：adv_dear_ttmr_035 0053。内部进学组：adv_cidol-ttmr-3-007_01 0010。偶像经历第4年：adv_cidol-ttmr-3-000_01 0009。
## 档案 / 自称与说话方式、称呼
- 统计见上。例句：adv_cidol-ttmr-3-018_03 0035、adv_dear_ttmr_017 0045（全名自称）；adv_cidol-ttmr-3-018_03 0019（担当アイドル）；adv_dear_ttmr_025 0065（敬语骂人）；adv_cidol-ttmr-3-007_03 0012（装失忆）；adv_dear_ttmr_013 0024、adv_cidol-ttmr-3-011_03 0044（口下手）；adv_dear_ttmr_006 0060（感情が薄くて）。
- 美鈴叫她「まりちゃん」：adv_dear_ttmr_007 0039、adv_cidol-ttmr-3-016_01 0005；美鈴的母亲：adv_cidol-ttmr-3-009_01 0025（她转述）。燐羽「ばか手毬」：adv_dear_ttmr_016 0073。撫子「手毬お姉さま」：adv_dear_ttmr_026 0033、adv_cidol-ttmr-3-021_01 0009。ことねの妹「手毬お姉ちゃん」：stats.md（S卡 3-0068）。
- 她叫燐羽「リーダー」：adv_cidol-ttmr-3-007_02 0032、0034；「継さん」「賀陽継」：adv_dear_ttmr_025 0021、0026；以前叫千奈「倉本」：adv_dear_ttmr_018 0029～0033；「あの黒井社長」：adv_dear_ttmr_025 0062；其余次数见 stats.md。
## 档案 / 体质与身体
- 体重、节食：adv_dear_ttmr_002 0030～0049；adv_cidol-ttmr-3-011_03 0004～0006。体力弱点：adv_dear_ttmr_004 0027～0035；adv_dear_ttmr_006 0065～0067；adv_dear_ttmr_026 0005、0039。怕冷：adv_cidol-ttmr-3-009_01 0001～0003。手笨：adv_cidol-ttmr-3-002_02 0008～0010、0020。容貌自卑：adv_cidol-ttmr-3-021_03 0016～0021。

## 亲爱度与 P 卡 / 总述
- 只制作她一人：adv_cidol-ttmr-3-011_02 0027～0030；制作人是プロデューサー科1年1組：adv_dear_ttmr_005 0043。
## 亲爱度与 P 卡 / 小时候与『SyngUp!』
- 小时候讨厌自己：adv_dear_ttmr_010 0061～0068。看『H.I.F』、遇见燐羽、継：adv_cidol-ttmr-3-009_01 0018～0037；adv_cidol-ttmr-3-009_02 0004～0038；继是契机：adv_dear_ttmr_011 0026、adv_dear_ttmr_025 0040（conflicts 6、8f：同一人、是燐羽的姐姐）。入学、ちくわぶ：adv_cidol-ttmr-3-009_03 0008～0029。
- 『SyngUp!』：adv_dear_ttmr_004 0013（成员）；adv_dear_ttmr_015 0004；adv_dear_ttmr_020 0004～0007（燐羽回忆）；adv_cidol-ttmr-3-007_02 0009～0034；adv_cidol-ttmr-3-007_03 0028～0029；adv_dear_ttmr_022 0031～0033；adv_dear_ttmr_024 0056～0067（美鈴讲的往事）；conflicts 8i。
- 坏传闻：adv_dear_ttmr_007 0006～0014；adv_dear_ttmr_014 0048。解散：adv_dear_ttmr_003 0046～0053；adv_dear_ttmr_004 0041～0058；adv_dear_ttmr_015 0014～0036；adv_dear_ttmr_016 0018～0036；conflicts 1。燐羽去極月：adv_dear_ttmr_010-01 0014～0020；adv_dear_ttmr_011 0014～0016。
## 亲爱度与 P 卡 / 和制作人相遇
- adv_dear_ttmr_001 0002～0035；adv_dear_ttmr_002 0002～0055；adv_dear_ttmr_003 0021～0066（0065 和 adv_dear_ttmr_037 0015 一字不差，是 conflicts 8e 的出处）；adv_dear_ttmr_004 0067～0076；adv_dear_ttmr_006 0002～0073。
## 亲爱度与 P 卡 / 和美鈴和好、燐羽回来
- adv_dear_ttmr_007～010（美鈴、打赌、和好、合住，0066～0067 是「一同」）；adv_dear_ttmr_010-01；adv_dear_ttmr_011～014（N.I.A 目标、プランA/B、SNS 炎上、極月冲突；013 是ことね/咲季两条并列分支）；adv_dear_ttmr_015～017（QUARTET、哭求、对质约定）；adv_dear_ttmr_018～020（视频、FINALE、N.I.A 优胜；020 0011 的「一同」不算她的）；conflicts 二·4、三·7、8g、8h。
## 亲爱度与 P 卡 / 夏冬两届『H.I.F』
- adv_dear_ttmr_021～023（夏季 H.I.F、美鈴的舞台、输给星南；023 0076 是美鈴，conflicts 二·4）；adv_dear_ttmr_024～028（看星南演出、極月特训、三连战、冬季规则）；adv_dear_ttmr_029～033（選抜試験、千奈広、咲季、ほうとう）；adv_dear_ttmr_034～037（决战、父母、授与式、拉面）；conflicts 2、3、8d、8j、8o。
## 亲爱度与 P 卡 / P 卡
- 【Luna say maybe】adv_cidol-ttmr-3-000_01～03；【常春藤】001_01～03（001_02 有制作人回忆和「予想される反応」想象，001_03 0033 是「一同」）；【变装狂想曲】002_01～03；【Campus mode!!】007_01～03（007_03 0011「賀陽さん」是燐羽，conflicts 8g）；【雪融之时】009_01～03；【雨后的鸢尾花】011_01～03（conflicts 4f）；【全力以赴！】015_01～03；【究竟从何时起】016_01～03；【荆棘之路】018_01～03（018_01 0033 是「一同」）；【「我要说了哦。」】021_01～03（021_01 0016 的「一同」是極月学園的人）。stem 前缀都是 adv_cidol-ttmr-3-。
## 亲爱度与 P 卡 / 人物关系
- 制作人：adv_dear_ttmr_024 0034～0035；adv_dear_ttmr_028 0041～0044；adv_dear_ttmr_018 0048；adv_cidol-ttmr-3-011_03 0039～0040；adv_dear_ttmr_005 0069～0072。美鈴：adv_dear_ttmr_019 0041～0045；adv_cidol-ttmr-3-016_01 0008～0037。燐羽：adv_dear_ttmr_025 0009～0017；adv_dear_ttmr_026 0072～0080；adv_dear_ttmr_024 0048～0049；adv_dear_ttmr_030 0011、0063；adv_dear_ttmr_035 0048～0068。咲季：adv_dear_ttmr_031 0060～0061；adv_cidol-ttmr-3-015_02 0023～0029。ことね：adv_cidol-ttmr-3-015_02 0030～0033；015_03 0028～0029。広、千奈：adv_dear_ttmr_029 0014～0039；adv_dear_ttmr_030 0037。星南：adv_dear_ttmr_027 0016～0019；adv_dear_ttmr_036 0013～0028。麻央：adv_cidol-ttmr-3-000_02 0041～0046。極月学園：adv_dear_ttmr_013 0064；adv_dear_ttmr_026 0019～0033。父母：adv_dear_ttmr_035 0011～0021。

## 培育 / 培育剧情 001
- adv_pstory_001_ttmr_opening-normal-01～05、opening-true-01～02（开场的不同版本；opening-true-02 0003「わかりました」是她，conflicts 5a）；after-step-1-normal-01～03；after-step-2-normal-01～03（体重：after-step-2-normal-03 0005～0032）；before-audition-mid-normal-01、after-audition-mid-normal-01～04；before-audition-final-normal-01、after-audition-final-normal-01～04（按结果分档）；ending-normal-01～05（A～E End）、ending-true-01。负面情绪的来源按 conflicts 8p（剧本本身没写）。
## 培育 / 培育剧情 002、003、成长剧情
- adv_pstory_002_ttmr_opening-normal-02；before-audition-a-normal-01、after-audition-a-normal-02／-03（结果分支）；before-audition-b-normal-01、after-audition-b-normal-02／-03（conflicts 8q）；after-audition-final-normal-01（元『SyngUp!』成员，conflicts 8i）；ending-normal-02。adv_pstory_003_ttmr_selection-normal-02、final-normal-02（conflicts 8j）。adv_pgrowth_001_ttmr_01～03。
## 培育 / 培育事件
- adv_pevent_001_ttmr_activity_001～020（含 017-01/02、018-01/02）；adv_pevent_001_ttmr_school_001～011；adv_pevent_002_ttmr_sales_1-001～4-006（每项 -01/-02 一对，只算一次）；adv_pevent_003_ttmr_activity_021、022。学业：activity_020 0005～0010、school_001、school_003 0018；失眠：activity_005；手冷：sales_4-003 0001～0003；怕鬼只对他说：sales_1-006 0008；センブリソーダ：sales_1-005 0003～0008；观光大使：sales_2-003 0006～0008；动画电影：sales_4-004 0002～0006；水族馆：activity_022 0008～0018。

## 主线
- 第1章：adv_unit_01-01_03（0062～0077）、01-01_04（0013～0038）、01-01_10、01-01_11（0021、0043～0051）、01-01_12（0013～0015、0053～0061）、01-01_13（0001～0101）、01-01_14（0020～0074）。
- 第2章：adv_unit_01-02_02（0021～0058）、01-02_03、01-02_04（0029～0040）、01-02_05、01-02_06（0010、0078）、01-02_07（0038～0056；0048～0051「？？？」不是她）、01-02_08、01-02_09、01-02_10（0033～0053）、01-02_11～15（0036～0037 道歉道谢）。
- 第3章：adv_unit_01-03_01（0019～0071；0065～0066「……3回くらい？」，笔记写错，按原文）、01-03_06～09、01-03_10（0042～0073）、01-03_11、01-03_12（0003～0078）。
- 第4章：adv_unit_01-04_01、01-04_04（0050～0065）、01-04_05（0033～0040；conflicts 8a）、01-04_07、01-04_08（美鈴的约定）、01-04_09（0025～0055）、01-04_10、01-04_12、01-04_13、01-04_17（0055～0073）、01-04_18（0078）、01-04_20（0020～0076；conflicts 4b）、01-04_22（0044～0078）、01-04_24。conflicts 1、4a、4c、8、8b、8c。

## 秦谷美鈴的亲爱度
- adv_dear_hmsz_007（0012～0064）、009（0034～0061）、010（0009～0031；0020 按 conflicts 8n）、013（0033～0047）、014、017（0002～0079）、018、019（0020～0023 是梦里的燐羽，conflicts 5d；0045～0052）、020（0022～0044）、021、023（0014～0058）、024、028（0011～0071）、029（0003、0004 是她，0007 不是，conflicts 5；0040～0041）、030（0035；conflicts 8o）、031、032（0018～0060）、034（0049）、036（0063～0102；0065～0066 conflicts 8m：原话不在她出场的剧情里）。
## 活动
- 001：adv_event_001_main-01～05（main-05 0056，conflicts 4d）。004：adv_event_004_main-01、04、05。007：adv_event_007_main-01～05（main-03 广的“第3个”，conflicts 4e）。008：adv_event_008_main-01～05。009：adv_event_009_main-01。010：adv_event_010_main-05 0038。011：adv_event_011_main-01～05。012：adv_event_012_main-02（リーリヤ的回忆）。014：adv_event_014_main-04、05。016：adv_event_016_main-01～05（main-03 0017～0025 是回忆，0025 是现在，conflicts 5k）。019：adv_event_019_main-01～05。022：adv_event_022_main-03 0052（ことね转述，conflicts 5e）。023：adv_event_023_main-01～05。026：adv_event_026_main-01、05。027：adv_event_027_main-01～05。029：adv_event_029_main-02、04。

## S 卡
- 美鈴（跨卡相连）：adv_csprt-1-0010_01（0012～0015，conflicts 8l）；adv_csprt-3-0001_01～03（0016「一同」）；adv_csprt-3-0012_01～03（0003～0013「一同」心声，0011 是回想中说过的话，conflicts 5i）；adv_csprt-3-0021_01～03（0011「りんはぁ」；_03 全在美鈴的梦里）；adv_csprt-3-0028_01～03（conflicts 8k、8l）；adv_csprt-2-0044_02；adv_csprt-3-0058_01～03；adv_csprt-3-0076_01、03；adv_csprt-3-0033_01～03（_02 0002～0007 是回忆）；adv_csprt-3-0096_01～03（_02 0017 是回想里的反应，conflicts 5k）；adv_csprt-3-0065_03；adv_csprt-3-0067_01；adv_csprt-3-0083_01；adv_csprt-3-0112_03；adv_csprt-3-0097_02（_01 0005 是黒井，conflicts 5c）。
- 同学们：咲季 adv_csprt-1-0001_01～02、2-0018_01～02、3-0000_01～03、3-0002_01～03（_03 0008 是ことね转述，conflicts 5h）、3-0029_01～03、3-0044_01～03、3-0057_01～03、3-0068_01～03、3-0102_01～03（conflicts 4g）、3-0110_03（0011「一同」报幕是演出）、3-0112_01～02；ことね 2-0001_01（conflicts 8：没点名的朋友）、2-0015_01～02、2-0050_01～02、3-0024_01；佑芽 2-0009_01～02、2-0063_01～02、2-0067_01～02；広 1-0005_01、2-0021_01～02、3-0090_01～03；千奈 2-0029_01～02、2-0044_01、3-0009_01、3-0084_01～03；清夏 2-0037_01～02、3-0036_01～03、3-0059_03；リーリヤ 3-0018_02、3-0031_01～03、3-0049_01～03；星南 2-0071_01～02、3-0076_02～03；莉波 2-0061_01～02、3-0106_01～03；麻央 2-0045_01～02、2-0078_01～02（_01 0018 叫的是燐羽，conflicts 5m）、3-0087_02；训练员 2-0040_01～02。stem 前缀都是 adv_csprt-。

## 其他偶像的亲爱度与 P 卡
- 千奈：adv_dear_kcna_004（0034～0070）、007、031（0011～0073；她和美鈴不参赛，conflicts 8j）、032、036 0041；adv_cidol-kcna-3-000_02、002_02～03、007_02。麻央：adv_dear_amao_021（0045「一同」）、022 0023、027 0060、030；adv_cidol-amao-3-001_03。ことね：adv_dear_fktn_029、034、035（0041 不是她，conflicts 5b）；adv_cidol-fktn-3-016_01（0006 是ことね再现）、016_03、019_02（0031～0034 是ことね再现，conflicts 5f）。咲季：adv_cidol-hski-3-012_02（0012～0015 炸猪排；0018 与 0038，conflicts 8s；0047「一同」）、015_03。佑芽：adv_cidol-hume-3-018_02（0021～0040）；adv_dear_hume_024。清夏：adv_cidol-ssmk-3-018_01～02；adv_dear_ssmk_025（0072）、031（0032～0033 是回想，conflicts 5g）。広：adv_cidol-shro-3-001_02 0030～0034（conflicts 8r，暂存）。燕：adv_dear_atbm_007、033。星南：adv_dear_jsna_034（0037「一同」）。リーリヤ：adv_dear_kllj_036 0039。美鈴 P 卡：adv_cidol-hmsz-3-005_01 0032。莉波 P 卡：adv_cidol-hrnm-3-012_02 0001～0002（conflicts 5j）。
- 其他：adv_live_ttmr_001_start-01-01～04-01、end-01-01～04-01；adv_startup_2024_bd-01_ttmr-01；adv_startup_2024_user-bd-01_ttmr-01；adv_tutorial_first_ttmr-01～02。
## 喜好
- 拉面：adv_pstory_001_ttmr_ending-normal-01；adv_dear_ttmr_037 0070～0072；adv_csprt-3-0058_01；adv_pevent_001_ttmr_school_009 0020。炸猪排：adv_cidol-hski-3-012_02 0012～0015；adv_csprt-3-0028_03 0015；adv_pevent_003_ttmr_activity_021。こってり：adv_pstory_001_ttmr_ending-normal-02 0018～0019。ちくわぶ：adv_cidol-ttmr-3-009_03 0021～0027。肉包、火锅：adv_csprt-2-0037_01～02。南瓜：adv_dear_hmsz_014 0006～0007。讨厌的菜：adv_pstory_001_ttmr_ending-normal-04～05；adv_dear_ttmr_032 0024～0025。蛇：adv_csprt-3-0002_01 0011。味道：adv_pevent_002_ttmr_sales_1-002、1-005。
- 唱歌：adv_pstory_001_ttmr_before-audition-mid-normal-01 0016；before-audition-final-normal-01 0007；adv_cidol-ttmr-3-007_03 0009；adv_pstory_001_ttmr_after-audition-mid-normal-02 0009。
- 怕的：adv_cidol-ttmr-3-000_02；adv_pevent_002_ttmr_sales_1-006 0008；adv_event_007_main-05；adv_csprt-3-0021_02；adv_csprt-2-0045_01～02；adv_pevent_003_ttmr_activity_022 0012～0014；adv_pevent_002_ttmr_sales_3-002 0008；adv_cidol-ttmr-3-009_01 0001～0003。讨厌：adv_cidol-ttmr-3-002_03 0016；adv_pevent_001_ttmr_school_002 0019；adv_dear_ttmr_020 0035；adv_dear_ttmr_025 0066～0070。
- 动物、水族馆、游戏：adv_csprt-2-0067_01～02；adv_csprt-3-0090_03；adv_pevent_003_ttmr_activity_022；adv_pevent_002_ttmr_sales_4-005 0006。
## 未收录与存疑
- conflicts 8m、8r、8j 后半（用户暂存）；8o（先代『一番星』）。digest/ 各组第 9 节还记了每组读不准的细节。
