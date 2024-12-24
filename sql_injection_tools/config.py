from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, host: str = None, port: str = None, cookie: str = None):
        self.host = host or os.getenv('HOST', '127.0.0.1')
        self.port = port or os.getenv('PORT', '8080')
        self.cookie = cookie or os.getenv('WEBGOAT')  # Changed from COOKIE to WEBGOAT
        
    @property
    def headers(self) -> Dict[str, str]:
        return {'Cookie': f'JSESSIONID={self.cookie}'} if self.cookie else {}  # Added JSESSIONID= prefix
    
    @property
    def base_url(self) -> str:
        return f'http://{self.host}:{self.port}/WebGoat/SqlInjectionAdvanced/challenge'
