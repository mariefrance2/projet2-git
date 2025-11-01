"""
State management utilities for the application
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AppState:
    """Application state manager"""
    current_user: Optional[str] = None
    currency: str = "USD"
    theme: str = "Light"
    last_updated: datetime = field(default_factory=datetime.now)
    
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update application settings"""
        for key, value in settings.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_updated = datetime.now()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state as dictionary"""
        return {
            "current_user": self.current_user,
            "currency": self.currency,
            "theme": self.theme,
            "last_updated": self.last_updated.isoformat()
        }
