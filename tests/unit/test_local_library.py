"""Unit tests for LocalAyurvedaLibrary scanner.
Validates detection and indexing of the 138 classical treatises in OneDrive/Documents/ayurveda,
identification of key Samhitas (Charaka, Sushruta, Ashtanga, Madhava, Sharngadhara, Bhavaprakasha),
and disease-to-treatise citation grounding.
"""
import pytest
from ayurnidana.knowledge.local_library import LocalAyurvedaLibrary
from ayurnidana.knowledge.classical_db import CLASSICAL_DISEASES

@pytest.fixture(scope="module")
def library():
    return LocalAyurvedaLibrary()

class TestLocalAyurvedaLibrary:

    def test_library_availability_and_count(self, library):
        status = library.get_library_status()
        assert status["available"] is True, f"Library not available at {status.get('path')}"
        assert status["total_treatises"] >= 100, f"Expected >=100 treatises, found {status.get('total_treatises')}"
        assert status["uploaded_count"] >= 30, f"Expected uploaded treatises, found {status.get('uploaded_count')}"

    def test_key_samhitas_identified(self, library):
        status = library.get_library_status()
        samhitas = status["key_samhitas"]
        assert any("Charaka" in s for s in samhitas), "Charaka Samhita should be identified"
        assert any("Sushruta" in s for s in samhitas), "Sushruta Samhita should be identified"
        assert any("Ashtanga" in s for s in samhitas), "Ashtanga Hridaya should be identified"
        assert any("Madhava" in s for s in samhitas), "Madhava Nidana should be identified"

    @pytest.mark.parametrize("condition_key", list(CLASSICAL_DISEASES.keys()))
    def test_all_20_conditions_grounded_to_treatises(self, library, condition_key):
        disease_info = CLASSICAL_DISEASES[condition_key]
        relevant = library.find_relevant_treatises(disease_info["name"])
        assert len(relevant) > 0, f"No treatises found for condition {condition_key} ({disease_info['name']})"
        assert all("filename" in item and "full_path" in item for item in relevant)

    def test_treatise_search_keyword(self, library):
        results = library.search_treatises("charak")
        assert len(results) > 0
        assert any("charak" in r["filename"].lower() for r in results)
