from app.ioc.ioc import SingletonMeta

from model2vec import StaticModel
from typing import List


class EmbeddingGenerator(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.model = StaticModel.from_pretrained("minishlab/potion-base-2M")

    def load_model(self) -> None:
        StaticModel.from_pretrained("minishlab/potion-base-2M").save_pretrained(
            "minishlab/potion-base-2M"
        )

    def get_embeddings(self, text: str) -> List[float]:
        embeddings = self.model.encode([text])
        return embeddings.tolist()[0]
