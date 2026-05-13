import json
import random
from pathlib import Path

from .templates import COLLISION_TEMPLATES

def generate_cases(
    n_per_collision: int = 50,
    seed: int = 404,
    out: str = "datasets/edgecase_benchmark.jsonl",
):
    random.seed(seed)
    rows = []

    for collision_type, spec in COLLISION_TEMPLATES.items():
        for i in range(n_per_collision):
            signals = [
                random.choice(spec["signals_a"]),
                random.choice(spec["signals_b"]),
            ]

            if random.random() < 0.35:
                pool = spec["signals_a"] + spec["signals_b"]
                extra = random.choice(pool)
                if extra not in signals:
                    signals.append(extra)

            prompt = random.choice(spec["prompts"])

            severity = round(random.uniform(0.25, 1.0), 3)
            ambiguity = round(random.uniform(0.15, 1.0), 3)

            rows.append({
                "id": f"{collision_type}_{i:04d}",
                "domain": spec["domain"],
                "collision_type": collision_type,
                "signals": signals,
                "prompt": prompt,
                "expected_mitigation": spec["expected_mitigation"],
                "severity": severity,
                "ambiguity": ambiguity,
            })

    random.shuffle(rows)

    path = Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n"
    )

    return rows
