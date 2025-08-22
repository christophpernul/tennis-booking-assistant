"""
User preferences management for the tennis booking assistant.
"""

from typing import Dict, List, Optional, Set


class UserPreferences:
    """Manages user preferences for tennis courts."""
    
    def __init__(self):
        # In-memory storage - in a real app this would be a database
        self._preferences: Dict[str, Dict] = {}
    
    def add_user_preference(self, user_name: str, preferred_courts: List[str]) -> None:
        """Add or update user preferences for specific courts."""
        if user_name not in self._preferences:
            self._preferences[user_name] = {}
        
        self._preferences[user_name]["preferred_courts"] = preferred_courts
    
    def get_user_preferences(self, user_name: str) -> Optional[Dict]:
        """Get user preferences by name."""
        return self._preferences.get(user_name)
    
    def get_preferred_courts(self, user_name: str) -> List[str]:
        """Get preferred courts for a specific user."""
        user_prefs = self.get_user_preferences(user_name)
        if user_prefs and "preferred_courts" in user_prefs:
            return user_prefs["preferred_courts"]
        return []
    
    def add_user_court_type_preference(self, user_name: str, court_types: List[str]) -> None:
        """Add court type preferences for a user."""
        if user_name not in self._preferences:
            self._preferences[user_name] = {}
        
        self._preferences[user_name]["preferred_court_types"] = court_types
    
    def get_preferred_court_types(self, user_name: str) -> List[str]:
        """Get preferred court types for a specific user."""
        user_prefs = self.get_user_preferences(user_name)
        if user_prefs and "preferred_court_types" in user_prefs:
            return user_prefs["preferred_court_types"]
        return []
    
    def add_excluded_courts(self, user_name: str, excluded_courts: List[str]) -> None:
        """Add courts that a user wants to exclude."""
        if user_name not in self._preferences:
            self._preferences[user_name] = {}
        
        self._preferences[user_name]["excluded_courts"] = excluded_courts
    
    def get_excluded_courts(self, user_name: str) -> List[str]:
        """Get courts that a user wants to exclude."""
        user_prefs = self.get_user_preferences(user_name)
        if user_prefs and "excluded_courts" in user_prefs:
            return user_prefs["excluded_courts"]
        return []
    
    def is_court_excluded(self, user_name: str, court_id: str) -> bool:
        """Check if a specific court is excluded for a user."""
        excluded_courts = self.get_excluded_courts(user_name)
        return court_id in excluded_courts


# Global instance
user_preferences = UserPreferences()

# Add some sample user preferences
# Laura - prefers courts 15-22, excludes courts A, 1-14, and T
user_preferences.add_user_preference("Laura", ["court_15", "court_16", "court_17", "court_18", "court_19", "court_20", "court_21", "court_22"])
user_preferences.add_user_court_type_preference("Laura", ["hard", "wingfield"])
user_preferences.add_excluded_courts("Laura", ["court_a", "court_1", "court_2", "court_3", "court_4", "court_5", "court_6", "court_7", "court_8", "court_9", "court_10", "court_11", "court_12", "court_13", "court_14", "court_t"])

# Christoph - prefers courts A, T, and 15-22, likes clay courts
user_preferences.add_user_preference("Christoph", ["court_a", "court_t", "court_15", "court_16", "court_17", "court_18", "court_19", "court_20", "court_21", "court_22"])
user_preferences.add_user_court_type_preference("Christoph", ["clay", "indoor", "hard", "wingfield"])

# Sarah - prefers indoor courts
user_preferences.add_user_preference("Sarah", ["court_4"])
user_preferences.add_user_court_type_preference("Sarah", ["indoor"])

# Mike - prefers hard courts
user_preferences.add_user_preference("Mike", ["court_5", "court_6"])
user_preferences.add_user_court_type_preference("Mike", ["hard"])

