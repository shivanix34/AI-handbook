import numpy as np

def preprocess_and_score(df):
    df["company_age"] = 2025 - df["founded"]

    size_map = {
        "1-10": 1, "11-50": 2, "51-200": 3, "201-500": 4,
        "501-1000": 5, "1001-5000": 6, "5001-10000": 7, "10001+": 8
    }
    df["size_bucket"] = df["size_range"].map(size_map)

    epsilon = 1e-8
    min_size, max_size = df["size_bucket"].min(), df["size_bucket"].max()
    norm_size = (df["size_bucket"] - min_size) / (max_size - min_size + epsilon)

    min_age, max_age = df["company_age"].min(), df["company_age"].max()
    norm_age = (max_age - df["company_age"]) / (max_age - min_age + epsilon)

    size_boost = norm_size ** 1.5
    age_boost = norm_age ** 1.8

    maturity_bonus = np.where((df["company_age"] > 20) & (df["size_bucket"] >= 7), 1.0, 0.0)
    growth_bonus = np.where(
        df["current employee estimate"] / (df["total employee estimate"] + epsilon) < 0.7, 1.0, 0.0
    )

    lead_score_raw = (
        0.5 * size_boost +
        0.4 * age_boost +
        0.05 * maturity_bonus +
        0.05 * growth_bonus
    )

    min_score, max_score = lead_score_raw.min(), lead_score_raw.max()
    df["lead_score"] = ((lead_score_raw - min_score) / (max_score - min_score + epsilon)) * 100
    df["lead_score"] = df["lead_score"].round(2)

    df = df.drop(columns=["company_age", "size_bucket"], errors="ignore")
    return df
