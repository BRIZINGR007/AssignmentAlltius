from typing import Dict, List, TypedDict


class EmbeddingModelTH(TypedDict):
    vectorId: str
    references: Dict[str, str]
    text: str
    token: int
    embedding: List[float]
