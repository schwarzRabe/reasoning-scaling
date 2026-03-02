"""
Анализ результатов и визуализация.

    select_best(metrics_list) -> dict
        Лучшая модель на каждый volume по accuracy.

    build_pareto(all_metrics) -> list[dict]
        Парето-фронт: точки (FLOPs, accuracy) без доминируемых.

    plot_pareto_front, plot_learning_curves, plot_grpo_convergence

Дополнительно (если хватает времени):
    math500_by_level, generation_diversity, cot_length_vs_accuracy,
    oracle_best_of_n, fit_scaling_law, find_crossover_points,
    error_decomposition
"""
