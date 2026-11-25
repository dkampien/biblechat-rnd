import json, collections

SRC = "/private/tmp/claude-501/-Users-dennisk-Documents-project---bib-content-gen/7fb1ee1b-33f1-4f3e-9e5e-9e998f7dd225/scratchpad/adsets.psv"
OUTDIR = "/Users/dennisk/Hub/focus/client - biblechat/project - bib content gen/_projects/funnel-maps/data/readings/app"

COLS = ["id","name","campaign_id","campaign_name","optimization_goal","promoted_object_custom_event",
        "attribution_setting","effective_status","destination_type","spend","impressions","reach",
        "link_clicks","landing_page_views","mobile_app_install","omni_app_install",
        "results_indicator","results","purchases"]

def num(v):
    if v == "NA": return None
    if v == "NOTAVAIL": return None
    return float(v) if "." in v else int(v)

def s(v):
    return None if v == "NA" else v

raw, pools = [], []
for line in open(SRC, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line: continue
    f = line.split("|")
    assert len(f) == 19, line
    r = dict(zip(COLS, f))
    ind = r["results_indicator"]
    res_raw = r["results"]
    # raw record
    raw.append({
        "id": r["id"], "name": r["name"],
        "campaign_id": r["campaign_id"], "campaign_name": r["campaign_name"],
        "optimization_goal": r["optimization_goal"],
        "promoted_object": {"custom_event_type": s(r["promoted_object_custom_event"])},
        "attribution_setting": r["attribution_setting"],
        "effective_status": r["effective_status"],
        "destination_type": r["destination_type"],
        "amount_spent": num(r["spend"]),
        "impressions": num(r["impressions"]),
        "reach": num(r["reach"]),
        "link_click": num(r["link_clicks"]),
        "omni_landing_page_view": num(r["landing_page_views"]),
        "mobile_app_install": num(r["mobile_app_install"]),
        "omni_app_install": num(r["omni_app_install"]),
        "results": {"indicator": ind,
                    "value": "Not available" if res_raw == "NOTAVAIL" else (None if res_raw=="NA" else int(res_raw))},
        "omni_purchase": num(r["purchases"]),
    })
    # door + events
    if ind == "conversions:app_custom_event.purchase_completed":
        door, result_event = "CPT", "purchase_completed"
    elif ind == "actions:mobile_app_install":
        door, result_event = "CPI", "mobile_app_install"
    elif ind == "actions:offsite_conversion.fb_pixel_lead":
        door, result_event = "WEB", "fb_pixel_lead"
    else:
        door, result_event = "other", ind
    if r["optimization_goal"] == "APP_INSTALLS":
        opt_event = "mobile_app_install"
    elif r["optimization_goal"] == "OFFSITE_CONVERSIONS":
        opt_event = result_event
    else:
        opt_event = None
    pools.append({
        "pool_id": r["id"], "pool_name": r["name"],
        "campaign_id": r["campaign_id"], "campaign_name": r["campaign_name"],
        "door": door,
        "optimization_goal": r["optimization_goal"],
        "promoted_object_custom_event": s(r["promoted_object_custom_event"]),
        "optimization_event": opt_event,
        "result_event": result_event,
        "effective_status": r["effective_status"],
        "destination_type": r["destination_type"],
        "attribution_setting": r["attribution_setting"],
        "counts": {
            "spend": num(r["spend"]),
            "impressions": num(r["impressions"]),
            "reach": num(r["reach"]),
            "link_clicks": num(r["link_clicks"]),
            "landing_page_views": num(r["landing_page_views"]),
            "app_installs": num(r["mobile_app_install"]),
            "trials": None,
            "results": None if res_raw in ("NA","NOTAVAIL") else int(res_raw),
            "result_event": result_event,
            "purchases": num(r["purchases"]),
        },
    })

# summary
tot_spend = round(sum(p["counts"]["spend"] for p in pools), 2)
tot_res = sum(p["counts"]["results"] or 0 for p in pools)
doors = collections.Counter(p["door"] for p in pools)
attrs = collections.Counter(p["attribution_setting"] for p in pools)
null_inst = sum(1 for p in pools if p["counts"]["app_installs"] is None)
null_res = sum(1 for p in pools if p["counts"]["results"] is None)
null_purch = sum(1 for p in pools if p["counts"]["purchases"] is None)
null_lpv = sum(1 for p in pools if p["counts"]["landing_page_views"] is None)
notavail = [p["pool_id"] for p in pools if p["counts"]["results"] is None]
small_count = sum(1 for p in pools if p['counts']['spend'] < 100)
tiny_count = sum(1 for p in pools if p['counts']['spend'] < 5)
android = sum(1 for p in pools if "ANDROID" in p["pool_name"].upper() or "Android" in p["campaign_name"])

notes = (
 "Pulled with the facebook-ads MCP tool ads_get_ad_entities, level=adset, 5 calls, all with "
 "time_range {\"since\":\"2026-09-08\",\"until\":\"2026-09-14\"} (explicit dates, no preset), "
 "filtering adset.amount_spent GREATER_THAN 0, sort=amount_spent_descending, limit=50, "
 "include_additional_context=false; paged with the returned pagination.next_cursor and every other "
 "parameter resent unchanged. Pages returned 50/50/50/50/18 = 218 ad sets; the 5th page had no "
 "next_cursor, so that is the complete set. All ad set ids are unique. Field names were verified "
 "first with ads_get_field_context: inline_link_clicks does NOT exist -- the canonical field is "
 "link_click (aliases link_clicks, actions:link_click); landing page views is omni_landing_page_view; "
 "app installs are mobile_app_install and omni_app_install; purchases is omni_purchase. "
 "start_trial / mobile_app_trial / trials_started are all unknown_fields, so counts.trials is null "
 "for every pool -- the tool exposes no trial metric. "
 f"COUNT: {len(pools)} ad sets with spend > 0 -- far above the 60-120 the brief expected, because the account "
 f"runs many small daily-rebuilt CPI-CREATOR and CPT-TEST ad sets; the tail is tiny ({small_count} ad sets under "
 f"$100, {tiny_count} under $5). "
 f"DOORS (by results indicator): CPT {doors['CPT']} (conversions:app_custom_event.purchase_completed), "
 f"CPI {doors['CPI']} (actions:mobile_app_install), WEB {doors['WEB']} "
 "(actions:offsite_conversion.fb_pixel_lead -- one ad set, 'ad set 3 - 6 new creatives' in "
 "'BC Creators campaign 1 - 30 July 2026', destination_type UNDEFINED, promoted_object custom_event_type "
 "LEAD with a real pixel_id 1076375544915405, cost_per_result labelled 'Clienti potentiali pe site-ul web'; "
 "it is a website-lead ad set sitting in this app account, not an app pool). "
 "ATTRIBUTION IS NOT UNIFORM: "
 f"{attrs['7d_click']} ad sets read 7d_click, {attrs['1d_click']} read 1d_click, "
 f"{attrs['1d_view_7d_click_1d_ev']} reads 1d_view_7d_click_1d_ev (the WEB one). The 1d_click pools are "
 "the Android SCALE/CPI-CREATOR/CPI-IMG and PH-Android sets. Every results value is tagged "
 "attribution_windows [\"default\"], i.e. each ad set's own setting; no per-window breakdown was requested "
 "or returned. So world.attribution_window is 'mixed' and the real window is on each pool as "
 "attribution_setting. "
 f"ANDROID: roughly {android} of the 218 ad sets are Android (names/campaigns say ANDROID), including the "
 "whole CPI-CREATOR / CPI-IMG test program and the SCALE - auto family. iOS and Android sit side by side "
 "in this one account. "
 f"NULLS: app_installs null on {null_inst} ad sets, results null on {null_res}, purchases null on "
 f"{null_purch}, landing_page_views null on {null_lpv}. "
 "results null means the tool returned results.value = \"Not available\" (Meta suppressing a tiny count) -- "
 f"those {len(notavail)} ad sets are {', '.join(notavail)}. Per the README, null = not read, NOT a verified zero. "
 "PURCHASES: omni_purchase comes back null on every Android ad set and on every CPI ad set -- Meta does not "
 "report a generic purchase for them here -- so counts.purchases is mostly null and its total is not "
 "comparable to counts.results. "
 "RESULTS != PURCHASES: on CPT pools results counts the app custom event purchase_completed "
 "(cost_per_result label '(purchase_completed)'), which is NOT Meta's generic omni_purchase; both are "
 "recorded separately. "
 "OPTIMIZATION: every CPT pool has optimization_goal OFFSITE_CONVERSIONS with promoted_object "
 "{pixel_id: null, custom_event_type: \"OTHER\", pixel_rule: null} -- the event is not named in "
 "promoted_object, so optimization_event is taken from the results indicator / cost_per_result label. "
 "CPI pools have optimization_goal APP_INSTALLS and a fully null promoted_object. "
 "ODD: omni_landing_page_view is tiny next to link_clicks on every app pool (e.g. 433 LPV vs 17,231 link "
 "clicks on the top ad set) -- for an app-store destination LPV is not a real funnel step, treat it as noise. "
 "The one exception is the WEB ad set, where LPV 2,208 against 3,139 link clicks behaves like a real "
 "web funnel. "
 "DRIFT vs the reference reading: ad set 120246661279120160 now reads spend 13552.42 / impressions 888901 "
 "against 13552.35 / 888895 in the single-ad-set reading taken earlier the same day (2026-09-15T14:09:55Z). "
 "Meta is still settling the window; everything else on that pool matches exactly. "
 "Read-only pull; nothing was created, updated, activated or paused. No per-ad rows were pulled this time."
)

world = {
  "route": "app",
  "account_id": "act_697155031095732",
  "account_name": "Basmo iOS",
  "level": "adset",
  "date_from": "2026-09-08",
  "date_to": "2026-09-14",
  "currency": "USD",
  "attribution_window": "mixed (per ad set): 7d_click on %d, 1d_click on %d, 1d_view_7d_click_1d_ev on %d -- see each pool's attribution_setting" % (attrs['7d_click'], attrs['1d_click'], attrs['1d_view_7d_click_1d_ev']),
  "read_at": "2026-09-15T00:00:00Z",
  "read_by": "facebook-ads MCP via subagent",
  "pool_count": len(pools),
  "totals": {"spend": tot_spend, "results": tot_res},
  "door_counts": dict(doors),
  "notes": notes,
}

with open(OUTDIR + "/scan-adsets_2026-09-08_2026-09-14.json", "w", encoding="utf-8") as fh:
    json.dump({"world": world, "pools": pools}, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

with open(OUTDIR + "/scan-adsets_2026-09-08_2026-09-14.raw.json", "w", encoding="utf-8") as fh:
    json.dump({
      "source": "facebook-ads MCP ads_get_ad_entities, level=adset, act_697155031095732, time_range 2026-09-08..2026-09-14, filtering adset.amount_spent>0, sort=amount_spent_descending, limit=50, 5 paged calls",
      "fields_requested": ["id","name","campaign_id","campaign_name","optimization_goal","promoted_object","attribution_setting","effective_status","destination_type","amount_spent","impressions","reach","link_click","omni_landing_page_view","mobile_app_install","omni_app_install","results","cost_per_result","omni_purchase"],
      "note": "Trimmed to the relevant fields; cost_per_result omitted (derived). amount_spent parsed from the '$X USD' strings the tool returns. results.value 'Not available' is kept verbatim.",
      "entity_count": len(raw),
      "ad_entities": raw,
    }, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

print("pools:", len(pools))
print("total spend:", tot_spend, "total results:", tot_res)
print("doors:", dict(doors))
print("attrs:", dict(attrs))
print("null installs:", null_inst, "null results:", null_res, "null purchases:", null_purch, "null lpv:", null_lpv)
print("android-ish:", android)
print("spend<100:", sum(1 for p in pools if p["counts"]["spend"]<100), "spend<5:", sum(1 for p in pools if p["counts"]["spend"]<5))
print("results by door:", {d: sum(p["counts"]["results"] or 0 for p in pools if p["door"]==d) for d in doors})
print("spend by door:", {d: round(sum(p["counts"]["spend"] for p in pools if p["door"]==d),2) for d in doors})
