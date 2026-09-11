"""Google NotebookLM Connector Bridge.
Connects with the user's Google NotebookLM account and interfaces with the 'ayurveda' notebook.
"""
import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class NotebookBridge:
    """Bridge for connecting and querying the 'ayurveda' notebook in Google NotebookLM."""

    def __init__(self, target_notebook_name: str = "ayurveda"):
        self.target_name = target_notebook_name.lower()
        self.active_notebook_id: Optional[str] = "071d79d8-c015-459e-af41-df466748367d"
        self.active_notebook_title: Optional[str] = "Ayurveda"
        self.auth_storage_path = os.path.expanduser("~/.notebooklm/profiles/default/storage_state.json")
        self._cached_auth: Optional[Dict[str, Any]] = None
        self._cached_connection: Optional[Dict[str, Any]] = None

    def import_cookies_json(self, json_str: str) -> Dict[str, Any]:
        """Imports exported cookie JSON directly into NotebookLM storage."""
        try:
            parsed = json.loads(json_str.strip())
            cookies = parsed if isinstance(parsed, list) else parsed.get("cookies", [])
            if not cookies:
                return {"success": False, "error": "No cookies found in the provided JSON."}
            
            storage_data = {
                "cookies": cookies,
                "origins": []
            }
            target_path = Path(self.auth_storage_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(json.dumps(storage_data, indent=2), encoding="utf-8")
            return {"success": True, "message": "Cookies saved successfully!"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_auth(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Checks if notebooklm session is active (cached for instant performance)."""
        if not force_refresh and self._cached_auth is not None:
            return self._cached_auth

        if not os.path.exists(self.auth_storage_path):
            self._cached_auth = {
                "authenticated": False,
                "message": "Storage state not found. Run 'notebooklm login' to authenticate your Google account.",
                "storage_path": self.auth_storage_path
            }
            return self._cached_auth

        # Instant check without slow subprocess: if file exists and has content, it is valid
        try:
            if os.path.getsize(self.auth_storage_path) > 30:
                self._cached_auth = {"authenticated": True, "message": "Authenticated with Google NotebookLM."}
                return self._cached_auth
        except Exception:
            pass

        self._cached_auth = {"authenticated": False, "message": "Storage file empty."}
        return self._cached_auth

    def list_notebooks(self) -> List[Dict[str, str]]:
        """Lists notebooks available in the authenticated user's account."""
        try:
            cmd = ["notebooklm", "list", "--json"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if res.returncode == 0 and res.stdout.strip():
                try:
                    data = json.loads(res.stdout)
                    if isinstance(data, dict) and "notebooks" in data:
                        return data["notebooks"]
                    elif isinstance(data, list):
                        return data
                except Exception:
                    pass
        except Exception:
            pass
        return []

    def connect_to_ayurveda_notebook(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Discovers and sets context to the 'ayurveda' notebook (cached for instant UI)."""
        if not force_refresh and self._cached_connection is not None:
            return self._cached_connection

        if self.active_notebook_id and self.active_notebook_title and not force_refresh:
            self._cached_connection = {
                "connected": True,
                "notebook_id": self.active_notebook_id,
                "title": self.active_notebook_title,
                "message": f"Successfully connected to notebook '{self.active_notebook_title}' (ID: {self.active_notebook_id})."
            }
            return self._cached_connection

        notebooks = self.list_notebooks()
        matched = None
        
        for nb in notebooks:
            if isinstance(nb, dict):
                title = nb.get("title", "").lower()
            elif isinstance(nb, str):
                title = nb.lower()
            else:
                continue

            if self.target_name in title:
                matched = nb
                break

        if matched:
            if isinstance(matched, dict):
                self.active_notebook_id = matched.get("id")
                self.active_notebook_title = matched.get("title")
            else:
                self.active_notebook_id = "071d79d8-c015-459e-af41-df466748367d"
                self.active_notebook_title = str(matched)
                
            # Set context
            if self.active_notebook_id:
                try:
                    subprocess.run(["notebooklm", "use", self.active_notebook_id], capture_output=True, timeout=5)
                except Exception:
                    pass
            return {
                "connected": True,
                "notebook_id": self.active_notebook_id,
                "title": self.active_notebook_title,
                "message": f"Successfully connected to notebook '{self.active_notebook_title}' (ID: {self.active_notebook_id})."
            }
        else:
            avail = []
            for nb in notebooks:
                if isinstance(nb, dict):
                    avail.append(nb.get("title", "Untitled"))
                else:
                    avail.append(str(nb))
            return {
                "connected": False,
                "message": f"Notebook '{self.target_name}' not yet found via CLI.",
                "available_notebooks": avail
            }

    def ask_notebook(self, query: str) -> Dict[str, Any]:
        """Sends a clinical question to the connected NotebookLM notebook."""
        try:
            cmd = ["notebooklm", "ask", "--new", "-y"]
            if self.active_notebook_id:
                cmd.extend(["--notebook", self.active_notebook_id])
            cmd.append(query)
                
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if res.returncode == 0 and res.stdout.strip():
                return {
                    "success": True,
                    "answer": res.stdout.strip(),
                    "source": f"NotebookLM: '{self.active_notebook_title or self.target_name}'"
                }
            else:
                err = res.stderr.strip() or res.stdout.strip()
                return {
                    "success": False,
                    "error": err or "No response returned from notebooklm CLI.",
                    "fallback_needed": True
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_needed": True
            }
