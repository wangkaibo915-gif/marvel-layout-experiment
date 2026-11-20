# Iron Man — экспериментальная группа

Страница воспроизводит слайд Iron Man из Pixso при размере **1440 × 1024 px**. В экспериментальной работе применялись SourceCraft Code Assistant, Pixso MCP и Context7 MCP. Реальные обращения к инструментам и результаты проверок перечислены в `docs/ai-interaction-report.md`.

## Состав проекта

- `index.html`, `styles.css`, `assets/` — страница и локальные ресурсы.
- `assets/reference.png`, `reference.html` — экспортированный эталон Pixso.
- `backstop.json`, `backstop_data/` — сценарий и сохранённые результаты визуальных проверок.
- `galen/specs/ironman.gspec`, `galen/tests/ironman.test.js` — сценарии проверки геометрии.
- `docs/sourcecraft-task.md`, `docs/ai-interaction-report.md` — задание агенту и отчёт о фактическом использовании инструментов.

## Запуск

В каталоге проекта выполните `npm ci`. В первом терминале запустите `npm run serve`, во втором — `npm run backstop:test`. Размер проверяемого экрана задан в `backstop.json`: 1440 × 1024 px. Для Galen требуется отдельная установка Galen Framework и ChromeDriver.

**Статус:** сохранённые проверки BackstopJS не прошли порог `0.1 %`; наименьшее подтверждённое расхождение — `11.88 %`. Успешный запуск Galen пока не подтверждён. Не следует представлять эти сценарии как успешно пройденные.
