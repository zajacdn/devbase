#!/usr/bin/env python3
"""Собирает галерею ассетов BlenderKit (категория liquid) в assets/blenderkit-liquid.json.

BlenderKit API публичный: /api/v1/search/?query=category_subtree:liquid&page_size=100
Все 229 ассетов категории — материалы (шейдеры), бесплатные, лицензия royalty-free.
"""
import json, re, time
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
API = "https://www.blenderkit.com/api/v1/search/"
OUT = "/root/devbase/assets/blenderkit-liquid.json"

CATS = {
    "water": "Вода",
    "lava": "Лава",
    "honey": "Мёд и масло",
    "blood": "Кровь",
    "gel": "Гель и слизь",
    "foam": "Пена и пузыри",
    "other": "Прочее",
}
RULES = [
    ("water", ["water", "ocean", "sea", "river", "lake", "pool", "aqua", "rain", "wave", "underwater"]),
    ("lava", ["lava", "magma", "molten", "fire"]),
    ("honey", ["honey", "syrup", "oil", "caramel", "chocolate", "milk"]),
    ("blood", ["blood", "gore"]),
    ("gel", ["gel", "slime", "soap", "goo", "jelly", "paint"]),
    ("foam", ["foam", "bubble", "fizz", "suds"]),
]


def classify(tags):
    low = [t.lower() for t in tags]
    hits = []
    for cat, keys in RULES:
        if any(k in low for k in keys):
            hits.append(cat)
    return hits or ["other"]


def main():
    items, url, seen = [], API + "?query=category_subtree:liquid&page_size=100", set()
    while url:
        j = requests.get(url, headers=UA, timeout=40).json()
        for a in j.get("results") or []:
            if a["assetBaseId"] in seen:
                continue
            seen.add(a["assetBaseId"])
            desc = re.sub(r"<[^>]+>", "", a.get("description") or "").strip()
            author = (a.get("author") or {}).get("fullName") or "BlenderKit"
            items.append({
                "id": a["assetBaseId"],
                "title": a.get("displayName") or a.get("name") or "Без названия",
                "prompt": desc[:220] or "Процедурный материал Blender",
                "handle": author,
                "poster": a.get("thumbnailMiddleUrlWebp") or a.get("thumbnailMiddleUrl"),
                "url": f"https://www.blendkit.com/asset-gallery-detail/{a['assetBaseId']}/",
                "cats": classify(a.get("tags") or []),
                "views": f"{(a.get('ratingsCount') or {}).get('bookmarks', 0)} в закладках",
                "tags": (a.get("tags") or [])[:4],
            })
        url = j.get("next")
        print(len(items), "/", j.get("count"), flush=True)
        time.sleep(1)

    items.sort(key=lambda x: -int((x["views"].split() or ["0"])[0]))
    cats = {k: v for k, v in CATS.items() if any(k in i["cats"] for i in items)}
    doc = {
        "slug": "blenderkit-liquid",
        "title": "BlenderKit — жидкости",
        "note": "229 процедурных материалов: вода, лава, мёд, кровь, гель, пена. Всё бесплатно, royalty-free. Превью и переход на ассет.",
        "source_label": "BlenderKit · API",
        "kind": "assets",
        "cats": cats,
        "items": items,
    }
    json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", OUT, len(items))


if __name__ == "__main__":
    main()
