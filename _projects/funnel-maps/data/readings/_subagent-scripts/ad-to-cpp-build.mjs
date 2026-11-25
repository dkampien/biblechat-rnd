import fs from "node:fs";
const BASE = "/Users/dennisk/Hub/focus/client - biblechat/project - bib content gen";
const raw = JSON.parse(fs.readFileSync(`${BASE}/_projects/funnel-maps/data/app-store/ad-destinations-2026-09-15.json`, "utf8"));
const inv = JSON.parse(fs.readFileSync(`${BASE}/_docs/core/cpp-inventory.json`, "utf8"));
const byPpid = new Map(inv.map(p => [p.ppid, p.name]));

const isApple = u => u.includes("itunes.apple.com") || u.includes("apps.apple.com");
const isPlay = u => u.includes("play.google.com");
const ppidOf = u => { const m = /[?&]ppid=([0-9a-fA-F-]{36})/.exec(u); return m ? m[1] : null; };
const stripRef = u => u.replace(/([?&])referrer=[^&]*&?/, "$1").replace(/[?&]$/, "");

const deepIntent = (u, decoded) => {
  const m = /^biblechatapp:\/\/launch-feature\/(.+)$/.exec(u);
  if (m) return m[1];
  if (decoded && typeof decoded === "object") {
    const t = decoded.tasks?.map(t => t.type + (t.match ? `:${t.match.join("|")}` : "")).join(" + ");
    if (t) return t;
  }
  return "encoded-task-payload";
};

const rows = raw.ads.map(a => {
  const ds = a.destinations || [];
  const urls = ds.map(x => x.url);
  const store = urls.find(u => isApple(u)) || urls.find(u => isPlay(u)) || null;
  const webUrl = urls.find(u => /^https?:/.test(u) && !isApple(u) && !isPlay(u)) || null;
  const deepEntry = ds.find(x => x.url.startsWith("biblechatapp://"));
  const platform = store ? (isApple(store) ? "ios_app_store" : "google_play") : (webUrl ? "web" : "unknown");
  const destination_type = platform === "web" ? "web" : "app_store";
  const ppid = a.app_product_page_id || (store ? ppidOf(store) : null) || (webUrl ? ppidOf(webUrl) : null);
  let product_page_name;
  if (!ppid) product_page_name = platform === "google_play" ? "default store page" : "default store page";
  else product_page_name = byPpid.get(ppid) ?? "not in inventory";
  return {
    ad_id: a.ad_id,
    ad_name: a.ad_name,
    created_time: a.created_time,
    adset_id: a.adset_id,
    adset_name: a.adset_name,
    campaign_id: a.campaign_id,
    campaign_name: a.campaign_name,
    effective_status: a.status,
    optimization_goal: a.optimization_goal ?? null,
    promoted_app_id: a.promoted_application_id ?? null,
    destination_type,
    platform,
    store_url: store ? stripRef(store) : null,
    web_url: webUrl,
    ppid: ppid ?? null,
    product_page_name,
    ppid_source: a.app_product_page_id ? "creative.app_product_page_id" : (ppid ? "url ppid param" : null),
    deep_link: deepEntry ? deepEntry.url : null,
    deep_link_intent: deepEntry ? deepIntent(deepEntry.url, deepEntry.decoded) : null,
    url_tags: a.url_tags ?? null,
  };
});

fs.writeFileSync(`${BASE}/_projects/funnel-maps/data/app-store/ad-to-cpp-2026-09-15.json`,
  JSON.stringify({ pulled_at_utc: raw.pulled_at_utc, scope: raw.scope, source: "ad-destinations-2026-09-15.json", cpp_inventory: "_docs/core/cpp-inventory.json", ad_count: rows.length, ads: rows }, null, 2));

// ---- summary aggregation ----
const pages = new Map();
for (const r of rows) {
  const key = r.ppid ?? `__default__${r.platform}`;
  const e = pages.get(key) ?? { ppid: r.ppid, name: r.product_page_name, platform: r.platform, ads: 0, adsets: new Set(), campaigns: new Set(), statuses: {} };
  e.ads++; e.adsets.add(r.adset_id); e.campaigns.add(r.campaign_id);
  e.statuses[r.effective_status] = (e.statuses[r.effective_status] || 0) + 1;
  pages.set(key, e);
}
const sorted = [...pages.values()].sort((a, b) => b.ads - a.ads || String(a.name).localeCompare(String(b.name)));
const out = { rows, sorted };
fs.writeFileSync("/private/tmp/claude-501/-Users-dennisk-Documents-project---bib-content-gen/7fb1ee1b-33f1-4f3e-9e5e-9e998f7dd225/scratchpad/agg.json", JSON.stringify({
  total: rows.length,
  byPlatform: rows.reduce((m, r) => (m[r.platform] = (m[r.platform] || 0) + 1, m), {}),
  byStatus: rows.reduce((m, r) => (m[r.effective_status] = (m[r.effective_status] || 0) + 1, m), {}),
  withPpid: rows.filter(r => r.ppid).length,
  notInInventory: [...new Set(rows.filter(r => r.product_page_name === "not in inventory").map(r => r.ppid))],
  deepLinks: rows.filter(r => r.deep_link).length,
  deepIntents: [...new Set(rows.filter(r => r.deep_link).map(r => r.deep_link_intent))],
  pages: sorted.map(p => ({ name: p.name, ppid: p.ppid, platform: p.platform, ads: p.ads, adsets: p.adsets.size, campaigns: p.campaigns.size, statuses: p.statuses })),
}, null, 2));
console.log("rows", rows.length);
