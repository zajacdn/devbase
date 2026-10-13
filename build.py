#!/usr/bin/env python3
"""devbase builder: links/**/*.md + template.html  ->  docs/index.html + docs/data.json

Usage:  python3 build.py
Никаких зависимостей — только stdlib.
"""
import os, re, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
LINKS = os.path.join(ROOT, "links")
DOCS = os.path.join(ROOT, "docs")
TEMPLATE = os.path.join(ROOT, "template.html")

CATS = {
    "design": "Дизайн и UI", "fonts": "Шрифты", "ai": "AI-модели и API",
    "images": "Изображения", "voice": "Голос и TTS", "music": "Музыка и звук",
    "video": "Видео и аватары", "payments": "Платежи", "hosting": "Хостинг и деплой",
    "infra": "Базы и бэкенд", "proxies": "Прокси и аккаунты", "scraping": "Парсинг и автоматизация",
    "code": "Код и инструменты", "no-code": "No-code и боты", "chat": "Чаты и боты",
    "seo": "SEO и аналитика", "affiliate": "Affiliate и трафик", "learning": "Обучение",
    "utils": "Утилиты", "misc": "Разное",
}
ORDER = list(CATS.keys())


def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
    if not m:
        return None
    fm = m.group(1)
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


def main():
    items = collect()
    os.makedirs(DOCS, exist_ok=True)
    clean = [{k: v for k, v in it.items()} for it in items]
    data = json.dumps(clean, ensure_ascii=False, indent=1)
    open(os.path.join(DOCS, "data.json"), "w", encoding="utf-8").write(data)
    upd = datetime.date.today().strftime("%d.%m.%Y")
    tpl = open(TEMPLATE, encoding="utf-8").read()
    out = (tpl.replace("__DATA__", data)
              .replace("__CATS__", json.dumps(CATS, ensure_ascii=False))
              .replace("__UPD__", json.dumps(upd)))
    open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(out)
    open(os.path.join(DOCS, ".nojekyll"), "w").write("")
    print(f"built: {len(items)} записей, {len({i['category'] for i in items})} категорий -> docs/")


if __name__ == "__main__":
    main()
