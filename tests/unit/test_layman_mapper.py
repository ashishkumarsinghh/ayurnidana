"""Unit tests for LaymanMapper.
Validates natural language extraction of clinical Ayurvedic symptom tokens
from English, Hinglish, and colloquial patient narratives.
"""
import pytest
from ayurnidana.core.layman_mapper import extract_symptoms_from_text, KEYWORD_MAP

class TestLaymanMapper:

    def test_extract_joint_symptoms(self):
        text = "Doctor, I am having extreme joint pain with clicking and cracking sounds in both my knees, and my legs feel very stiff in the morning."
        tokens = extract_symptoms_from_text(text)
        assert "joint_pain_cracking" in tokens or "tremors_stiffness" in tokens

    def test_extract_acid_peptic_symptoms(self):
        text = "I have terrible heartburn, sour belching and acid reflux every time I eat spicy food. There is a burning sensation in my chest."
        tokens = extract_symptoms_from_text(text)
        assert "acid_reflux_heartburn" in tokens
        assert "burning_sensation" in tokens

    def test_extract_respiratory_symptoms(self):
        text = "I suffer from severe wheezing, breathlessness, and shortness of breath when cold weather strikes. Also heavy cough with phlegm and mucus."
        tokens = extract_symptoms_from_text(text)
        assert "wheezing_shortness_of_breath" in tokens
        assert "cough_chronic" in tokens or "excess_mucus_congestion" in tokens

    def test_extract_urinary_symptoms(self):
        text = "It burns terribly when I pee, painful urination and very frequent visits to the washroom."
        tokens = extract_symptoms_from_text(text)
        assert "burning_painful_urination" in tokens or "frequent_cloudy_urination" in tokens

    def test_extract_cephalic_and_psychiatric_symptoms(self):
        text = "Constant throbbing migraine headache, terrible insomnia where I cannot sleep at night, and severe anxiety attacks with panic."
        tokens = extract_symptoms_from_text(text)
        assert "headache_migraine_throbbing" in tokens
        assert "insomnia_disturbed_sleep" in tokens
        assert "anxiety_restlessness" in tokens or "anxiety_panic_palpitations" in tokens

    def test_extract_hinglish_and_vernacular(self):
        text = "Mujhe bahut jalan ho rahi hai chaati mein, gale me khatta paani aata hai aur pet me gas banti hai."
        tokens = extract_symptoms_from_text(text)
        assert "burning_sensation" in tokens or "acid_reflux_heartburn" in tokens or "bloating_flatulence" in tokens

    def test_empty_or_unrelated_text(self):
        text = "The quick brown fox jumps over the lazy dog."
        tokens = extract_symptoms_from_text(text)
        assert isinstance(tokens, list)
        assert len(tokens) == 0
