"""
Расчёт вычислительных затрат. Формулы из thesis_plan §10.

    compute_sft_flops(params, tokens) -> float
        F = 6 * P * T
        Верхняя оценка для LoRA: forward через всю модель,
        backward через chain rule, обновляется только адаптер.
        Экономия порядка 10-20%. Коэффициент 0.5 занижает вдвое.

    compute_inference_flops(params, tokens_per_solution, n) -> float
        F = 2 * P * T_gen * N

    compute_prm_flops(prm_params, tokens_per_solution, n) -> float
        F = 2 * P_prm * T_eval * N
"""
