from typing import Dict, List

# This file contains LoggingGlobal variables
levels: Dict[str, int] = {'DEBUG': 10, 'INFO': 20,
                          'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}

console_types: List[str] = ['normal', 'color']
logging_types: List[str] = ['console', 'file']
