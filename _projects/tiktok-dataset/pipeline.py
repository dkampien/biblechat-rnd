"""
TikTok faith-vertical extraction for BibleChat creative (Options A + C).

Input : one partition of kuben-developer/tiktok-videos-4b (parquet, ~166M rows)
Output: _projects/tiktok-dataset/out/*  (CSV + markdown)

Run:   python3 pipeline.py data/videos-00.parquet
Test:  python3 pipeline.py <parquet path or URL> --limit 300000
"""
import sys, os, re, time, argparse
import duckdb

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("--limit", type=int, default=0)
ap.add_argument("--skip-extract", action="store_true", help="reuse out/faith_en.parquet")
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
FAITH_PQ = os.path.join(OUT, "faith_en.parquet")
BASE_CSV = os.path.join(OUT, "baseline_en.csv")

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute("SET threads TO 8;")

# ---------------------------------------------------------------- filters
# strong faith words need a word boundary; hashtag stems match without one
FAITH_RE = (
    r"(\b(jesus|christ|bible|scripture|scriptures|gospel|psalm|psalms|devotional|devotion|"
    r"christian|christians|holy spirit|holyspirit|prayer|prayers|praying|prayed|pray|church|"
    r"worship|sermon|testimony|amen|god|lord|faith|blessed|bible verse|verse of the day)\b"
    r"|#(christian|jesus|bible|god|pray|faith|church|scripture|gospel|holyspirit|bibleverse|"
    r"catholic|worship|devotional))"
)
SECULAR_RE = r"(oh my god|omg|god damn|goddamn|god tier|god mode|godzilla|god of war|thank god it|lord of the rings|faith hill|faith evans|church's chicken|churchill)"

# pain map: problem id -> regex on lower(desc). Grouped by the 60-problem map.
PAIN = {
    "marriage-in-trouble":      r"\b(my marriage|our marriage|marriage is (falling|struggling|hard|failing)|save (my|our) marriage|fighting with my (husband|wife)|husband and i (fight|argue)|marriage (problems|trouble|struggles))\b",
    "going-through-divorce":    r"\b(divorce|divorced|divorcing|separated from my|separation|ex husband|ex wife|ex-husband|ex-wife)\b",
    "spouse-infidelity":        r"\b(cheated on me|he cheated|she cheated|cheating (husband|wife|spouse)|infidelity|affair|unfaithful|betrayed me)\b",
    "lonely-in-marriage":       r"\b(lonely in (my|a) marriage|alone in (my|a) marriage|married but (alone|lonely)|roommates|emotionally unavailable husband)\b",
    "keep-marriage-strong":     r"\b(godly marriage|christian marriage|marriage goals|strong marriage|pray for your (husband|wife|marriage)|praying for my (husband|wife)|wife prayer|husband prayer)\b",
    "relationship-struggles":   r"\b(my relationship|our relationship|relationship (problems|struggles|advice)|toxic relationship|situationship|my boyfriend|my girlfriend)\b",
    "breakup-heartbreak":       r"\b(breakup|break up|broke up|heartbreak|heartbroken|he left me|she left me|left me for|getting over him|getting over her|moving on from)\b",
    "single-and-searching":     r"\b(single (and|but) (waiting|christian|praying)|waiting (on|for) my (husband|wife)|future husband|future wife|godly (man|woman|husband|wife)|still single|will i ever (find|get))\b",
    "widowed":                  r"\b(widow|widowed|widower|my late husband|my late wife|lost my husband|lost my wife|husband passed|wife passed|husband died|wife died)\b",
    "lost-a-child":             r"\b(lost my (son|daughter|baby|child)|my (son|daughter|child) (died|passed)|child loss|infant loss|angel baby|stillborn|stillbirth|buried my (son|daughter|child))\b",
    "parent-died":              r"\b(lost my (mom|mum|mother|dad|father)|my (mom|mum|mother|dad|father) (died|passed)|miss my (mom|mum|dad)|rip (mom|dad)|without my (mom|dad))\b",
    "family-member-died":       r"\b(lost my (brother|sister|grandma|grandmother|grandpa|grandfather|nana|papa|uncle|aunt|cousin|best friend)|my (brother|sister|grandma|grandpa|nana|papa) (died|passed))\b",
    "grieving-a-loss":          r"\b(grief|grieving|grieve|mourning|bereaved|bereavement|loss of a loved one|heaven gained|gained an angel|passed away)\b",
    "fear-of-death":            r"\b(afraid of dying|fear of death|scared of death|scared to die|thanatophobia|what happens when (we|you) die)\b",
    "own-illness":              r"\b(my diagnosis|diagnosed with|chronic illness|chronic pain|cancer (journey|battle|fight)|chemo|chemotherapy|my cancer|autoimmune|fibromyalgia|lupus|ms warrior|sick and tired of being sick|my body is)\b",
    "health-anxiety":           r"\b(health anxiety|hypochondria|scared (something is|it's) (wrong|serious)|waiting (on|for) (test|biopsy|scan) results|fear of (cancer|dying young))\b",
    "sick-loved-one":           r"\b(my (mom|mum|dad|husband|wife|sister|brother|grandma|grandpa) (has|had|is battling|is fighting) (cancer|dementia|alzheimer)|(mom|dad|husband|wife)('s| is) (in the hospital|in icu|in hospice)|hospice|pray for my (mom|dad|husband|wife|sister|brother))\b",
    "child-health-struggles":   r"\b(my (son|daughter|baby|child|kid) (has|is battling|was diagnosed|is in the (hospital|nicu|icu))|nicu|pediatric cancer|childhood cancer|special needs (mom|mama|parent)|autism mom)\b",
    "caregiver-burnout":        r"\b(caregiver|caregiving|caring for my (mom|dad|mother|father|husband|wife|parents)|dementia (mom|dad|caregiver)|sandwich generation|compassion fatigue)\b",
    "drowning-in-bills":        r"\b(drowning in (debt|bills)|can't pay (my|the) (bills|rent)|behind on (rent|bills)|debt free journey|paying off debt|in debt|eviction|overdue)\b",
    "struggling-financially":   r"\b(financial (stress|struggle|struggles|breakthrough|freedom)|money (stress|problems|struggles|is tight)|broke and|struggling financially|living paycheck|paycheck to paycheck|can't afford)\b",
    "job-search-struggles":     r"\b(job (search|hunting|hunt|rejection|rejections)|unemployed|laid off|lost my job|can't find (a job|work)|no callbacks|got rejected again)\b",
    "work-stress":              r"\b(work stress|toxic (workplace|job|boss)|burnt out at work|burnout at work|hate my job|my boss|stressed at work|overworked)\b",
    "overwhelmed-exhausted":    r"\b(overwhelmed|exhausted|burnout|burnt out|burned out|running on empty|so tired of everything|mentally exhausted|emotionally drained|drained)\b",
    "carrying-it-alone":        r"\b(carrying it alone|no one asks (how|if) i|nobody asks (how|if) i|strong for everyone|everyone's rock|the strong friend|bottling it up|nobody checks on)\b",
    "feels-alone":              r"\b(i feel (so |completely )?alone|feeling (so |completely )?alone|lonely|loneliness|no one (cares|would notice)|nobody (cares|would notice)|all alone|i have no one|no friends)\b",
    "depression":               r"\b(depression|depressed|dark place|darkest|don't want to be here|suicidal|i'm not okay|im not okay|mental health (struggle|battle|journey)|struggling mentally)\b",
    "future-dread":             r"\b(anxiety|anxious|worried about (the|my) future|overthinking|panic attack|panic attacks|can't stop worrying|worry|what if)\b",
    "not-good-enough":          r"\b(not (good )?enough|never enough|worthless|self[- ]worth|self[- ]doubt|insecure|insecurity|imposter|compare myself|comparing myself|feel like a failure|i'm a failure)\b",
    "past-hurts":               r"\b(trauma|childhood trauma|healing journey|past hurts|let go of the past|forgive (him|her|them|myself)|forgiveness|inner child|what (he|she|they) did to me)\b",
    "abusive-relationship":     r"\b(abusive|abuse|narcissist|narcissistic|gaslighting|domestic violence|toxic (marriage|husband|wife|ex)|manipulation|controlling (husband|wife|partner))\b",
    "anger-battles":            r"\b(anger issues|my anger|my temper|lose my temper|losing my temper|rage|angry all the time|snapping at)\b",
    "family-conflict":          r"\b(family (drama|conflict|issues|problems|feud)|toxic family|estranged|my (mom|mother|dad|father|sister|brother) (hates|doesn't talk to) me|family fell apart|dysfunctional family)\b",
    "estranged-adult-child":    r"\b(estranged (son|daughter|child|children)|my (son|daughter) (won't|doesn't) (talk|speak) to me|cut me off|no contact with my (son|daughter)|grandchildren i can't see|alienated)\b",
    "single-parent":            r"\b(single (mom|mum|mother|dad|father|parent)|solo (mom|parent)|raising (my )?(kids|children|son|daughter) (alone|on my own)|co-?parenting|custody)\b",
    "parenting-overwhelm":      r"\b(mom guilt|mum guilt|bad mom|bad mother|losing my patience with my kids|yelled at my kids|postpartum|ppd|touched out|mom burnout|parenting is hard|motherhood is hard)\b",
    "children-straying-from-god":r"\b(prodigal (son|daughter|child|children)|my (kids|children|son|daughter) (don't|doesn't|won't) (believe|go to church)|walked away from (god|the faith|church)|pray for (my|your) (children|kids) (to|who))\b",
    "mother-of-an-addict":      r"\b(my (son|daughter|child) is (an addict|addicted|using|in rehab)|(son|daughter)('s| is) addiction|addict (son|daughter)|loving an addict|mom of an addict|parent of an addict)\b",
    "alcohol-addiction":        r"\b(sober|sobriety|alcoholic|alcoholism|quit drinking|stop drinking|drinking problem|aa meeting|days sober|years sober|recovery journey)\b",
    "drug-addiction":           r"\b(addiction|addicted|relapse|relapsed|rehab|recovering addict|clean and sober|drug (addict|addiction|abuse)|fentanyl|meth|opioid)\b",
    "my-quiet-addiction":       r"\b(lust|porn|pornography|purity|sexual sin|secret sin|hidden sin|struggle nobody knows|no one knows i)\b",
    "temptation-battles":       r"\b(temptation|tempted|same sin|keep sinning|fall into sin|struggling with sin|the flesh|battle with sin|conviction)\b",
    "no-discipline":            r"\b(discipline|disciplined|procrastination|procrastinating|no motivation|lazy|consistency|consistent|can't stay consistent|bad habits|self[- ]control)\b",
    "no-time-for-god":          r"\b(no time (for god|to pray|to read)|too busy (for god|to pray)|quiet time|neglecting (god|my faith)|make time for god|phone instead of (praying|bible)|skipping (church|prayer))\b",
    "feels-distant-from-god":   r"\b(god feels (far|distant|silent)|far from god|distant from god|can't feel god|god is silent|where is god|feel disconnected from god|why isn't god)\b",
    "doubting-faith":           r"\b(doubt|doubting|doubts|deconstruct|deconstruction|losing my faith|lost my faith|is god real|questioning (god|my faith)|scared of hell|going to hell|am i saved)\b",
    "prodigal-return":          r"\b(backslid|backslider|backsliding|came back to (god|christ|church|jesus)|coming back to (god|christ|church|jesus)|rededicat|return(ed|ing) to (god|church|faith)|been away from (god|church)|starting over with god)\b",
    "new-believer":             r"\b(new believer|new christian|new to (faith|christianity|the bible)|just got saved|gave my life to (christ|jesus|god)|recently saved|baby christian|where do i start (in|with) the bible|how to (start|read the) bible)\b",
    "fellowship-starved":       r"\b(church hurt|hurt by the church|no church (family|community)|looking for a church|find a church|left the church|church trauma|no christian friends)\b",
    "feels-lost-no-direction":  r"\b(feel(ing)? lost|i'm lost|no direction|no purpose|what is my purpose|god's plan for my life|don't know what to do with my life|lost sense of self|who am i)\b",
    "life-falling-apart":       r"\b(everything is falling apart|falling apart|life is falling apart|hitting rock bottom|rock bottom|can't catch a break|when it rains it pours|worst year|hardest season|going through it|hard times|hard season)\b",
    "miscarriage-infertility":  r"\b(miscarriage|miscarried|infertility|infertile|ttc|trying to conceive|ivf|rainbow baby|pregnancy loss|chemical pregnancy|waiting for a baby)\b",
    "school-pressure":          r"\b(exam|exams|finals|nclex|bar exam|board exam|failed my|failing (school|class)|college stress|student stress|studying for)\b",
    "social-fear":              r"\b(social anxiety|socially anxious|scared of people|afraid of people|introvert at church|anxious in crowds)\b",
    "unbelieving-family":       r"\b(unbelieving (husband|wife|spouse|family|parents)|unequally yoked|only christian in my (family|house|home)|husband (isn't|is not|doesn't) (a )?(believer|saved|christian)|wife (isn't|is not|doesn't) (a )?(believer|saved|christian)|saved wife unsaved husband)\b",
    "just-relocated":           r"\b(just moved|moved to a new (city|state|country)|new city|relocated|starting over in a new|far from home|no friends here)\b",
    "immigrant-far-from-home":  r"\b(immigrant|immigration|far from (my )?family|miss my family back home|back home|ofw|diaspora|living abroad)\b",
    "loved-one-in-prison":      r"\b(prison (wife|mom|wifey)|incarcerated|inmate|behind bars|locked up|in prison|in jail|prison ministry)\b",
    "after-prison":             r"\b(ex[- ]con|felon|after prison|out of prison|released from prison|second chance|got out of (prison|jail)|reentry)\b",
}

COMPETITORS = {
    "hallow": r"\bhallow\b",
    "pray.com": r"\bpray\.com\b|#praycom\b",
    "glorify": r"\bglorify app\b|#glorifyapp\b|\bglorify\b",
    "youversion": r"\byouversion\b|\bbible app\b",
    "bible chat": r"\bbible ?chat\b|#biblechat\b",
    "abide": r"\babide (app|bible|meditation)\b|#abideapp\b",
}

def sq(rx):
    return rx.replace("'", "''")

def q(sql, **kw):
    t = time.time()
    r = con.execute(sql).fetchall()
    return r

# ---------------------------------------------------------------- 1. extract
if not args.skip_extract:
    lim = f"LIMIT {args.limit}" if args.limit else ""
    src = f"(SELECT * FROM read_parquet('{args.src}') {lim})"
    print("extracting faith_en ...", flush=True); t = time.time()
    con.execute(f"""
        COPY (
          SELECT content_id, create_time, "desc", duration, is_video, music_id, music_title,
                 views, likes, comments, shares, saves, country, language,
                 lower("desc") AS d
          FROM {src}
          WHERE language = 'en' AND is_ad = 0 AND views > 0
            AND regexp_matches(lower("desc"), '{sq(FAITH_RE)}')
            AND NOT regexp_matches(lower("desc"), '{sq(SECULAR_RE)}')
        ) TO '{FAITH_PQ}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
    print(f"  done {time.time()-t:.0f}s", flush=True)

    print("baseline (all english, non-ad) ...", flush=True); t = time.time()
    con.execute(f"""
        COPY (
          SELECT
            CASE WHEN duration<=7 THEN '01_0-7s' WHEN duration<=15 THEN '02_8-15s' WHEN duration<=30 THEN '03_16-30s'
                 WHEN duration<=60 THEN '04_31-60s' WHEN duration<=120 THEN '05_61-120s' ELSE '06_120s+' END AS duration_bucket,
            is_video,
            count(*) AS posts,
            median(views) AS median_views,
            sum(saves)*1000.0/sum(views) AS saves_per_1k,
            sum(shares)*1000.0/sum(views) AS shares_per_1k,
            sum(likes)*1000.0/sum(views) AS likes_per_1k,
            sum(comments)*1000.0/sum(views) AS comments_per_1k
          FROM {src}
          WHERE language='en' AND is_ad=0 AND views >= 1000 AND create_time < '2026-07-01'
          GROUP BY 1,2 ORDER BY 1,2
        ) TO '{BASE_CSV}' (HEADER)
    """)
    print(f"  done {time.time()-t:.0f}s", flush=True)

# ---------------------------------------------------------------- 2. faith table
con.execute(f"CREATE OR REPLACE TABLE f AS SELECT *, saves*1000.0/views AS s1k, shares*1000.0/views AS sh1k, likes*1000.0/views AS l1k FROM read_parquet('{FAITH_PQ}')")
n = q("SELECT count(*), sum(views), count(*) FILTER (WHERE views>=1000) FROM f")[0]
print(f"faith_en rows: {n[0]:,}  total views: {n[1]:,}  rows>=1k views: {n[2]:,}")
if n[0] == 0:
    print("no rows; stop"); sys.exit(0)

# 2a. tag problems (one boolean column per problem)
for pid, rx in PAIN.items():
    con.execute(f"ALTER TABLE f ADD COLUMN IF NOT EXISTS \"p_{pid}\" BOOLEAN")
    con.execute(f"UPDATE f SET \"p_{pid}\" = regexp_matches(d, '{rx.replace(chr(39), chr(39)*2)}')")

# ---------------------------------------------------------------- 3. Option B-ish: demand table per problem
rows = []
for pid in PAIN:
    r = q(f"""
      SELECT count(*), count(*) FILTER (WHERE views>=5000), sum(views),
             median(views) FILTER (WHERE views>=1000),
             sum(saves)*1000.0/nullif(sum(views),0), sum(shares)*1000.0/nullif(sum(views),0), sum(likes)*1000.0/nullif(sum(views),0),
             count(*) FILTER (WHERE views>=5000 AND country='US')
      FROM f WHERE "p_{pid}" AND create_time < '2026-07-01'
    """)[0]
    rows.append((pid,)+tuple(r))
import csv
with open(os.path.join(OUT,"problem_demand.csv"),"w",newline="") as fh:
    w = csv.writer(fh); w.writerow(["problem","posts","posts_5k_views","total_views","median_views_1k+","saves_per_1k","shares_per_1k","likes_per_1k","us_posts_5k_views"])
    for r in sorted(rows, key=lambda x:-(x[3] or 0)): w.writerow([r[0]]+[round(x,2) if isinstance(x,float) else x for x in r[1:]])

faith_all = q("SELECT sum(saves)*1000.0/sum(views), sum(shares)*1000.0/sum(views), sum(likes)*1000.0/sum(views), median(views) FILTER (WHERE views>=1000) FROM f WHERE create_time < '2026-07-01'")[0]
with open(os.path.join(OUT,"faith_overall.csv"),"w") as fh:
    fh.write("saves_per_1k,shares_per_1k,likes_per_1k,median_views_1k+\n"); fh.write(",".join(f"{x:.2f}" for x in faith_all)+"\n")

# ---------------------------------------------------------------- 4. Option A: hooks per problem
def clean(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:220]

with open(os.path.join(OUT,"hooks_by_problem.md"),"w") as fh:
    fh.write("# TikTok faith posts, top captions by save rate, per problem\n\nSource: tiktok-videos-4b partition 00, English, non-ad, faith filter, views >= 20k, created before 2026-07-01. `s/1k` = saves per 1,000 views, `sh/1k` = shares per 1,000 views.\n\n")
    for pid,_ in sorted(((r[0], r[3] or 0) for r in rows), key=lambda x:-x[1]):
        top = q(f"""
          SELECT "desc", views, s1k, sh1k, country, duration, create_time::date
          FROM f WHERE "p_{pid}" AND views >= 20000 AND create_time < '2026-07-01'
          ORDER BY s1k DESC LIMIT 25
        """)
        if not top: continue
        fh.write(f"## {pid}  ({len(top)} shown)\n\n| s/1k | sh/1k | views | cc | dur | caption |\n|---|---|---|---|---|---|\n")
        for d,v,s,sh,cc,dur,dt in top:
            fh.write(f"| {s:.1f} | {sh:.1f} | {v:,} | {cc} | {dur}s | {clean(d).replace('|','/')} |\n")
        fh.write("\n")

# top pain hooks overall (any problem), by save rate, strong reach
with open(os.path.join(OUT,"hooks_overall_top200.md"),"w") as fh:
    fh.write("# Top 200 faith+pain captions by save rate (views >= 50k)\n\n| s/1k | sh/1k | views | cc | dur | problems | caption |\n|---|---|---|---|---|---|---|\n")
    anyp = " OR ".join(f'"p_{p}"' for p in PAIN)
    caseexpr = ", ".join(f"CASE WHEN \"p_{p}\" THEN '{p}' END" for p in PAIN)
    for d,v,s,sh,cc,dur,probs in q(f"""
        SELECT "desc", views, s1k, sh1k, country, duration,
               array_to_string(list_filter([{caseexpr}], x -> x IS NOT NULL), ', ')
        FROM f WHERE ({anyp}) AND views >= 50000 AND create_time < '2026-07-01'
        ORDER BY s1k DESC LIMIT 200"""):
        fh.write(f"| {s:.1f} | {sh:.1f} | {v:,} | {cc} | {dur}s | {probs} | {clean(d).replace('|','/')} |\n")

# ---------------------------------------------------------------- 5. Option C: format brief
con.execute(f"""
  COPY (
    SELECT CASE WHEN duration<=7 THEN '01_0-7s' WHEN duration<=15 THEN '02_8-15s' WHEN duration<=30 THEN '03_16-30s'
                WHEN duration<=60 THEN '04_31-60s' WHEN duration<=120 THEN '05_61-120s' ELSE '06_120s+' END AS duration_bucket,
           is_video, count(*) AS posts, median(views) AS median_views,
           quantile_cont(views, 0.9) AS p90_views,
           sum(saves)*1000.0/sum(views) AS saves_per_1k, sum(shares)*1000.0/sum(views) AS shares_per_1k,
           sum(likes)*1000.0/sum(views) AS likes_per_1k, sum(comments)*1000.0/sum(views) AS comments_per_1k
    FROM f WHERE views >= 1000 AND create_time < '2026-07-01'
    GROUP BY 1,2 ORDER BY 1,2
  ) TO '{os.path.join(OUT,"format_faith.csv")}' (HEADER)
""")
# same, pain-tagged only
anyp = " OR ".join(f'"p_{p}"' for p in PAIN)
con.execute(f"""
  COPY (
    SELECT CASE WHEN duration<=7 THEN '01_0-7s' WHEN duration<=15 THEN '02_8-15s' WHEN duration<=30 THEN '03_16-30s'
                WHEN duration<=60 THEN '04_31-60s' WHEN duration<=120 THEN '05_61-120s' ELSE '06_120s+' END AS duration_bucket,
           is_video, count(*) AS posts, median(views) AS median_views,
           sum(saves)*1000.0/sum(views) AS saves_per_1k, sum(shares)*1000.0/sum(views) AS shares_per_1k,
           sum(likes)*1000.0/sum(views) AS likes_per_1k
    FROM f WHERE ({anyp}) AND views >= 1000 AND create_time < '2026-07-01'
    GROUP BY 1,2 ORDER BY 1,2
  ) TO '{os.path.join(OUT,"format_faith_pain.csv")}' (HEADER)
""")
# US-only faith, by duration
con.execute(f"""
  COPY (
    SELECT CASE WHEN duration<=7 THEN '01_0-7s' WHEN duration<=15 THEN '02_8-15s' WHEN duration<=30 THEN '03_16-30s'
                WHEN duration<=60 THEN '04_31-60s' WHEN duration<=120 THEN '05_61-120s' ELSE '06_120s+' END AS duration_bucket,
           is_video, count(*) AS posts, median(views) AS median_views,
           sum(saves)*1000.0/sum(views) AS saves_per_1k, sum(shares)*1000.0/sum(views) AS shares_per_1k
    FROM f WHERE country='US' AND views >= 1000 AND create_time < '2026-07-01'
    GROUP BY 1,2 ORDER BY 1,2
  ) TO '{os.path.join(OUT,"format_faith_us.csv")}' (HEADER)
""")

# sounds: reusable (not "original sound - x") under faith posts, ranked by posts and by save-weighted reach
con.execute(f"""
  COPY (
    SELECT music_title, music_id, count(*) AS posts, sum(views) AS total_views,
           sum(saves)*1000.0/sum(views) AS saves_per_1k, sum(shares)*1000.0/sum(views) AS shares_per_1k,
           min(create_time)::date AS first_seen, max(create_time)::date AS last_seen,
           count(*) FILTER (WHERE {anyp}) AS pain_posts
    FROM f WHERE views >= 1000 AND music_title IS NOT NULL
      AND NOT starts_with(lower(music_title), 'original sound') AND NOT starts_with(lower(music_title), 'original audio')
      AND NOT starts_with(lower(music_title), 'sonido original') AND NOT starts_with(lower(music_title), 'som original')
    GROUP BY 1,2 HAVING count(*) >= 30
    ORDER BY total_views DESC LIMIT 300
  ) TO '{os.path.join(OUT,"sounds_top.csv")}' (HEADER)
""")
con.execute(f"""
  COPY (
    SELECT music_title, music_id, count(*) AS posts, sum(views) AS total_views,
           sum(saves)*1000.0/sum(views) AS saves_per_1k, sum(shares)*1000.0/sum(views) AS shares_per_1k,
           min(create_time)::date AS first_seen, max(create_time)::date AS last_seen
    FROM f WHERE views >= 1000 AND music_title IS NOT NULL AND ({anyp})
      AND NOT starts_with(lower(music_title), 'original sound') AND NOT starts_with(lower(music_title), 'original audio')
    GROUP BY 1,2 HAVING count(*) >= 15
    ORDER BY total_views DESC LIMIT 200
  ) TO '{os.path.join(OUT,"sounds_pain_posts.csv")}' (HEADER)
""")
# sound share: what fraction of high-reach faith posts use a reusable sound vs original
snd = q(f"""SELECT
  count(*) FILTER (WHERE starts_with(lower(music_title),'original')) * 1.0 / count(*),
  sum(saves) FILTER (WHERE starts_with(lower(music_title),'original')) * 1000.0 / sum(views) FILTER (WHERE starts_with(lower(music_title),'original')),
  sum(saves) FILTER (WHERE NOT starts_with(lower(music_title),'original')) * 1000.0 / sum(views) FILTER (WHERE NOT starts_with(lower(music_title),'original'))
  FROM f WHERE views >= 20000 AND music_title IS NOT NULL""")[0]
with open(os.path.join(OUT,"sound_original_vs_reused.csv"),"w") as fh:
    fh.write("share_original_sound_posts_20k+,saves_per_1k_original,saves_per_1k_reused\n"); fh.write(",".join(f"{x:.3f}" for x in snd)+"\n")

# country and monthly volume (context)
con.execute(f"COPY (SELECT country, count(*) AS posts, sum(views) AS views, sum(saves)*1000.0/sum(views) AS saves_per_1k FROM f WHERE views>=1000 GROUP BY 1 ORDER BY 2 DESC LIMIT 40) TO '{os.path.join(OUT,'faith_by_country.csv')}' (HEADER)")
con.execute(f"COPY (SELECT date_trunc('month', create_time)::date AS month, count(*) AS posts, count(*) FILTER (WHERE {anyp}) AS pain_posts FROM f GROUP BY 1 ORDER BY 1) TO '{os.path.join(OUT,'faith_by_month.csv')}' (HEADER)")

# ---------------------------------------------------------------- 6. competitors (all english incl. ads, from source)
if not args.skip_extract:
    lim = f"LIMIT {args.limit}" if args.limit else ""
    src = f"(SELECT * FROM read_parquet('{args.src}') {lim})"
    ce = ", ".join(f"CASE WHEN regexp_matches(lower(\"desc\"), '{rx}') THEN '{k}' END" for k,rx in COMPETITORS.items())
    con.execute(f"""
      COPY (
        SELECT array_to_string(list_filter([{ce}], x -> x IS NOT NULL), ', ') AS brand, is_ad, create_time::date AS dt, country,
               views, likes, saves, shares, duration, is_video, music_title, "desc"
        FROM {src}
        WHERE language='en' AND regexp_matches(lower("desc"), '{"|".join(COMPETITORS.values())}')
        ORDER BY is_ad DESC, views DESC
      ) TO '{os.path.join(OUT,"competitors.csv")}' (HEADER)
    """)

print("outputs in", OUT)
for fn in sorted(os.listdir(OUT)): print("  ", fn, os.path.getsize(os.path.join(OUT,fn)))
