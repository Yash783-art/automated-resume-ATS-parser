from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Embedder, cls).__new__(cls)
            # Load model lazily
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._instance

    def embed(self, texts: list[str]) -> np.ndarray:
        """
        Generates embeddings for a list of strings.
        """
        if not texts:
            return np.array([])
        return self._model.encode(texts)

embedder = Embedder()
