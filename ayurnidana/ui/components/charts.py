"""Visualization components for Doshic profiles and Samprapti stages."""
import pandas as pd
from typing import Dict

def get_dosha_df(dosha_scores: Dict[str, float]) -> pd.DataFrame:
    data = []
    colors = {"Vata": "#3182CE", "Pitta": "#DD6B20", "Kapha": "#38A169"}
    for dosha, pct in dosha_scores.items():
        data.append({
            "Dosha": dosha,
            "Percentage (%)": pct,
            "Color": colors.get(dosha, "#718096")
        })
    return pd.DataFrame(data)
