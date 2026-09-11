import sys
import os
import pytest
sys.path.insert(0, '/home/ashish/projects/ayurnidana')

from ayurnidana.auth.user_db import register_user, authenticate_user, save_consultation, get_user_consultations

def test_auth_workflow():
    # 1. Register new user
    import time
    ts = int(time.time())
    uname = f"testuser_{ts}"
    email = f"test_{ts}@example.com"
    
    ok, msg, udata = register_user(uname, email, "secret123", "Test Patient", 40, "Female")
    assert ok is True, f"Registration failed: {msg}"
    assert udata is not None
    assert udata["username"] == uname
    assert udata["age"] == 40
    
    # 2. Duplicate registration should fail
    ok_dup, msg_dup, _ = register_user(uname, "other@email.com", "secret123", "Dup")
    assert ok_dup is False
    assert "already taken" in msg_dup

    # 3. Successful authentication
    ok_login, msg_login, user_login = authenticate_user(uname, "secret123")
    assert ok_login is True
    assert user_login["email"] == email

    # 4. Failed authentication (bad password)
    ok_bad, msg_bad, _ = authenticate_user(uname, "wrongpassword")
    assert ok_bad is False

    # 5. Save consultation
    cid = save_consultation(
        user_id=user_login["id"],
        chief_complaint="Knee stiffness and clicking",
        symptoms=["joint_pain_cracking", "tremors_stiffness"],
        primary_condition="Sandhivata",
        sanskrit_name="Sandhivata (संधिवात)",
        dosha_scores={"Vata": 70.0, "Pitta": 15.0, "Kapha": 15.0},
        treatment_summary="Yogaraja Guggulu 2 tabs BD",
        case_sheet_md="# Case Sheet"
    )
    assert cid is not None
    assert cid > 0

    # 6. Retrieve consultations
    history = get_user_consultations(user_login["id"])
    assert len(history) >= 1
    assert history[0]["primary_condition"] == "Sandhivata"
    assert "joint_pain_cracking" in history[0]["symptoms"]

if __name__ == "__main__":
    test_auth_workflow()
    print("ALL AUTH TESTS PASSED!")
