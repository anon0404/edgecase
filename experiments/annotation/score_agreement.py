import csv
import json
from pathlib import Path

import openpyxl
from sklearn.metrics import cohen_kappa_score

ANSWER_KEY = Path("experiments/annotation/annotation_answer_key.csv")
ANNOTATOR_FILES = {
    "aidanreilly": Path("experiments/annotation/annotation_blind_aidanreilly.xlsx"),
    "shiva": Path("experiments/annotation/annotation_blind_shiva.xlsx"),
}
OUT_JSON = Path("experiments/results/annotation_agreement.json")
OUT_MD = Path("experiments/tables/annotation_agreement.md")

UNCLEAR = "unclear / none of the above"

def load_answer_key():
    with ANSWER_KEY.open() as f:
        return {int(row["row_number"]): row for row in csv.DictReader(f)}

def load_annotations(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Annotate"]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_number, prompt, signals, collision, mitigation, confidence, notes = row
        if row_number is None:
            continue
        out[int(row_number)] = {
            "collision": (collision or UNCLEAR).strip(),
            "mitigation": (mitigation or UNCLEAR).strip(),
            "confidence": confidence,
        }
    return out

def main():
    key = load_answer_key()
    annotations = {name: load_annotations(path) for name, path in ANNOTATOR_FILES.items()}

    n_rows = len(key)
    for name, ann in annotations.items():
        missing = set(key) - set(ann)
        if missing:
            raise ValueError(f"{name} is missing rows: {sorted(missing)}")

    per_annotator = {}
    for name, ann in annotations.items():
        collision_correct = sum(1 for r in key if ann[r]["collision"] == key[r]["true_collision"])
        mitigation_correct = sum(1 for r in key if ann[r]["mitigation"] == key[r]["true_expected_mitigation"])
        both_correct = sum(
            1 for r in key
            if ann[r]["collision"] == key[r]["true_collision"]
            and ann[r]["mitigation"] == key[r]["true_expected_mitigation"]
        )
        unclear_count = sum(1 for r in key if ann[r]["collision"] == UNCLEAR)

        true_labels = [key[r]["true_collision"] for r in sorted(key)]
        pred_labels = [ann[r]["collision"] for r in sorted(key)]
        kappa_vs_key = cohen_kappa_score(true_labels, pred_labels)

        per_annotator[name] = {
            "n_rows": n_rows,
            "collision_accuracy_vs_key": round(collision_correct / n_rows, 4),
            "mitigation_accuracy_vs_key": round(mitigation_correct / n_rows, 4),
            "both_correct_vs_key": round(both_correct / n_rows, 4),
            "cohen_kappa_collision_vs_key": round(kappa_vs_key, 4),
            "n_marked_unclear": unclear_count,
            "mean_confidence": round(
                sum(a["confidence"] for a in ann.values() if isinstance(a["confidence"], (int, float)))
                / max(1, sum(1 for a in ann.values() if isinstance(a["confidence"], (int, float)))),
                2,
            ),
        }

    names = list(annotations)
    a_labels = [annotations[names[0]][r]["collision"] for r in sorted(key)]
    b_labels = [annotations[names[1]][r]["collision"] for r in sorted(key)]
    inter_annotator_kappa = cohen_kappa_score(a_labels, b_labels)
    inter_annotator_agreement = sum(
        1 for r in sorted(key)
        if annotations[names[0]][r]["collision"] == annotations[names[1]][r]["collision"]
    ) / n_rows

    both_wrong_same_way = [
        r for r in sorted(key)
        if annotations[names[0]][r]["collision"] != key[r]["true_collision"]
        and annotations[names[1]][r]["collision"] != key[r]["true_collision"]
        and annotations[names[0]][r]["collision"] == annotations[names[1]][r]["collision"]
    ]

    disagreements_with_key = {
        r: {
            "true_collision": key[r]["true_collision"],
            "domain": key[r]["domain"],
            names[0]: annotations[names[0]][r]["collision"],
            names[1]: annotations[names[1]][r]["collision"],
        }
        for r in sorted(key)
        if annotations[names[0]][r]["collision"] != key[r]["true_collision"]
        or annotations[names[1]][r]["collision"] != key[r]["true_collision"]
    }

    result = {
        "n_rows": n_rows,
        "per_annotator": per_annotator,
        "inter_annotator_agreement_pct": round(inter_annotator_agreement, 4),
        "inter_annotator_cohen_kappa": round(inter_annotator_kappa, 4),
        "n_both_wrong_same_way": len(both_wrong_same_way),
        "both_wrong_same_way_rows": both_wrong_same_way,
        "n_disagreements_with_key_either_annotator": len(disagreements_with_key),
        "disagreements_with_key": disagreements_with_key,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2))

    with OUT_MD.open("w") as f:
        f.write(f"# Human annotator agreement ({n_rows} blinded, stratified cases)\n\n")
        f.write("## Per-annotator vs. benchmark's own ground-truth labels\n\n")
        f.write("| Annotator | Collision-type accuracy | Mitigation accuracy | Both correct | Cohen's kappa (collision) | Marked unclear | Mean confidence |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        for name, m in per_annotator.items():
            f.write(
                f"| {name} | {m['collision_accuracy_vs_key']} | {m['mitigation_accuracy_vs_key']} | "
                f"{m['both_correct_vs_key']} | {m['cohen_kappa_collision_vs_key']} | {m['n_marked_unclear']} | {m['mean_confidence']} |\n"
            )
        f.write(f"\n## Inter-annotator agreement\n\n")
        f.write(f"Raw agreement: {result['inter_annotator_agreement_pct']} · Cohen's kappa: {result['inter_annotator_cohen_kappa']}\n\n")
        f.write(f"Cases where both annotators agreed with each other but disagreed with the benchmark's label: {result['n_both_wrong_same_way']}\n\n")
        f.write(f"Full per-row disagreements: `experiments/results/annotation_agreement.json`\n")

    print(json.dumps({k: v for k, v in result.items() if k not in ("disagreements_with_key", "both_wrong_same_way_rows")}, indent=2))
    print(f"Wrote {OUT_JSON}, {OUT_MD}")

if __name__ == "__main__":
    main()
