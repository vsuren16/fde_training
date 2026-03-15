import React, { useEffect, useMemo, useRef, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8050";
const EMAIL_RE = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const MOBILE_RE = /^\d{10}$/;
const TOP_BRANDS = ["AeroFit", "UrbanThread", "ClassicWeave", "NoteCraft", "PeakMove"];

async function parseJsonSafe(r) {
  const t = await r.text();
  if (!t) return {};
  try { return JSON.parse(t); } catch { return { detail: t }; }
}

function readStorageJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return fallback;
    return JSON.parse(raw);
  } catch {
    localStorage.removeItem(key);
    return fallback;
  }
}

function imgFallback(name = "Product", color = "beige") {
  const c = color.toLowerCase();
  const bg = c === "black" ? "#111" : c === "blue" ? "#c8dcf7" : "#f0e0ce";
  const fg = c === "black" ? "#fff" : "#1a1a1a";
  const lbl = (name || "Product").slice(0, 20);
  return `data:image/svg+xml;utf8,${encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><rect width='100%' height='100%' fill='${bg}'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='Georgia' font-size='16' fill='${fg}'>${lbl}</text></svg>`
  )}`;
}

function resolveImageUrl(url = "") {
  if (!url) return "";
  if (url.startsWith("http://") || url.startsWith("https://") || url.startsWith("data:")) {
    return url;
  }
  if (url.startsWith("/")) {
    return `${API_BASE}${url}`;
  }
  return `${API_BASE}/${url.replace(/^\.?\//, "")}`;
}

function normalizeItem(item) {
  const imageUrls = item.image_urls?.length ? item.image_urls : [item.image_url].filter(Boolean);
  return {
    id: item.id,
    product_name: item.product_name || item.name || "Product",
    short_description: item.short_description || "Curated by AIra.",
    description: item.description || "",
    brand: item.brand || "AIra Edit",
    color: item.color || "Classic",
    size: item.size || "M",
    category: item.category || "Fashion",
    price: Number(item.price || 0),
    image_url: resolveImageUrl(item.image_url || ""),
    image_urls: imageUrls.map(resolveImageUrl),
  };
}

const S = `
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --ink:#0c0906;
  --ink2:#130f08;
  --gold:#c9954c;
  --gold2:#e8b96a;
  --gold3:#f5d08a;
  --gold4:rgba(201,149,76,0.22);
  --parch:#faf4eb;
  --parch2:#f2e8d5;
  --mist:#a89070;
  --mist2:#7a6040;
  --border:rgba(201,149,76,0.25);
  --border2:rgba(201,149,76,0.45);
  --shadow:0 40px 100px rgba(0,0,0,0.55);
  --r:16px;--r-sm:10px;--nav:60px;
  --fd:'Cormorant Garamond',Georgia,serif;
  --fb:'DM Sans',sans-serif;
  --ease:cubic-bezier(.4,0,.2,1);
}

html,body,#root{width:100%;height:100%;overflow:hidden;font-family:var(--fb);background:var(--ink);color:var(--parch)}
.scroll-y{overflow-y:auto;overflow-x:hidden}
.scroll-y::-webkit-scrollbar{width:5px}
.scroll-y::-webkit-scrollbar-thumb{background:rgba(201,149,76,.35);border-radius:5px}
.scroll-y::-webkit-scrollbar-track{background:rgba(201,149,76,.04)}

/* SHELL */
.shell{display:flex;flex-direction:column;width:100vw;height:100vh;overflow:hidden}

/* GOLD LINE */
.gold-line{
  height:3px;flex-shrink:0;
  background:linear-gradient(90deg,
    transparent 0%,var(--gold) 25%,var(--gold3) 50%,var(--gold) 75%,transparent 100%
  );
  box-shadow:0 0 18px rgba(201,149,76,.5);
}

/* ── TOPBAR ── */
.topbar{
  flex-shrink:0;height:var(--nav);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 40px;
  background:linear-gradient(180deg,rgba(20,13,6,.98),rgba(12,9,6,.98));
  border-bottom:2px solid var(--border2);
  z-index:200;
}
.logo-wrap{display:flex;flex-direction:column;cursor:pointer;gap:2px}
.logo-main{
  font-family:var(--fd);font-size:22px;font-weight:600;
  letter-spacing:0.04em;color:var(--parch);line-height:1;
}
.logo-main span{
  background:linear-gradient(135deg,var(--gold),var(--gold3),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.logo-sub{
  font-size:11px;font-weight:400;letter-spacing:0.32em;
  text-transform:uppercase;color:var(--gold);opacity:.7;
}
.nav{display:flex;align-items:center;gap:4px}
.nb{
  font-family:var(--fb);font-size:10px;font-weight:500;
  letter-spacing:0.08em;text-transform:uppercase;
  padding:10px 20px;border-radius:999px;
  border:1px solid transparent;background:transparent;
  color:rgba(201,149,76,.65);cursor:pointer;
  transition:all .25s var(--ease);white-space:nowrap;
}
.nb:hover{color:var(--gold2);background:rgba(201,149,76,.12);border-color:var(--border2)}
.nb.on{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);border-color:transparent;font-weight:700;
  box-shadow:0 4px 18px rgba(201,149,76,.5);
}
.nb.cart-nb{border-color:var(--border);color:var(--parch2);display:flex;align-items:center;gap:6px}
.cart-badge{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);border-radius:999px;font-size:11px;font-weight:700;
  min-width:20px;height:20px;
  display:inline-flex;align-items:center;justify-content:center;padding:0 5px;
}

/* PAGE AREA */
.page-area{flex:1;min-height:0;display:flex;flex-direction:column;overflow:hidden}

/* ════ HOME ════ */
.home-layout{
  display:flex;flex-direction:column;
  height:100%;overflow:hidden;
  background:
    radial-gradient(ellipse at 0% 0%,rgba(201,149,76,.22) 0%,transparent 45%),
    radial-gradient(ellipse at 100% 5%,rgba(201,149,76,.14) 0%,transparent 38%),
    radial-gradient(ellipse at 50% 95%,rgba(201,149,76,.1) 0%,transparent 45%),
    linear-gradient(180deg,#130f08 0%,#0c0906 100%);
}

/* HERO STRIP */
.home-hero-strip{
  flex-shrink:0;
  display:flex;align-items:center;justify-content:space-between;
  padding:20px 48px 16px;
  background:linear-gradient(180deg,rgba(201,149,76,.1) 0%,rgba(201,149,76,.03) 100%);
  border-bottom:1px solid var(--border2);
  position:relative;
}
.home-hero-strip::before{
  content:'';position:absolute;
  inset:0;pointer-events:none;
  background:
    radial-gradient(ellipse at 30% 50%,rgba(201,149,76,.06),transparent 60%);
}
.home-hero-strip::after{
  content:'';position:absolute;
  bottom:-1px;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent 0%,var(--gold) 30%,var(--gold3) 50%,var(--gold) 70%,transparent 100%);
  opacity:.55;
}
.home-hero-left{flex:1;min-width:0}

.kicker{
  display:inline-flex;align-items:center;gap:9px;
  font-size:10px;font-weight:600;letter-spacing:0.28em;text-transform:uppercase;
  color:var(--gold2);margin-bottom:12px;
  background:rgba(201,149,76,.1);border:1px solid var(--border);
  padding:5px 14px;border-radius:999px;
}
.kicker::before{content:'✦';font-size:11px;color:var(--gold3)}

.hero-h{
  font-family:var(--fd);
  font-size:clamp(32px,2.8vw,46px);
  font-weight:300;line-height:1.04;
  color:var(--parch);letter-spacing:-0.015em;margin-bottom:12px;
}
.hero-h em{
  font-style:italic;font-weight:400;
  background:linear-gradient(135deg,var(--gold),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

.hero-sub{
  font-size:13px;
  color:rgba(250,244,235,.6);
  line-height:1.65;font-weight:300;max-width:560px;
}

.brand-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.bchip{
  font-size:10px;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;
  padding:6px 16px;border-radius:999px;
  border:1px solid var(--border2);
  color:var(--gold2);
  background:rgba(201,149,76,.1);
  cursor:default;transition:all .25s;
}
.bchip:hover{
  border-color:var(--gold3);color:var(--gold3);
  background:rgba(201,149,76,.18);
  box-shadow:0 2px 12px rgba(201,149,76,.2);
}

.home-hero-right{
  display:flex;align-items:center;gap:40px;
  flex-shrink:0;margin-left:52px;
}
.stat-col{text-align:center;min-width:68px}
.stat-n{
  font-family:var(--fd);font-size:33px;font-weight:600;line-height:1;
  background:linear-gradient(135deg,var(--gold),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.stat-l{
  font-size:11px;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;
  color:rgba(201,149,76,.7);margin-top:5px;
}
.stat-div{
  width:1px;height:44px;
  background:linear-gradient(180deg,transparent,var(--gold2),transparent);
  opacity:.5;
}

/* PROMPT + RECS BODY */
.home-body{
  flex:1;min-height:0;
  display:flex;flex-direction:column;
  align-items:center;
  padding:20px 48px 16px;
  overflow:hidden;
  background:
    radial-gradient(ellipse at 50% 20%,rgba(201,149,76,.07),transparent 55%);
}

.prompt-card{
  flex-shrink:0;width:100%;max-width:920px;
  background:linear-gradient(145deg,rgba(201,149,76,.12),rgba(201,149,76,.04));
  border:1.5px solid var(--border2);border-radius:20px;
  padding:22px 28px;margin-bottom:22px;
  transition:all .3s var(--ease);
  box-shadow:0 8px 40px rgba(0,0,0,.3),inset 0 1px 0 rgba(201,149,76,.2);
  position:relative;overflow:hidden;
}
.prompt-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold2),transparent);
  opacity:.6;
}
.prompt-card::after{
  content:'';position:absolute;
  top:-80px;right:-80px;
  width:200px;height:200px;border-radius:50%;
  background:radial-gradient(circle,rgba(201,149,76,.15),transparent 70%);
  pointer-events:none;
}
.prompt-card:focus-within{
  border-color:var(--gold2);
  box-shadow:0 0 0 3px rgba(201,149,76,.15),0 12px 48px rgba(0,0,0,.4);
}
.prompt-lbl{
  font-size:10px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;
  color:var(--gold2);margin-bottom:11px;
  display:flex;align-items:center;gap:8px;
}
.prompt-lbl::before{content:'✦';font-size:11px;color:var(--gold3)}
.prompt-ta{
  width:100%;background:transparent;border:none;outline:none;
  font-family:var(--fb);font-size:15px;color:var(--parch);
  resize:none;line-height:1.6;min-height:46px;
}
.prompt-ta::placeholder{color:rgba(250,244,235,.3)}
.prompt-row{
  display:flex;align-items:center;justify-content:space-between;
  margin-top:14px;padding-top:14px;
  border-top:1px solid rgba(201,149,76,.2);
}
.prompt-hint{font-size:10px;color:rgba(201,149,76,.5);font-style:italic}

/* RECS ZONE — centered between hero and footer */
.recs-zone{
  flex:1;min-height:0;
  width:100%;
  display:flex;flex-direction:column;
  overflow-y:auto;overflow-x:hidden;
  padding-right:8px;
}
.recs-zone::-webkit-scrollbar{width:5px}
.recs-zone::-webkit-scrollbar-thumb{background:rgba(201,149,76,.35);border-radius:5px}
.recs-zone::-webkit-scrollbar-track{background:rgba(201,149,76,.04)}
.recs-inner{
  max-width:1300px;width:100%;margin:0 auto;
  padding-bottom:40px;
  flex-shrink:0;
}
.recs-centered{
  flex:1;min-height:0;
  display:flex;flex-direction:column;align-items:center;
  justify-content:flex-start;
  width:100%;
}
.recs-spacer-top{flex:6;min-height:0;max-flex:6}
.recs-spacer-bot{flex:4;min-height:0}

.aira-banner{
  display:flex;gap:16px;align-items:flex-start;
  background:linear-gradient(135deg,rgba(201,149,76,.15),rgba(201,149,76,.05));
  border:1.5px solid var(--border2);border-radius:var(--r);
  padding:18px 24px;margin-bottom:22px;animation:fadeIn .4s ease;
}
.aira-icon{
  width:40px;height:40px;border-radius:50%;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);display:flex;align-items:center;justify-content:center;
  font-size:14px;flex-shrink:0;font-weight:700;font-family:var(--fd);
  box-shadow:0 4px 16px rgba(201,149,76,.4);
}
.aira-text{font-size:12px;color:var(--parch2);line-height:1.65}
.aira-text strong{
  display:block;margin-bottom:4px;
  font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;
  color:var(--gold2);
}

.empty-recs{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100%;gap:18px;text-align:center;
  padding:20px;
}
.empty-recs-ico{
  font-size:40px;
  background:linear-gradient(135deg,var(--gold),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 4px 16px rgba(201,149,76,.45));
  line-height:1;
}
.empty-recs-title{
  font-family:var(--fd);font-size:26px;font-weight:400;
  background:linear-gradient(135deg,var(--parch),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.empty-recs-sub{font-size:13px;color:var(--mist);max-width:300px;line-height:1.65}

/* PRODUCT GRID */
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px}
.pcard{
  background:linear-gradient(160deg,rgba(201,149,76,.08),rgba(201,149,76,.02));
  border:1px solid var(--border);border-radius:var(--r);
  overflow:hidden;transition:all .35s var(--ease);
}
.pcard:hover{
  transform:translateY(-7px);
  border-color:var(--border2);
  box-shadow:0 28px 64px rgba(0,0,0,.55),0 0 0 1px rgba(201,149,76,.3);
}
.pcard-img{position:relative;aspect-ratio:1;overflow:hidden;background:rgba(201,149,76,.07)}
.pcard-img img{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.pcard:hover .pcard-img img{transform:scale(1.08)}
.pcard-overlay{
  position:absolute;inset:0;
  background:linear-gradient(to top,rgba(6,4,2,.88) 0%,transparent 55%);
  display:flex;align-items:flex-end;justify-content:center;
  padding:18px;opacity:0;transition:opacity .35s;
}
.pcard:hover .pcard-overlay{opacity:1}
.score-pill{
  position:absolute;top:10px;right:10px;
  background:rgba(6,4,2,.82);backdrop-filter:blur(8px);
  color:var(--gold2);font-size:11px;font-weight:700;
  letter-spacing:0.06em;padding:5px 12px;border-radius:999px;
  border:1px solid rgba(201,149,76,.3);
}
.pcard-body{padding:18px}
.ptags{display:flex;gap:5px;margin-bottom:10px;flex-wrap:wrap}
.ptag{
  font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;
  padding:3px 10px;border-radius:999px;
  border:1px solid var(--border);color:var(--gold);
  background:rgba(201,149,76,.08);
}
.pname{
  font-family:var(--fd);font-size:18px;font-weight:500;
  color:var(--parch);margin-bottom:6px;line-height:1.2;
}
.pdesc{
  font-size:12px;color:var(--mist);line-height:1.5;margin-bottom:14px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.pfoot{
  display:flex;align-items:center;justify-content:space-between;
  padding-top:13px;
  border-top:1px solid rgba(201,149,76,.15);
}
.pprice{font-family:var(--fd);font-size:19px;font-weight:600;color:var(--gold2)}
.pprice span{font-size:10px;font-weight:300;color:var(--mist);margin-right:2px}

/* ── BUTTONS ── */
.btn-gold{
  display:inline-flex;align-items:center;gap:7px;
  font-family:var(--fb);font-size:10px;font-weight:700;
  letter-spacing:0.1em;text-transform:uppercase;
  padding:12px 28px;border-radius:999px;border:none;cursor:pointer;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);transition:all .25s var(--ease);white-space:nowrap;
  box-shadow:0 4px 18px rgba(201,149,76,.4);
}
.btn-gold:hover{
  background:linear-gradient(135deg,var(--gold2),var(--gold3));
  transform:translateY(-2px);box-shadow:0 8px 28px rgba(201,149,76,.55);
}
.btn-gold:active{transform:translateY(0)}
.btn-gold:disabled{opacity:.5;cursor:default;transform:none;box-shadow:none}

.btn-dark{
  display:inline-flex;align-items:center;gap:7px;
  font-family:var(--fb);font-size:10px;font-weight:500;
  letter-spacing:0.08em;text-transform:uppercase;
  padding:11px 22px;border-radius:999px;
  border:1.5px solid var(--border2);cursor:pointer;
  background:rgba(201,149,76,.1);color:var(--gold2);
  transition:all .25s;
}
.btn-dark:hover{border-color:var(--gold2);color:var(--gold3);background:rgba(201,149,76,.16)}

.btn-sm{
  font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
  padding:9px 18px;border-radius:999px;border:none;cursor:pointer;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);transition:all .2s;
  box-shadow:0 3px 12px rgba(201,149,76,.3);
}
.btn-sm:hover{background:linear-gradient(135deg,var(--gold2),var(--gold3))}
.btn-danger{
  font-size:10px;font-weight:500;padding:9px 18px;border-radius:999px;
  border:1px solid rgba(220,100,80,.3);background:transparent;
  color:#e8907a;cursor:pointer;transition:all .2s;
}
.btn-danger:hover{background:rgba(220,100,80,.1);border-color:#e8907a}

/* ── FULL PAGE WRAPPER ── */
.fp{flex:1;min-height:0;display:flex;flex-direction:column;overflow:hidden;
  background:linear-gradient(180deg,rgba(201,149,76,.05) 0%,var(--ink2) 20%)}
.fp-scroll{flex:1;min-height:0;padding:42px 56px}
.fp-hdr{
  display:flex;align-items:flex-end;justify-content:space-between;
  margin-bottom:30px;padding-bottom:22px;
  border-bottom:1px solid var(--border2);position:relative;
}
.fp-hdr::after{
  content:'';position:absolute;bottom:-1px;left:0;width:120px;height:2px;
  background:linear-gradient(90deg,var(--gold2),transparent);
}
.fp-title{
  font-family:var(--fd);font-size:33px;font-weight:400;
  color:var(--parch);letter-spacing:-0.01em;
}
.fp-sub{font-size:12px;color:var(--mist);margin-top:5px}

/* ── CART ── */
.cart-list{display:flex;flex-direction:column;gap:14px;margin-bottom:22px}
.cart-item{
  display:flex;align-items:center;gap:18px;
  background:linear-gradient(145deg,rgba(201,149,76,.08),rgba(201,149,76,.03));
  border:1px solid var(--border);border-radius:var(--r);
  padding:18px 24px;transition:all .2s;
}
.cart-item:hover{border-color:var(--border2);background:rgba(201,149,76,.1)}
.ci-thumb{
  width:54px;height:54px;border-radius:var(--r-sm);
  background:rgba(201,149,76,.15);
  display:flex;align-items:center;justify-content:center;
  font-size:19px;flex-shrink:0;
}
.ci-info{flex:1}
.ci-name{font-family:var(--fd);font-size:16px;color:var(--parch);margin-bottom:3px}
.ci-price{font-size:12px;color:var(--gold2);font-weight:600}
.cart-summary{
  background:linear-gradient(135deg,rgba(201,149,76,.14),rgba(201,149,76,.06));
  border:1.5px solid var(--border2);border-radius:var(--r);
  padding:26px 32px;
  display:flex;align-items:center;justify-content:space-between;gap:22px;
}
.cs-lbl{font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:var(--gold);margin-bottom:5px}
.cs-amt{
  font-family:var(--fd);font-size:33px;font-weight:600;
  background:linear-gradient(135deg,var(--parch),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}

/* ── EMPTY STATE ── */
.empty{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;gap:16px;color:var(--mist)}
.empty-ico{font-size:40px;opacity:.22;margin-bottom:6px}
.empty-t{font-family:var(--fd);font-size:26px;color:var(--parch2)}
.empty-s{font-size:12px;text-align:center;max-width:290px;margin-bottom:12px;line-height:1.65}
.guest-bar{
  display:flex;align-items:center;gap:11px;
  background:rgba(201,149,76,.1);border:1.5px solid var(--border2);
  border-radius:var(--r-sm);padding:12px 18px;
  font-size:12px;color:var(--gold2);margin-bottom:22px;
}

/* ── LOGIN ── */
.login-outer{
  flex:1;min-height:0;display:flex;align-items:center;justify-content:center;
  background:
    radial-gradient(ellipse at 50% 40%,rgba(201,149,76,.14),transparent 60%),
    var(--ink2);
}
.login-box{
  width:100%;max-width:460px;
  background:linear-gradient(160deg,rgba(201,149,76,.1),rgba(201,149,76,.03));
  border:1.5px solid var(--border2);border-radius:20px;
  padding:48px;box-shadow:var(--shadow);
  position:relative;overflow:hidden;animation:fadeUp .4s ease;
}
.login-box::before{
  content:'';position:absolute;top:-100px;right:-70px;
  width:260px;height:260px;border-radius:50%;
  background:radial-gradient(circle,rgba(201,149,76,.16),transparent 70%);
  pointer-events:none;
}
.l-logo{font-family:var(--fd);font-size:27px;font-weight:600;color:var(--parch);text-align:center;margin-bottom:6px}
.l-logo span{
  background:linear-gradient(135deg,var(--gold),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.l-tag{font-size:12px;color:var(--mist);text-align:center;margin-bottom:30px;line-height:1.5}
.tabs-row{
  display:flex;background:rgba(201,149,76,.08);
  border-radius:999px;padding:4px;margin-bottom:26px;
  border:1.5px solid var(--border2);
}
.tab{
  flex:1;text-align:center;font-size:12px;font-weight:500;
  padding:10px;border-radius:999px;cursor:pointer;border:none;
  background:transparent;color:var(--mist);transition:all .25s;
}
.tab.on{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);font-weight:700;
}
.field{margin-bottom:16px}
.flbl{
  display:block;font-size:10px;font-weight:600;
  letter-spacing:0.14em;text-transform:uppercase;
  color:var(--gold);margin-bottom:8px;
}
.finp{
  width:100%;padding:14px 18px;
  font-family:var(--fb);font-size:12px;
  color:var(--parch);background:rgba(201,149,76,.06);
  border:1.5px solid var(--border);border-radius:var(--r-sm);outline:none;
  transition:all .25s;
}
.finp:focus{border-color:var(--gold2);background:rgba(201,149,76,.1);box-shadow:0 0 0 3px rgba(201,149,76,.15)}
.btn-submit{
  width:100%;padding:15px;margin-top:22px;
  font-size:12px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
  border:none;border-radius:var(--r-sm);cursor:pointer;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);transition:all .25s;
  box-shadow:0 6px 20px rgba(201,149,76,.4);
}
.btn-submit:hover{background:linear-gradient(135deg,var(--gold2),var(--gold3));box-shadow:0 8px 28px rgba(201,149,76,.5)}
.link-btn{
  background:none;border:none;cursor:pointer;
  font-size:12px;color:var(--gold2);
  text-decoration:underline;text-underline-offset:3px;
  margin-top:12px;display:block;width:100%;text-align:center;transition:color .2s;
}
.link-btn:hover{color:var(--gold3)}
.msg-err{background:rgba(200,60,50,.1);border:1px solid rgba(200,60,50,.25);border-radius:var(--r-sm);padding:11px 16px;font-size:12px;color:#e87a6a;margin-top:14px}
.msg-ok{background:rgba(30,180,80,.1);border:1px solid rgba(30,180,80,.22);border-radius:var(--r-sm);padding:11px 16px;font-size:12px;color:#5ae09a;margin-top:14px}

/* ── PAYMENT ── */
.pay-outer{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;background:var(--ink2)}
.pay-box{
  max-width:480px;width:100%;
  background:linear-gradient(160deg,rgba(201,149,76,.1),rgba(201,149,76,.03));
  border:1.5px solid var(--border2);border-radius:20px;
  padding:56px;text-align:center;
  box-shadow:var(--shadow);animation:fadeUp .4s ease;
}
.pay-ico{font-size:40px;margin-bottom:22px}
.pay-title{font-family:var(--fd);font-size:31px;color:var(--parch);margin-bottom:14px}
.pay-msg{font-size:13px;color:var(--mist);margin-bottom:16px;line-height:1.65}
.spin{display:inline-block;width:36px;height:36px;border:3px solid rgba(201,149,76,.2);border-top-color:var(--gold2);border-radius:50%;animation:spin .9s linear infinite;margin:16px auto}
.order-pill{
  font-family:'Courier New',monospace;font-size:12px;
  background:rgba(201,149,76,.1);border:1px solid var(--border2);
  border-radius:var(--r-sm);padding:11px 18px;
  color:var(--gold2);margin:12px auto;display:inline-block;
}

/* ── ALL PRODUCTS ── */
.allp-layout{display:grid;grid-template-columns:230px 1fr;height:100%;overflow:hidden}
.allp-sidebar{
  background:linear-gradient(180deg,rgba(201,149,76,.07) 0%,var(--ink2) 100%);
  border-right:1.5px solid var(--border);
  padding:30px 22px;overflow-y:auto;flex-shrink:0;
}
.allp-sidebar::-webkit-scrollbar{width:3px}
.allp-sidebar::-webkit-scrollbar-thumb{background:var(--border2)}
.sidebar-ttl{
  font-size:10px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;
  color:var(--gold2);margin-bottom:22px;
  display:flex;align-items:center;gap:8px;
}
.sidebar-ttl::before{content:'✦';font-size:11px;color:var(--gold3)}
.ss-section{margin-bottom:28px}
.ss-lbl{
  font-size:11px;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;
  color:rgba(201,149,76,.6);margin-bottom:12px;
}
.fchip{
  display:block;width:100%;text-align:left;
  font-size:12px;
  padding:9px 14px;border-radius:var(--r-sm);
  border:1px solid transparent;background:transparent;
  color:var(--mist);cursor:pointer;margin-bottom:3px;
  transition:all .2s;
}
.fchip:hover{color:var(--gold2);background:rgba(201,149,76,.08)}
.fchip.on{
  background:rgba(201,149,76,.14);
  border-color:var(--border2);color:var(--gold2);font-weight:600;
}
.allp-main{display:flex;flex-direction:column;overflow:hidden}
.allp-topbar{
  flex-shrink:0;padding:22px 32px;
  display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--border);
  background:rgba(201,149,76,.04);
}
.allp-count{font-size:12px;color:var(--mist)}
.allp-count strong{color:var(--parch);font-weight:600;font-size:13px}
.allp-grid-wrap{flex:1;min-height:0;padding:26px 32px}
.allp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:18px}

.pagination{
  flex-shrink:0;
  display:flex;align-items:center;justify-content:center;gap:7px;
  padding:18px 32px;border-top:1px solid var(--border);
  background:rgba(201,149,76,.03);
}
.pg-btn{
  min-width:38px;height:38px;padding:0 14px;border-radius:var(--r-sm);
  border:1px solid var(--border);background:rgba(201,149,76,.06);
  color:var(--gold);font-size:12px;font-weight:500;
  cursor:pointer;display:flex;align-items:center;justify-content:center;
  transition:all .2s;
}
.pg-btn:hover:not(:disabled){border-color:var(--gold2);color:var(--gold2);background:rgba(201,149,76,.12)}
.pg-btn.on{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);border-color:transparent;font-weight:700;
}
.pg-btn:disabled{opacity:.28;cursor:default}

/* SKELETON */
.skel{background:rgba(201,149,76,.04);border:1px solid var(--border);border-radius:var(--r);overflow:hidden}
.skel-img{height:210px;background:linear-gradient(90deg,rgba(201,149,76,.04) 25%,rgba(201,149,76,.12) 50%,rgba(201,149,76,.04) 75%);background-size:200% 100%;animation:shimmer 1.6s infinite}
.skel-body{padding:16px}
.skel-line{height:13px;border-radius:4px;margin-bottom:9px;background:linear-gradient(90deg,rgba(201,149,76,.04) 25%,rgba(201,149,76,.12) 50%,rgba(201,149,76,.04) 75%);background-size:200% 100%;animation:shimmer 1.6s infinite}
.skel-line.s{width:55%}

/* ── ORDERS ── */
.o-card{
  background:linear-gradient(145deg,rgba(201,149,76,.07),rgba(201,149,76,.02));
  border:1px solid var(--border);border-radius:var(--r);padding:24px 28px;margin-bottom:14px;
  transition:all .2s;
}
.o-card:hover{border-color:var(--border2);background:rgba(201,149,76,.09)}
.o-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.o-id{
  font-family:'Courier New',monospace;font-size:10px;color:var(--gold);
  background:rgba(201,149,76,.1);padding:4px 11px;border-radius:5px;
  border:1px solid var(--border);
}
.o-status{
  font-size:10px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
  padding:5px 14px;border-radius:999px;
  background:rgba(74,222,128,.1);color:#5ae09a;border:1px solid rgba(74,222,128,.2);
}
.o-items{font-size:12px;color:var(--mist);margin-bottom:10px;line-height:1.5}
.o-total{font-family:var(--fd);font-size:19px;color:var(--parch)}

/* ── ABOUT ── */
.about-layout{flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;overflow:hidden}
.about-left{
  background:
    radial-gradient(ellipse at 25% 35%,rgba(201,149,76,.16),transparent 55%),
    linear-gradient(160deg,#0c0906 0%,#1c1208 100%);
  display:flex;flex-direction:column;justify-content:center;
  padding:64px 56px;border-right:1px solid var(--border2);
}
.about-eyebrow{
  font-size:10px;font-weight:700;letter-spacing:0.24em;text-transform:uppercase;
  color:var(--gold2);margin-bottom:18px;display:flex;align-items:center;gap:10px;
}
.about-eyebrow::before{content:'✦';font-size:11px;color:var(--gold3)}
.about-h{
  font-family:var(--fd);font-size:clamp(32px,2.8vw,46px);
  font-weight:300;line-height:1.08;color:var(--parch);margin-bottom:22px;
}
.about-h em{
  font-style:italic;color:var(--gold2);font-weight:400;
  background:linear-gradient(135deg,var(--gold),var(--gold3));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.about-p{font-size:13px;color:rgba(250,244,235,.6);line-height:1.78;max-width:480px}
.about-right{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border2);overflow:hidden}
.about-panel{
  background:var(--ink2);padding:38px 32px;
  display:flex;flex-direction:column;justify-content:flex-end;
  transition:background .3s;
}
.about-panel:hover{background:rgba(201,149,76,.08)}
.ap-ico{font-size:26px;margin-bottom:auto;padding-bottom:22px}
.ap-title{font-family:var(--fd);font-size:19px;color:var(--parch);margin-bottom:10px}
.ap-text{font-size:12px;color:var(--mist);line-height:1.65}

/* ── CHAT ── */
.chat-fab{position:fixed;bottom:28px;right:28px;z-index:500}
.chat-btn{
  width:58px;height:58px;border-radius:50%;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);border:none;cursor:pointer;font-size:18px;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 8px 32px rgba(201,149,76,.55);
  transition:all .3s;font-weight:700;font-family:var(--fd);
}
.chat-btn:hover{background:linear-gradient(135deg,var(--gold2),var(--gold3));transform:scale(1.08)}
.chat-window{
  position:absolute;bottom:70px;right:0;width:360px;
  background:linear-gradient(180deg,rgba(201,149,76,.06),var(--ink2));
  border:1.5px solid var(--border2);border-radius:20px;
  box-shadow:var(--shadow);overflow:hidden;animation:fadeUp .25s ease;
  display:flex;flex-direction:column;max-height:510px;
}
.chat-head{
  flex-shrink:0;
  background:linear-gradient(135deg,rgba(201,149,76,.2),rgba(201,149,76,.06));
  padding:16px 20px;display:flex;align-items:center;gap:12px;
  border-bottom:1.5px solid var(--border2);
}
.chat-dot{width:9px;height:9px;border-radius:50%;background:#4ade80;box-shadow:0 0 10px rgba(74,222,128,.6)}
.chat-name{font-family:var(--fd);font-size:18px;color:var(--parch)}
.chat-status{font-size:10px;color:rgba(250,244,235,.5);margin-top:2px}
.chat-msgs{
  flex:1;min-height:0;overflow-y:auto;padding:16px;
  display:flex;flex-direction:column;gap:9px;background:rgba(6,4,2,.55);
}
.chat-msgs::-webkit-scrollbar{width:3px}
.chat-msgs::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
.cmsg{font-size:12px;line-height:1.55;padding:11px 15px;border-radius:15px;max-width:86%;animation:fadeIn .2s ease}
.cmsg.bot{background:rgba(201,149,76,.08);border:1px solid var(--border);color:var(--parch2);align-self:flex-start;border-bottom-left-radius:4px}
.cmsg.user{background:linear-gradient(135deg,var(--gold),var(--gold2));color:var(--ink);align-self:flex-end;border-bottom-right-radius:4px;font-weight:600}
.chat-inp-row{
  flex-shrink:0;display:flex;align-items:center;gap:9px;
  padding:12px 16px;border-top:1.5px solid var(--border);background:rgba(6,4,2,.8);
}
.chat-inp{
  flex:1;min-width:0;
  font-size:12px;color:var(--parch);
  background:rgba(201,149,76,.08);border:1.5px solid var(--border);
  border-radius:999px;padding:10px 16px;outline:none;
  transition:border-color .25s;-webkit-appearance:none;appearance:none;
  font-family:var(--fb);
}
.chat-inp:focus{border-color:var(--gold2);background:rgba(201,149,76,.12)}
.chat-send{
  width:36px;height:36px;flex-shrink:0;border-radius:50%;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:var(--ink);border:none;cursor:pointer;font-size:12px;
  display:flex;align-items:center;justify-content:center;transition:all .2s;
}
.chat-send:hover{background:linear-gradient(135deg,var(--gold2),var(--gold3))}
.chat-send:disabled{opacity:.35;cursor:default}

/* ── FOOTER ── */
.footer{
  flex-shrink:0;
  background:linear-gradient(180deg,rgba(201,149,76,.07),rgba(6,4,2,.98));
  border-top:1.5px solid var(--border2);
  text-align:center;padding:14px 40px;
  font-size:10px;letter-spacing:0.06em;
  color:rgba(201,149,76,.55);
  display:flex;align-items:center;justify-content:center;gap:18px;
}
.footer strong{
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  font-weight:700;font-size:12px;
}
.fdot{width:4px;height:4px;border-radius:50%;background:var(--gold);opacity:.4}

/* ── ANIMATIONS ── */
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}

@media(max-width:900px){
  .topbar{padding:0 20px}
  .nb{padding:8px 13px;font-size:10px}
  .home-hero-strip{flex-direction:column;align-items:flex-start;padding:22px 26px}
  .home-hero-right{display:none}
  .home-body{padding:20px 26px}
  .allp-layout{grid-template-columns:1fr}
  .allp-sidebar{display:none}
  .about-layout{grid-template-columns:1fr}
  .about-right{display:none}
  .fp-scroll{padding:26px 22px}
}
`;

export default function App() {
  const [page, setPage] = useState("home");
  const [auth, setAuth] = useState(() => readStorageJson("auth_session", null));
  const [cart, setCart] = useState([]);

  const [prompt, setPrompt] = useState("Suggest elegant party outfits for women");
  const [recs, setRecs] = useState([]);
  const [recText, setRecText] = useState("");
  const [recLoading, setRecLoading] = useState(false);

  const [authMode, setAuthMode] = useState("login");
  const [lf, setLf] = useState({ username: "", password: "" });
  const [sf, setSf] = useState({ username: "", password: "", confirmPassword: "" });
  const [authErr, setAuthErr] = useState("");
  const [authOk, setAuthOk] = useState("");

  const [pay, setPay] = useState({ running: false, success: false, orderId: "", message: "" });

  const [allProds, setAllProds] = useState([]);
  const [allPage, setAllPage] = useState(1);
  const [allTotal, setAllTotal] = useState(0);
  const [allLoading, setAllLoading] = useState(false);
  const [catFilter, setCatFilter] = useState("all");

  const [orders, setOrders] = useState([]);
  const [ordLoading, setOrdLoading] = useState(false);

  const [chatOpen, setChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatBusy, setChatBusy] = useState(false);
  const [chatMsgs, setChatMsgs] = useState([
    { role: "bot", text: "Hi! I'm AIra, your personal style concierge. Ask me anything about products, orders, returns or tracking ✦" }
  ]);
  const chatEndRef = useRef(null);

  const cartKey = useMemo(
    () => auth?.user?.username ? `cart_${auth.user.username}` : "cart_guest",
    [auth?.user?.username]
  );

  useEffect(() => { setCart(readStorageJson(cartKey, [])); }, [cartKey]);
  useEffect(() => { localStorage.setItem(cartKey, JSON.stringify(cart)); }, [cart, cartKey]);
  useEffect(() => { if (chatEndRef.current) chatEndRef.current.scrollIntoView({ behavior: "smooth" }); }, [chatMsgs]);

  const valid = u => u === "admin" || EMAIL_RE.test(u) || MOBILE_RE.test(u);

  async function fetchRecs(e) {
    e?.preventDefault();
    const q = prompt.trim();
    if (!q) return;
    setRecLoading(true);
    setRecs([]);
    setRecText("");
    try {
      const res = await fetch(`${API_BASE}/products/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: q }),
      });
      const d = await parseJsonSafe(res);
      if (!res.ok) {
        const errMsg = d?.detail || d?.message || `Error ${res.status}: Unable to fetch recommendations.`;
        setRecText(errMsg);
        return;
      }
      // Backend returns: { query, model_version, latency_ms, assistant_response, results: [...] }
      const results = Array.isArray(d?.results) ? d.results : [];
      const assistantMsg = d?.assistant_response || "";
      setRecs(results);
      setRecText(assistantMsg);
      if (results.length === 0 && !assistantMsg) {
        setRecText("No matching products found. Try describing a style, occasion, or colour.");
      }
    } catch (err) {
      console.error("fetchRecs error:", err);
      setRecText("Could not reach the recommendation service. Please ensure the backend is running.");
    } finally {
      setRecLoading(false);
    }
  }

  async function fetchAll(pg = 1, cat = catFilter) {
    setAllLoading(true);
    try {
      let url = `${API_BASE}/products?page=${pg}&page_size=9`;
      if (cat !== "all") url += `&category=${cat}`;
      const res = await fetch(url);
      const d = await parseJsonSafe(res);
      if (res.ok) {
        setAllProds(d.items || d.products || d.results || []);
        setAllTotal(d.total_items || d.total || 0);
        setAllPage(d.page || pg);
      } else { setAllProds([]); setAllTotal(0); }
    } catch { setAllProds([]); setAllTotal(0); }
    finally { setAllLoading(false); }
  }

  async function fetchOrders() {
    if (!auth?.access_token) { setPage("login"); setAuthErr("Please login to view orders."); return; }
    setOrdLoading(true);
    try {
      const res = await fetch(`${API_BASE}/orders/me`, { headers: { Authorization: `Bearer ${auth.access_token}` } });
      const d = await parseJsonSafe(res);
      setOrders(Array.isArray(d) ? d : (d.orders || []));
    } catch { setOrders([]); }
    finally { setOrdLoading(false); }
  }

  async function doLogin(e) {
    e.preventDefault(); setAuthErr(""); setAuthOk("");
    const u = lf.username.trim();
    if (!valid(u)) { setAuthErr("Enter valid email, 10-digit mobile, or 'admin'."); return; }
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, password: lf.password }),
    });
    const d = await parseJsonSafe(res);
    if (!res.ok) { setAuthErr(d.detail || "Login failed"); return; }
    setAuth(d); localStorage.setItem("auth_session", JSON.stringify(d)); setPage("home");
  }

  async function doSignup(e) {
    e.preventDefault(); setAuthErr(""); setAuthOk("");
    const u = sf.username.trim();
    if (!valid(u)) { setAuthErr("Enter valid email or 10-digit mobile."); return; }
    if (sf.password.length < 6) { setAuthErr("Password must be 6+ characters."); return; }
    if (sf.password !== sf.confirmPassword) { setAuthErr("Passwords do not match."); return; }
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, password: sf.password }),
    });
    const d = await parseJsonSafe(res);
    if (!res.ok) { setAuthErr(d.detail || "Signup failed"); return; }
    setAuthMode("login"); setLf({ username: u, password: "" });
    setAuthOk("Account created! Please log in.");
  }

  async function forgotPw() {
    setAuthOk(""); setAuthErr("");
    const u = lf.username.trim();
    if (!valid(u)) { setAuthOk("Enter your email/mobile first."); return; }
    const res = await fetch(`${API_BASE}/auth/forgot-password`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u }),
    });
    const d = await parseJsonSafe(res);
    setAuthOk(d.temp_password ? `Temp password: ${d.temp_password}` : d.message || "Done.");
  }

  function logout() { localStorage.removeItem("auth_session"); setAuth(null); setPage("home"); }
  function addCart(item) { if (cart.some(x => x.id === item.id)) return; setCart(p => [...p, item]); }
  function remCart(id) { setCart(p => p.filter(x => x.id !== id)); }

  async function checkout() {
    if (!auth?.access_token) { setPage("login"); setAuthErr("Please login to checkout."); return; }
    if (!cart.length) return;
    const items = cart.map(x => ({ id: x.id, product_name: x.product_name, price: Number(x.price), quantity: 1, image_url: x.image_url || "" }));
    setPage("payment");
    setPay({ running: true, success: false, orderId: "", message: "Processing…" });
    setTimeout(async () => {
      const res = await fetch(`${API_BASE}/orders/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${auth.access_token}` },
        body: JSON.stringify({ items }),
      });
      const d = await parseJsonSafe(res);
      if (!res.ok) { setPay({ running: false, success: false, orderId: "", message: d.detail || "Failed" }); return; }
      setCart([]);
      setPay({ running: false, success: true, orderId: d.order_id, message: "Payment successful!" });
    }, 5000);
  }

  async function sendChat(e) {
    e?.preventDefault();
    const t = chatInput.trim(); if (!t || chatBusy) return;
    setChatMsgs(p => [...p, { role: "user", text: t }]);
    setChatInput(""); setChatBusy(true);
    try {
      const headers = { "Content-Type": "application/json" };
      if (auth?.access_token) headers.Authorization = `Bearer ${auth.access_token}`;
      const res = await fetch(`${API_BASE}/chat/ask`, { method: "POST", headers, body: JSON.stringify({ message: t }) });
      const d = await parseJsonSafe(res);
      setChatMsgs(p => [...p, { role: "bot", text: d.answer || d.detail || "No response." }]);
    } catch { setChatMsgs(p => [...p, { role: "bot", text: "Service unavailable." }]); }
    finally { setChatBusy(false); }
  }

  function goAllProds() { setPage("allproducts"); if (!allProds.length) fetchAll(1, "all"); }

  const totalPages = Math.ceil(allTotal / 9);

  function PCard({ item, showScore = false }) {
    const n = normalizeItem(item);
    const inCart = cart.some(x => x.id === n.id);
    return (
      <article className="pcard">
        <div className="pcard-img">
          {showScore && item.similarity_score && <span className="score-pill">✦ {Number(item.similarity_score).toFixed(3)}</span>}
          <img src={n.image_url || imgFallback(n.product_name, n.color)} alt={n.product_name}
            onError={e => { e.currentTarget.src = imgFallback(n.product_name, n.color); }} />
          <div className="pcard-overlay">
            <button className="btn-sm" onClick={() => addCart(n)}>{inCart ? "✓ In Cart" : "+ Add to Cart"}</button>
          </div>
        </div>
        <div className="pcard-body">
          <div className="ptags">
            {n.brand && <span className="ptag">{n.brand}</span>}
            {n.color && <span className="ptag">{n.color}</span>}
            {n.category && <span className="ptag">{n.category}</span>}
          </div>
          <div className="pname">{n.product_name}</div>
          <div className="pdesc">{n.short_description}</div>
          <div className="pfoot">
            <div className="pprice"><span>INR</span>{Number(n.price).toLocaleString("en-IN", { minimumFractionDigits: 2 })}</div>
            <button className="btn-sm" onClick={() => addCart(n)}>{inCart ? "✓" : "+ Cart"}</button>
          </div>
        </div>
      </article>
    );
  }

  const CATS = ["all","traditional","party","baby","beachwear","trendy","linen","casual","sportswear","formal","winterwear"];

  return (
    <>
      <style>{S}</style>
      <div className="shell">
        <div className="gold-line" />

        {/* TOPBAR */}
        <header className="topbar">
          <div className="logo-wrap" onClick={() => setPage("home")}>
            <div className="logo-main">AIra <span>Styles</span></div>
            <div className="logo-sub">Luxury AI Curation</div>
          </div>
          <nav className="nav">
            <button className={`nb ${page==="home"?"on":""}`} onClick={() => setPage("home")}>Home</button>
            <button className={`nb ${page==="about"?"on":""}`} onClick={() => setPage("about")}>About</button>
            <button className={`nb ${page==="allproducts"?"on":""}`} onClick={goAllProds}>All Products</button>
            <button className={`nb ${page==="orders"?"on":""}`} onClick={() => { setPage("orders"); fetchOrders(); }}>Orders</button>
            <button className={`nb cart-nb ${page==="cart"?"on":""}`} onClick={() => setPage("cart")}>
              🛍 Cart {cart.length > 0 && <span className="cart-badge">{cart.length}</span>}
            </button>
            {!auth
              ? <button className={`nb ${page==="login"?"on":""}`} onClick={() => setPage("login")}>Login</button>
              : <button className="nb" onClick={logout} title={`Logged in as ${auth?.user?.username}`}>Logout</button>
            }
          </nav>
        </header>

        {/* HOME */}
        {page === "home" && (
          <div className="home-layout page-area">
            {/* Hero strip across the top */}
            <div className="home-hero-strip">
              <div className="home-hero-left">
                <div className="kicker">AIra — Luxury Shopping Concierge</div>
                <h1 className="hero-h">Discover your <em>perfect style</em></h1>
                <p className="hero-sub">Styled by AIra. Curated for your mood, occasion, and budget with a refined editorial touch.</p>
                <div className="brand-row">{TOP_BRANDS.map(b => <span key={b} className="bchip">{b}</span>)}</div>
              </div>
              <div className="home-hero-right">
                <div className="stat-col"><div className="stat-n">1.5K+</div><div className="stat-l">Products</div></div>
                <div className="stat-div"/>
                <div className="stat-col"><div className="stat-n">10</div><div className="stat-l">Categories</div></div>
                <div className="stat-div"/>
                <div className="stat-col"><div className="stat-n">5★</div><div className="stat-l">Rated</div></div>
              </div>
            </div>

            {/* Prompt + recs body */}
            <div className="home-body">
              <div className="prompt-card">
                <div className="prompt-lbl">Ask AIra Styles</div>
                <textarea className="prompt-ta" rows={2} value={prompt} onChange={e => setPrompt(e.target.value)}
                  placeholder="e.g. Elegant sarees for a wedding guest…"
                  onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); fetchRecs(); } }} />
                <div className="prompt-row">
                  <span className="prompt-hint">↵ Enter to curate · Shift+Enter for new line</span>
                  <div style={{ display:"flex", gap:"7px" }}>
                    {(recs.length > 0 || recText) && (
                      <button className="btn-dark" onClick={() => { setRecs([]); setRecText(""); setPrompt(""); }}>✕ Clear</button>
                    )}
                    <button className="btn-gold" onClick={fetchRecs} disabled={recLoading}>
                      {recLoading ? "Curating…" : "✦ Curate"}
                    </button>
                  </div>
                </div>
              </div>

              <div className="recs-zone">
                {/* results: scrollable inner */}
                {(recLoading || recText || recs.length > 0) ? (
                  <div className="recs-inner">
                    {recLoading && (
                      <div className="pgrid">
                        {Array.from({length:6}).map((_,i) => (
                          <div key={i} className="skel"><div className="skel-img"/><div className="skel-body"><div className="skel-line"/><div className="skel-line s"/></div></div>
                        ))}
                      </div>
                    )}
                    {!recLoading && recText && (
                      <div className="aira-banner">
                        <div className="aira-icon">A</div>
                        <div className="aira-text"><strong>AIra says</strong>{recText}</div>
                      </div>
                    )}
                    {!recLoading && recs.length > 0 && (
                      <div className="pgrid">{recs.map(item => <PCard key={item.id} item={item} showScore />)}</div>
                    )}
                  </div>
                ) : (
                  /* empty: perfectly centered between prompt card and footer */
                  <div className="recs-centered">
                    <div className="recs-spacer-top" />
                    <div className="empty-recs">
                      <div className="empty-recs-ico">✦</div>
                      <div className="empty-recs-title">AIra awaits</div>
                      <div className="empty-recs-sub">Describe a style, occasion, or mood — AIra will curate the perfect look.</div>
                    </div>
                    <div className="recs-spacer-bot" />
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ABOUT */}
        {page === "about" && (
          <div className="about-layout page-area">
            <div className="about-left">
              <div className="about-eyebrow">Our Story</div>
              <h2 className="about-h">We're building<br />the future of<br /><em>personal style</em></h2>
              <p className="about-p">AIra Styles delivers hyper-personalized product recommendations by understanding your style, occasion, budget, and preferences — in real time. Think of it as your own luxury personal shopper, always on call.</p>
            </div>
            <div className="about-right">
              {[
                {ico:"✦",title:"AIra-Powered Discovery",text:"Ask by occasion, mood, or style. AIra understands context and delivers curated results instantly."},
                {ico:"🎨",title:"Personalized Curation",text:"Every recommendation tailored to you, ensuring you find exactly what suits your unique taste."},
                {ico:"⚡",title:"Lightning Fast",text:"Real-time vector search and AI inference deliver your results in under a second."},
                {ico:"🛡",title:"Secure & Trusted",text:"Enterprise-grade security protects your data and transactions. Shop with confidence."},
              ].map(p => (
                <div key={p.title} className="about-panel">
                  <div className="ap-ico">{p.ico}</div>
                  <div className="ap-title">{p.title}</div>
                  <p className="ap-text">{p.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CART */}
        {page === "cart" && (
          <div className="fp page-area">
            <div className="fp-scroll scroll-y">
              <div className="fp-hdr">
                <div><div className="fp-title">Your Cart</div><div className="fp-sub">{cart.length} item{cart.length!==1?"s":""} selected</div></div>
              </div>
              {!auth && <div className="guest-bar">ℹ️ Add freely as guest — login required only at checkout.</div>}
              {cart.length === 0 ? (
                <div className="empty">
                  <div className="empty-ico">🛍</div>
                  <div className="empty-t">Your cart is empty</div>
                  <div className="empty-s">Let AIra find you something beautiful.</div>
                  <button className="btn-gold" onClick={() => setPage("home")}>✦ Explore Now</button>
                </div>
              ) : (
                <>
                  <div className="cart-list">
                    {cart.map(item => (
                      <div key={item.id} className="cart-item">
                        <div className="ci-thumb">🛍</div>
                        <div className="ci-info">
                          <div className="ci-name">{item.product_name}</div>
                          <div className="ci-price">INR {Number(item.price).toLocaleString("en-IN",{minimumFractionDigits:2})}</div>
                        </div>
                        <button className="btn-danger" onClick={() => remCart(item.id)}>Remove</button>
                      </div>
                    ))}
                  </div>
                  <div className="cart-summary">
                    <div>
                      <div className="cs-lbl">Order Total</div>
                      <div className="cs-amt">INR {cart.reduce((s,x)=>s+Number(x.price||0),0).toLocaleString("en-IN",{minimumFractionDigits:2})}</div>
                    </div>
                    <button className="btn-gold" style={{fontSize:"11.5px",padding:"13px 28px"}} onClick={checkout}>Proceed to Payment →</button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}

        {/* LOGIN */}
        {page === "login" && (
          <div className="login-outer page-area">
            <div className="login-box">
              <div className="l-logo">AIra <span>Styles</span></div>
              <div className="l-tag">Your luxury fashion destination, guided by AIra</div>
              <div className="tabs-row">
                <button className={`tab ${authMode==="login"?"on":""}`} onClick={()=>{setAuthMode("login");setAuthErr("");setAuthOk("");}}>Login</button>
                <button className={`tab ${authMode==="signup"?"on":""}`} onClick={()=>{setAuthMode("signup");setAuthErr("");setAuthOk("");}}>Sign Up</button>
              </div>
              {authMode === "login" ? (
                <form onSubmit={doLogin}>
                  <div className="field"><label className="flbl">Email / Mobile / Username</label><input className="finp" placeholder="you@example.com" value={lf.username} onChange={e=>setLf(p=>({...p,username:e.target.value}))}/></div>
                  <div className="field"><label className="flbl">Password</label><input className="finp" type="password" placeholder="••••••••" value={lf.password} onChange={e=>setLf(p=>({...p,password:e.target.value}))}/></div>
                  <button type="submit" className="btn-submit">Login</button>
                  <button type="button" className="link-btn" onClick={forgotPw}>Forgot password?</button>
                </form>
              ) : (
                <form onSubmit={doSignup}>
                  <div className="field"><label className="flbl">Email or Mobile</label><input className="finp" placeholder="you@example.com" value={sf.username} onChange={e=>setSf(p=>({...p,username:e.target.value}))}/></div>
                  <div className="field"><label className="flbl">Password</label><input className="finp" type="password" placeholder="At least 6 characters" value={sf.password} onChange={e=>setSf(p=>({...p,password:e.target.value}))}/></div>
                  <div className="field"><label className="flbl">Confirm Password</label><input className="finp" type="password" placeholder="Repeat password" value={sf.confirmPassword} onChange={e=>setSf(p=>({...p,confirmPassword:e.target.value}))}/></div>
                  <button type="submit" className="btn-submit">Create Account</button>
                </form>
              )}
              {authErr && <div className="msg-err">{authErr}</div>}
              {authOk && <div className="msg-ok">{authOk}</div>}
            </div>
          </div>
        )}

        {/* PAYMENT */}
        {page === "payment" && (
          <div className="pay-outer page-area">
            <div className="pay-box">
              {pay.running ? (<><div className="pay-ico">🔒</div><div className="pay-title">Processing</div><div className="pay-msg">Securing your order…</div><div className="spin"/></>)
              : pay.success ? (<><div className="pay-ico">✅</div><div className="pay-title">Order Confirmed!</div><div className="pay-msg">Thank you. Your order is on its way.</div><div className="order-pill">Order: {pay.orderId}</div><div style={{marginTop:"22px"}}><button className="btn-gold" onClick={()=>setPage("home")}>Continue Shopping</button></div></>)
              : (<><div className="pay-ico">❌</div><div className="pay-title">Payment Failed</div><div className="pay-msg">{pay.message}</div><div style={{marginTop:"22px"}}><button className="btn-gold" onClick={()=>setPage("cart")}>← Back to Cart</button></div></>)}
            </div>
          </div>
        )}

        {/* ALL PRODUCTS */}
        {page === "allproducts" && (
          <div className="allp-layout page-area">
            <div className="allp-sidebar">
              <div className="sidebar-ttl">Filters</div>
              <div className="ss-section">
                <div className="ss-lbl">Category</div>
                {CATS.map(c=>(
                  <button key={c} className={`fchip ${catFilter===c?"on":""}`} onClick={()=>{setCatFilter(c);fetchAll(1,c);}}>
                    {c==="all"?"All Categories":c.charAt(0).toUpperCase()+c.slice(1)}
                  </button>
                ))}
              </div>
            </div>
            <div className="allp-main">
              <div className="allp-topbar">
                <div className="allp-count">
                  {allLoading ? "Loading…" : <><strong>{allTotal}</strong> products {catFilter!=="all"?`in ${catFilter}`:""}</>}
                </div>
                <div style={{fontSize:"11.5px",color:"var(--mist)"}}>
                  {totalPages > 1 && `Page ${allPage} of ${totalPages}`}
                </div>
              </div>
              <div className="allp-grid-wrap scroll-y">
                {allLoading ? (
                  <div className="allp-grid">
                    {Array.from({length:9}).map((_,i)=>(
                      <div key={i} className="skel"><div className="skel-img"/><div className="skel-body"><div className="skel-line"/><div className="skel-line s"/></div></div>
                    ))}
                  </div>
                ) : allProds.length === 0 ? (
                  <div className="empty" style={{height:"100%"}}>
                    <div className="empty-ico">📦</div><div className="empty-t">No products found</div><div className="empty-s">Try a different filter</div>
                  </div>
                ) : (
                  <div className="allp-grid">{allProds.map(item=><PCard key={item.id} item={item}/>)}</div>
                )}
              </div>
              {totalPages > 1 && (
                <div className="pagination">
                  <button className="pg-btn" disabled={allPage===1} onClick={()=>fetchAll(allPage-1,catFilter)}>← Prev</button>
                  {Array.from({length:totalPages},(_,i)=>i+1)
                    .filter(p=>p===1||p===totalPages||Math.abs(p-allPage)<=2)
                    .reduce((acc,p,idx,arr)=>{if(idx>0&&p-arr[idx-1]>1)acc.push("…");acc.push(p);return acc;},[])
                    .map((p,i)=>p==="…"
                      ?<span key={`e${i}`} style={{color:"var(--mist)",padding:"0 4px"}}>…</span>
                      :<button key={p} className={`pg-btn ${p===allPage?"on":""}`} onClick={()=>fetchAll(p,catFilter)}>{p}</button>
                    )}
                  <button className="pg-btn" disabled={allPage===totalPages} onClick={()=>fetchAll(allPage+1,catFilter)}>Next →</button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ORDERS */}
        {page === "orders" && (
          <div className="fp page-area">
            <div className="fp-scroll scroll-y">
              <div className="fp-hdr">
                <div><div className="fp-title">My Orders</div><div className="fp-sub">Track and review your past purchases</div></div>
              </div>
              {ordLoading ? (
                <div style={{textAlign:"center",padding:"60px",color:"var(--mist)"}}>
                  <div className="spin" style={{margin:"0 auto 13px"}}/><p>Loading orders…</p>
                </div>
              ) : orders.length === 0 ? (
                <div className="empty">
                  <div className="empty-ico">📋</div><div className="empty-t">No orders yet</div>
                  <div className="empty-s">Your purchase history will appear here.</div>
                  <button className="btn-gold" onClick={()=>setPage("home")}>✦ Start Shopping</button>
                </div>
              ) : orders.map((o,i)=>(
                <div key={o.order_id||o.id||i} className="o-card">
                  <div className="o-head">
                    <span className="o-id">#{o.order_id||o.id||`ORD-${i+1}`}</span>
                    <span className="o-status">{o.status||"Confirmed"}</span>
                  </div>
                  <div className="o-items">
                    {(o.items||[]).map((x,j)=><span key={j}>{x.product_name}{j<(o.items?.length||0)-1?", ":""}</span>)}
                    {(!o.items||!o.items.length)&&"—"}
                  </div>
                  <div className="o-total">INR {Number(o.total||o.total_amount||0).toLocaleString("en-IN",{minimumFractionDigits:2})}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* FOOTER */}
        <footer className="footer">
          <strong>AIra Styles</strong>
          <span className="fdot"/>
          <span>Luxury AI Fashion Curation</span>
          <span className="fdot"/>
          <span>© {new Date().getFullYear()}</span>
        </footer>

        {/* CHAT — only on all products page */}
        {page === "allproducts" && (
          <div className="chat-fab">
            {chatOpen && (
              <div className="chat-window">
                <div className="chat-head">
                  <div className="chat-dot"/>
                  <div>
                    <div className="chat-name">AIra</div>
                    <div className="chat-status">Your personal style concierge · Always online</div>
                  </div>
                </div>
                <div className="chat-msgs">
                  {chatMsgs.map((m,i)=><div key={i} className={`cmsg ${m.role}`}>{m.text}</div>)}
                  <div ref={chatEndRef}/>
                </div>
                <div className="chat-inp-row">
                  <input className="chat-inp" value={chatInput} onChange={e=>setChatInput(e.target.value)}
                    placeholder="Ask AIra anything…"
                    onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendChat(e);}}}/>
                  <button className="chat-send" onClick={sendChat} disabled={chatBusy}>{chatBusy?"…":"→"}</button>
                </div>
              </div>
            )}
            <button className="chat-btn" onClick={()=>setChatOpen(s=>!s)} title="Chat with AIra">
              {chatOpen?"✕":"✦"}
            </button>
          </div>
        )}
      </div>
    </>
  );
}
