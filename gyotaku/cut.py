"""ChatGPTで作ったカラー魚拓の4匹シート（2×2）を、1匹ずつの透明WebPに切り分ける。

使い方: python3 cut.py   （raw/colorN.png があるぶんだけ処理する）
出力:   <魚のid>.webp（白い紙の部分は透明にし、魚の色はそのまま残す）
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
# シートごとの並び（左上・右上・左下・右下）。釣果予報の魚のidと同じ名前にする
SHEETS = {
    1: ["aori", "buri", "kobuRI", "hata"],
    2: ["flat", "aji", "kisu", "tachi"],
    3: ["madai", "suzuki", "chinu", "kamasu"],
    4: ["mebaru", "kawahagi", "maika", "akamutsu"],
}
OUT_W = 200   # 出力の横幅（表示は約90pxだが、高精細画面用に2倍強）


def unpaper(cell):
    """白い紙に近い所ほど透明にし、色は紙の白さを取り除いた本来の色に戻す。"""
    out = []
    for r, g, b in cell.getdata():
        a = max(0, min(255, int((255 - min(r, g, b) - 12) * 1.6)))
        if a == 0:
            out.append((0, 0, 0, 0))
            continue
        f = a / 255
        out.append(tuple(max(0, min(255, int((v - (1 - f) * 255) / f))) for v in (r, g, b)) + (a,))
    im = Image.new("RGBA", cell.size)
    im.putdata(out)
    return im


def cut_sheet(n, ids):
    src = HERE / "raw" / f"color{n}.png"
    if not src.exists():
        return []
    sheet = Image.open(src).convert("RGB")
    w, h = sheet.size
    done = []
    for i, fid in enumerate(ids):
        x0, y0 = (i % 2) * w // 2, (i // 2) * h // 2
        im = unpaper(sheet.crop((x0, y0, x0 + w // 2, y0 + h // 2)))
        box = im.getchannel("A").point(lambda v: 255 if v > 60 else 0).getbbox()
        if not box:
            continue
        pad = 6
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
        im = im.crop(box)
        if im.width > OUT_W:
            im = im.resize((OUT_W, round(im.height * OUT_W / im.width)), Image.LANCZOS)
        im.save(HERE / f"{fid}.webp", "WEBP", quality=82, method=6)
        done.append((fid, im.size))
    return done


if __name__ == "__main__":
    for n, ids in SHEETS.items():
        for fid, size in cut_sheet(n, ids):
            print(f"color{n}: {fid} {size[0]}x{size[1]}")
