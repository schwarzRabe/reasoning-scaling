"""
Генерация решений и inference-стратегии.

Генерация кэшируется: один раз на (модель, N),
стратегии работают поверх кэша.

    generate(model_path, dataset_path, n, output_path, seed) -> Path
        Генерирует N решений на задачу, сохраняет в JSONL.
        Рядом кладёт .meta.json с параметрами генерации.

    validate_fingerprint(generations_path, expected_model)
        Проверяет, что кэш соответствует ожидаемой модели.

    majority_vote(generations_path) -> dict
    prm_best(generations_path, prm_model_path) -> dict
    weighted_vote(generations_path, prm_model_path) -> dict
"""
