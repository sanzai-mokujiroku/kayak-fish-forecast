"""図鑑ページを作る: python3 zukan/_src/build.py（kayak-fish-forecast で実行）"""
import re, html, urllib.parse, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'zukan'/'_src'))
from fish import FISH, KYOKYO
src = (ROOT/'index.html').read_text(encoding='utf-8')
def tackle(tid):
    m = re.search(r"id:'%s'.*?tackle:'(.*?)',\s*tips:'(.*?)'" % re.escape(tid), src, re.S)
    return (m.group(1), m.group(2)) if m else ('', '')
names = ''.join(f['name'] for f in FISH) + '富山湾の魚図鑑カヤックで狙える'
FONT = 'https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@800&display=swap&text=' + urllib.parse.quote(''.join(sorted(set(names))))
NOTE = '''<div class="note"><b class="t">⚠️ 漁獲量＝釣れやすさ、ではない</b>
<ul><li>漁況報告の数字は、漁師さんの網（主に定置網）に入った量。<b>釣り人が釣った数ではない。</b></li>
<li>網に入る量は、魚の数だけでなく、網を張る場所や時期にも左右される。</li>
<li>少ない時期でも狙えば釣れることはあるし、多い時期でも釣れない日はある。</li></ul>
「この時期は、湾に入ってくる数が多い」くらいの目安として見てください。</div>'''
def head(title, desc, canon, img):
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://sanzai-mokujiroku.github.io/kayak-fish-forecast/zukan/{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://sanzai-mokujiroku.github.io/kayak-fish-forecast/{img}">
<meta name="theme-color" content="#0e294e">
<link rel="icon" type="image/png" href="../icon-192.png">
<link rel="stylesheet" href="{FONT}">
<link rel="stylesheet" href="zukan.css">
</head>
<body>'''
FOOT = '''<footer>富山湾カヤックの<a href="https://sanzai-mokujiroku.github.io/">無料ツール</a>／ブログ <a href="https://kayak-papa.hatenablog.com/">富山湾カヤック釣行 散財黙示録</a></footer>
</body>
</html>'''
def chart(vals, cap):
    mx = max(v for v in vals if v)
    bars = ''.join(f'<div class="{"hi" if v and v >= mx*0.7 else ""}" style="height:{max(2, round((v or 0)/mx*100))}%"></div>' for v in vals)
    labels = ''.join(f'<span>{m}</span>' for m in range(1, 13))
    return f'<div class="months">{bars}</div><div class="mlabel">{labels}</div><p class="cap">{cap}</p>'
for f in FISH:
    if f['id'] == 'aori':
        continue
    tk, tips = tackle(f['tool'])
    tips = f.get('tips', tips)
    full = f['name'] + f.get('kana', '')
    uses_kyokyo = 'KYOKYO' in f['srcs']
    srcs = ''.join(f'<li><a href="{KYOKYO[1] if s=="KYOKYO" else s[1]}">{KYOKYO[0] if s=="KYOKYO" else s[0]}</a></li>' for s in f['srcs'])
    body = f'''<div class="hero"><div class="wrap">
  <div class="crumb"><a href="../">釣果予報</a> › <a href="./">富山湾の魚図鑑</a></div>
  <div class="hero-in">
    <div><h1>{f["name"]}</h1>{f'<p class="kana">{f["kana"]}</p>' if f.get("kana") else ''}<p class="sub">{f["sub"]}</p></div>
    <div class="gyotaku"><img src="../gyotaku/{f["id"]}.webp" alt="{f["name"]}のカラー魚拓（イラスト）"></div>
  </div>
</div></div>
<main>
  <section><h2>時期と、くらし</h2>
    {chart(f["chart"], f["chartcap"]) if f.get("chart") else ""}
    {f["when"]}
    {NOTE if uses_kyokyo else ""}
  </section>
  <section><h2>どこにいる？</h2>{f["where"]}</section>
  <section><h2>カヤックでの狙い方（目安）</h2>
    <p>{tk}</p><p>{tips}</p>
    <p class="cap">※釣果予報の「道具の目安」と同じ内容。一般的な釣り方の目安です。</p>
  </section>
  <section><h2>釣れたら・注意</h2><ul>{f["care"]}</ul></section>
  {f.get("extra", "")}
  <a class="cta" href="../">今日の「釣れそう度」を釣果予報で見る →</a>
  <section class="src"><h2>出典</h2><ul>{srcs}</ul>
    <p class="cap">確かめられなかったことは書いていません。間違いに気づいたら教えてください。</p></section>
</main>'''
    title = f'富山湾の{full}｜時期・すみか・カヤックでの狙い方'
    desc = f'{full}の生態（産卵期・すみか）と、富山湾での獲れる時期、カヤックでの狙い方・注意点を出典つきでまとめました。'
    (ROOT/'zukan'/f'{f["id"]}.html').write_text(head(title, desc, f'{f["id"]}.html', f'gyotaku/{f["id"]}.webp') + body + FOOT, encoding='utf-8')
# 一覧
cards = ''.join(f'<a class="fish" href="{f["id"]}.html"><img src="../gyotaku/{f["id"]}.webp" alt=""><span>{f["name"]}</span><small>{f["sub"].split("。")[0]}</small></a>' for f in FISH)
idx = head('富山湾の魚図鑑｜カヤックで狙える16種の時期・すみか・狙い方', '富山湾でカヤックから狙える魚16種を、カラー魚拓つきで。富山県水産研究所の資料など出典つきで、時期・すみか・狙い方をまとめました。', '', 'gyotaku/madai.webp') + f'''<div class="hero"><div class="wrap">
  <div class="crumb"><a href="../">釣果予報</a> › 富山湾の魚図鑑</div>
  <h1 style="margin-top:10px">富山湾の魚図鑑</h1>
  <p class="sub">カヤックで狙える16種。魚拓はイラスト（AIで作成）、中身は出典つき。</p>
</div></div>
<main>
  <div class="grid">{cards}</div>
  <p class="cap" style="margin-top:14px">富山湾の数字は、富山県水産研究所の論文や漁況報告から。漁獲量（網の水揚げ）は、釣れやすさとは別物です。</p>
  <a class="cta" href="../">今日の「釣れそう度」を釣果予報で見る →</a>
</main>''' + FOOT
(ROOT/'zukan'/'index.html').write_text(idx, encoding='utf-8')
print('ok', len(FISH))
