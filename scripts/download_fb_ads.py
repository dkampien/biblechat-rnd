"""Extract video URLs from a Facebook ads CSV export and download the first N videos."""
import os
import sys
import pandas as pd
import requests

CSV_PATH = "/Users/dennisk/Downloads/facebook_ads_1781681260992.csv"
OUT_DIR = "/Users/dennisk/Hub/focus/client - biblechat/project - bib content gen/_ads-initiative"
VIDEO_COL = "Відео URL"   # column 15: "Video URL"
ID_COL = "ID"
N = 10

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH, dtype=str)

# Keep rows that actually have a video URL
videos = df[df[VIDEO_COL].notna() & (df[VIDEO_COL].str.strip() != "")]
videos = videos.head(N)

print(f"Found {len(videos)} rows with video URLs (downloading up to {N}).")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

for i, (_, row) in enumerate(videos.iterrows(), start=1):
    url = row[VIDEO_COL].strip()
    ad_id = (row.get(ID_COL) or f"video_{i}").strip()
    dest = os.path.join(OUT_DIR, f"{i:02d}_{ad_id}.mp4")
    print(f"[{i}/{len(videos)}] {ad_id} -> {dest}")
    try:
        with requests.get(url, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 16):
                    f.write(chunk)
        size = os.path.getsize(dest)
        print(f"    ok ({size/1_000_000:.2f} MB)")
    except Exception as e:
        print(f"    FAILED: {e}", file=sys.stderr)

print("Done.")
