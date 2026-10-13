#!/usr/bin/env python3
"""devbase builder: links/**/*.md  ->  docs/index.html + docs/data.json

Usage:  python3 build.py
Никаких зависимостей — только stdlib.
"""
import os, re, json, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
LINKS = os.path.join(ROOT, "links")
DOCS = os.path.join(ROOT, "docs")

CATS = {
    "design": "Дизайн и UI", "fonts": "Шрифты", "ai": "AI-модели и API",
    "images": "Изображения", "voice": "Голос и TTS", "music": "Музыка и звук",
    "payments": "Платежи", "hosting": "Хостинг и деплой", "infra": "Базы и бэкенд",
    "proxies": "Прокси и аккаунты", "code": "Код и инструменты",
    "no-code": "No-code и боты", "learning": "Обучение", "utils": "Утилиты",
    "seo": "SEO и аналитика", "affiliate": "Affiliate и трафик",
    "scraping": "Парсинг и автоматизация", "video": "Видео и аватары",
    "chat": "Чаты и боты", "misc": "Разное",
}
ORDER = list(CATS.keys())


def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
    if not m:
        return None
    fm, body = m.group(1), m.group(2)
    d = {}
    for line in fm.splitlines():
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if not k:
            continue
        if v.startswith("[") and v.endswith("]"):
            d[k] = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
        else:
            d[k] = v
    d["body"] = body.strip()
    d["path"] = os.path.relpath(path, ROOT)
    return d


def collect():
    out = []
    for dirpath, _, files in os.walk(LINKS):
        for f in files:
            if not f.endswith(".md"):
                continue
            it = parse(os.path.join(dirpath, f))
            if it and it.get("url"):
                it.setdefault("category", "misc")
                it.setdefault("tags", [])
                it.setdefault("title", f[:-3])
                it["tags"] = it["tags"] if isinstance(it["tags"], list) else [it["tags"]]
                out.append(it)
    out.sort(key=lambda x: (ORDER.index(x["category"]) if x["category"] in ORDER else 99,
                            x["title"].lower()))
    return out


def domain(url):
    return re.sub(r"^https?://(www\.)?", "", url).split("/")[0]


HTML = """<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DEVBASE — база ссылок для веб-разработки</title>
<meta name="description" content="Открытая база сервисов и инструментов: шрифты, дизайн, AI, голос, платежи, хостинг, прокси.">
<style>
:root{--ink:#0a0a0a;--line:#0a0a0a;--bg:#ffffff;--muted:#6b6b6b;--soft:#f4f4f2;--acc:#ff3b00}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
 -webkit-text-size-adjust:100%}
.wrap{max-width:1180px;margin:0 auto;padding:22px 16px 80px}
header{border-bottom:3px solid var(--line);padding-bottom:18px;margin-bottom:20px}
h1{font:800 clamp(30px,7vw,58px)/0.95 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:-2px;text-transform:uppercase}
.sub{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin-top:10px;font-size:13px;color:var(--muted)}
.sub b{color:var(--ink)}
.tagline{margin-top:12px;font-size:14px;max-width:70ch}
.bar{position:sticky;top:0;background:var(--bg);border-bottom:2px solid var(--line);padding:12px 0;z-index:9;margin-bottom:16px}
input[type=search]{width:100%;font:16px ui-monospace,Menlo,monospace;padding:13px 14px;border:2px solid var(--line);
 background:var(--bg);color:var(--ink);outline:none}
input[type=search]:focus{background:#fffdf7;box-shadow:4px 4px 0 var(--line)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 4px}
.chip{font:600 12px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.5px;padding:7px 12px;
 border:2px solid var(--line);background:var(--bg);cursor:pointer;user-select:none;
 clip-path:polygon(7px 0,100% 0,100% calc(100% - 7px),calc(100% - 7px) 100%,0 100%,0 7px)}
.chip.on{background:var(--ink);color:#fff}
.chip span{opacity:.5}
.count{font:600 12px ui-monospace,Menlo,monospace;color:var(--muted);margin:14px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
.card{display:block;border:2px solid var(--line);background:var(--bg);padding:14px 15px;color:inherit;
 text-decoration:none;transition:transform .08s,box-shadow .08s}
.card:hover{transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--line)}
.card h3{font-size:16px;font-weight:800;letter-spacing:-.2px;display:flex;gap:8px;justify-content:space-between;align-items:baseline}
.dom{font:600 11px ui-monospace,Menlo,monospace;color:var(--acc);white-space:nowrap}
.cat{display:inline-block;font:700 10px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.6px;
 border:1px solid var(--line);padding:2px 6px;margin:8px 0 6px;background:var(--soft)}
.card p{font-size:13.5px;color:#242424;margin-bottom:10px}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.t{font:600 10.5px ui-monospace,Menlo,monospace;color:var(--muted);border:1px dashed #c9c9c9;padding:2px 6px}
.empty{border:2px dashed var(--line);padding:34px;text-align:center;font:600 14px ui-monospace,Menlo,monospace}
footer{margin-top:44px;border-top:3px solid var(--line);padding-top:16px;font-size:12.5px;color:var(--muted)}
footer a{color:var(--ink)}
code{font:600 12px ui-monospace,Menlo,monospace;background:var(--soft);padding:2px 5px;border:1px solid #e2e2e2}
@media(max-width:520px){.grid{grid-template-columns:1fr}.wrap{padding:16px 12px 60px}}
</style></head><body><div class="wrap">
<header>
 <h1>Devbase</h1>
 <div class="sub"><b id="total"></b> <span>записей</span> · <span id="cats"></span> <span>категорий</span>
 · <span>обновлено <b id="upd"></b></span></div>
 <p class="tagline">Открытая база сервисов, инструментов и ссылок для веб-разработки.
 Копится из чатов: кидаешь ссылку агенту — она попадает в нужную категорию.
 Люди открывают сайт, агенты читают <code>docs/data.json</code>.</p>
</header>
<div class="bar">
 <input type="search" id="q" placeholder="поиск: шрифт, tts, платёжка, прокси, sitemap..." autocomplete="off">
 <div class="chips" id="chips"></div>
</div>
<div class="count" id="count"></div>
<div class="grid" id="grid"></div>
<footer>
 Репозиторий: <a href="https://github.com/zajacdn/devbase">github.com/zajacdn/devbase</a> ·
 машинный индекс: <a href="data.json">data.json</a> ·
 формат: Obsidian-vault (<code>links/&lt;категория&gt;/&lt;слаг&gt;.md</code>)<br>
 Добавить запись: кинуть ссылку агенту Hermes или сделать PR с новым .md + <code>python3 build.py</code>.
</footer>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const CATS = __CATS__;
let active = 'all', q = '';
const el = id => document.getElementById(id);
function render(){
  const needle = q.trim().toLowerCase();
  const rows = DATA.filter(d => {
    if(active !== 'all' && d.category !== active) return false;
    if(!needle) return true;
    return (d.title+' '+d.url+' '+d.category+' '+(d.note||'')+' '+(d.tags||[]).join(' ')).toLowerCase().includes(needle);
  });
  el('count').textContent = 'Показано ' + rows.length + ' из ' + DATA.length;
  el('grid').innerHTML = rows.length ? rows.map(d => `
    <a class="card" href="${d.url}" target="_blank" rel="noopener">
      <h3>${esc(d.title)}<span class="dom">${esc(dom(d.url))}</span></h3>
      <div class="cat">${esc(CATS[d.category]||d.category)}</div>
      <p>${esc(d.note||'')}</p>
      <div class="tags">${(d.tags||[]).map(t=>`<span class="t">${esc(t)}</span>`).join('')}</div>
    </a>`).join('') : '<div class="empty">Ничего не найдено</div>';
}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function dom(u){return String(u).replace(/^https?:\\/\\/(www\\.)?/,'').split('/')[0];}
function chips(){
  const counts = {}; DATA.forEach(d => counts[d.category] = (counts[d.category]||0)+1);
  const list = Object.keys(CATS).filter(c => counts[c]).map(c => [c,counts[c]]);
  el('chips').innerHTML = `<div class="chip on" data-c="all">Все <span>${DATA.length}</span></div>` +
    list.map(([c,n]) => `<div class="chip" data-c="${c}">${CATS[c]} <span>${n}</span></div>`).join('');
  el('chips').querySelectorAll('.chip').forEach(ch => ch.onclick = () => {
    active = ch.dataset.c;
    el('chips').querySelectorAll('.chip').forEach(x => x.classList.toggle('on', x === ch));
    render();
  });
}
el('q').oninput = e => { q = e.target.value; render(); };
el('total').textContent = DATA.length;
el('cats').textContent = new Set(DATA.map(d=>d.category)).size;
el('upd').textContent = __UPD__;
chips(); render();
</script></body></html>
"""


def main():
    items = collect()
    os.makedirs(DOCS, exist_ok=True)
    clean = [{k: v for k, v in it.items() if k != "body"} for it in items]
    data = json.dumps(clean, ensure_ascii=False, indent=1)
    open(os.path.join(DOCS, "data.json"), "w", encoding="utf-8").write(data)
    upd = datetime.date.today().isoformat()
    out = (HTML.replace("__DATA__", data)
               .replace("__CATS__", json.dumps(CATS, ensure_ascii=False))
               .replace("__UPD__", json.dumps(upd)))
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(out)
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print(f"built: {len(items)} записей, {len({i['category'] for i in items})} категорий -> docs/")


if __name__ == "__main__":
    main()
