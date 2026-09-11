"""Dosha calculation, Vikriti determination, and Ama evaluation engine.
Supports frequency and severity weighting (e.g. sometimes/mild vs constant/severe).
"""
from typing import List, Dict, Tuple, Any, Union
from .models import Dosha, PrakritiType, AmaStatus, AgniType, KoshthaType

VATA_INDICATORS = {
    'joint_pain_cracking': 3.0,
    'pain_sharp_throbbing': 3.0,
    'sciatica_radiating_leg_pain': 3.5,
    'headache_migraine_throbbing': 3.0,
    'panic_intense_worry': 3.5,
    'dryness_skin_hair': 2.0,
    'constipation_hard_stools': 2.5,
    'bloating_flatulence': 2.5,
    'insomnia_disturbed_sleep': 2.5,
    'anxiety_restlessness': 2.5,
    'weight_loss_emaciation': 2.0,
    'cold_intolerance': 2.0,
    'tremors_stiffness': 3.0,
    'irregular_appetite': 2.0,
    'wheezing_shortness_of_breath': 2.5,
    'cough_chronic': 2.0,
    'malabsorption_mucus_stools': 2.0,
    'anal_pain_bleeding_piles': 2.5,
    'nadi_sarpa_gati_cobra': 3.0,
    'tongue_dry_rough_cracked': 2.5
}

PITTA_INDICATORS = {
    'burning_sensation': 3.0,
    'acid_reflux_heartburn': 3.0,
    'burning_painful_urination': 3.5,
    'severe_acute_diarrhea': 3.0,
    'headache_migraine_throbbing': 2.0,
    'excessive_thirst_sweating': 2.0,
    'skin_rashes_inflammation_acne': 2.5,
    'loose_stools_diarrhea': 2.5,
    'irritability_anger': 2.0,
    'heat_intolerance': 2.5,
    'yellowish_eyes_urine': 3.5,
    'ulceration_bleeding_tendency': 3.0,
    'intense_sharp_hunger': 2.0,
    'gout_big_toe_burning_pain': 3.0,
    'anal_pain_bleeding_piles': 2.0,
    'nadi_manduka_gati_frog': 3.0,
    'tongue_red_yellow_coating': 2.5
}

KAPHA_INDICATORS = {
    'heaviness_body_limbs': 3.0,
    'excess_mucus_congestion': 3.0,
    'dull_pain_swelling_edema': 2.5,
    'pallor_fatigue_anemia': 2.5,
    'excessive_sleep_lethargy': 2.5,
    'weight_gain_slow_metabolism': 3.0,
    'sweet_taste_in_mouth': 2.0,
    'cold_clammy_skin': 2.0,
    'oily_greasy_skin': 2.0,
    'slow_sluggish_digestion': 2.5,
    'attachment_depression': 2.0,
    'fever': 2.0,
    'wheezing_shortness_of_breath': 3.0,
    'cough_chronic': 2.5,
    'frequent_cloudy_urination': 2.5,
    'malabsorption_mucus_stools': 2.0,
    'nadi_hamsa_gati_swan': 3.0,
    'tongue_pale_thick_white_coating': 2.5
}

AMA_INDICATORS = [
    'tongue_thick_white_coating',
    'foul_breath',
    'lethargy_post_meal_drowsiness',
    'loss_of_taste_aruchi',
    'obstruction_mala_stambha',
    'body_aches_angamarda',
    'sticky_foul_smelling_stools',
    'heaviness_in_abdomen',
    'malabsorption_mucus_stools'
]

class DoshaEngine:
    @staticmethod
    def calculate_vikriti(selected_symptoms: Union[List[str], Dict[str, Any]]) -> Tuple[Dict[str, float], str]:
        """Calculates Vikriti percentages and pattern with frequency/severity weighting."""
        scores = {'Vata': 0.0, 'Pitta': 0.0, 'Kapha': 0.0}
        
        symptom_weights: Dict[str, float] = {}
        if isinstance(selected_symptoms, dict):
            for k, v in selected_symptoms.items():
                if isinstance(v, (int, float)):
                    symptom_weights[k] = float(v)
                elif isinstance(v, str):
                    v_low = v.lower()
                    if v_low in ['sometimes', 'mild', 'occasional']:
                        symptom_weights[k] = 0.6
                    elif v_low in ['constant', 'severe', 'frequent', 'chronic']:
                        symptom_weights[k] = 1.2
                    else:
                        symptom_weights[k] = 1.0
                else:
                    symptom_weights[k] = 1.0
        else:
            for s in selected_symptoms:
                symptom_weights[s] = 1.0
        
        for sym, weight in symptom_weights.items():
            if sym in VATA_INDICATORS:
                scores['Vata'] += VATA_INDICATORS[sym] * weight
            if sym in PITTA_INDICATORS:
                scores['Pitta'] += PITTA_INDICATORS[sym] * weight
            if sym in KAPHA_INDICATORS:
                scores['Kapha'] += KAPHA_INDICATORS[sym] * weight

        total = sum(scores.values())
        if total == 0:
            percentages = {'Vata': 33.3, 'Pitta': 33.3, 'Kapha': 33.3}
            pattern = 'Balanced / Undetermined'
            return percentages, pattern

        percentages = {k: round((v / total) * 100, 1) for k, v in scores.items()}
        
        sorted_doshas = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        top_name, top_pct = sorted_doshas[0]
        second_name, second_pct = sorted_doshas[1]

        if top_pct >= 60.0:
            pattern = f'{top_name} Pradhana (Predominantly {top_name} Vikriti)'
        elif (top_pct - second_pct) <= 15.0:
            pattern = f'Dvandvaja ({top_name}-{second_name} Dual Imbalance)'
        elif all(p >= 25.0 for p in percentages.values()):
            pattern = 'Sannipataja (Tridoshic Imbalance)'
        else:
            pattern = f'{top_name} with secondary {second_name} Vikriti'

        return percentages, pattern

    @staticmethod
    def assess_ama(symptoms: Union[List[str], Dict[str, Any]], tongue_finding: str = "") -> Tuple[AmaStatus, List[str]]:
        sym_list = list(symptoms.keys()) if isinstance(symptoms, dict) else list(symptoms)
        present_ama = [ind for ind in AMA_INDICATORS if ind in sym_list]
        if tongue_finding and ('thick' in tongue_finding.lower() or 'white' in tongue_finding.lower() or 'coated' in tongue_finding.lower()):
            present_ama.append('thick_tongue_coating')

        count = len(present_ama)
        if count >= 3:
            return AmaStatus.SAMA, present_ama
        elif count >= 1:
            return AmaStatus.MILD_AMA, present_ama
        else:
            return AmaStatus.NIRAMA, present_ama

    @staticmethod
    def determine_dhatu_and_srotas(symptoms: Union[List[str], Dict[str, Any]]) -> Tuple[List[str], List[str]]:
        dhatus = set()
        srotas = set()

        sym_list = list(symptoms.keys()) if isinstance(symptoms, dict) else list(symptoms)
        sym_str = ' '.join(sym_list).lower()

        if any(w in sym_str for w in ['taste', 'fever', 'nausea', 'dryness', 'thirst', 'lethargy', 'aruchi', 'pallor', 'anemia', 'swelling', 'edema']):
            dhatus.add('Rasa Dhatu (Plasma & Lymph)')
            srotas.add('Rasavaha Srotas')
        if any(w in sym_str for w in ['skin', 'burning', 'bleeding', 'red', 'acne', 'rash', 'inflammation', 'yellow', 'gout', 'piles', 'anemia', 'pallor']):
            dhatus.add('Rakta Dhatu (Blood & Hemoglobin)')
            srotas.add('Raktavaha Srotas')
        if any(w in sym_str for w in ['muscle', 'heaviness', 'stiffness', 'cramps', 'piles', 'rectal']):
            dhatus.add('Mamsa Dhatu (Muscle Tissue)')
            srotas.add('Mamsavaha Srotas')
        if any(w in sym_str for w in ['weight_gain', 'fat', 'sweating', 'obesity', 'sthaulya', 'prameha']):
            dhatus.add('Meda Dhatu (Adipose Tissue)')
            srotas.add('Medovaha Srotas')
        if any(w in sym_str for w in ['joint', 'bone', 'cracking', 'hair_fall', 'brittle_nails', 'sciatica', 'gout']):
            dhatus.add('Asthi Dhatu (Bone Matrix)')
            srotas.add('Asthivaha Srotas')
        if any(w in sym_str for w in ['insomnia', 'anxiety', 'vertigo', 'nerves', 'tremors', 'headache', 'sciatica', 'chittodvega', 'panic']):
            dhatus.add('Majja Dhatu (Nervous & Bone Marrow)')
            srotas.add('Majjavaha Srotas')
            srotas.add('Manovaha Srotas (Mental Channel)')
        if any(w in sym_str for w in ['breath', 'cough', 'wheezing', 'congestion', 'mucus', 'shwasa', 'kasa']):
            srotas.add('Pranavaha Srotas (Respiratory Channel)')
        if any(w in sym_str for w in ['bloating', 'acid', 'appetite', 'digestion', 'constipation', 'stools', 'mucus_stools', 'malabsorption', 'diarrhea']):
            srotas.add('Annavaha Srotas (Digestive Channel)')
            srotas.add('Purishavaha Srotas (Excretory Channel)')
        if any(w in sym_str for w in ['diarrhea', 'loose', 'thirst', 'edema', 'swelling', 'water']):
            srotas.add('Udakavaha Srotas (Fluid Regulation Channel)')
        if any(w in sym_str for w in ['urine', 'burning_micturition', 'yellowish_urine', 'cloudy_urination', 'prameha', 'burning_painful_urination']):
            srotas.add('Mutravaha Srotas (Urinary Channel)')
        if any(w in sym_str for w in ['sweat', 'daha', 'burning']):
            srotas.add('Svedavaha Srotas (Sweat Gland Channel)')

        return list(dhatus) or ['Rasa Dhatu (Plasma)'], list(srotas) or ['Annavaha Srotas (Digestive)']
