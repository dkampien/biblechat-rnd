"""Build a manifest (ad ID, page, ad text, CTA, link) for the downloaded FB ad videos."""
import os
import pandas as pd

CSV_PATH = "/Users/dennisk/Downloads/facebook_ads_1781681260992.csv"
OUT_DIR = "/Users/dennisk/Documents/project - bib content gen/_ads-initiative"
VIDEO_COL = "Відео URL"
N = 10

df = pd.read_csv(CSV_PATH, dtype=str)
videos = df[df[VIDEO_COL].notna() & (df[VIDEO_COL].str.strip() != "")].head(N)


def s(r, col):
    """Safely get a stripped string from a row cell (NaN -> '')."""
    v = r.get(col)
    return "" if pd.isna(v) else str(v).strip()


rows = []
for i, (_, r) in enumerate(videos.iterrows(), start=1):
    rows.append({
        "file": f"{i:02d}_{s(r, 'ID')}.mp4",
        "ad_id": s(r, "ID"),
        "status": s(r, "Статус"),
        "start_date": s(r, "Дата початку"),
        "page": s(r, "Назва сторінки"),
        "ad_text": s(r, "Текст реклами"),
        "cta": s(r, "Call to Action"),
        "landing_link": s(r, "Посилання"),
        "link_title": s(r, "Заголовок посилання"),
    })

manifest = pd.DataFrame(rows)
out_path = os.path.join(OUT_DIR, "manifest.csv")
manifest.to_csv(out_path, index=False)
print(f"Wrote {out_path} ({len(manifest)} rows)")
print(manifest[["file", "page", "cta", "ad_text"]].to_string(index=False, max_colwidth=50))
