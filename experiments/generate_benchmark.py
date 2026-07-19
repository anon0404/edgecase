# Prototype benchmark generator (4 collision types, tiny template pools),
# superseded by build_edgecase_benchmark_v1.py. Not called by run_all.sh and
# not the source of any paper-reported result. Kept for reference only.
from edgecase.benchmark import generate_cases

def main():
    rows = generate_cases(n_per_collision=75)
    print(f"Generated {len(rows)} benchmark cases.")

if __name__ == "__main__":
    main()
