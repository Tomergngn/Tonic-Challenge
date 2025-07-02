def main():
    import csv, json, random

    # Load config
    with open("config.json") as f:
        config = json.load(f)

    servers = config["servers"]

    # Helper to randomly pick from a distribution
    def pick_with_distribution(distr):
        distr = {k: v for k, v in distr.items() if k != "id"}
        choices, weights = zip(*distr.items())
        return random.choices(choices, weights=weights, k=1)[0]

    # Description templates
    descriptions = [
        "The system is down on {servers}.",
        "Experiencing latency on {servers}.",
        "Unable to authenticate users on {servers}.",
        "Logs show memory leak in {servers}.",
        "Database connection timeout at {servers}.",
        "Intermittent issue – might be {servers} or unrelated.",
        "{servers} and {servers} crashed unexpectedly.",
        "High CPU usage.",
        "Users reporting errors – could be {servers}.",
        "Couldn’t reproduce, maybe check {servers}?"
    ]

    # Random server selection
    def random_server_subset():
        if random.random() < 0.15:
            return []
        n = random.randint(1, 3)
        subset = random.sample(servers, n)
        return [
            s.upper() if random.random() < 0.5 else s.lower()
            for s in subset
        ]

    # Determine additional fields from config
    extra_fields = []
    field_generators = {}
    for key, distr in config.items():
        if isinstance(distr, dict) and "id" in distr:
            extra_fields.append(key.capitalize().replace("_distribution", ""))
            field_generators[key] = lambda d=distr: pick_with_distribution(d)

    # Write CSV
    with open("jira_issues.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["Summary", "Description"] + extra_fields
        writer.writerow(header)

        for i in range(5000):
            server_subset = random_server_subset()
            placeholder = ", ".join(server_subset) if server_subset else ""
            template = random.choice(descriptions)
            description = template.replace("{servers}", placeholder)
            summary = f"Issue {i+1}: Support case"
            row = [summary, description] + [gen() for gen in field_generators.values()]
            writer.writerow(row)

if __name__ == "__main__":
    main()
