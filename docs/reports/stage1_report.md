# Этап 1 — Окружение и данные

## Что сделано

### Настройка окружения
- Google Colab Pro+, GPU A100 80 ГБ
- Модели: Qwen2.5-1.5B, Qwen2.5-Math-PRM-7B
- parsing.py: извлечение ответов, сравнение, bootstrap CI

### Подготовка данных
- OpenR1-Math-220k (split default): 93 733 задачи
- Дедупликация (13-gram containment, порог ≥0.5): 4 утечки MATH-500, 0 GSM8K
- Валидационная выборка: 500 задач (seed=0)
- 12 подмножеств: 4 объёма (500, 1000, 2000, 5000) × 3 порога CoT (2048, 4096, 8192)
- Вложенные: 500 ⊂ 1000 ⊂ 2000 ⊂ 5000
- Статистика D_train сохранена: data/manifests/data_stats.json

## Результаты

**Базлайн (Qwen2.5-1.5B без дообучения):**
- GSM8K: acc=0.625 [0.598, 0.651], none_rate=0.1%
- MATH-500: acc=0.276 [0.238, 0.316], none_rate=25.2%
- Промпт: plain text (без ChatML), temperature=0, max_tokens=512
- Парсер: GSM8K — lenient (последнее число), MATH-500 — строгий (\boxed{})
- Результаты: results/baselines/baseline.json

## Проблемы
- MATH-500 none_rate 25.2%: четверть задач без маркера \boxed{} — ожидаемо для base модели без instruction tuning
- Базлайн и SFT eval используют разные протоколы (промпт, парсер, max_tokens) — прямое сравнение accuracy некорректно, отмечено в тексте ВКР
