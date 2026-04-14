def generate_advice(best_role, results):

    role_data = results[best_role]

    matched = role_data["matched"]
    missing = role_data["missing"]

    advice = []

    if matched:
        advice.append(
            f"You already have strong skills in {', '.join(matched)}."
        )

    if missing:
        advice.append(
            f"To become a stronger {best_role}, focus on learning: {', '.join(missing)}."
        )

    advice.append(
        "Improving these skills can significantly increase your job match score."
    )

    return " ".join(advice)