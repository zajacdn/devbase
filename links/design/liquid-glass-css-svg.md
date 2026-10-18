---
title: "Liquid Glass in the Browser"
url: https://kube.io/blog/liquid-glass-css-svg/
category: design
tags: [css, svg, glassmorphism, effects, tutorial]
added: 2026-10-18
added_by: Гермес
note: "Рецепт эффекта Liquid Glass (как в iOS 26) на CSS + SVG displacement map: преломление по Снеллу, блик. Демо работает в Chrome."
---

# Liquid Glass in the Browser

<https://kube.io/blog/liquid-glass-css-svg/>

Разбор эффекта Liquid Glass из WWDC 2025: как сделать преломление стекла в браузере
на CSS `backdrop-filter` + SVG-фильтрах. Считают физику по закону Снелла (n=1.5),
строят карту смещения, добавляют specular-блик.

- Демо интерактивное, но только в Chrome (SVG-фильтры как backdrop-filter).
- Ограничения оговорены: одна среда (воздух), одно преломление, только круги.
- Готовый POC, который можно расширять на другие формы.
