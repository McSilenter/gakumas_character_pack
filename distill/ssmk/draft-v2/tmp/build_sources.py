# 生成 draft-v2/facts/sumika.sources.md：开头说明＋参考网站＋统计（沿用第一版）＋按 v2 facts 各节列出处和引文＋未收录
import re,sys
sys.path.insert(0,'/home/claude/distill-work/ssmk/draft-v2/tmp')
from corpus import load,norm
B='/home/claude/distill-work/ssmk/'
rows=load(); N=[(s,i,n,norm(t)) for s,i,n,t in rows]
old=open(B+'draft-v2/tmp/sources-v1base.md',encoding='utf-8').read().split('\n')  # 11-22: v1 sources copy, edited for 萌百 profile
# 第一版 facts/sheet 每行：引文 -> 该行引用的 stem
dmap=[]
for f in ['draft/facts/sumika.md','draft/sheets/sumika.md','draft/facts/sumika.sources.md']:
    for line in open(B+f,encoding='utf-8'):
        st=set(re.findall(r'adv_[A-Za-z0-9_\-]+',line))
        for q in re.findall(r'「([^「」]{4,})」',line): dmap.append((norm(q),st))
def locate(q):
    k=norm(q); pref=set()
    for Q,st in dmap:
        if k in Q: pref|=st
    hit=[(s,i,n) for s,i,n,t in N if k in t]
    if pref:
        h2=[x for x in hit if x[0] in pref]
        if h2: hit=h2
    hit.sort(key=lambda x:(x[2]!='清夏', not x[0].startswith('adv_dear_ssmk'), not x[0].startswith('adv_cidol-ssmk')))
    return hit[0] if hit else None
PC={'000':'【Tame-Lie-One-Step】','001':'【与你共度的湛蓝夏日】','002':'【隐藏的我】','007':'【Campus mode!!】','010':'【樱花相册】','012':'【Love & Joy】','014':'【奇迹正是现在(ﾟ∀ﾟ)！】','017':'【怦然心动】','018':'【标】'}
def label(s):
    m=re.fullmatch(r'adv_dear_ssmk_(\d{3})(-01)?',s)
    if m: return f'亲爱度第 {int(m.group(1))}{".5" if m.group(2) else ""} 话（{s}）'
    m=re.fullmatch(r'adv_cidol-ssmk-3-(\d{3})_(\d\d)',s)
    if m: return f'P 卡{PC.get(m.group(1),"")}第 {int(m.group(2))} 话（{s}）'
    return s
def short(q): return q if len(q)<=12 else q[:11]+'……'
def ref(q):
    h=locate(q)
    if not h and q=='あたしが本気で踊るとこ、見せたげる♪': return f'「{short(q)}」官方标语，非台词（萌百，见“参考网站”）'
    if not h: return f'「{short(q)}」未找到'
    s,i,n=h
    who='' if n=='清夏' else '（说话人「？？？」）' if n=='？？？' else f'（{n}）'
    return f'「{short(q)}」{s} {i}{who}'
def qlist(body):
    seen=[]
    for line in body:
        for q in re.findall(r'「([^「」]{4,})」',line):
            if q not in seen: seen.append(q)
    return ['- 引文：'+'；'.join(ref(q) for q in seen)+'。'] if seen else []
# 第一版各节的“出处”行
olds={}
cur=None
for l in old:
    if l.startswith('## '): cur=l[3:].strip(); continue
    if cur and l.startswith('- 出处：'): olds[cur]=l[5:]
M={
'档案 / 基本信息':['档案 / 基本信息'],'档案 / 故事线':['档案 / 故事线'],
'档案 / 兴趣与特技':['档案 / 能力与课题','喜好 / 唱歌、卡拉OK与游戏厅'],
'档案 / 自称与说话方式':['档案 / 自称与说话方式','档案 / “面具”与真心话'],
'档案 / 家人与北海道':['档案 / 北海道的家与父母'],
'档案 / 芭蕾与瑞典':['档案 / 芭蕾与『神童』','档案 / 瑞典留学与リーリヤ'],
'档案 / 膝伤与偶像梦':['档案 / 膝伤与心理阴影','档案 / 偶像梦的由来'],
'档案 / 学园生活':['档案 / 学园生活与宿舍'],
'人物关系 / 『REVERSI』':['组合 / 『REVERSI』'],'人物关系 / 和リーリヤ的约定':['档案 / 和リーリヤ的约定'],
'人物关系 / 制作人':['人物关系 / 制作人','人物关系 / 制作人与“幸福”'],
'人物关系 / 葛城リーリヤ':['人物关系 / 葛城リーリヤ'],
'人物关系 / 月村手毬':['人物关系 / 月村手毬、花海咲季'],
'人物关系 / 雨夜燕':['人物关系 / 雨夜燕、十王星南'],'人物关系 / 十王星南':['人物关系 / 雨夜燕、十王星南'],
'人物关系 / 白草四音':['人物关系 / 白草四音、藍井撫子'],
'人物关系 / 其他偶像':['人物关系 / 别的故事里的同学和前辈','人物关系 / 月村手毬、花海咲季'],
'人物关系 / 同学、朋友与粉丝':['人物关系 / 同学、朋友与粉丝'],
'经历 / 被スカウト':['经历 / 逃课与スカウト（第 1～4 话）'],
'经历 / 跨过阴影与首场 live':['经历 / 跨过阴影与首场 live（第 5～10 话）'],
'经历 / 『N.I.A』与四音':['经历 / 『N.I.A』与四音（第 10.5～20 话）'],
'经历 / 夏季『H.I.F』与“任性”':['经历 / 夏季『H.I.F』与“任性”（第 21～26 话）'],
'经历 / 『REVERSI』与冬季選抜':['经历 / 『REVERSI』与冬季選抜（第 27～33 话）'],
'经历 / 冬季『H.I.F』与『一番星』':['经历 / 冬季『H.I.F』与『一番星』（第 34～37 话）'],
'经历 / 『一番星』之后':['经历 / 『一番星』之后（现在）'],
'经历 / P 卡里的工作与日常':['经历 / P 卡里的事'],
'经历 / 现在：P 卡【標】（标，第 37 话之后）':['经历 / P 卡【标】（第 37 话之后）'],
'喜好 / 时尚、化妆与拍照':['喜好 / 时尚、化妆与拍照'],'喜好 / 唱歌与游戏厅':['喜好 / 唱歌、卡拉OK与游戏厅'],
'喜好 / 吃的东西':['喜好 / 吃的'],'喜好 / 讨厌、怕的、不擅长的':['喜好 / 讨厌、怕的、不擅长的'],
'另一种可能（不是她的经历）':[],
}
for k in ['培育剧情','培育事件与成长剧情','S 卡','活动与主线','别的偶像的线里']:
    M['另一种可能（不是她的经历） / '+k]=['另一种可能（不是她的经历） / '+k]
EXTRA=open('/home/claude/distill-work/ssmk/draft-v2/tmp/sources-extra.txt',encoding='utf-8').read()
ex={}; cur=None
for l in EXTRA.split('\n'):
    if l.startswith('@@ '): cur=l[3:].strip(); ex[cur]=[]; continue
    if cur is not None and l.strip(): ex[cur].append(l)
out=list(ex['HEAD'])+old[2:7]+ex['HEAD2']
out.append('')
# 参考网站、统计：沿用第一版
i0=old.index('## 参考网站'); i1=next(i for i,l in enumerate(old) if l.startswith('## 人设 / 身份'))
for l in old[i0:i1]:
    out.append(l.replace('（questions ','（draft/tmp/questions.md ').replace('questions 二','questions.md 二'))
out+=ex['STAT']
# 各节
h1=''; secs=[]; cur=None
for line in open(B+'draft-v2/facts/sumika.md',encoding='utf-8'):
    line=line.rstrip('\n')
    if line.startswith('# '):
        h1=line[2:]; cur=[h1,[]]; secs.append(cur); continue
    if line.startswith('## '):
        cur=[h1+' / '+line[3:],[]]; secs.append(cur); continue
    cur[1].append(line)
for name,body in secs:
    if not any(b.strip() for b in body): continue
    out.append(''); out.append('## '+name)
    out+=ex.get(name,[])
    os_=[olds[o].rstrip('。') for o in M.get(name,[]) if o in olds]
    if os_: out.append('- 出处：'+'；'.join(os_)+'。')
    out+=qlist(body)
# 人设引文
out.append(''); out.append('## 人设的引文')
out+=ex['SHEET']
sh=[l.rstrip('\n') for l in open(B+'draft-v2/sheets/sumika.md',encoding='utf-8')]
fq=set(norm(q) for _,b in secs for l in b for q in re.findall(r'「([^「」]{4,})」',l))
only=[l for l in sh if any(norm(q) not in fq for q in re.findall(r'「([^「」]{4,})」',l))]
qs=[]
for l in only:
    for q in re.findall(r'「([^「」]{4,})」',l):
        if norm(q) not in fq and q not in qs: qs.append(q)
res=['- 引文：'+'；'.join(ref(q) for q in qs)+'。']
out+=res
# 未收录
j0=old.index('## 未收录'); j1=old.index('## 引文检查')
out.append(''); out+=old[j0:j1]
out+=ex['TAIL']
open(B+'draft-v2/facts/sumika.sources.md','w',encoding='utf-8').write('\n'.join(out).rstrip()+'\n')
print('ok', sum(len(x.encode()) for x in out))
