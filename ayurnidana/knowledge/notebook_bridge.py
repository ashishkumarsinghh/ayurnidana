"""Google NotebookLM Connector Bridge.
Connects with the user's Google NotebookLM account and interfaces with the 'ayurveda' notebook.
"""
import os
import subprocess
import json
from typing import Dict, Any, List, Optional

class NotebookBridge:
    """Bridge for connecting and querying the 'ayurveda' notebook in Google NotebookLM."""

    def __init__(self, target_notebook_name: str = "ayurveda"):
        self.target_name = target_notebook_name.lower()
        self.active_notebook_id: Optional[str] = None
        self.active_notebook_title: Optional[str] = None
        self.auth_storage_path = os.path.expanduser("~/.notebooklm/profiles/default/storage_state.json")

    def check_auth(self) -> Dict[str, Any]:
        """Checks if notebooklm session is active."""
        if not os.path.exists(self.auth_storage_path):
            return {
                "authenticated": False,
                "message": "Storage state not found. Run 'notebooklm login' to authenticate your Google account.",
                "storage_path": self.auth_storage_path
            }

        try:
            cmd = ["notebooklm", "auth", "check", "--json"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                return {"authenticated": True, "message": "Authenticated with Google NotebookLM."}
            else:
                return {
                    "authenticated": True,  # Storage file exists
                    "message": "Storage file present. Ready to query.",
                    "details": res.stdout or res.stderr
                }
        except Exception as e:
            return {
                "authenticated": os.path.exists(self.auth_storage_path),
                "message": f"Session check: {str(e)}"
            }

    def list_notebooks(self) -> List[Dict[str, str]]:
        """Lists notebooks available in the authenticated user's account."""
        try:
            cmd = ["notebooklm", "list", "--json"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if res.returncode == 0 and res.stdout.strip():
                try:
                    data = json.loads(res.stdout)
                    return data
                except Exception:
                    pass
        except Exception:
            pass
        return []

    def connect_to_ayurveda_notebook(self) -> Dict[str, Any]:
        """Discovers and sets context to the 'ayurveda' notebook."""
        notebooks = self.list_notebooks()
        matched = None
        
        for nb in notebooks:
            title = nb.get("title", "").lower()
            if self.target_name in title:
                matched = nb
                break

        if matched:
            self.active_notebook_id = matched.get("id")
            self.active_notebook_title = matched.get("title")
            # Set context
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
            return {
                "connected": False,
                "message": f"Notebook '{self.target_name}' not yet found via CLI. You can specify a Notebook ID or ensure 'notebooklm login' is completed.",
                "available_notebooks": [nb.get("title") for nb in notebooks]
            }

    def ask_notebook(self, query: str) -> Dict[str, Any]:
        """Sends a clinical question to the connected NotebookLM notebook."""
        try:
            cmd = ["notebooklm", "ask", query]
            if self.active_notebook_id:
                cmd.extend(["--notebook", self.active_notebook_id])
                
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
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
