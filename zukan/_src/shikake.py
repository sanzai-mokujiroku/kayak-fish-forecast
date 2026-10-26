"""仕掛けページ（8種）を作る: python3 zukan/_src/shikake.py（kayak-fish-forecast で実行）。eging/sabiki は手書き。"""
import pathlib, urllib.parse
OUT = pathlib.Path(__file__).resolve().parents[1]/'shikake'
T='font-family="Hiragino Sans,sans-serif"'
def lab(x,y,t,col="#0e294e",fs=14,w=800): return f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="{w}" fill="{col}" {T}>{t}</text>'
COL={'pe':'#e6a100','nylon':'#7fb7d9','fluoro':'#2a76a3','gray':'#9fb0c2'}
def svg(items, rod, reel):
    y=40; parts=[]; X=170
    # 先端からの道糸
    for it in items:
        k=it[0]
        if k=='line':
            _,col,t1,t2,ln=it
            parts.append(f'<path d="M{X},{y} L{X},{y+ln}" stroke="{COL[col]}" stroke-width="2.6"/>')
            parts.append(lab(X+14,y+ln/2+2,t1,{'nylon':'#2a76a3','gray':'#67778a'}.get(col,COL[col])))
            if t2: parts.append(lab(X+14,y+ln/2+20,t2,'#3b4a5a',13,600))
            y+=ln
        elif k=='knot':
            parts.append(f'<circle cx="{X}" cy="{y}" r="4.5" fill="#d9482b"/>'+lab(X+14,y+5,it[1],'#d9482b',13)); y+=18
        elif k=='swivel':
            parts.append(f'<rect x="{X-4}" y="{y}" width="8" height="14" rx="3" fill="#6b7d8f"/>'+lab(X+14,y+12,it[1],'#33475b',13)); y+=26
        elif k=='float':
            parts.append(f'<path d="M{X},{y} l-10,18 l10,18 l10,-18 z" fill="#ff8fbb" stroke="#c2306f"/>'+lab(X+18,y+22,it[1],'#c2306f',13)); y+=44
        elif k=='sinker':
            parts.append(f'<path d="M{X-6},{y} L{X+6},{y} L{X+3},{y+22} L{X-3},{y+22} Z" fill="#6b7d8f"/>'+lab(X+14,y+16,it[1],'#33475b',13)); y+=34
        elif k=='egg':  # 中通しオモリ
            parts.append(f'<ellipse cx="{X}" cy="{y+10}" rx="7" ry="11" fill="#6b7d8f"/>'+lab(X+14,y+15,it[1],'#33475b',13)); y+=28
        elif k=='hook':
            parts.append(f'<path d="M{X},{y} l0,14 q0,9 -8,9 q-7,0 -7,-7" fill="none" stroke="#33475b" stroke-width="2.4"/>'+lab(X+14,y+16,it[1],'#33475b',13)); y+=32
        elif k=='jighead':
            parts.append(f'<circle cx="{X}" cy="{y+6}" r="6" fill="#6b7d8f"/><path d="M{X},{y+12} q4,14 0,30 q-4,10 2,16" fill="none" stroke="#ff8fbb" stroke-width="7" stroke-linecap="round"/>'+lab(X+16,y+22,it[1],'#c2306f',13)+(lab(X+16,y+40,it[2],'#3b4a5a',12,600) if len(it)>2 else '')); y+=64
        elif k=='minnow':
            parts.append(f'<path d="M{X},{y} c10,6 12,40 0,56 c-12,-16 -10,-50 0,-56z" fill="#9fc3e0" stroke="#2a76a3"/>'+lab(X+16,y+26,it[1],'#2a76a3',13)+(lab(X+16,y+44,it[2],'#3b4a5a',12,600) if len(it)>2 else '')); y+=66
        elif k=='jig':
            parts.append(f'<rect x="{X-5}" y="{y}" width="10" height="50" rx="4" fill="#e9c46a" stroke="#b07a00"/>'+lab(X+16,y+28,it[1],'#b07a00',13)); y+=62
        elif k=='branch':  # 胴突き・カワハギの枝針
            _,n,t1,t2=it
            parts.append(f'<path d="M{X},{y} L{X},{y+n*30}" stroke="{COL["fluoro"]}" stroke-width="2.2"/>')
            for i in range(n): parts.append(f'<path d="M{X},{y+10+i*30} l18,8" stroke="#2a76a3" stroke-width="1.6"/><path d="M{X+18},{y+18+i*30} q5,5 0,10 q-5,2 -6,-3" fill="none" stroke="#33475b" stroke-width="2"/>')
            parts.append(lab(X+34,y+n*15,t1,'#2a76a3',13)+lab(X+34,y+n*15+18,t2,'#3b4a5a',12,600)); y+=n*30+6
        elif k=='tenbin':
            parts.append(f'<path d="M{X},{y} L{X},{y+10} L{X+30},{y+10}" fill="none" stroke="#33475b" stroke-width="2.4"/><path d="M{X+30},{y+10} L{X+30},{y+30}" stroke="#33475b" stroke-width="2"/><path d="M{X+24},{y+30} L{X+36},{y+30} L{X+33},{y+48} L{X+27},{y+48} Z" fill="#6b7d8f"/>'+lab(X+44,y+28,it[1],'#33475b',13)+lab(X+44,y+46,it[2],'#33475b',13))
            y+=56
    H=y+90
    rodp=f'<path d="M24,{H-70} C40,{H*0.6} 80,{H*0.25} 160,32" fill="none" stroke="#33475b" stroke-width="6" stroke-linecap="round"/><rect x="18" y="{H-90}" width="12" height="30" rx="5" fill="#33475b"/><g transform="translate(40,{H-130})"><circle r="15" fill="#8a97a6"/><rect x="-5" y="-4" width="26" height="7" rx="3" fill="#6b7d8f"/><circle r="6" fill="#d5dde6"/></g><path d="M160,32 L170,40" stroke="#9fb0c2" stroke-width="2"/>'
    leg=f'<line x1="10" y1="{H-40}" x2="350" y2="{H-40}" stroke="#d5dde6"/>'+lab(14,H-18,'竿','#67778a',13,700)+lab(60,H-18,rod,'#0e294e',13)+lab(14,H+6,'リール','#67778a',13,700)+lab(60,H+6,reel,'#0e294e',13)
    return f'<div class="rig"><svg viewBox="0 0 360 {H+20}" xmlns="http://www.w3.org/2000/svg">{rodp}{"".join(parts)}{leg}</svg></div>'
def li(xs): return '<ul>'+''.join(f'<li>{x}</li>' for x in xs)+'</ul>'
CSS='''<style>.rig{margin:6px 0 12px}.rig svg{width:100%;height:auto;display:block}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 12px}th,td{border:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}th{background:#eef3f8;font-size:12.5px;white-space:nowrap}.rec{color:var(--shu);font-weight:800}.tag{display:inline-block;background:#fff4e0;color:#8a5a00;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:700;margin-bottom:6px}</style>'''
M=[]
def add(**k): M.append(k)
add(fn='anatsuri', h1='穴釣りの仕掛け', sub='テトラのすき間に落として、カサゴなどの根魚を。', tag=None,
 items=[('line','nylon','道糸：ナイロン 2〜3号','',70),('swivel','ヨリモドシ 5〜6号'),('egg','中通しオモリ 3〜10号'),('line','fluoro','ハリス：フロロ 2〜3号','30cm前後',60),('hook','ハリ：ムツ10〜12号ほか')],
 rod='磯竿・投げ竿 3.6〜4.5m／ルアーロッド', reel='スピニング 2000番クラス',
 table=[('竿','磯竿か投げ竿 3.6〜4.5m、またはルアーロッド 6〜8フィート（ML・M）','下で説明'),('リール','2000番クラスのスピニング','—'),('道糸','ナイロン 2〜3号','—'),('仕掛け','中通しオモリ3〜10号＋ハリス フロロ2〜3号30cm前後＋ハリ（ムツ10〜12号、丸セイゴ11〜13号）','市販の「堤防根魚仕掛け」でよい')],
 perf=['<b>根掛かりしても仕掛けを外せる・切れる強さ。</b>岩の穴に落とす釣りなので、根掛かりは避けられない。','<b>オモリ（3〜10号＝約11〜38g）を下げられる強さ。</b>','<b>掛けたら穴から素早く引き出せる張り。</b>モタモタすると、魚が穴の奥に潜る。','<b>投げる性能は要らない。</b>足元のすき間に落とすだけ。'],
 subs=['ダイワの入門ページは、磯竿・投げ竿・ルアーロッド（ML・M）を挙げている。','リール付きの万能竿でも、オモリが竿の負荷の範囲内なら使える。'],
 ng=['ぐにゃっと曲がるだけの柔らかすぎる竿（魚を穴から出せない）。'],
 reelnote='ナイロン2〜3号を巻ける2000番前後なら、ほかの釣り用でも使える。',
 points=['仕掛けは根掛かりで失いやすい。<b>多めに持っていく</b>。','穴釣りは針1本の仕掛けが基本。テトラ以外の底を探る胴突き仕掛けは針2〜3本が一般的で、初めてなら2本のほうが扱いやすい（ダイワ）。','テトラの上は滑りやすく、すき間に落ちると危ない。足元に気をつけ、ライフジャケットを着ける。'],
 fish=[('hata','カサゴ'),('mebaru','メバル')], src=[('ダイワ「初心者のための釣り入門：穴釣りで釣る」','https://www.daiwa.com/jp/beginner/place/anatsuri')])
add(fn='nage', h1='ちょい投げ・投げ釣りの仕掛け', sub='砂浜や堤防から投げて、シロギスを。', tag=None,
 items=[('line','nylon','道糸','',40),('line','gray','力糸：3〜12号','10〜15m',70),('tenbin','テンビン＋オモリ','15〜25号'),('line','fluoro','幹糸：フロロ 3〜4号','50〜60cm',50),('branch',2,'ハリス：フロロ 2〜3号','30cm前後')],
 rod='投げ竿 3.5〜4.2m', reel='投げ釣り専用リール',
 table=[('竿','<span class="rec">投げ竿</span> 3.5〜4.2m','下で説明'),('リール','投げ釣り専用リール','—'),('糸','道糸の先に力糸（3〜12号・10〜15m）','—'),('仕掛け','テンビン＋オモリ15〜25号＋幹糸フロロ3〜4号＋ハリス2〜3号（ハリは丸セイゴ10〜13号、流線8〜14号）','市販の投げ仕掛けでよい'),('エサ','ジャリメ（ゴカイ）、細いアオイソメ','—')],
 perf=['<b>重いオモリ（15〜25号＝約56〜94g）を投げられる強さ。</b>ふつうのルアーロッドでは重すぎる重さ。','<b>遠くへ投げられる長さ。</b>','<b>小さなアタリが分かる穂先。</b>'],
 subs=['<b>「ちょい投げ」なら</b>：オモリを軽くして近くに投げる釣りにすれば、ルアーロッドや万能竿でもできる。<b>竿に書いてある「ルアー重量」や「オモリ負荷」の範囲を超えるオモリは使わない</b>（竿が折れる）。'],
 ng=['重いオモリを、負荷の小さい竿で思い切り投げること。竿が折れたり、オモリが飛んで人に当たったりする。'],
 reelnote='専用リールでなくても、糸がたくさん巻ける大きめのスピニングなら使える。',
 points=['投げる前に<b>後ろと周りに人がいないか</b>必ず確認する。','エサの付け方が大事。シロギスにはジャリメや細いアオイソメを通し刺しに（ダイワ）。'],
 fish=[('kisu','シロギス')], src=[('ダイワ「初心者のための釣り入門：カレイ、シロギスをちょい投げ仕掛けで釣る」','https://www.daiwa.com/jp/beginner/place/karei_shirogisu_nage')])
add(fn='light', h1='メバリング・アジングの仕掛け', sub='軽いジグヘッドとワームで、夜のメバル・アジを。', tag=None,
 items=[('line','pe','道糸：PE 0.2〜0.4号','（またはフロロ 2〜4lb）',70),('knot','FGノット'),('line','fluoro','リーダー：フロロ','4〜8lb',60),('knot','クリンチノット'),('jighead','ジグヘッド 1〜3g','＋ワーム2インチ前後')],
 rod='ライトソルト用ロッド 5〜7フィート（UL・L）', reel='スピニング 2000番クラス',
 table=[('竿','<span class="rec">ライトソルト用ロッド</span> 5〜7フィート（UL・L）','下で説明'),('リール','2000番クラスのスピニング','—'),('道糸','フロロカーボン 2〜4lb、またはPE 0.2〜0.4号','フロロならルアーに直結でよい'),('リーダー','（PEのとき）フロロ 4〜8lb','—'),('ルアー','ジグヘッド1〜3g＋ソフトルアー2インチ前後','—')],
 perf=['<b>1〜3gという、とても軽いルアーを投げられること。</b>ふつうのルアーロッドでは軽すぎて飛ばない。','<b>小さなアタリを取れる柔らかく敏感な穂先。</b>','<b>細い糸（2〜4lb）を使っても切れにくいしなやかさ。</b>'],
 subs=['<b>トラウトロッド</b>や<b>ライトゲーム用のバスロッド</b>など、ルアー重量が数g〜10g程度の柔らかい竿なら近いことができる（ルアー重量の下限が1〜3gに近いものを選ぶ）。','重めのジグヘッド（5g以上）やプラグにすれば、エギングロッドやシーバスロッドでも投げられるが、アタリは取りにくくなる。'],
 ng=['硬い竿＋太い糸。軽いルアーが飛ばず、アタリも分からない。'],
 reelnote='細い糸を100m以上巻ける1000〜2500番くらいのスピニングなら、ほかの釣り用でも使える。',
 points=['夜の常夜灯まわりや、潮の当たる所。ゆっくり巻くのが基本。','メバルは根の上や海藻のまわりに、頭を上にして群れていることが多い。'],
 fish=[('mebaru','メバル'),('aji','アジ')], src=[('ダイワ「初心者のための釣り入門：メバル、アジをルアーで釣る」','https://www.daiwa.com/jp/beginner/place/mebaru_mekki_lure')])
add(fn='seabass', h1='シーバス（スズキ）のルアーの仕掛け', sub='河口や港で、ミノーやバイブレーションを投げる。', tag=None,
 items=[('line','pe','道糸：PE 0.8〜1.5号','',70),('knot','FGノットか電車結び'),('line','fluoro','リーダー：フロロ','16〜20lb',60),('knot','クリンチノット'),('minnow','ミノー・バイブなど','シンキングペンシルも')],
 rod='シーバスロッド 7〜13フィート（ML〜H）', reel='スピニング LT3000〜4000番',
 table=[('竿','<span class="rec">シーバスロッド</span> 7〜13フィート（ML〜H）。最初の1本なら<b>9フィート前後のML</b>','下で説明'),('リール','LT3000〜4000番のスピニング','—'),('道糸','PE 0.8〜1.5号（最初は1.0号）','—'),('リーダー','フロロ 16〜20lb（最初は16lb）、70cm〜1.5m','—'),('ルアー','シンキングペンシル、フローティングミノー、バイブレーション','—')],
 perf=['<b>10〜30g前後のルアーを遠くへ投げられること。</b>','<b>場所に合った長さ。</b>港の中なら短め、河口や浜なら長め。ダイワは、最初は9フィート前後をすすめている。','<b>跳ねたり首を振ったりする魚に、糸をゆるめず付いていけること。</b>'],
 subs=['<b>エギングロッド</b>：長さと硬さが近く、軽めのルアーなら使える（エギングの代用にシーバスロッドが使えるのと逆）。','<b>サーフ用・ショアジギング用のルアーロッド</b>：重めのルアーに向く。'],
 ng=['メバリング用などの軽すぎる竿（ルアーが重すぎる・大きい魚に負ける）。'],
 reelnote='PE1号前後を150m以上巻ける3000〜4000番クラスなら、ほかの釣り用でも使える。',
 points=['夜や、雨のあとの濁りがよいとされる。','掛かると水面で跳ねて首を振る（エラ洗い）。竿を寝かせて、糸をゆるめない。'],
 fish=[('suzuki','スズキ')], src=[('ダイワ「初心者のための釣り入門：シーバスをルアーで釣る」','https://www.daiwa.com/jp/beginner/place/seabass_lure')])
add(fn='surf', h1='サーフ（砂浜）のルアーの仕掛け', sub='浜から遠くへ投げて、ヒラメを。', tag=None,
 items=[('line','pe','道糸：PE 0.8〜1.2号','',70),('knot','FGノット'),('line','fluoro','リーダー：フロロ','16〜20lb・1.5〜2m',70),('knot','クリンチノット'),('minnow','ミノー 9〜14cm','メタルジグ30〜40gも')],
 rod='サーフ用ルアーロッド 9〜11フィート（ML・M）', reel='スピニング LT4000〜5000番',
 table=[('竿','<span class="rec">サーフ用のルアーロッド</span> 9〜11フィート（ML・M）','下で説明'),('リール','LT4000〜5000番のスピニング','—'),('道糸','PE 0.8〜1.2号','—'),('リーダー','フロロ 16〜20lb、1.5〜2m','—'),('ルアー','ミノー（9〜14cm）、メタルジグ（30〜40g）、ジグヘッドワーム（14〜28g）','色はピンク・オレンジ・派手な色に実績')],
 perf=['<b>飛距離。</b>ダイワも「サーフ攻略で重要な要素のひとつが飛距離。長めのロッドが有利」としている。','<b>30〜40gのメタルジグまで投げられる強さ。</b>','<b>底近くをずっと引いてこられる、重めのルアーに合う張り。</b>'],
 subs=['<b>長めのシーバスロッド</b>（10フィート前後・M）：ルアー重量に30〜40gが入っていれば近いことができる。','<b>ショアジギング用ロッド</b>：重いジグを投げるのは得意。'],
 ng=['短い竿（飛距離が出ない）。','エギングロッドなど、30g以上のルアーが重量の範囲外になる竿。'],
 reelnote='PE1号前後を150〜200m巻ける4000番前後なら、ほかの釣り用でも使える。',
 points=['波打ち際から少し沖の、底近くをゆっくり引く。','浜は波が急に高くなることがある。波打ち際に近づきすぎない。'],
 fish=[('flat','ヒラメ')], src=[('ダイワ「初心者のための釣り入門：サーフからフラットフィッシュをルアーで釣る」','https://www.daiwa.com/jp/beginner/place/hirame_magochi_lure')])
add(fn='uki', h1='ウキ釣りの仕掛け（クロダイ）', sub='堤防や磯で、ウキを流してクロダイを。', tag=None,
 items=[('line','nylon','道糸：ナイロン 2〜3号','',50),('knot','ウキ止め'),('float','円錐ウキ（下にシモリ玉）'),('swivel','ヨリモドシ 10号'),('line','fluoro','ハリス：フロロ 1.5〜3号','1.5〜4m・途中にガン玉',70),('hook','ハリ：チヌ 1〜3号')],
 rod='磯竿 1〜1.5号・4.2〜5.3m', reel='スピニング 2500番クラス',
 table=[('竿','<span class="rec">磯竿</span> 1〜1.5号、4.2〜5.3m','下で説明'),('リール','2500番クラスのスピニング','—'),('道糸','ナイロン 2〜3号','—'),('仕掛け','ウキ止め＋シモリ玉＋円錐ウキ＋クッションゴム＋ヨリモドシ10号＋ハリス フロロ1.5〜3号（1.5〜4m）＋ガン玉＋ハリ（チヌ1〜3号）','—')],
 perf=['<b>長い仕掛け（ハリス1.5〜4m）を扱える長さ。</b>','<b>細いハリスでも切られないよう、魚の引きを竿全体で受けるしなやかさ。</b>磯竿の「1〜1.5号」は柔らかめの竿。','<b>ウキを流して、狙った所へ運べる操作性。</b>'],
 subs=['<b>同じくらいの長さ・柔らかさの磯竿</b>なら、号数が少し違っても使える（太い号数ほど硬い）。','リールのない<b>万能竿</b>でも、近くを狙う簡単なウキ釣りならできる。'],
 ng=['短く硬いルアーロッド。長いハリスを扱いにくく、細いハリスが切れやすい。'],
 reelnote='ナイロン2〜3号を巻ける2500番前後なら、ほかの釣り用でも使える。',
 points=['ガン玉は、ウキの浮く力に合わせて付ける。','時期によっては深い底まで探るので、ウキ止めの位置を動かして深さを変える（遊動仕掛け）。'],
 fish=[('chinu','クロダイ')], src=[('ダイワ「初心者のための釣り入門：ウキ釣りで釣る」','https://www.daiwa.com/jp/beginner/place/uminouki')])
add(fn='kawahagi', h1='カワハギ釣りの仕掛け', sub='小さなアタリを取る、エサ取り名人との勝負。', tag='数字は船・カヤックから釣る場合',
 items=[('line','pe','道糸：PE 0.8〜1.0号','',60),('swivel','ヨリモドシ 5〜6号'),('line','fluoro','幹糸：フロロ 3号','70cm〜1m',40),('branch',3,'枝ス：フロロ 2〜3号','10cm前後'),('sinker','オモリ 25〜30号')],
 rod='先調子の竿 1.8〜2.1m（オモリ負荷25〜30号）', reel='両軸受けリール 100〜150番',
 table=[('竿','<span class="rec">先調子の竿</span> 1.8〜2.1m（オモリ負荷25〜30号）','下で説明'),('リール','100〜150番クラスの両軸受けリール','—'),('道糸','PE 0.8〜1.0号','—'),('仕掛け','幹糸フロロ3号＋枝ス フロロ2〜3号（10cm前後）＋ハリ（丸セイゴ8〜9号、ハゲバリ4〜6号）＋オモリ25〜30号','—'),('エサ','アサリなど','—')],
 perf=['<b>小さなアタリが手元に出る、硬めで先の敏感な竿（先調子）。</b>カワハギはエサを吸い取るように食べるので、アタリが小さい。','<b>オモリ（25〜30号＝約94〜113g）を下げられる強さ。</b>','<b>針先が命。</b>ダイワも「一匹釣ったら針先をチェック」としている。'],
 subs=['<b>岸（堤防）から</b>なら：オモリを軽くして足元〜少し先の底を探る。オモリに合ったルアーロッドや万能竿でもできる。','船・カヤックでは、オモリ負荷が合う<b>先調子の船竿</b>なら代用できる。'],
 ng=['柔らかすぎる竿（アタリが分からず、エサだけ取られる）。'],
 reelnote='船では両軸受けリール。岸からならスピニングでよい。',
 points=['針の向きは必ず上に。','エサだけ取られたら、すぐ付け直す。'],
 fish=[('kawahagi','カワハギ')], src=[('ダイワ「初心者のための釣り入門：カワハギを釣る」','https://www.daiwa.com/jp/beginner/place/kawahagi')])
add(fn='jigging', h1='ジギングの仕掛け（青物）', sub='金属のルアー（メタルジグ）を沈めて、しゃくって巻く。', tag='数字は船から大型を狙う場合',
 items=[('line','pe','道糸：PE 2〜4号','',70),('knot','FGノットなど'),('line','fluoro','リーダー：フロロ','30〜60lb・3〜6m',70),('knot','クリンチノット'),('jig','メタルジグ')],
 rod='ジギングロッド 5.5〜6.5フィート前後', reel='スピニング5000〜8000番／両軸300番',
 table=[('竿','<span class="rec">ジギングロッド</span> 5.5〜6.5フィート前後（PE2〜4号クラス）','下で説明'),('リール','スピニング 5000〜8000番、または両軸受け 300番クラス','初めてならスピニングがおすすめ（ダイワ）'),('道糸','PE 2〜4号','—'),('リーダー','フロロ 30〜60lb、3〜6m','魚が大きいほど・根が荒いほど太く'),('ルアー','メタルジグ','—')],
 perf=['<b>ジグの重さに合った強さ。</b>竿に書いてある「ジグ重量」を見て選ぶ。','<b>大きな魚の引きに耐える強さと、リールの巻く力。</b>','<b>しゃくりやすい長さ（短め）。</b>船の上でジグを動かすので、長い竿は扱いにくい。'],
 subs=['<b>ライトジギングロッド</b>：小〜中型の青物（ツバイソ・フクラギ・サゴシ）や根魚なら、軽めのジグで十分。<br><b>筆者のカヤックの例</b>：シマノ グラップラー タイプLJ（適合ジグ50〜160g）＋オシアコンクエスト300HG＋PE2号。','<b>岸からは「ショアジギング」</b>：長いショアジギング用ロッド（またはサーフ用・シーバスロッドの強いもの）で、ジグを遠くへ投げる。'],
 ng=['ジグ重量の範囲外の竿（重いジグで竿が折れる・軽すぎて動かない）。'],
 reelnote='PEの号数に合わせて、たくさん巻けて巻く力の強いリールを。',
 points=['ダイワは「最初の一本は、操作がしやすいスピニングがおすすめ」としている。','カヤックでは、大きな魚に艇ごと引っぱられる。ドラグは緩めに。'],
 fish=[('buri','ブリ'),('kobuRI','サゴシ'),('akamutsu','アカムツ（深場は重いジグ）')], src=[('ダイワ「初心者のための釣り入門：ジギングで釣る」','https://www.daiwa.com/jp/beginner/place/kanpachi_buri_jigging'),('シマノ グラップラー タイプLJ 仕様','https://fishshop.shimano.com/products/25grappler-type-lj-cast-us')])

# ---- 新しい図（rigdraw）の部品の並び ----
import sys as _s; _s.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rigdraw
RIGS = {
 'eging':   ([('line','pe',70,'道糸：PE','0.6〜1号'),('knot','FGノット'),('line','fluoro',60,'リーダー：フロロ','1.5〜2.5号・1〜1.5m'),('knot','クリンチノット'),('egi','エギ','2.5〜3.5号')],'エギングロッド 7〜9フィート','スピニング 2500番クラス',False),
 'sabiki':  ([('line','nylon',50,'道糸：ナイロン','2〜3号'),('swivel','ヨリモドシ','スナップ付き・5〜6号'),('bag','コマセ袋','アミエビを詰める'),('sabiki',5,'サビキ仕掛け','市販品'),('sinker','オモリ','5〜15号')],'磯竿か投げ竿 3.6〜4.5m','スピニング 2500番クラス',False),
 'anatsuri':([('line','nylon',70,'道糸：ナイロン','2〜3号'),('swivel','ヨリモドシ','5〜6号'),('egg','中通しオモリ','3〜10号'),('line','fluoro',56,'ハリス：フロロ','2〜3号・30cm前後'),('hook','ハリ','ムツ10〜12号など')],'磯竿・投げ竿 3.6〜4.5m など','スピニング 2000番クラス',True),
 'nage':    ([('line','nylon',36,'道糸',None),('line','power',60,'力糸','3〜12号・10〜15m'),('tenbin','テンビン＋オモリ','15〜25号'),('line','fluoro',50,'幹糸：フロロ','3〜4号・50〜60cm'),('branch',2,'ハリス：フロロ','2〜3号・30cm前後')],'投げ竿 3.5〜4.2m','投げ釣り専用リール',True),
 'light':   ([('line','pe',70,'道糸：PE 0.2〜0.4号','またはフロロ 2〜4lb'),('knot','FGノット'),('line','fluoro',56,'リーダー：フロロ','4〜8lb'),('knot','クリンチノット'),('jighead','ジグヘッド 1〜3g','＋ワーム2インチ前後')],'ライトソルト用 5〜7フィート（UL・L）','スピニング 2000番クラス',False),
 'seabass': ([('line','pe',70,'道糸：PE','0.8〜1.5号'),('knot','FGノットか電車結び'),('line','fluoro',60,'リーダー：フロロ','16〜20lb'),('knot','クリンチノット'),('minnow','ミノー・バイブなど','シンキングペンシルも')],'シーバスロッド 7〜13フィート（ML〜H）','スピニング LT3000〜4000番',False),
 'surf':    ([('line','pe',70,'道糸：PE','0.8〜1.2号'),('knot','FGノット'),('line','fluoro',66,'リーダー：フロロ','16〜20lb・1.5〜2m'),('knot','クリンチノット'),('minnow','ミノー 9〜14cm','メタルジグ30〜40gも')],'サーフ用ルアーロッド 9〜11フィート','スピニング LT4000〜5000番',True),
 'uki':     ([('line','nylon',40,'道糸：ナイロン','2〜3号'),('knot','ウキ止め'),('float','円錐ウキ','上にシモリ玉'),('swivel','ヨリモドシ','10号'),('line','fluoro',70,'ハリス：フロロ','1.5〜3号・1.5〜4m'),('hook','ハリ','チヌ1〜3号')],'磯竿 1〜1.5号・4.2〜5.3m','スピニング 2500番クラス',False),
 'kawahagi':([('line','pe',60,'道糸：PE','0.8〜1.0号'),('swivel','ヨリモドシ','5〜6号'),('line','fluoro',40,'幹糸：フロロ 3号','70cm〜1m'),('branch',3,'枝ス：フロロ 2〜3号','10cm前後'),('sinker','オモリ','25〜30号')],'先調子の竿 1.8〜2.1m','両軸受けリール 100〜150番',True),
 'jigging': ([('line','pe',70,'道糸：PE','2〜4号'),('knot','FGノットなど'),('line','fluoro',70,'リーダー：フロロ','30〜60lb・3〜6m'),('knot','クリンチノット'),('jig','メタルジグ','重さは竿に合わせる')],'ジギングロッド 5.5〜6.5フィート','スピニング5000〜8000番 など',False),
}
def rigsvg(fn):
    it, rod, reel, bed = RIGS[fn]
    return rigdraw.draw(it, rod, reel, bed)
FONT='https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@800&display=swap&text='+urllib.parse.quote(''.join(sorted(set(''.join(m['h1'] for m in M)+'エギングサビキの仕掛け釣り方富山湾魚図鑑'))))
for m in M:
    tbl='<table><tr><th></th><th>おすすめ（専用）</th><th>代わり・補足</th></tr>'+''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for a,b,c in m['table'])+'</table>'
    fish=' ・ '.join(f'<a href="../{i}.html">{n}</a>' for i,n in m['fish'])
    body=f'''{'<span class="tag">⚠️ '+m['tag']+'</span>' if m['tag'] else ''}
{rigsvg(m['fn'])}
<section><h2>道具の目安</h2>{tbl}</section>
<section><h2>専用じゃない竿を使うなら：最低限ほしい性能</h2>
<h3>この釣りは、こんな性能がほしい</h3>{li(m['perf'])}
<h3>だから、こんな竿でも代用できる</h3>{li(m['subs'])}
<h3>向かない竿</h3>{li(m['ng'])}
<p class="cap">リール：{m['reelnote']}</p></section>
<section><h2>釣り方のポイント</h2>{li(m['points'])}<p>この仕掛けで狙う魚：{fish}</p></section>'''
    srcs=''.join(f'<li><a href="{u}">{t}</a></li>' for t,u in m['src'])
    html=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{m['h1']}と道具の目安｜竿・リール・糸の号数（図解）</title><meta name="description" content="{m['h1']}を図解。竿・リール・道糸・リーダーの目安と、専用じゃない竿で代用するときに最低限ほしい性能。">
<link rel="canonical" href="https://sanzai-mokujiroku.github.io/kayak-fish-forecast/zukan/shikake/{m['fn']}.html">
<meta name="theme-color" content="#0e294e"><link rel="icon" type="image/png" href="../../icon-192.png">
<link rel="stylesheet" href="{FONT}"><link rel="stylesheet" href="../zukan.css">{CSS}</head><body>
<div class="hero"><div class="wrap"><div class="crumb"><a href="../../">釣果予報</a> › <a href="../">富山湾の魚図鑑</a> › <a href="./">仕掛け</a></div>
<h1 style="margin-top:10px">{m['h1']}</h1><p class="sub">{m['sub']}</p></div></div>
<main>{body}
<section class="src"><h2>出典</h2><ul>{srcs}</ul><p class="cap">号数・長さは目安。釣り場や狙う大きさで変わります。図はこのページ用に描き起こしたもの。</p></section></main>
<footer>富山湾カヤックの<a href="https://sanzai-mokujiroku.github.io/">無料ツール</a>／ブログ <a href="https://kayak-papa.hatenablog.com/">富山湾カヤック釣行 散財黙示録</a></footer></body></html>'''
    (OUT/f"{m['fn']}.html").write_text(html,encoding='utf-8')
# 仕掛け一覧
lst=[('eging','エギング','アオリイカ'),('sabiki','サビキ','アジ・カマス'),('light','メバリング・アジング','メバル・アジ'),('anatsuri','穴釣り','カサゴ・メバル'),('nage','ちょい投げ・投げ釣り','シロギス'),('seabass','シーバスのルアー','スズキ'),('surf','サーフのルアー','ヒラメ'),('uki','ウキ釣り','クロダイ'),('kawahagi','カワハギ釣り','カワハギ'),('jigging','ジギング','ブリ・サゴシ・アカムツ')]
cards=''.join(f'<a class="tool" style="display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin-bottom:10px;text-decoration:none;color:var(--ink)" href="{f}.html"><b style="font-size:16px;color:var(--kon)">{n}</b><br><small style="color:var(--muted)">{w}</small></a>' for f,n,w in lst)
idx=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>釣り方別の仕掛けと道具の目安｜図解・代用できる竿も</title><meta name="description" content="エギング・サビキ・穴釣り・投げ釣り・メバリング・シーバス・サーフ・ウキ釣り・カワハギ・ジギングの仕掛けを図解。専用じゃない竿で代用するときの目安も。">
<link rel="canonical" href="https://sanzai-mokujiroku.github.io/kayak-fish-forecast/zukan/shikake/">
<meta name="theme-color" content="#0e294e"><link rel="icon" type="image/png" href="../../icon-192.png">
<link rel="stylesheet" href="{FONT}"><link rel="stylesheet" href="../zukan.css"></head><body>
<div class="hero"><div class="wrap"><div class="crumb"><a href="../../">釣果予報</a> › <a href="../">富山湾の魚図鑑</a> › 仕掛け</div>
<h1 style="margin-top:10px">釣り方別の仕掛け</h1><p class="sub">道具の目安と、手持ちの竿で代用するときに最低限ほしい性能。</p></div></div>
<main>{cards}<p class="cap">数字はダイワ「初心者のための釣り入門」をもとにした目安です。</p></main>
<footer>富山湾カヤックの<a href="https://sanzai-mokujiroku.github.io/">無料ツール</a>／ブログ <a href="https://kayak-papa.hatenablog.com/">富山湾カヤック釣行 散財黙示録</a></footer></body></html>'''
(OUT/'index.html').write_text(idx,encoding='utf-8')
import re as _re
for fn in ('eging','sabiki'):
    f=OUT/f'{fn}.html'; t=f.read_text(encoding='utf-8')
    t=_re.sub(r'<div class="rig">.*?</svg></div>', lambda _m: rigsvg(fn), t, count=1, flags=_re.S)
    t=t.replace('.rig{background:#f6f9fc;border-radius:12px;padding:6px;margin:6px 0 10px}','.rig{margin:6px 0 12px}')
    f.write_text(t,encoding='utf-8')
print('ok',len(M))
