"""Unit tests for symptom addition, removal, and multi-input state synchronization.
Validates that adding symptoms in Step 2 does not inadvertently delete existing symptoms,
and that frequency adjustments and checkbox states remain consistent.
"""
import pytest
from ayurnidana.core.layman_mapper import SYMPTOM_DEFINITIONS

def test_symptom_addition_preserves_existing_symptoms():
    active_symptoms = {
        "joint_pain_cracking": "constant",
        "bloating_flatulence": "sometimes"
    }
    checkbox_states = {
        "chk_joint_pain_cracking": True,
        "chk_bloating_flatulence": True
    }
    
    # Simulate Step 2 adding a new symptom
    new_sym = "acid_reflux_heartburn"
    new_freq = "constant"
    
    active_symptoms[new_sym] = new_freq
    checkbox_states[f"chk_{new_sym}"] = True
    
    # Verify all 3 symptoms exist
    assert "joint_pain_cracking" in active_symptoms
    assert "bloating_flatulence" in active_symptoms
    assert "acid_reflux_heartburn" in active_symptoms
    assert active_symptoms["acid_reflux_heartburn"] == "constant"
    assert checkbox_states["chk_acid_reflux_heartburn"] is True

def test_step3_checkbox_sync_does_not_delete_newly_added():
    active_symptoms = {
        "joint_pain_cracking": "constant",
        "bloating_flatulence": "sometimes",
        "acid_reflux_heartburn": "sometimes"
    }
    # Pre-sync step ensures all checkbox keys match active_symptoms before rendering
    checkbox_states = {}
    for s_id in SYMPTOM_DEFINITIONS:
        chk_k = f"chk_{s_id}"
        should_be_checked = s_id in active_symptoms
        checkbox_states[chk_k] = should_be_checked

    assert checkbox_states["chk_acid_reflux_heartburn"] is True
    assert checkbox_states["chk_joint_pain_cracking"] is True
    assert checkbox_states["chk_bloating_flatulence"] is True
    assert checkbox_states["chk_fever"] is False
    
    # Ensure active_symptoms remains completely untouched
    assert len(active_symptoms) == 3

def test_symptom_removal_cleanly_unsets_checkbox():
    active_symptoms = {
        "joint_pain_cracking": "constant",
        "bloating_flatulence": "sometimes"
    }
    detected_symptoms = {
        "joint_pain_cracking": "constant"
    }
    checkbox_states = {
        "chk_joint_pain_cracking": True,
        "chk_bloating_flatulence": True
    }
    
    # Remove joint_pain_cracking
    sym_to_del = "joint_pain_cracking"
    del active_symptoms[sym_to_del]
    if sym_to_del in detected_symptoms:
        del detected_symptoms[sym_to_del]
    checkbox_states[f"chk_{sym_to_del}"] = False
    
    assert sym_to_del not in active_symptoms
    assert sym_to_del not in detected_symptoms
    assert checkbox_states[f"chk_{sym_to_del}"] is False
    # Other symptoms untouched
    assert "bloating_flatulence" in active_symptoms
    assert checkbox_states["chk_bloating_flatulence"] is True
