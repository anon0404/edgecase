from edgecase.benchmark import generate_cases

def main():
    rows = generate_cases(n_per_collision=75)
    print(f"Generated {len(rows)} benchmark cases.")

if __name__ == "__main__":
    main()
