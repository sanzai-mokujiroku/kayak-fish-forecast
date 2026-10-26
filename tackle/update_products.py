#!/usr/bin/env python3
"""タックル計画の「実際の竿・リールの例」を、各社公式サイトの仕様表から自動で更新する。

- tackle/products.json の各品について、公式ページ(url)を開き、仕様表から型番(model)の行を探す。
- 見つかれば 長さ・対応する重さ・PE・価格 を書き直し、checked(確認日)を今日にする。
- 見つからなければ found=false にする（ツール側では表示しない）。型番の廃止・変更のサイン。
- GitHub Actions（.github/workflows/update-products.yml）が毎週月曜に実行し、変わっていれば commit する。
標準ライブラリだけで動く。手元では  python3 tackle/update_products.py  で試せる。
"""
import json, re, sys, unicodedata, urllib.request, datetime, pathlib
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).parent
DATA = HERE / "products.json"

def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(r"\s+", " ", s).strip()

class Tables(HTMLParser):
    """ページ内の <table> を [[セル文字列,...],...] の並びとして集める"""
    def __init__(self):
        super().__init__(); self.tables=[]; self.stack=[]; self.cell=None
    def handle_starttag(self, tag, a):
        if tag == "table": self.stack.append([])
        elif tag == "tr" and self.stack: self.stack[-1].append([])
        elif tag in ("td", "th") and self.stack: self.cell = []
        elif tag == "br" and self.cell is not None: self.cell.append(" ")
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None and self.stack and self.stack[-1]:
            self.stack[-1][-1].append(norm("".join(self.cell))); self.cell = None
        elif tag == "table" and self.stack:
            self.tables.append(self.stack.pop())
    def handle_data(self, d):
        if self.cell is not None: self.cell.append(d)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (tackle-planner updater; +https://sanzai-mokujiroku.github.io/)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

# 仕様表の見出し → 取り出す項目（上から順に最初に当たったもの）
COLS = {
    "len":   [r"全長\(ft", r"全長\(m\)", r"全長"],
    "load":  [r"エギサイズ", r"エギウェイト", r"対応エギ", r"ルアーウェイト", r"ルアー重量", r"ジグウェイト", r"バーチカルウェイト"],
    "pe":    [r"適合ライン ?PE", r"糸巻量PE", r"標準巻糸量PE"],
    "price": [r"本体価格"],
}

def pick(header, row, pats):
    for p in pats:
        for i, h in enumerate(header):
            if re.search(p, h) and i < len(row) and row[i] not in ("", "-"):
                return row[i], h
    return None, None

def model_key(s):
    return re.sub(r"[^0-9A-Z+]", "", norm(s).upper())

def find_row(tables, model):
    want = model_key(model)
    for t in tables:
        if not t: continue
        header = t[0]
        if not any(re.search("全長|ギア比|自重", h) for h in header): continue
        for row in t[1:]:
            if not row: continue
            k = model_key(row[0])
            # 例: シマノ「S86ML」と一致、ダイワ「EMERALDAS X 86ML・J」は末尾に型番を含む
            if k == want or k.endswith(want) or k.endswith(want + "J") or k.endswith(want + "E") or k.endswith(want + "R"):
                return header, row
    return None, None

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()   # 日本時間
    cache, changed, report = {}, False, []
    for it in data["items"]:
        url = it["url"]
        if not it.get("auto", True):
            continue   # シマノは自動取得を断っている（403）ので、手で確かめた値のまま（manual_checked を見る）
        try:
            if url not in cache:
                t = Tables(); t.feed(fetch(url)); cache[url] = t
        except Exception as e:
            report.append(f"取得失敗（前の値のまま）: {it['name']} {e}"); continue
        header, row = find_row(cache[url].tables, it["model"])
        if not row:
            if it.get("found", True):
                it["found"] = False; changed = True
            report.append(f"見つからない（非表示にした）: {it['name']} {it['model']}"); continue
        new = {}
        for k, pats in COLS.items():
            v, h = pick(header, row, pats)
            if v is None: continue
            if k == "len" and "(m)" in h.replace("（", "(").replace("）", ")"): v = v + "m"
            if k == "pe" and re.search("巻", h): v = "PE" + v.split(",")[0].split("_")[0].replace(" ", "") + "m巻ける"
            if k == "load":
                unit = "g" if re.search(r"[（(]g[)）]|ウェイト|重量", h) else "号"
                if not re.search("[号g]", v): v = v + unit
                if "鯛ラバ" in h or "バーチカル" in h: v = "タイラバ " + v
            if k == "price":
                v = re.sub(r"[^0-9]", "", v)
                v = f"{int(v):,}円" if v else None
            if v: new[k] = v.replace("～", "-").replace("~", "-")
        for k, v in new.items():
            if it.get(k) != v:
                report.append(f"変更: {it['name']} {k}: {it.get(k)} → {v}"); it[k] = v; changed = True
        if not it.get("found", True): it["found"] = True; changed = True
    ok = sum(1 for it in data["items"] if it.get("auto", True)) - sum(1 for r in report if r.startswith("取得失敗"))
    if ok > 0 and data.get("checked") != today:
        data["checked"] = today; changed = True   # 自動で確かめた日（ダイワ分）
    if changed:
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\n".join(report) or "変更なし")
    print("CHANGED" if changed else "NOCHANGE")

if __name__ == "__main__":
    sys.exit(main())
