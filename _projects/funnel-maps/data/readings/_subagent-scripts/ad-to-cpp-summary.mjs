import fs from "node:fs";
const BASE = "/Users/dennisk/Hub/focus/client - biblechat/project - bib content gen";
const t = JSON.parse(fs.readFileSync(`${BASE}/_projects/funnel-maps/data/app-store/ad-to-cpp-2026-09-15.json`, "utf8"));
const rows = t.ads;
const pages = new Map();
for (const r of rows) {
  const k = r.ppid ?? "__default__";
  const e = pages.get(k) ?? { ppid: r.ppid, name: r.product_page_name, ads: 0, adsets: new Set(), campaigns: new Set(), plat: {}, status: {} };
  e.ads++; e.adsets.add(r.adset_id); e.campaigns.add(r.campaign_id);
  e.plat[r.platform] = (e.plat[r.platform] || 0) + 1;
  e.status[r.effective_status] = (e.status[r.effective_status] || 0) + 1;
  pages.set(k, e);
}
const sorted = [...pages.values()].sort((a,b)=>b.ads-a.ads);
console.log("PAGES");
for (const p of sorted) console.log([p.name, p.ppid, p.ads, p.adsets.size, p.campaigns.size, JSON.stringify(p.plat), JSON.stringify(p.status)].join(" | "));

// default page split
const def = rows.filter(r=>!r.ppid);
console.log("\nDEFAULT split:", def.reduce((m,r)=>(m[r.platform]=(m[r.platform]||0)+1,m),{}));
const defIOS = def.filter(r=>r.platform==="ios_app_store");
console.log("default ios ads:", defIOS.map(r=>`${r.ad_id} ${r.ad_name} | ${r.campaign_name}`));

// web ads
const web = rows.filter(r=>r.platform==="web");
console.log("\nWEB ads:", web.length, "adsets", new Set(web.map(r=>r.adset_id)).size, "campaigns", new Set(web.map(r=>r.campaign_id)).size);
console.log("web campaigns:", [...new Set(web.map(r=>r.campaign_name))]);
console.log("web with ppid:", web.filter(r=>r.ppid).length, JSON.stringify(web.filter(r=>r.ppid).reduce((m,r)=>(m[r.product_page_name]=(m[r.product_page_name]||0)+1,m),{})));
console.log("web status:", web.reduce((m,r)=>(m[r.effective_status]=(m[r.effective_status]||0)+1,m),{}));
console.log("web hosts:", [...new Set(web.map(r=>new URL(r.web_url).host))]);

// deep links
const dl = rows.filter(r=>r.deep_link);
console.log("\nDEEPLINKS", dl.length, JSON.stringify(dl.reduce((m,r)=>(m[r.deep_link_intent]=(m[r.deep_link_intent]||0)+1,m),{}),null,1));
console.log("deeplink platforms:", dl.reduce((m,r)=>(m[r.platform]=(m[r.platform]||0)+1,m),{}));

// adsets mixing destinations
const bySet = new Map();
for (const r of rows) { const e = bySet.get(r.adset_id) ?? {name:r.adset_name, camp:r.campaign_name, pp:new Set(), plat:new Set(), n:0}; e.n++; e.pp.add(r.ppid ?? "default"); e.plat.add(r.platform); bySet.set(r.adset_id, e); }
console.log("\nADSETS total", bySet.size);
for (const [id,e] of bySet) if (e.pp.size>1 || e.plat.size>1) console.log(`MIX ${id} (${e.n} ads) pages=${[...e.pp].join(",")} plat=${[...e.plat].join(",")} :: ${e.name.slice(0,80)} :: ${e.camp.slice(0,70)}`);

// campaigns mixing
const byC = new Map();
for (const r of rows) { const e = byC.get(r.campaign_id) ?? {name:r.campaign_name, pp:new Set(), plat:new Set()}; e.pp.add(r.ppid??"default"); e.plat.add(r.platform); byC.set(r.campaign_id,e); }
console.log("\nCAMPAIGNS total", byC.size);
for (const [id,e] of byC) if (e.plat.size>1) console.log(`CAMP-PLAT-MIX ${id} ${e.name} :: ${[...e.plat].join(",")}`);

// android campaigns named IOS / ios campaigns named android
for (const [id,e] of byC) { const n=e.name.toUpperCase(); const p=[...e.plat][0];
  if ((n.includes("IOS")&&p==="google_play")||(n.includes("ANDROID")&&p==="ios_app_store")) console.log(`NAME-MISMATCH ${id} ${e.name} -> ${p}`); }

// promoted app ids
console.log("\npromoted app ids:", JSON.stringify(rows.reduce((m,r)=>(m[String(r.promoted_app_id)]=(m[String(r.promoted_app_id)]||0)+1,m),{})));
console.log("goals:", JSON.stringify(rows.reduce((m,r)=>(m[String(r.optimization_goal)]=(m[String(r.optimization_goal)]||0)+1,m),{})));
console.log("url_tags non-null:", rows.filter(r=>r.url_tags).length);
console.log("store urls:", [...new Set(rows.map(r=>r.store_url).filter(Boolean))]);
