---
created: 2026-09-15
updated: 2026-09-15
---
# Readings

One file per pool per period. A reading holds only what a sensor counted; the ladder computes rates, cost-pers and diagnosis from it. Nothing derived is stored here.

Path: `readings/<route>/<level>-<id>_<from>_<to>.json` (route = app | web; level = ad | adset | campaign | blend).

```json
{
  "world": {
    "route": "app",
    "account_id": "act_697155031095732",
    "account_name": "Basmo IOS",
    "door": "CPT",
    "level": "adset",
    "pool_id": "<adset id>",
    "pool_name": "<adset name>",
    "campaign_id": "<campaign id>",
    "campaign_name": "<campaign name>",
    "optimization_event": "<as Ads Manager shows it, e.g. purchase_completed>",
    "attribution_window": "7d_click",
    "date_from": "2026-09-08",
    "date_to": "2026-09-14",
    "currency": "USD",
    "read_at": "2026-09-15T..Z",
    "read_by": "facebook-ads MCP via subagent",
    "notes": "anything odd about the pull"
  },
  "counts": {
    "spend": 0,
    "impressions": 0,
    "reach": null,
    "link_clicks": 0,
    "landing_page_views": null,
    "app_installs": null,
    "trials": null,
    "results": 0,
    "result_event": "purchase_completed",
    "purchases": null
  },
  "ads": [
    { "ad_id": "", "ad_name": "", "spend": 0, "impressions": 0, "link_clicks": 0, "app_installs": null, "results": 0 }
  ]
}
```

Rules: `null` means the column exists but was not read; `0` means it was read and is zero. Never fill a blank-by-design column with a guess. Per-ad rows are optional but wanted, so the same reading can feed the ad-level scan later.
