"""
Data management utilities for budget data
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import json
from pathlib import Path

class DataManager:
    """Manage budget data persistence"""
    
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_data(self, filename: str, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> bool:
        """Save data to JSON file"""
        try:
            filepath = self.data_dir / f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            print(f"[v0] Data saved successfully to {filepath}")
            return True
        except Exception as e:
            print(f"[v0] Error saving data: {e}")
            return False
    
    def load_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            filepath = self.data_dir / f"{filename}.json"
            if not filepath.exists():
                print(f"[v0] No saved data found at {filepath}")
                return []

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # ✅ Vérification du type du JSON avant de le retourner
            if isinstance(data, dict):
                return [data]
            elif isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
            else:
                print(f"[v0] Unexpected data format in {filepath}: {type(data)}")
                return []
        except Exception as e:
            print(f"[v0] Error loading data: {e}")
            return []
    
    def export_all_data(self) -> Dict[str, Any]:
        """Export all budget data"""
        return {
            "income": self.load_data("income") or [],
            "expenses": self.load_data("expenses") or [],
            "savings_goals": self.load_data("savings_goals") or [],
            "settings": self.load_data("settings") or {},
            "export_date": datetime.now().isoformat()
        }
