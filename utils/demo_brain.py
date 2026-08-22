def get_demo_prediction(village):

    predictions = {

        "Village A": {
            "risk_score": 87,
            "risk_level": "HIGH",
            "cases_change": 180,
            "water_quality": "HIGH",
            "rainfall": "HIGH",
            "flooding": True,
        },

        "Village B": {
            "risk_score": 24,
            "risk_level": "LOW",
            "cases_change": 5,
            "water_quality": "GOOD",
            "rainfall": "NORMAL",
            "flooding": False,
        },

        "Village C": {
            "risk_score": 61,
            "risk_level": "MEDIUM",
            "cases_change": 72,
            "water_quality": "MODERATE",
            "rainfall": "HIGH",
            "flooding": False,
        },
    }

    return predictions[village]