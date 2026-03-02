"""
GRPO-дообучение лучших SFT-моделей.

    train_grpo(config, reward_fn) -> Path
        Загружает SFT-checkpoint, запускает TRL GRPOTrainer.
        reward_fn передаётся снаружи.
        Полный режим (2000 шагов) для vol 500 и 5000,
        укороченный (500 шагов) для vol 1000 и 2000.
"""
