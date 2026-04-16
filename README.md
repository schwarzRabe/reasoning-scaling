# reasoning-scaling
 
Сравнительный анализ методов повышения качества рассуждений компактных языковых моделей на этапах обучения и инференса. Магистерская ВКР, МИФИ, 2026.
 
## Пайплайн
 
```
00_setup       — окружение, модели, тесты
01_data_prep   — данные, дедупликация, baseline
02_sft         — 36 SFT-прогонов (4 объёма × 3 порога CoT × 3 seed)
03_grpo        — выбор лучших SFT-моделей, merge адаптера, GRPO
04_inference   — генерация n=32, majority voting, best-of-N, weighted voting
05_analysis    — FLOPs расчёт, Парето-фронт, графики
```
 
Запуск последовательный: 00 → 01 → 02 → 03 → 04 → 05. Ручной контроль между этапами.
 
## Структура
 
```
rscaling/       общие функции (parsing)
configs/        параметры экспериментов (YAML)
notebooks/      ноутбуки Colab (точки входа)
results/        метрики и логи (git)
data/           датасеты и подмножества (.gitignore)
docs/           текст ВКР и отчёты
```
 
## Модели
 
- **Генератор:** Qwen2.5-1.5B (1,54 × 10⁹ параметров)
- **Верификатор:** Qwen2.5-Math-PRM-7B (7 × 10⁹ параметров)
- **Датасет:** OpenR1-Math-220k (split default, 93 733 задачи)
- **Бенчмарки:** GSM8K test (1319 задач), MATH-500 (500 задач)
 
## Воспроизведение
 
1. Google Colab Pro+ с GPU A100 80 ГБ
2. Скачать модели с HuggingFace
3. Запустить ноутбуки последовательно
 
Параметры экспериментов зафиксированы в `configs/`. Результаты сохраняются на Google Drive с кэшированием и resume.

## Google Drive
https://drive.google.com/drive/folders/1Qq5Nhlb6d_A0ptdI_-6x6bPCIr6FZgWq?usp=drive_link
https://drive.google.com/drive/folders/11Q0MwHX_y_0fd4ngmJ1p4IymsBNULEkP?usp=drive_link
https://drive.google.com/drive/folders/1UhbCTb21tA9dYBz2IvYT869XA5iepfWK?usp=drive_link
