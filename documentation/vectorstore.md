# Documentación del Sistema Vectorstore

## VectorStoreManager

El `VectorStoreManager` es el componente central para la gestión de documentos vectorizados. Proporciona una interfaz completa para crear, mantener y consultar bases de datos vectoriales de documentos.

### Inicialización

```python
manager = VectorStoreManager(path="ruta_documentos", name="nombre_base")
```

Parámetros:

- `path`: Ruta al directorio que contiene los documentos a procesar
- `name`: Identificador único para la base de datos vectorial

### Métodos Principales

#### create_vectorstore() -> bool

Crea una nueva base de datos vectorial procesando todos los documentos en el directorio especificado.

- Divide los documentos en chunks de 1000 caracteres con overlap de 200
- Genera embeddings usando el modelo nomic-embed-text
- Almacena la base de datos en el directorio `database/{name}`

#### search_similarity(query: str, fuente: Optional[str] = None) -> str

Realiza búsquedas semánticas en la base de datos.

- `query`: Texto de búsqueda
- `fuente`: Opcional, filtra resultados por fuente específica
- Retorna: Lista de los 5 documentos más relevantes

#### add_files_vectorstore() -> Optional[FAISS]

Añade nuevos documentos a una base de datos existente.

- Los documentos deben estar en el directorio `documentation/`
- Mantiene la consistencia de la base de datos existente
- Retorna la base de datos actualizada o None si hay error

## DocumentProcessor

Gestiona la carga y procesamiento de diferentes tipos de documentos.

### Formatos Soportados

- PDF (usando PyMuPDF)
- DOCX/DOC (usando Docx2txt)
- TXT (con codificación UTF-8)

### Uso

```python
processor = DocumentProcessor(path="ruta_documentos")
documents = processor.files_to_texts()
```

El procesador automáticamente:

1. Detecta el tipo de archivo
2. Aplica el loader correspondiente
3. Extrae el texto manteniendo metadatos relevantes

## EmbeddingManager

Implementación singleton para la gestión eficiente de embeddings.

### Características

- Utiliza el modelo nomic-embed-text de Ollama
- Reutiliza la instancia del modelo para optimizar recursos
- Gestión automática de warnings

### Uso de Embeddings

```python
embeddings = EmbeddingManager.get_embeddings()
```

## Consideraciones Técnicas

### Rendimiento

- Los chunks de 1000 caracteres están optimizados para balance entre contexto y precisión
- El overlap de 200 caracteres ayuda a mantener coherencia entre chunks
- FAISS proporciona búsqueda eficiente en grandes volúmenes de datos

### Almacenamiento

- Las bases de datos se almacenan en formato FAISS en el directorio `database/`
- Cada base tiene su propio subdirectorio para aislamiento
- Soporte para exportación/importación mediante ZIP

### Escalabilidad

- Diseño modular para fácil extensión
- Soporte para procesamiento por lotes
- Gestión eficiente de memoria con grandes volúmenes de datos
