"""
SFT-обучение Qwen2.5-1.5B на CoT-решениях от DeepSeek-R1.

    check_disk_space(path, min_gb=10)
        Проверяет свободное место перед обучением.

    train_sft(config) -> Path
        Загружает данные, настраивает LoRA, запускает HF Trainer
        с resume_from_checkpoint. Возвращает путь к checkpoint.
"""
