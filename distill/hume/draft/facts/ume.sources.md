花海佑芽 角色资料（facts/ume.md）和人设（sheets/ume.md）的出处。只是整理记录，不被程序读取。
剧情来源：corpus/gakumas/csv 下按剧本转出的 CSV（日文原文 text 列，中文 trans 列），写法为“剧本 stem 行号”；stem 和 CSV 路径的对应见 distill/hume/index.tsv。逐篇笔记在 distill/hume/notes/<stem>.md（481 篇），分组提炼在 distill/hume/digest/（O1-dear、O2-pcard、O3-pstory、O4-pevent、S1-main、S2-scard-a、S3-scard-b、S4-scard-c、S5-event、S6-others），用户确认过的说话人、冲突和未交代的事见 distill/hume/conflicts.md（下文写作 conflicts 编号）；和咲季、手毬、美鈴共同出场的篇目照那几边的结论，两人共有的事实（家人、老家、勝ち逃げ、姐妹胜负）和 hski 资料对齐。
世界线：经历、人物关系以她自己的亲爱度剧情（adv_dear_hume_*，含 010-01）和她的 P 卡（adv_cidol-hume-3-*，同一条线）为准；这条线里制作人从第 1 话起制作的就是佑芽，她是他第一个担当。人设站在这条线的结尾（冬季『H.I.F』优胜、接过『一番星』之后）。主线（Begrazia）、培育剧情和培育事件、活动、S 卡、别的偶像的线、startup/live 里只取和这条线不冲突的日常、喜好、人际关系（正文写“别的故事里”）；和这条线冲突的情节（星南当她制作人的线、千奈/広/星南线里她的『N.I.A』结果、咲季线里夏天的『一番星』、培育剧情各结局等）写在“另一种可能（不是她的经历）”一章，措辞写成假设。培育剧情 001/002/003 和同一剧本里的分支都按并列的可能写。
说话人：照 conflicts 二·1～6 的结论——adv_live_hmsz_001_start-03-01 两行是美鈴的，不用；adv_dear_hume_028 0051～0052 是她转述咲季的心愿，不当她的想法；念别人写的字（adv_csprt-2-0031_02 0016～0017、adv_csprt-3-0109_03 0016、adv_pevent_003_hume_activity_021 0014）、复述别人的话（adv_dear_shro_030 0039）不算；别人梦里的她（adv_csprt-3-0004_02、adv_unit_01-04_13 0001～0008）不算；她自己梦里的话算、标梦（adv_csprt-3-0004_01）；模仿别人（adv_dear_hume_012 0016、024 0083～0090、025 0021～0022、adv_cidol-hume-3-016_01 0037～0043、adv_csprt-2-0019_02 0017、adv_pstory_002_hume_ending-normal-02 0003、0011～0013）只写成“爱模仿”，不当成她的说话方式。演戏、广告台词、歌词（adv_event_030_main-04 0044、adv_event_026 歌词、adv_csprt-2-0082 僵尸扮演、adv_csprt-3-0023_01「彼氏役」）不当成她的口吻。
引文规则：正文「」里只放日文原文，换行写作「／」，和 CSV text 列一字不差（取整行或行内连续的一段）。下面每节的“引文”一行按正文里出现的顺序，列出该节每句长于 7 个字的「」引文对应的剧本 stem 和行号；7 字以内的称呼、口癖短词（如「佑芽さん」「ぐぬぬ」）不逐条列，已对全部剧本做过存在性检查。引文里有别人的台词时正文已写明是谁说的（制作人、咲季、星南、燐羽、広、手毬、美鈴、训练员的几句）。

## 参考网站
- 官网学園名簿 https://gakuen.idolmaster-official.jp/idol/ume/ （本次没有取；标语、年龄、生日待补）
- 萌娘百科、wikiwiki、imas-db 印象色一览：同手毬、美鈴那批网站，本资料没有从中摘录。
- master 数据 distill-work/ref/master-dl/CharacterDetail.yaml（hume 条目）里年龄是 15歳、生日是 4月1日（咲季条目是 16歳、4月2日）；资料里先写“待补”，是否采用待用户确认。

## 统计（人设的“自称”“口癖”的依据）
我对 distill/hume 的 481 篇 CSV 直接统计（标签“佑芽”的行，2026-11-14）：她的台词 5960 行、481 篇，其中亲爱度 1387 行（38 篇）、P 卡 607 行（27 篇）。口径：只按标签“佑芽”算，不含匿名“？？？”和“一同”；按标签照算的也包括 conflicts 二·1 定为美鈴台词的 adv_live_hmsz_001_start-03-01 两行、二·5 定为咲季梦里的 adv_csprt-3-0004_02 六行，以及模仿、转述、念字、演戏的行。带「あたし」866 行（14.5%）；「わたし」7 行，第一人称只有 adv_dear_shro_010-01 0017 一处，其余是广告台词、模仿姐姐、转述和反问别人的话；「私」2 行（私服、私物，不是自称）；「お姉ちゃん」593 行（9.9%）；「プロデューサー」432 行（其中「プロデューサーさん」394、「プロデューサーちゃん」9），「あなた」25 行；含「勝」284 行（4.8%）、「負け」110、「勝負」91、「悔し」45；「はいっ」157、「えへへ」99、「ふっふっふ」49、「ぐぬぬ」20；「大好き」44；「です」1188 行（19.9%）；带「！」3130 行（52.5%）、「～」1062 行（17.8%）、「♪」217、「♡」49；「……」26.3%（同篇其他有名字标签的角色 33.5%，她比别人少用省略号）。口径和手毬的 stats.md 不同。

## 人设 / 身份
- 出处：档案、故事线、经历各节；conflicts 三·5（不是双胞胎、同年级、1年2組）、三·6（无所属事务所、志望100プロ）、三·7（生徒会庶務）、三·8（冬季『一番星』）。初遇：adv_dear_hume_001；第一次赢姐姐：adv_dear_hume_019；夏冬『H.I.F』：adv_dear_hume_022、036～037。“第一个担当”按用户规则（亲爱度线里制作人从第 1 话起制作的就是她）和 adv_dear_hume_017 0022。
- 引文：adv_dear_hume_017 0022；adv_dear_hume_001 0026；adv_dear_hume_001 0021；adv_dear_hume_001 0044；adv_dear_hume_002 0073；adv_dear_hume_002 0074；adv_dear_hume_019 0012；adv_dear_hume_019 0031；adv_dear_hume_036 0055；adv_dear_hume_036 0056；adv_dear_hume_037 0069；adv_dear_hume_037 0077
## 人设 / 自称
- 出处：统计见上；conflicts 四（第一人称「わたし」只有広线一处）；adv_dear_hume_036 0041（情報通）；adv_event_026_main-04 0058 是别的线的一句自我鼓劲，用作口气参考。
- 引文：adv_dear_hume_020 0001；adv_dear_hume_010 0080；adv_event_026_main-04 0058；adv_dear_hume_027 0101；adv_dear_hume_023 0038；adv_dear_hume_035 0054
## 人设 / 对他人的称呼
- 出处：各人称呼按 digest 称呼表：adv_dear_hume_001 0063、0067，002 0020（佑芽さん）；adv_dear_hume_002 0032（咲季叫佑芽）；adv_dear_hume_022 0020（花海咲季）；adv_cidol-hume-3-012_01 0009（可愛い後輩）；adv_dear_hume_012 0054～0056、024 0026（燐羽）；adv_dear_hume_024 0063、025 0005、0009（広、千奈）；adv_cidol-hume-3-012_01 0003（美鈴）；adv_dear_hume_024 0085（手毬）；别的线：adv_event_009_main-02 0028、adv_event_009_main-03 0005～0006（ことね、リーリヤ）、adv_csprt-2-0049_02 0017、adv_event_024_main-03 0024（燕）、adv_csprt-3-0047_01 0001～0002（莉波）、adv_csprt-3-0078_01 0006（麻央）；adv_dear_hume_002 0057（お父さん、お母さん）。
- 引文：adv_dear_hume_001 0024；adv_dear_hume_005 0018；adv_dear_hume_035 0062；adv_dear_hume_021 0074；adv_dear_hume_002 0031；adv_dear_hume_001 0067；adv_dear_hume_012 0070；adv_dear_hume_036 0039；adv_dear_hume_012 0055
## 人设 / 口癖
- 出处：统计见上；各句见下。平口滑出：adv_cidol-hume-3-006_02 0016（あ、照れてる。）。
- 引文：adv_dear_hume_021 0067；adv_dear_hume_035 0017；adv_dear_hume_031 0024；adv_dear_hume_024 0055；adv_dear_hume_007 0070；adv_dear_hume_006 0056；adv_dear_hume_007 0069；adv_dear_hume_037 0010；adv_dear_hume_018 0005；adv_dear_hume_003 0001；adv_dear_hume_012 0069；adv_dear_hume_003 0050；adv_cidol-hume-3-000_02 0009；adv_cidol-hume-3-006_02 0030；adv_dear_hume_010 0064；adv_dear_hume_035 0012；adv_dear_hume_030 0003；adv_cidol-hume-3-016_02 0014；adv_dear_hume_035 0009
## 人设 / 与对手、伙伴的关系
- 出处：人物关系各节；conflicts 一·1、三·2（勝ち逃げ）、一·2（配方保密）、三·4（隔壁房间）。
- 引文：adv_cidol-hume-3-016_03 0042；adv_dear_hume_008 0061；adv_dear_hume_010 0036；adv_dear_hume_019 0016；adv_dear_hume_029 0050；adv_dear_hume_033 0025；adv_dear_hume_026 0053；adv_dear_hume_027 0032；adv_cidol-hume-3-017_02 0044；adv_dear_hume_032 0034；adv_dear_hume_029 0062；adv_dear_hume_016 0060；adv_dear_hume_022 0058；adv_cidol-hume-3-012_03 0049
## 人设 / 硬性规则
- 出处：用户规则（亲爱度线为正史、另一种可能写成假设）；conflicts 二·5（模仿、念字、复述不算她的说话方式）、三·10（「大好き」不是恋爱）、一·2（SSD 配方咲季保密）；剧本没交代的事见 adv_dear_hume_034 0039～0040（母亲的项目）、adv_dear_hume_024 0012～0014（燐羽回不回来）、adv_dear_hume_010-01 0010～0014（最讨厌的对手）；饮食：adv_pevent_003_hume_activity_021 0004、adv_pevent_001_hume_activity_004 0003（别的线，跨线一致）。
- 引文：adv_dear_hume_004 0024；adv_dear_hume_001 0056；adv_dear_hume_036 0035；adv_dear_hume_017 0025；adv_cidol-hume-3-012_02 0020；adv_dear_hume_003 0050
## 档案 / 基本信息
- 出处：官方数据：distill-work/ref/master-dl/CharacterDetail.yaml（vertesan/gakumasu-diff，hume 条目：学年1年生、身高158、体重50、AB型、ZodiacSign おひつじ座、CV 松田 彩音、Age 15、Birthday 4月1日、惯用手右、愛知県、特技 スポーツ全般、マッサージ、兴趣 お姉ちゃんとの勝負、介绍文）。「お姉ちゃんとの勝負」是 master 的兴趣栏，不逐条列剧本出处。按用户要求年龄、生日写“照官网（待补）”；剧本里只有 adv_startup_2025_bd-01_hume-01 是她的生日，没写日期。补欠合格：adv_dear_hume_001 0033～0038；adv_pevent_001_hume_activity_020 0002（有人辞退入学）。不是双胞胎、1年2組：conflicts 三·5。ソロ：adv_cidol-hume-3-012_03 0053。事务所：conflicts 三·6，adv_dear_hume_035 0038～0039（014 笔记的“所属 100プロ”是笔记写错）。生徒会庶務：conflicts 三·7。
- 引文：adv_dear_hume_001 0033；adv_dear_hume_001 0056；adv_pevent_001_hume_activity_015 0014
## 档案 / 故事线
- 出处：用户规则（2026-10-31、2026-11-11）；adv_dear_hume_001（入学式）、017 0022；conflicts 三·8（夏季『一番星』是星南、冬季是她）；adv_dear_hume_022 0033、036 0008～0010；adv_dear_hume_024（暑假刚结束）。
- 引文：adv_dear_hume_017 0022
## 档案 / 兴趣与特技
- 出处：官方数据；adv_dear_hume_014 0013～0017（见取り稽古）；adv_dear_hume_025 0024～0025；别的线：adv_csprt-2-0022_02 0008（游泳赢星南）、adv_csprt-2-0043_02（滑雪）、adv_csprt-3-0094_01 0011（爬树）、adv_event_002_main-02 0028（气味）、adv_dear_shro_006 0042～0045（按摩痛）。
- 引文：adv_dear_hume_001 0053；adv_dear_hume_010 0009；adv_csprt-2-0063_01 0017；adv_dear_hume_025 0024
## 档案 / 自称与说话方式
- 出处：统计见上；conflicts 四（第一人称、心声、模仿）；adv_dear_hume_001 0015 起自称一律「あたし」；adv_dear_hume_021 0061、031 0024（平口滑出）；adv_dear_hume_032 0041、034 0026（对前辈、训练员敬语）；adv_pevent_001_hume_activity_003 0011（平假名复述）。
- 引文：无（本节「」都是 7 字以内的称呼、口癖或官方资料）
## 档案 / 家人
- 出处：conflicts 三·3；adv_dear_hume_002 0058～0060；003 0018～0021、0056～0058；021 0032～0042；025 0040～0065；026 0074～0089；023 0015～0018（父亲教的方法）；033 0053～0054（家里负责咲季经纪）；034 0038～0043；别的线：adv_dear_hski_010 0055～0057（咲季说祖父母照看，同 hski 资料）；adv_csprt-3-0078_03 0008～0009（祖父寄菜、种田）。
- 引文：adv_dear_hume_003 0021；adv_csprt-2-0028_02 0008；adv_dear_hume_003 0058；adv_dear_hume_025 0058；adv_dear_hume_026 0083；adv_dear_hume_026 0089；adv_dear_hume_021 0040；adv_dear_hume_034 0039；adv_dear_hume_021 0036
## 档案 / 老家与花海トレーニングセンター
- 出处：conflicts 三·3、三·4；adv_dear_hume_021 0039～0045（母亲建设施，制作人也参与）；adv_dear_hume_025 0001～0004、0041（花海トレーニング／センター，父亲的话）、0051～0064；adv_dear_hume_027（コンペ）；adv_dear_hume_019 0056（姐姐回老家特训）。「花海トレーニングセンター」整词出自星南线 adv_dear_jsna_014 0038，只作名称。
- 引文：adv_dear_jsna_014 0038；adv_dear_hume_024 0069；adv_dear_hume_025 0004
## 档案 / 小时候与运动经历
- 出处：adv_dear_hume_008 0068～0072；adv_dear_hume_003 0056～0058；adv_cidol-hume-3-000_02 0009～0015；adv_cidol-hume-3-016_02 0029（模仿姐姐时进步快）；conflicts 四（学得慢与模仿快两说并存）；别的线：adv_dear_amao_031 0005～0007（乡下的路）、adv_dear_hski_005 0050（没受过大伤）、adv_csprt-2-0034_02 0020、2-0043_02 0014、2-0077_02 0011（比赛都输）、adv_dear_hski_010 0060～0064（咲季的回忆，同 hski 资料）。
- 引文：adv_dear_hume_008 0069；adv_dear_hume_008 0071；adv_cidol-hume-3-000_02 0009
## 档案 / 姐妹胜负：一次也没赢过
- 出处：conflicts 一·1、三·2（照咲季 一·1、一·3）；adv_dear_hume_004 0047～0049（猜拳、掰手腕）、0052～0056（体力测试）；009 0046（平局）；010 0032～0034；019 0001～0040；022 0034～0041（两人都输给星南）；033 0031～0034；036、037（姐姐名次没写）。
- 引文：adv_dear_hume_001 0047；adv_dear_hume_004 0044；adv_dear_hume_004 0057；adv_dear_hume_004 0060；adv_dear_hume_010 0036；adv_dear_hume_019 0012；adv_dear_hume_019 0013；adv_dear_hume_019 0023；adv_dear_hume_019 0037；adv_dear_hume_022 0038
## 档案 / 当偶像的理由
- 出处：conflicts 三·1（按亲爱度顺序：追姐姐、想赢姐姐 → 喜欢偶像、自己想当）；adv_dear_hume_004 0015～0016；006 0060～0069；019 0027～0031；020 0030～0052；目标变化：adv_dear_hume_001 0059、006 0064、010 0076、020 0030～0034、037 0065～0077；adv_cidol-hume-3-018_01 0020～0026。
- 引文：adv_dear_hume_001 0044；adv_dear_hume_004 0014；adv_dear_hume_006 0063；adv_dear_hume_006 0064；adv_cidol-hume-3-009_01 0031；adv_dear_hume_019 0030；adv_dear_hume_019 0031；adv_dear_hume_020 0035；adv_dear_hume_020 0047；adv_cidol-hume-3-018_03 0039；adv_dear_hume_035 0054；adv_dear_hume_037 0065
## 档案 / 补欠入学与学业
- 出处：adv_dear_hume_026 0052～0053、036 0020；adv_dear_hume_007 0026～0043；别的线：adv_pevent_001_hume_activity_008 0004、adv_csprt-3-0085_02 0016～0020、adv_csprt-3-0035_02 0015；conflicts 四（补欠各线一致）。
- 引文：adv_dear_hume_026 0053；adv_dear_hume_007 0029；adv_dear_hume_007 0042；adv_pevent_001_hume_school_001 0006；adv_csprt-3-0035_02 0015
## 档案 / 体质与身体
- 出处：adv_dear_hume_003 0048～0055；adv_cidol-hume-3-000_03 0008、000_02 0019（本番强、窮地）；adv_dear_hume_009 0005（鼻血）；032 0035～0038（拥抱）；034 0028～0033（自由曲）；别的线：adv_csprt-2-0063_02 0012（怕热）、adv_pevent_002_hume_sales_4-003-01 0004（握力）。
- 引文：adv_dear_hume_003 0055；adv_dear_hume_003 0050；adv_event_009_main-02 0032
## 档案 / 作息与日常
- 出处：adv_dear_hume_024 0001；034 0034；010 0001～0009；别的线：adv_pevent_001_hume_activity_002 0003、adv_csprt-3-0035_02、3-0035_03、adv_event_026_main-04 0002。
- 引文：adv_dear_hume_024 0001；adv_event_026_main-04 0002
## 档案 / 宿舍、班级与生徒会
- 出处：conflicts 三·4（宿舍、姐妹隔壁）、三·5（1年2組）、三·7（庶務）；adv_cidol-hume-3-012_01 0009～0015；adv_cidol-hume-3-012_03 0049；别的线：adv_dear_hski_005 0002（隔壁）、adv_csprt-3-0009_03 0015、adv_csprt-3-0109_02 0006～0008（房间乱，conflicts 四）、adv_event_002_main-04 0029、adv_event_014_main-04 0033（姐姐 1年1組）、adv_csprt-3-0015_01 0017。
- 引文：adv_csprt-3-0009_03 0015；adv_cidol-hume-3-012_01 0009；adv_cidol-hume-3-012_03 0049；adv_csprt-3-0015_01 0017
## 人物关系 / 制作人
- 出处：adv_dear_hume_001 0021～0029、0067；003 0036～0038、0068～0072；005 0007、0020～0021；008 0050～0055；017 0014～0027；023 0006～0038；035 0062～0063；adv_cidol-hume-3-000_02 0004；adv_cidol-hume-3-012_02 0020、0036～0039；adv_cidol-hume-3-022_01 0002～0005；conflicts 三·10（不是恋爱）。
- 引文：adv_dear_hume_001 0026；adv_dear_hume_001 0024；adv_dear_hume_002 0031；adv_dear_hume_003 0038；adv_dear_hume_003 0072；adv_dear_hume_008 0050；adv_dear_hume_017 0025；adv_cidol-hume-3-012_02 0039；adv_dear_hume_023 0033；adv_dear_hume_023 0036；adv_cidol-hume-3-006_02 0034；adv_dear_hume_035 0062；adv_dear_hume_035 0063；adv_cidol-hume-3-016_02 0037
## 人物关系 / 花海咲季
- 出处：conflicts 一·1、一·2、三·2；adv_dear_hume_002；005 0026～0028、0067；012 0040～0043；013 0010～0011；019 0016；024 0032～0033；029 0033；033 0041、0061；adv_cidol-hume-3-009_01～009_03；别的线：adv_csprt-2-0000_01、adv_csprt-3-0047_01 0003、adv_csprt-3-0081_02 0013、adv_csprt-3-0092_01 0020。
- 引文：adv_dear_hume_002 0073；adv_dear_hume_002 0074；adv_dear_hume_008 0061；adv_dear_hume_005 0028；adv_dear_hume_012 0070；adv_dear_hume_013 0010；adv_dear_hume_019 0016；adv_dear_hume_017 0038；adv_cidol-hume-3-009_01 0009；adv_cidol-hume-3-009_03 0048；adv_csprt-2-0017_02 0016；adv_csprt-3-0092_01 0020
## 人物关系 / 篠澤広
- 出处：adv_dear_hume_026 0026～0028；032 0014～0038；adv_cidol-hume-3-009_02 0024～0030；adv_cidol-hume-3-017_02 0017、0041～0044；adv_cidol-hume-3-018_01 0027；别的线：adv_csprt-3-0010_01 0012。
- 引文：adv_dear_hume_026 0026；adv_dear_hume_026 0028；adv_dear_hume_032 0034；adv_cidol-hume-3-009_02 0027；adv_cidol-hume-3-017_02 0044；adv_cidol-hume-3-018_01 0027；adv_csprt-3-0010_01 0012
## 人物关系 / 倉本千奈
- 出处：adv_dear_hume_025 0032～0038；026 0036、0052～0070；027 0032；adv_cidol-hume-3-005_02 0022、0044；adv_cidol-hume-3-017_02 0026～0032；别的线：adv_event_002_main-01 0032～0048。
- 引文：adv_dear_hume_026 0055；adv_dear_hume_027 0032；adv_cidol-hume-3-017_02 0032；adv_event_002_main-01 0048
## 人物关系 / 賀陽燐羽
- 出处：adv_dear_hume_012 0025～0070；013 0066～0072；015 0025～0059；016 0028～0060；024 0012～0014；029 0048～0062；025 0024。燐羽是否回来当偶像没写（O1 digest 第 9 节）。
- 引文：adv_dear_hume_012 0038；adv_dear_hume_013 0072；adv_dear_hume_016 0031；adv_dear_hume_016 0043；adv_dear_hume_016 0060；adv_dear_hume_029 0053；adv_dear_hume_029 0055；adv_dear_hume_029 0062
## 人物关系 / 十王星南
- 出处：adv_dear_hume_022 0033、0057～0058；024 0025；032 0054～0074；036 0010～0047；adv_cidol-hume-3-012_01 0010～0030（星南曾想招揽她，conflicts 四）；adv_cidol-hume-3-016_03 0016～0022。
- 引文：adv_dear_hume_022 0058；adv_dear_hume_024 0025；adv_cidol-hume-3-016_03 0021；adv_dear_hume_036 0013；adv_dear_hume_036 0021；adv_dear_hume_036 0044
## 人物关系 / 秦谷美鈴
- 出处：adv_cidol-hume-3-012_01～012_03；adv_cidol-hume-3-016_02 0024、016_03 0010、0013～0014、0039～0041；别的线：adv_event_002_main-02、adv_event_024_main-01 0042～0044。
- 引文：adv_cidol-hume-3-012_02 0040；adv_cidol-hume-3-016_03 0014；adv_cidol-hume-3-016_03 0040
## 人物关系 / 月村手毬
- 出处：adv_cidol-hume-3-018_02 0009～0044；adv_dear_hume_024 0058～0059、0095；别的线：adv_csprt-2-0067_01 0005～0010。
- 引文：adv_cidol-hume-3-018_02 0021；adv_cidol-hume-3-018_02 0034；adv_dear_hume_024 0095
## 人物关系 / 藤田ことね、葛城リーリヤ、紫雲清夏
- 出处：别的线：adv_event_009_main-02～05；adv_event_012_main-04 0039；adv_event_026_main-02 0032、main-05 0016；adv_csprt-3-0067_03 0013、0020。
- 引文：adv_event_009_main-02 0028；adv_event_009_main-03 0062
## 人物关系 / 雨夜燕、姫崎莉波、有村麻央
- 出处：别的线：adv_dear_atbm_021 0009、adv_csprt-3-0094_01 0019、adv_csprt-3-0047_01～03、adv_csprt-3-0078_02 0017。
- 引文：adv_dear_atbm_021 0009；adv_csprt-3-0094_01 0019；adv_csprt-3-0078_02 0017
## 人物关系 / 训练员、極月学園、765プロ的偶像
- 出处：adv_dear_hume_034 0009～0052；adv_dear_hume_016 0001～0027（她不在场）；adv_dear_hume_035 0028～0039；adv_cidol-hume-3-018_03 0025～0045（0045 是她转述对方的话，不当她的话）。
- 引文：adv_dear_hume_034 0026；adv_dear_hume_035 0038
## 人物关系 / 粉丝
- 出处：adv_dear_hume_016 0049～0052；adv_cidol-hume-3-006_03 0006～0053；adv_cidol-hume-3-018_03 0004。
- 引文：adv_cidol-hume-3-006_03 0007；adv_cidol-hume-3-006_03 0053；adv_cidol-hume-3-018_03 0004
## 经历 / 入学与认识制作人
- 出处：adv_dear_hume_001～004。
- 引文：adv_dear_hume_001 0049；adv_dear_hume_001 0060；adv_dear_hume_002 0065；adv_dear_hume_004 0024
## 经历 / 『選抜試験』与平局
- 出处：adv_dear_hume_005～010、010-01（010-01 后半黒井、四音的场面她不在场）。
- 引文：adv_dear_hume_005 0051；adv_dear_hume_006 0049；adv_dear_hume_007 0018；adv_dear_hume_008 0065；adv_dear_hume_009 0025；adv_dear_hume_010 0076；adv_dear_hume_010 0080
## 经历 / 『N.I.A』
- 出处：adv_dear_hume_011～020；014 0013～0017（见取り稽古）；018 0009；019 0008。
- 引文：adv_dear_hume_017 0045；adv_dear_hume_019 0008；adv_dear_hume_020 0043；adv_dear_hume_020 0034
## 经历 / 夏季『H.I.F』
- 出处：adv_dear_hume_021～023；conflicts 三·8（夏季『一番星』是星南）。
- 引文：adv_dear_hume_021 0017；adv_dear_hume_022 0048；adv_dear_hume_022 0049；adv_dear_hume_022 0065
## 经历 / 愛知合宿与コンペ
- 出处：adv_dear_hume_024～027；027 0099「完全敗北」所指不单独写（conflicts 三·9）。
- 引文：adv_dear_hume_024 0033；adv_dear_hume_027 0047；adv_dear_hume_027 0102
## 经历 / 冬季『H.I.F』与『一番星』
- 出处：adv_dear_hume_028～037；029『Try it now』与新曲是否同一首不单独写（conflicts 三·9）。
- 引文：adv_dear_hume_028 0066；adv_dear_hume_029 0050；adv_dear_hume_035 0005；adv_dear_hume_036 0031；adv_dear_hume_037 0055
## 经历 / P 卡里的歌与舞台
- 出处：【The Rolling Riceball】3-000；【Campus mode!!】3-006；【GUSUPI】3-009；【ENDLESS DANCE】3-016；【纯白画页与水彩绘就的主角】3-017；【GO MY WAY!!】3-018；【Agitato】3-022。卡与卡之间的先后大多看不出，不排先后；3-006_01 0025「定期公演」、3-017 夏天唱『Campus mode!!』、3-022_01 0040 方针时间照 conflicts 三·9 不写。000、009、017 卡里曲名没出现。
- 引文：adv_cidol-hume-3-000_01 0004；adv_cidol-hume-3-000_03 0031；adv_cidol-hume-3-006_01 0001；adv_cidol-hume-3-009_03 0014；adv_cidol-hume-3-009_03 0017；adv_cidol-hume-3-016_01 0048；adv_cidol-hume-3-017_01 0007；adv_cidol-hume-3-022_02 0028；adv_cidol-hume-3-022_03 0034
## 经历 / P 卡里的日常
- 出处：【White Night! White Wish!】3-005；【Star-mine】3-012。「ばくおんライオン」是什么剧本没写。
- 引文：adv_cidol-hume-3-005_01 0030；adv_cidol-hume-3-005_03 0023；adv_cidol-hume-3-005_03 0024；adv_cidol-hume-3-012_02 0030；adv_cidol-hume-3-012_02 0031
## 喜好 / 胜负
- 出处：adv_dear_hume_027 0005；adv_cidol-hume-3-000_02 0018～0022；adv_dear_hume_016 0028～0031；别的线：adv_pevent_002_hume_sales_1-005-01 0003、1-006-01 0006。
- 引文：adv_dear_hume_027 0005；adv_cidol-hume-3-000_02 0018；adv_dear_hume_016 0028
## 喜好 / 吃的东西
- 出处：adv_dear_hume_021 0033；adv_cidol-hume-3-022_03 0018～0019、0029；conflicts 一·2（配方只写“咲季保密”）；别的线：adv_csprt-2-0017_01 0012～0019、adv_csprt-2-0031_02 0005～0006、adv_pevent_001_hume_activity_004 0001～0006、adv_pevent_001_hume_activity_007 0016～0017、adv_csprt-3-0091_01、adv_csprt-3-0109_03 0007、adv_event_009_main-04 0013。
- 引文：adv_csprt-2-0017_01 0012；adv_pevent_003_hume_activity_021 0005
## 喜好 / 运动、偶像与爱好
- 出处：adv_dear_hume_020 0044～0045；030 0003、0027；adv_cidol-hume-3-018_02 0036～0037；adv_cidol-hume-3-016_01 0004；adv_cidol-hume-3-009_02 0018～0020。
- 引文：adv_dear_hume_030 0003；adv_cidol-hume-3-018_02 0036；adv_cidol-hume-3-016_01 0004；adv_cidol-hume-3-009_02 0020
## 喜好 / 讨厌与害怕的东西
- 出处：adv_dear_hume_007 0026；010-01 0020；035 0014；adv_cidol-hume-3-012_02 0020、0031；adv_cidol-hume-3-016_01 0029～0035；adv_dear_hume_009 0025；019 0021；033 0025～0029。
- 引文：adv_dear_hume_010-01 0020；adv_dear_hume_019 0021；adv_dear_hume_033 0029
## 另一种可能（不是她的经历） / 主线：Begrazia 与星南
- 出处：S1 digest；conflicts 一·1（4 章 7 话第一次赢、21 话 1勝1敗）、四（主线里星南是她的制作人）；adv_unit_01-01_01、01-02_08、01-03_04～05、01-03_12 0086、01-04_07、01-04_14、01-04_21、01-04_23。
- 引文：adv_unit_01-03_04 0074；adv_unit_01-04_07 0037；adv_unit_01-04_14 0071；adv_unit_01-04_21 0051；adv_unit_01-04_21 0057；adv_unit_01-04_21 0058；adv_unit_01-04_23 0065
## 另一种可能（不是她的经历） / 培育剧情
- 出处：O3、O4 digest；conflicts 四（并列分支、003 口气甜）、三·10（True End 的「大好き」不是恋爱）。
- 引文：adv_pstory_001_hume_opening-normal-02 0003；adv_pstory_001_hume_after-audition-mid-normal-02 0027；adv_pstory_001_hume_ending-true-01 0033；adv_pstory_002_hume_after-audition-a-normal-03 0011
## 另一种可能（不是她的经历） / 姐姐的制作人身边（咲季的亲爱度）
- 出处：S6 digest；conflicts 三·8（咲季线里夏天是她）；adv_dear_hski_002、019、022、033、036。
- 引文：adv_dear_hski_002 0018；adv_dear_hski_022 0044；adv_dear_hski_036 0031
## 另一种可能（不是她的经历） / 别的偶像身边的她（其他偶像的亲爱度）
- 出处：S6 digest；conflicts 四；adv_dear_jsna_019、022、035；adv_dear_kcna_026 0048～0049、027 0066、036；adv_dear_shro_016、030 0062。
- 引文：adv_dear_jsna_022 0003；adv_dear_jsna_019 0012；adv_dear_jsna_035 0027；adv_dear_shro_016 0014
## 另一种可能（不是她的经历） / 活动和 S 卡里的另一种发展
- 出处：S2～S5 digest；adv_event_005_main-05 0050～0070；adv_event_024（星南是制作人）；adv_csprt-3-0089（星南是制作人）；adv_event_026；adv_event_030；adv_csprt-3-0004_01 0003～0020（她自己的梦，conflicts 二·5）；adv_csprt-3-0052_01。
- 引文：adv_event_024_main-01 0013；adv_csprt-3-0004_01 0020；adv_csprt-3-0052_01 0012；adv_csprt-3-0052_01 0013
