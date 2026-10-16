---
title: "Originkit"
url: https://www.originkit.dev
category: code
tags: [react, nextjs, ui, animation, framer, cli, threejs]
added: 2026-10-16
added_by: Заяц
note: "Библиотека анимированных компонентов и секций для React/Next.js и Framer: `npx originkit@latest add <name>` кладёт исходник в проект. Нужен аккаунт, есть дневная квота на установки."
---

# Originkit

Каталог готовых анимированных UI-компонентов, секций и шаблонов. Работает по принципу shadcn:
исходник приезжает в проект, а не подключается как зависимость.

- Сайт: https://www.originkit.dev
- CLI: `npx originkit@latest add <component>` (React, Next.js, Vite, Framer)
- Просмотр и тюнинг контролов — бесплатно, квота тратится только на установку/копирование кода
- Авторизация: `npx originkit login` (браузер) или `ORIGINKIT_API_KEY` для агентов и CI

Пример: `npx originkit@latest add still-sunset-meadow` — воксельный луг на закате на three.js
(инстансинг, GPU depth-of-field, day-night цикл).
