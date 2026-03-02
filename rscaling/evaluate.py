"""
Оценка модели на бенчмарке.

    eval_model(model_path, dataset, eval_config, limit=None) -> dict
        Загружает модель, генерирует ответы (greedy),
        парсит через extract_answer, считает accuracy и CI.
        Возвращает: accuracy, ci_lower, ci_upper, total,
        correct, mean_cot_length.

Параметры eval передаются снаружи (из base.yaml через ноутбук).
"""
