def score_lead(answers):
    score = 0

    if "yes" in answers["decision_maker"].lower():
        score += 1

    if "excel" not in answers["current_tool"].lower():
        score += 1

    try:
        size = int("".join(filter(str.isdigit, answers["company_size"])))
        if size > 10:
            score += 1
    except:
        pass

    return score >= 2
