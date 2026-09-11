"""Local & Cloud-Resilient Ayurvedic Library Reference Indexer.
Connects directly with the user's classical treatise library at OneDrive/Documents/ayurveda,
with seamless automated fallback to bundled cloud catalog for Streamlit Cloud deployment.
"""
import os
import json
from typing import List, Dict, Any

class LocalAyurvedaLibrary:
    """Indexes and provides direct citation access to the 138 classical treatises."""

    DEFAULT_PATHS = [
        "/mnt/c/Users/ashis/OneDrive/Documents/ayurveda",
        os.path.expanduser("~/OneDrive/Documents/ayurveda")
    ]

    BUNDLED_CATALOG_PATH = os.path.join(
        os.path.dirname(__file__), "data", "treatise_catalog.json"
    )

    def __init__(self, custom_path: str = None):
        self.library_dir = None
        self.catalog_data = None
        self._cached_status = None
        paths_to_check = [custom_path] if custom_path else []
        paths_to_check.extend(self.DEFAULT_PATHS)
        
        for p in paths_to_check:
            if p and os.path.exists(p):
                self.library_dir = p
                break

        # Fallback to bundled catalog for Streamlit Cloud
        if not self.library_dir and os.path.exists(self.BUNDLED_CATALOG_PATH):
            try:
                with open(self.BUNDLED_CATALOG_PATH, "r", encoding="utf-8") as f:
                    self.catalog_data = json.load(f)
            except Exception:
                self.catalog_data = None

    def get_library_status(self, force_refresh: bool = False) -> Dict[str, Any]:
        if not force_refresh and self._cached_status is not None:
            return self._cached_status

        if self.library_dir:
            all_files = []
            for root, _, files in os.walk(self.library_dir):
                for f in files:
                    if f.endswith(('.pdf', '.epub', '.txt')):
                        all_files.append(os.path.join(root, f))

            uploaded_files = [f for f in all_files if "uploaded" in f.lower()]

            self._cached_status = {
                "available": True,
                "path": self.library_dir,
                "storage_mode": "Local OneDrive Library",
                "total_treatises": len(all_files),
                "uploaded_count": len(uploaded_files),
                "key_samhitas": self._identify_samhitas(all_files)
            }
            return self._cached_status

        elif self.catalog_data:
            all_files = [item["filename"] for item in self.catalog_data]
            uploaded_files = [item["filename"] for item in self.catalog_data if item.get("is_uploaded")]

            self._cached_status = {
                "available": True,
                "path": "Cloud Catalog (Bundled)",
                "storage_mode": "Streamlit Cloud Knowledge Base",
                "total_treatises": len(self.catalog_data),
                "uploaded_count": len(uploaded_files),
                "key_samhitas": self._identify_samhitas(all_files)
            }
            return self._cached_status

        return {
            "available": False,
            "path": None,
            "storage_mode": "Not Connected",
            "message": "Local Ayurveda documents directory not found and catalog unavailable.",
            "total_treatises": 0,
            "uploaded_count": 0,
            "key_samhitas": []
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
        kw = keyword.lower()
        results = []

        if self.library_dir:
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

        elif self.catalog_data:
            for item in self.catalog_data:
                fn = item["filename"]
                if kw in fn.lower():
                    results.append({
                        "filename": fn,
                        "folder": item.get("category", "Local Samhita Library"),
                        "full_path": item.get("relative_path", fn)
                    })
            return results[:15]

        return []

    def find_relevant_treatises(self, condition_name: str, dosha_name: str = "") -> List[Dict[str, str]]:
        """Maps an active diagnostic condition to specific classical texts in user's library."""
        keywords = ["charak", "madhav", "bhaisajya", "ashtanga", "sushrut"]
        cond_clean = condition_name.lower().split("/")[0].strip()
        
        if "osteo" in cond_clean or "sandhivata" in cond_clean:
            keywords.extend(["vatavyadhi", "charak", "madhav", "bhaisajya"])
        elif "rheumatoid" in cond_clean or "amavata" in cond_clean:
            keywords.extend(["amavata", "madhav", "bhaisajya"])
        elif "sciatica" in cond_clean or "gridhrasi" in cond_clean:
            keywords.extend(["gridhrasi", "vatavyadhi", "charak", "ashtanga"])
        elif "gout" in cond_clean or "vatarakta" in cond_clean:
            keywords.extend(["vatarakta", "charak", "ashtanga", "amritadi"])
        elif "ibs" in cond_clean or "grahani" in cond_clean:
            keywords.extend(["grahani", "charak", "bhaisajya"])
        elif "asthma" in cond_clean or "shwasa" in cond_clean:
            keywords.extend(["shwasa", "tamaka", "charak", "bhaisajya"])
        elif "bronchitis" in cond_clean or "kasa" in cond_clean or "cough" in cond_clean:
            keywords.extend(["kasa", "charak", "bhaisajya"])
        elif "diabetes" in cond_clean or "prameha" in cond_clean:
            keywords.extend(["prameha", "charak", "sushrut"])
        elif "acid" in cond_clean or "amlapitta" in cond_clean:
            keywords.extend(["amlapitta", "madhav", "bhaisajya"])
        elif "skin" in cond_clean or "kushtha" in cond_clean or "psoriasis" in cond_clean or "eczema" in cond_clean:
            keywords.extend(["kushtha", "kushta", "charak", "sushrut"])
        elif "jaundice" in cond_clean or "kamala" in cond_clean:
            keywords.extend(["kamala", "pandu", "charak"])
        elif "hemorrhoid" in cond_clean or "arsha" in cond_clean or "piles" in cond_clean:
            keywords.extend(["arsha", "sushrut", "charak"])
        elif "obesity" in cond_clean or "sthaulya" in cond_clean:
            keywords.extend(["sthaulya", "medoroga", "charak"])
        elif "insomnia" in cond_clean or "anidra" in cond_clean or "chittodvega" in cond_clean:
            keywords.extend(["manas", "anidra", "charak", "ashtanga"])
        elif "headache" in cond_clean or "shirashoola" in cond_clean or "migraine" in cond_clean:
            keywords.extend(["shiroroga", "shirashoola", "charak"])
        elif "anemia" in cond_clean or "pandu" in cond_clean:
            keywords.extend(["pandu", "charak", "bhaisajya"])
        elif "edema" in cond_clean or "shotha" in cond_clean:
            keywords.extend(["shotha", "shopha", "charak"])
        elif "dysuria" in cond_clean or "mutrakrichhra" in cond_clean or "urinary" in cond_clean:
            keywords.extend(["mutrakrichhra", "mutra", "sushrut", "charak"])
        elif "diarrhea" in cond_clean or "atisara" in cond_clean:
            keywords.extend(["atisara", "charak", "madhav"])
        elif "anxiety" in cond_clean or "cittodvega" in cond_clean:
            keywords.extend(["manas", "unmada", "charak"])

        found = []
        seen = set()

        for kw in keywords:
            matches = self.search_treatises(kw)
            for m in matches:
                fn = m["filename"]
                if fn not in seen:
                    seen.add(fn)
                    found.append(m)
                if len(found) >= 8:
                    break
            if len(found) >= 8:
                break

        return found
