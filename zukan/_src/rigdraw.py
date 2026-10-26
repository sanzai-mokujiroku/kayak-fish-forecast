"""仕掛け図を描く（SVG）。shikake.py から使う。
items は上（竿先）から下への部品の並び。
  ('line', 種類, 長さpx, 見出し, 補足)   種類: pe / nylon / fluoro / power
  ('knot', 名前)
  ('swivel', 見出し, 補足)  ('float', ...)  ('sinker', ...)  ('egg', ...)
  ('hook', ...)  ('egi', ...)  ('jighead', ...)  ('minnow', ...)  ('jig', ...)
  ('sabiki', 本数, 見出し, 補足)  ('branch', 本数, 見出し, 補足)  ('tenbin', 見出し, 補足)  ('bag', 見出し, 補足)
"""
import math

F = 'font-family="Hiragino Sans,Hiragino Kaku Gothic ProN,sans-serif"'
LINE = {'pe': ('#e9a400', 'PE'), 'nylon': ('#5aa9de', 'ナイロン'), 'fluoro': ('#2b6cb0', 'フロロ'), 'power': ('#8a6fd1', '')}
AX = 196            # 仕掛けの軸
CARD_X = 214        # 説明カードの左端
CARD_W = 143


def _txt(x, y, s, size=12, w=700, col='#0e294e', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{col}" text-anchor="{anchor}" {F}>{s}</text>'


def _rod(H):
    """先が細くなる竿・ガイド・グリップ・リール。"""
    p0, p1, p2 = (34, H - 64), (60, H * 0.32), (AX - 22, 30)

    def bez(t):
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
        dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        n = math.hypot(dx, dy)
        return x, y, -dy / n, dx / n
    L, R = [], []
    for i in range(41):
        t = i / 40
        x, y, nx, ny = bez(t)
        w = 5.2 - 4.0 * t
        L.append(f'{x + nx * w:.1f},{y + ny * w:.1f}')
        R.append(f'{x - nx * w:.1f},{y - ny * w:.1f}')
    rod = f'<polygon points="{" ".join(L + R[::-1])}" fill="url(#rodg)"/>'
    # 道糸（ガイドを通って竿先へ）
    gl = []
    for t in (0.18, 0.4, 0.58, 0.73, 0.86, 0.96, 1.0):
        x, y, nx, ny = bez(t)
        gl.append((x + nx * 9, y + ny * 9) if t < 1 else (x, y))
    line = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in gl)
    guides = ''
    for t in (0.4, 0.58, 0.73, 0.86, 0.96):
        x, y, nx, ny = bez(t)
        r = 4.2 - 2.4 * t
        guides += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + nx * 9:.1f}" y2="{y + ny * 9:.1f}" stroke="#55606e" stroke-width="1.6"/><circle cx="{x + nx * 9:.1f}" cy="{y + ny * 9:.1f}" r="{r:.1f}" fill="none" stroke="#55606e" stroke-width="1.6"/>'
    gx, gy, _, _ = bez(0.0)
    grip = f'<path d="M{gx - 6},{gy} L{gx - 4},{gy + 34} Q{gx + 1},{gy + 40} {gx + 6},{gy + 34} L{gx + 6},{gy}" fill="#c8a47a" stroke="#9c7a55" stroke-width="1"/>'
    rx, ry, nx, ny = bez(0.12)
    reel = (f'<g transform="translate({rx + nx * 12:.1f},{ry + ny * 12:.1f})">'
            '<rect x="-3" y="-14" width="6" height="12" fill="#6b7480"/>'
            '<ellipse cx="0" cy="6" rx="15" ry="13" fill="#3e4652"/>'
            '<ellipse cx="0" cy="6" rx="9" ry="8" fill="#9aa5b1"/><ellipse cx="0" cy="6" rx="4" ry="3.5" fill="#d7dee6"/>'
            '<path d="M13,6 L26,10" stroke="#3e4652" stroke-width="3" stroke-linecap="round"/><circle cx="27" cy="10" r="4" fill="#c2306f"/>'
            '</g>')
    tip = bez(1.0)
    return rod + grip + reel + guides + f'<path d="{line}" fill="none" stroke="#c9d3de" stroke-width="1.2"/>', (tip[0], tip[1])


def _card(y_comp, title, sub, col, cy):
    """説明カード。y_comp=部品の位置, cy=カード上端。"""
    h = 36 if sub else 24
    mid = cy + h / 2
    s = f'<path d="M{AX + 6},{y_comp:.1f} L{CARD_X - 8},{mid:.1f} L{CARD_X},{mid:.1f}" fill="none" stroke="#b9c6d3" stroke-width="1"/>'
    s += f'<rect x="{CARD_X}" y="{cy:.1f}" width="{CARD_W}" height="{h}" rx="8" fill="#ffffff" stroke="#dbe3ec"/>'
    s += f'<rect x="{CARD_X}" y="{cy:.1f}" width="4" height="{h}" rx="2" fill="{col}"/>'
    s += _txt(CARD_X + 10, cy + 16, title, 12, 800, '#0e294e')
    if sub:
        s += _txt(CARD_X + 10, cy + 30, sub, 11, 600, '#5b6b7c')
    return s, cy + h


def draw(items, rod_spec, reel_spec, seabed=False):
    y = 0
    body, cards = [], []
    comps = []          # (部品のy, 見出し, 補足, 色)
    X = AX
    y = 70              # 水面より少し上から仕掛け
    for it in items:
        k = it[0]
        if k == 'line':
            _, kind, ln, t1, t2 = it
            col = LINE[kind][0]
            body.append(f'<line x1="{X}" y1="{y}" x2="{X}" y2="{y + ln}" stroke="{col}" stroke-width="{2.6 if kind != "power" else 3.4}"/>')
            comps.append((y + ln / 2, t1, t2, col))
            y += ln
        elif k == 'knot':
            body.append(f'<circle cx="{X}" cy="{y}" r="5" fill="#ffffff" stroke="#d9482b" stroke-width="2.4"/>')
            comps.append((y, it[1], None, '#d9482b'))
            y += 14
        elif k == 'swivel':
            body.append(f'<g transform="translate({X},{y})"><circle cy="2" r="3" fill="none" stroke="#6b7480" stroke-width="1.8"/><rect x="-4" y="5" width="8" height="12" rx="3.5" fill="#8d97a3"/><circle cy="20" r="3" fill="none" stroke="#6b7480" stroke-width="1.8"/></g>')
            comps.append((y + 11, it[1], it[2] if len(it) > 2 else None, '#6b7480'))
            y += 26
        elif k == 'float':
            body.append(f'<g transform="translate({X},{y})"><circle cy="3" r="3" fill="#ffd166"/><path d="M0,8 L-13,24 Q0,46 13,24 Z" fill="#f2f4f7" stroke="#8a97a6"/><path d="M0,8 L-13,24 L13,24 Z" fill="#ff7a3d"/></g>')
            comps.append((y + 26, it[1], it[2] if len(it) > 2 else None, '#ff7a3d'))
            y += 50
        elif k in ('sinker', 'egg'):
            if k == 'sinker':
                body.append(f'<g transform="translate({X},{y})"><circle cy="2" r="3" fill="none" stroke="#6b7480" stroke-width="1.8"/><path d="M-3,5 Q-11,26 0,30 Q11,26 3,5 Z" fill="url(#leadg)"/></g>')
                comps.append((y + 18, it[1], it[2] if len(it) > 2 else None, '#5b6470'))
                y += 36
            else:
                body.append(f'<ellipse cx="{X}" cy="{y + 12}" rx="8" ry="12" fill="url(#leadg)"/><line x1="{X}" y1="{y}" x2="{X}" y2="{y + 24}" stroke="#2b6cb0" stroke-width="1.5"/>')
                comps.append((y + 12, it[1], it[2] if len(it) > 2 else None, '#5b6470'))
                y += 28
        elif k == 'hook':
            body.append(f'<path d="M{X},{y} L{X},{y + 16} Q{X},{y + 27} {X - 9},{y + 27} Q{X - 15},{y + 27} {X - 15},{y + 19} L{X - 11},{y + 22}" fill="none" stroke="#3e4652" stroke-width="2.2" stroke-linecap="round"/>')
            comps.append((y + 16, it[1], it[2] if len(it) > 2 else None, '#3e4652'))
            y += 34
        elif k == 'egi':
            body.append(f'''<g transform="translate({X},{y}) rotate(6)">
<path d="M0,0 C11,6 14,30 9,52 L0,62 L-9,52 C-14,30 -11,6 0,0 Z" fill="#ff7aa8" stroke="#c2306f" stroke-width="1"/>
<path d="M-6,14 L6,18 M-7,24 L7,28 M-7,34 L7,38 M-6,44 L6,48" stroke="#ffe0ea" stroke-width="1.6"/>
<circle cx="-3" cy="9" r="2.4" fill="#0e294e"/><path d="M8,22 l9,6 l-8,4 z" fill="#ffb3cb"/>
<path d="M-6,62 q-2,6 -6,8 M0,62 v9 M6,62 q2,6 6,8 M-3,62 q-1,6 -3,9 M3,62 q1,6 3,9" stroke="#3e4652" stroke-width="1.4" fill="none"/></g>''')
            comps.append((y + 32, it[1], it[2] if len(it) > 2 else None, '#c2306f'))
            y += 80
        elif k == 'jighead':
            body.append(f'''<g transform="translate({X},{y})"><circle cy="7" r="7" fill="url(#leadg)"/><circle cx="2" cy="5" r="1.8" fill="#fff"/>
<path d="M0,13 C3,24 -3,32 2,42 C6,50 -2,56 4,62" fill="none" stroke="#ff8fbb" stroke-width="7" stroke-linecap="round"/>
<path d="M0,12 L0,30 Q0,36 -6,36" fill="none" stroke="#3e4652" stroke-width="1.6"/></g>''')
            comps.append((y + 22, it[1], it[2] if len(it) > 2 else None, '#c2306f'))
            y += 70
        elif k == 'minnow':
            body.append(f'''<g transform="translate({X},{y})"><circle cy="2" r="3" fill="none" stroke="#6b7480" stroke-width="1.6"/>
<path d="M0,5 C12,12 13,46 2,64 L0,70 L-2,64 C-13,46 -12,12 0,5 Z" fill="url(#minnowg)" stroke="#2b6cb0" stroke-width="1"/>
<path d="M-5,6 L5,6 L4,0 L-4,0 Z" fill="#cfe5f7" opacity=".8"/><circle cx="-3" cy="14" r="2.6" fill="#0e294e"/>
<path d="M8,30 l7,6 M8,30 l9,0" stroke="#3e4652" stroke-width="1.4"/><path d="M0,70 l-5,7 M0,70 l5,7" stroke="#3e4652" stroke-width="1.4"/></g>''')
            comps.append((y + 34, it[1], it[2] if len(it) > 2 else None, '#2b6cb0'))
            y += 82
        elif k == 'jig':
            body.append(f'''<g transform="translate({X},{y})"><circle cy="2" r="3" fill="none" stroke="#6b7480" stroke-width="1.6"/>
<path d="M-6,8 Q-8,30 -4,60 L0,66 L4,60 Q8,30 6,8 Q0,4 -6,8 Z" fill="url(#jigg)" stroke="#9c7a20" stroke-width="1"/>
<path d="M2,4 q10,4 8,14 q-2,4 -5,1" fill="none" stroke="#3e4652" stroke-width="1.5"/><circle cx="-1" cy="16" r="2" fill="#0e294e"/></g>''')
            comps.append((y + 34, it[1], it[2] if len(it) > 2 else None, '#b07a00'))
            y += 74
        elif k in ('sabiki', 'branch'):
            _, n, t1, t2 = it
            col = '#c2306f' if k == 'sabiki' else '#2b6cb0'
            body.append(f'<line x1="{X}" y1="{y}" x2="{X}" y2="{y + n * 30 + 4}" stroke="#2b6cb0" stroke-width="2"/>')
            for i in range(n):
                yy = y + 10 + i * 30
                side = 1 if i % 2 == 0 else -1
                body.append(f'<path d="M{X},{yy} l{side * 16},7" stroke="#7fb7d9" stroke-width="1.4"/>')
                hx = X + side * 16
                if k == 'sabiki':
                    body.append(f'<rect x="{hx - 3}" y="{yy + 5}" width="6" height="9" rx="2.5" fill="#ff8fbb"/>')
                body.append(f'<path d="M{hx},{yy + 7} L{hx},{yy + 16} Q{hx},{yy + 22} {hx - side * 5},{yy + 22}" fill="none" stroke="#3e4652" stroke-width="1.6"/>')
            comps.append((y + n * 15, t1, t2, col))
            y += n * 30 + 8
        elif k == 'tenbin':
            body.append(f'''<g transform="translate({X},{y})"><path d="M0,0 L0,8 L-26,8" fill="none" stroke="#3e4652" stroke-width="2.4"/>
<path d="M-26,8 L-26,22" stroke="#3e4652" stroke-width="1.6"/><path d="M-29,22 Q-37,42 -26,46 Q-15,42 -23,22 Z" fill="url(#leadg)"/></g>''')
            comps.append((y + 24, it[1], it[2] if len(it) > 2 else None, '#5b6470'))
            y += 22
        elif k == 'bag':
            body.append(f'<g transform="translate({X},{y})"><rect x="-9" y="0" width="18" height="30" rx="6" fill="#d89b4a" stroke="#9c6a24"/><path d="M-9,8 h18 M-9,16 h18 M-9,24 h18" stroke="#9c6a24" stroke-width=".8"/></g>')
            comps.append((y + 15, it[1], it[2] if len(it) > 2 else None, '#b07a00'))
            y += 36
    bottom = y + 14
    # 説明カードを重ならないように並べる
    cy = 26
    for (yc, t1, t2, col) in comps:
        top = max(cy, yc - (18 if t2 else 12))
        s, cy = _card(yc, t1, t2, col, top)
        cards.append(s)
        cy += 6
    H = max(bottom, cy) + 96
    rod, tip = _rod(H - 60)
    water_y = 54
    sea = (f'<rect x="178" y="{water_y}" width="182" height="{H - 60 - water_y}" fill="url(#seag)"/>'
           f'<path d="M178,{water_y} q11,-5 22,0 t22,0 t22,0 t22,0 t22,0 t22,0 t22,0 t22,0" fill="none" stroke="#9cc8e6" stroke-width="2"/>')
    if seabed:
        sea += f'<path d="M178,{H - 74} Q230,{H - 86} 280,{H - 76} T360,{H - 80} L360,{H - 60} L178,{H - 60} Z" fill="#e7d6ad"/>'
    tipline = f'<path d="M{tip[0]:.1f},{tip[1]:.1f} Q{AX - 4},{40} {AX},{70}" fill="none" stroke="{LINE[items[0][1]][0] if items[0][0] == "line" else "#c9d3de"}" stroke-width="2"/>'
    legend = (f'<g transform="translate(12,{H - 52})"><rect width="336" height="44" rx="10" fill="#0e294e"/>'
              + _txt(12, 18, '竿', 11, 700, '#9fb6cf') + _txt(60, 18, rod_spec, 12, 800, '#ffffff')
              + _txt(12, 36, 'リール', 11, 700, '#9fb6cf') + _txt(60, 36, reel_spec, 12, 800, '#ffffff') + '</g>')
    defs = '''<defs>
<linearGradient id="rodg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f3a48"/><stop offset="1" stop-color="#55606e"/></linearGradient>
<linearGradient id="seag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3f1fb"/><stop offset="1" stop-color="#bcdcf1"/></linearGradient>
<linearGradient id="leadg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7d8794"/><stop offset=".5" stop-color="#b6bec8"/><stop offset="1" stop-color="#5f6874"/></linearGradient>
<linearGradient id="minnowg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f8fc6"/><stop offset=".55" stop-color="#d9ecf9"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
<linearGradient id="jigg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e2b23c"/><stop offset=".5" stop-color="#fff0b8"/><stop offset="1" stop-color="#c99520"/></linearGradient>
</defs>'''
    return (f'<div class="rig"><svg viewBox="0 0 360 {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="仕掛けの図">{defs}'
            f'<rect width="360" height="{H}" rx="12" fill="#f7fafc"/>{sea}{rod}{tipline}{"".join(body)}{"".join(cards)}{legend}</svg></div>')
