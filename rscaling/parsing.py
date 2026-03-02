"""
Извлечение ответов из текста модели и расчёт метрик.

    extract_answer(text) -> float | None
        Ищет паттерн #### <число> в CoT-решении.
        Возвращает число или None если маркер не найден.

    accuracy(predictions, targets) -> float
        Доля правильных ответов. None считается ошибкой.

    bootstrap_ci(predictions, targets) -> (mean, lower, upper)
        95%-й доверительный интервал для accuracy.

Перед запуском прогонов обязательны assert-тесты
и ручная проверка на 30 реальных генерациях.
"""
