import sys
import random
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ayurnidana.core.nidana_engine import NidanaEngine
from ayurnidana.core.models import AmaStatus, AgniType, KoshthaType
from ayurnidana.knowledge.classical_db import CLASSICAL_DISEASES
from ayurnidana.core.layman_mapper import SYMPTOM_DEFINITIONS

def run_comprehensive_tests():
    print("=== AyurNidana Diagnostic Engine Robustness Test ===")
    print(f"Loaded {len(CLASSICAL_DISEASES)} Classical Diseases.")
    
    total_tests = 0
    passed = 0
    failures = []
    
    all_symptoms = list(SYMPTOM_DEFINITIONS.keys())

    # Generate 200+ variations
    for dis_id, data in CLASSICAL_DISEASES.items():
        cardinals = data.get('cardinal_symptoms', [])
        if not cardinals:
            continue
            
        primary_dosha = data.get('primary_dosha', 'Vata')
        dhatu = data.get('dhatu', [])
        srotas = data.get('srotas', [])
        req_ama = data.get('requires_ama', False)
        ama = AmaStatus.SAMA if req_ama else AmaStatus.NIRAMA
        
        # Base Case 1: Exact Match (1x)
        total_tests += 1
        dx = NidanaEngine.diagnose({s: 'constant' for s in cardinals}, primary_dosha, ama, AgniType.SAMAGNI, KoshthaType.MADHYAMA, dhatu, srotas)
        if dx.primary_condition == data['name']: passed += 1
        else: failures.append((dis_id, "Exact Match", dx.primary_condition))

        # Case 2: Partial Matches (remove 1 symptom) (1x)
        if len(cardinals) > 1:
            for i in range(len(cardinals)):
                total_tests += 1
                partial = cardinals.copy()
                partial.pop(i)
                dx = NidanaEngine.diagnose({s: 'constant' for s in partial}, primary_dosha, ama, AgniType.SAMAGNI, KoshthaType.MADHYAMA, dhatu, srotas)
                if dx.primary_condition == data['name']: 
                    passed += 1
                else: 
                    # We tolerate a fallback to syndromic or a close relative
                    failures.append((dis_id, f"Partial Match (missing {cardinals[i]})", dx.primary_condition))
                    
        # Case 3: Distractor Addition (Add 2 random unrelated symptoms) (3x per disease)
        for _ in range(3):
            total_tests += 1
            distractors = random.sample([s for s in all_symptoms if s not in cardinals], 2)
            symps_distract = {s: 'constant' for s in cardinals}
            for d in distractors: symps_distract[d] = 'occasional'
            
            dx = NidanaEngine.diagnose(symps_distract, primary_dosha, ama, AgniType.SAMAGNI, KoshthaType.MADHYAMA, dhatu, srotas)
            if dx.primary_condition == data['name']: passed += 1
            else: failures.append((dis_id, f"Distractor Match (+{distractors})", dx.primary_condition))
            
        # Case 4: Misaligned Dosha / Real-world confusion (1x)
        # E.g. Patient presents symptoms but Dosha engine gets confused
        total_tests += 1
        wrong_dosha = "Kapha" if "Vata" in primary_dosha else "Vata"
        dx = NidanaEngine.diagnose({s: 'constant' for s in cardinals}, wrong_dosha, ama, AgniType.SAMAGNI, KoshthaType.MADHYAMA, dhatu, srotas)
        if dx.primary_condition == data['name']: passed += 1
        else: failures.append((dis_id, f"Wrong Dosha Match ({wrong_dosha})", dx.primary_condition))

    print(f"\\nRan {total_tests} complex diagnostic permutations.")
    print(f"Passed: {passed}")
    print(f"Failed: {total_tests - passed}")
    print(f"Accuracy: {(passed/total_tests)*100:.2f}%\\n")
    
    if failures:
        print("--- Edge Case Analysis (Failures) ---")
        for f in failures[:15]: # Show top 15
            print(f"Disease: {f[0]} | Scenario: {f[1]} -> Diagnosed As: {f[2]}")
        print("-------------------------------------")
        print("Note: Partial match failures between highly similar diseases (e.g. Sthaulya vs Prameha) are expected and clinically valid in Ayurveda without lab tests.")

if __name__ == '__main__':
    run_comprehensive_tests()
