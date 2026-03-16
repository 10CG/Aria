from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ResponseMeta:
    """Pagination metadata"""
    total: int
    page: int
    page_size: int
    has_next: bool

def task_list_response(tasks: List[Dict[str, Any]], total: int, page: int, page_size: int) -> Dict[str, Any]:
    """New response schema: {data: [...], meta: {...}}
    
    BREAKING CHANGE: Response format changed from {tasks: [...]} to {data: [...], meta: {...}}
    This requires all API consumers to update their response parsing logic.
    """
    has_next = page * page_size < total
    return {
        "data": tasks,
        "meta": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_next": has_next
        }
    }
