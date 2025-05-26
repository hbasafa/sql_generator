from typing import List, Dict, Any


def find_all_matches(data: List[Dict[str, Any]], query: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [item for item in data if all(item.get(k) == v for k, v in query.items())]
