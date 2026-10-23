"""ChatGPTで作った魚拓の4匹シート（2×2）を、1匹ずつの透明PNGに切り分ける。

使い方: python3 cut.py   （raw/sheetN.png があるぶんだけ処理する）
出力:   <魚のid>.webp（墨の部分だけ残し、白い背景は透明にする）
"""
from pathlib import Path
from PIL import Image, ImageOps

HERE = Path(__file__).parent
# シートごとの並び（左上・右上・左下・右下）。釣果予報の魚のidと同じ名前にする
SHEETS = {
    1: ["aori", "buri", "kobuRI", "hata"],
    2: ["flat", "aji", "kisu", "tachi"],
    3: ["madai", "suzuki", "chinu", "kamasu"],
    4: ["mebaru", "kawahagi", "maika", "akamutsu"],
}
INK = (28, 39, 51)        # 墨の色（ツールの文字色に合わせた濃紺寄りの黒）
OUT_W = 200               # 出力の横幅（表示は約90pxだが、高精細画面用に2倍強）


def cut_sheet(n, ids):
    src = HERE / "raw" / f"sheet{n}.png"
    if not src.exists():
        return []
    im = Image.open(src).convert("L")
    w, h = im.size
    done = []
    for i, fid in enumerate(ids):
        x0, y0 = (i % 2) * w // 2, (i // 2) * h // 2
        cell = im.crop((x0, y0, x0 + w // 2, y0 + h // 2))
        # 墨の濃さ＝透明度（白は完全に透明、黒ほど不透明）
        alpha = ImageOps.invert(cell).point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.4)))
        box = alpha.point(lambda v: 255 if v > 60 else 0).getbbox()
        if not box:
            continue
        pad = 6
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(cell.width, box[2] + pad), min(cell.height, box[3] + pad))
        a = alpha.crop(box)
        out = Image.new("RGBA", a.size, INK + (0,))
        out.putalpha(a)
        if out.width > OUT_W:
            out = out.resize((OUT_W, round(out.height * OUT_W / out.width)), Image.LANCZOS)
        out.save(HERE / f"{fid}.webp", "WEBP", quality=82, method=6)   # 軽いWebP（透明あり）
        done.append((fid, out.size))
    return done


if __name__ == "__main__":
    for n, ids in SHEETS.items():
        for fid, size in cut_sheet(n, ids):
            print(f"sheet{n}: {fid} {size[0]}x{size[1]}")
