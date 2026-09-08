"""Local Ayurvedic Library Scanner & Reference Indexer.
Connects directly with the user's classical treatise library at OneDrive/Documents/ayurveda.
"""
import os
import glob
from typing import List, Dict, Any

class LocalAyurvedaLibrary:
    """Indexes and provides direct citation access to the user's 100+ classical treatises."""

    DEFAULT_PATHS = [
        "/mnt/c/Users/ashis/OneDrive/Documents/ayurveda",
        os.path.expanduser("~/OneDrive/Documents/ayurveda")
    ]

    def __init__(self, custom_path: str = None):
        self.library_dir = None
        paths_to_check = [custom_path] if custom_path else []
        paths_to_check.extend(self.DEFAULT_PATHS)
        
        for p in paths_to_check:
            if p and os.path.exists(p):
                self.library_dir = p
                break

    def get_library_status(self) -> Dict[str, Any]:
        if not self.library_dir:
            return {
                "available": False,
                "message": "Local Ayurveda documents directory not found at standard paths.",
                "total_treatises": 0
            }

        all_files = []
        for root, _, files in os.walk(self.library_dir):
            for f in files:
                if f.endswith(('.pdf', '.epub', '.txt')):
                    all_files.append(os.path.join(root, f))

        uploaded_files = [f for f in all_files if "uploaded" in f.lower()]

        return {
            "available": True,
            "path": self.library_dir,
            "total_treatises": len(all_files),
            "uploaded_count": len(uploaded_files),
            "key_samhitas": self._identify_samhitas(all_files)
        }

    def _identify_samhitas(self, file_paths: List[str]) -> List[str]:
        samhitas = set()
        for fp in file_paths:
            base = os.path.basename(fp).lower()
            if "charak" in base or "charaka" in base:
                samhitas.add("Charaka Samhita (Brihat Trayi)")
            elif "sushrut" in base or "sushruta" in base:
                samhitas.add("Sushruta Samhita (Brihat Trayi)")
            elif "ashtanga" in base or "astanga" in base or "vagbhata" in base:
                samhitas.add("Ashtanga Hridaya / Sangraha (Brihat Trayi)")
            elif "madhav" in base or "madhava" in base:
                samhitas.add("Madhava Nidana (Laghu Trayi - Diagnostics)")
            elif "sharngadhara" in base:
                samhitas.add("Sharngadhara Samhita (Laghu Trayi - Pharmaceutics)")
            elif "bhavaprakasha" in base or "bhavprakash" in base:
                samhitas.add("Bhavaprakasha (Laghu Trayi - Nighantu & Chikitsa)")
            elif "bhaisajya" in base or "bhaishajya" in base:
                samhitas.add("Bhaishajya Ratnavali (Formulations)")
            elif "panchakarma" in base:
                samhitas.add("Standard Panchakarma Protocols")
            elif "rognidan" in base or "nidan" in base:
                samhitas.add("Roga Nidana (Pathology & Diagnostics)")
        return sorted(list(samhitas))

    def search_treatises(self, keyword: str) -> List[Dict[str, str]]:
        if not self.library_dir:
            return []

        results = []
        kw = keyword.lower()
        for root, _, files in os.walk(self.library_dir):
            for f in files:
                if f.endswith(('.pdf', '.epub', '.txt')) and kw in f.lower():
                    is_uploaded = "uploaded" in root.lower()
                    results.append({
                        "filename": f,
                        "folder": "Uploaded to NotebookLM" if is_uploaded else "Local Library",
                        "full_path": os.path.join(root, f)
                    })
        return results[:15]
