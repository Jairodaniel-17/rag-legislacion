import os

from langchain_community.vectorstores.faiss import DistanceStrategy


class DistanceStrategyManager:
    """Clase para gestionar la estrategia de distancia a utilizar en el vectorstore.

    Esta clase implementa un patrón singleton para garantizar que sólo se configure
    una vez la estrategia de distancia en toda la aplicación. La estrategia se selecciona
    en función del tipo de embeddings que se estén utilizando:

    - **OllamaEmbeddings**: Si se activa el flag de embeddings (FLAG_EMBEDDINGS == "1"), se asume
      que se están usando embeddings de Ollama (por ejemplo, "nomic-embed-text"), los cuales
      generalmente **no están normalizados**. En este caso, se forza el uso de la estrategia
      `MAX_INNER_PRODUCT`, ya que es la más adecuada para comparar vectores sin normalizar.

    - **HuggingFaceEmbeddings**: Cuando FLAG_EMBEDDINGS no es "1", se asume que se utilizan embeddings
      de HuggingFace, los cuales se configuran para normalizar los vectores
      (usando `normalize_embeddings=True`).
      En este escenario se permite elegir la estrategia de distancia a través de la variable de entorno
      `DISTANCE_STRATEGY`. El valor por defecto es `EUCLIDEAN_DISTANCE`, aunque comúnmente se recomienda
      utilizar `COSINE` para vectores normalizados.
    """  # noqa: E501

    _instance = None
    _strategy = None

    def __new__(cls):  # noqa: D102
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la estrategia de distancia según el tipo de embeddings configurado.

        Proceso de inicialización:

        1. Se lee la variable de entorno `FLAG_EMBEDDINGS`:
           - Si `FLAG_EMBEDDINGS` es "1", se están utilizando embeddings de Ollama.
             Dado que estos embeddings (por ejemplo, con el modelo "nomic-embed-text")
             **no se normalizan**, se fuerza el uso de `MAX_INNER_PRODUCT` para obtener
             comparaciones más precisas teniendo en cuenta la magnitud de los vectores.

           - Si `FLAG_EMBEDDINGS` es distinto de "1" (por defecto "0"), se asume que se
             utilizan embeddings de HuggingFace, los cuales se configuran para
             normalización. En este caso, se permite elegir la estrategia de distancia
             mediante la variable `DISTANCE_STRATEGY`.

        2. Si se está en el caso de HuggingFace, se toma el valor de `DISTANCE_STRATEGY`
           (por defecto "EUCLIDEAN_DISTANCE"), se convierte a mayúsculas y se resuelve a
           la estrategia correspondiente mediante el método `_resolve_strategy`.
        """
        flag_embeddings = os.getenv("FLAG_EMBEDDINGS", "0")
        if flag_embeddings == "1":
            self._strategy = DistanceStrategy.MAX_INNER_PRODUCT
        else:
            strategy = os.getenv("DISTANCE_STRATEGY", "EUCLIDEAN_DISTANCE").upper()
            self._strategy = self._resolve_strategy(strategy)

    def _resolve_strategy(self, strategy: str) -> DistanceStrategy:
        """Resuelve la estrategia de distancia a partir de una cadena de texto.

        Parámetros:
            strategy (str): La estrategia en formato de cadena. Puede ser:
                - "EUCLIDEAN_DISTANCE"
                - "MAX_INNER_PRODUCT"
                - "DOT_PRODUCT"
                - "JACCARD"
                - "COSINE"

        Retorna:
            DistanceStrategy: La estrategia de distancia correspondiente.

        Lanza:
            ValueError: Si la estrategia proporcionada no es reconocida.
        """
        match strategy:
            case "EUCLIDEAN_DISTANCE":
                return DistanceStrategy.EUCLIDEAN_DISTANCE
            case "MAX_INNER_PRODUCT":
                return DistanceStrategy.MAX_INNER_PRODUCT
            case "DOT_PRODUCT":
                return DistanceStrategy.DOT_PRODUCT
            case "JACCARD":
                return DistanceStrategy.JACCARD
            case "COSINE":
                return DistanceStrategy.COSINE
            case _:
                raise ValueError(f"Estrategia desconocida: {strategy}")

    @property
    def strategy(self) -> DistanceStrategy:
        """Propiedad para obtener la estrategia de distancia configurada.

        Retorna:
            DistanceStrategy: La estrategia de distancia que se usará en el vectorstore.
        """
        return self._strategy
