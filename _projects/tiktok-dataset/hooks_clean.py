import duckdb, re, csv
con = duckdb.connect(); con.execute("SET threads TO 8")
src = open('pipeline.py').read(); ns = {}
exec(src[src.index("PAIN = {"):src.index("COMPETITORS = {")], ns); PAIN = ns['PAIN']
sq = lambda s: s.replace("'", "''")
con.execute("CREATE TABLE f AS SELECT *, saves*1000.0/views AS s1k, shares*1000.0/views AS sh1k FROM read_parquet('out/faith_en.parquet')")
for pid, rx in PAIN.items():
    con.execute(f'ALTER TABLE f ADD COLUMN "p_{pid}" BOOLEAN'); con.execute(f'UPDATE f SET "p_{pid}" = regexp_matches(d, \'{sq(rx)}\')')
SPAM = r"(receive a prophec|prophec|#internetmoney|link in (my )?bio|tiktokshop|tiktok shop|comment .?link|dm me|#ad\b|godofwar|undertale|juice wrld|#edit\b|#fanfic|#anime|#roblox|#minecraft|#fortnite|#skz|#bts|#kpop|slander)"
FIRST = r"\b(i|i'm|im|i’m|my|me|we|our|us)\b"
base = f"""FROM f WHERE views >= 20000 AND create_time < '2026-07-01'
  AND length("desc") BETWEEN 15 AND 200
  AND NOT regexp_matches(d, '{sq(SPAM)}') AND regexp_matches(d, '{sq(FIRST)}')"""
def clean(s): return re.sub(r"\s+"," ",s or "").strip().replace("|","/")
anyp = " OR ".join(f'"p_{p}"' for p in PAIN)
caseexpr = ", ".join(f"CASE WHEN \"p_{p}\" THEN '{p}' END" for p in PAIN)
n = con.execute(f"SELECT count(*) {base} AND ({anyp})").fetchone()[0]
print("clean first-person pain hooks with 20k+ views:", n)
with open('out/hooks_clean.md','w') as fh:
    fh.write("# Clean hook bank: first-person faith+pain captions, ranked by save rate\n\nPartition 00 of tiktok-videos-4b (1 of 27). English, non-ad, views >= 20k, posted before 2026-07-01, caption 15-200 chars, first-person wording, content-farm and off-topic spam removed. s/1k = saves per 1,000 views (faith average 8.7). sh/1k = shares per 1,000 views (faith average 7.2).\n\n")
    fh.write("## Top 120 overall\n\n| s/1k | sh/1k | views | dur | problem | caption |\n|---|---|---|---|---|---|\n")
    for d,v,s,sh,dur,probs in con.execute(f"""SELECT "desc", views, s1k, sh1k, duration, array_to_string(list_filter([{caseexpr}], x -> x IS NOT NULL), ', ') {base} AND ({anyp}) ORDER BY s1k DESC LIMIT 120""").fetchall():
        fh.write(f"| {s:.1f} | {sh:.1f} | {v:,} | {dur}s | {probs} | {clean(d)} |\n")
    fh.write("\n## Per problem (top 15 each, ordered by problem volume)\n\n")
    order = [r[0] for r in csv.reader(open('out/problem_demand.csv'))][1:]
    for pid in order:
        rows = con.execute(f"""SELECT "desc", views, s1k, sh1k, duration {base} AND "p_{pid}" ORDER BY s1k DESC LIMIT 15""").fetchall()
        if len(rows) < 3: continue
        fh.write(f"### {pid}\n\n| s/1k | sh/1k | views | dur | caption |\n|---|---|---|---|---|\n")
        for d,v,s,sh,dur in rows: fh.write(f"| {s:.1f} | {sh:.1f} | {v:,} | {dur}s | {clean(d)} |\n")
        fh.write("\n")
print("\n=== hallow app organic mentions (top by views) ===")
for r in con.execute(r"""SELECT views, s1k, "desc" FROM f WHERE regexp_matches(d, '\bhallow (app|prayer|meditation)|#hallowapp|hallow\.com|the hallow app|download hallow|@hallow') ORDER BY views DESC LIMIT 12""").fetchall(): print(r[0], f"{r[1]:.1f}", clean(r[2])[:160])
print("\n=== bible chat organic mentions ===")
for r in con.execute(r"""SELECT views, s1k, create_time::date, "desc" FROM f WHERE regexp_matches(d, '\bbible ?chat\b|#biblechat') ORDER BY views DESC LIMIT 12""").fetchall(): print(r[0], f"{r[1]:.1f}", r[2], clean(r[3])[:160])
print("\n=== app mentions ===")
for r in con.execute(r"""SELECT regexp_extract(d, '(haven bible app|blessed bible app|blessed app|abide app|pray\.com|glorify app|hallow app|bible ?chat)') b, count(*), sum(views), min(create_time)::date, max(create_time)::date FROM f WHERE regexp_matches(d, '(haven bible app|blessed bible app|blessed app|abide app|pray\.com|glorify app|hallow app|bible ?chat)') GROUP BY b ORDER BY 2 DESC""").fetchall(): print(r)
