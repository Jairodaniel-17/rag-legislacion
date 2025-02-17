# RAG Legislación

Sistema de Recuperación Aumentada por Generación (RAG) para documentos legislativos. Este sistema permite procesar, indexar y consultar documentos legales utilizando modelos de lenguaje y búsqueda semántica.

## Características

- Procesamiento de múltiples formatos de documentos (PDF, DOCX, TXT)
- Sistema de embeddings usando Ollama
- Búsqueda semántica con FAISS
- Integración con modelos de lenguaje para generación de respuestas
- Gestión eficiente de bases de datos vectoriales
- Busqueda de documentos similares y generación de respuestas en base a contexto relevante utilizando el algoritmo de recuperación de documentos (RAG)
- Busqueda de similitud entre documentos utilizando embeddings

## Requisitos

- Python >= 3.11
- Ollama instalado localmente (para embeddings)
- Acceso a API de OpenAI o compatible (para LLM)

### Opcional (para desarrollo)

```bash
# Ollama con un LLM es compatible con la API de OpenAI 
LLM_MODEL_NAME="llama3.2:latest"
LLM_API_KEY="ollama"
LLM_BASE_URL="http://localhost:11434/v1"
LLM_TEMPERATURE=0.3
```

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual de Python:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:

   ```bash
   pip install .
   ```

## Configuración

Crear un archivo `.env` basado en el `example.env` proporcionado:

```env
LLM_MODEL_NAME=gpt4o-mini
LLM_TEMPERATURE=0.7
LLM_API_KEY=tu-api-key
LLM_BASE_URL=https://api.openai.com/v1  # O la URL de tu proveedor compatible
```

## Estructura del Proyecto

```plainttext
|
├── database/            # Almacenamiento de bases de datos vectoriales
├── derecho_files/       # Archivos de legislación
├── documentation/       # Documentación del proyecto
├── llm/              
│   └── llm_manager.py   # Gestión de modelos de lenguaje
├── vectorstore/
│   ├── document_processor.py  # Procesamiento de documentos
│   ├── embeddings.py         # Gestión de embeddings
│   └── vectorstore_manager.py # Gestión de la base de datos vectorial
└── hello.py            # Script principal
```

Para una documentación más detallada, consulta los siguientes recursos:

- [Guía de Instalación y Configuración](documentation/setup.md)
- [Documentación del Sistema Vectorstore](documentation/vectorstore.md)
- [Documentación del Sistema LLM](documentation/llm.md)

## Uso

### Procesamiento de Documentos

```python
from vectorstore.vectorstore_manager import VectorStoreManager

# Inicializar gestor
manager = VectorStoreManager(path="derecho_files", name="mi_base")

# Crear base de datos vectorial
manager.create_vectorstore()
```

### Búsqueda de Documentos

```python
# Buscar documentos similares
resultados = manager.search_similarity("¿Cuál es la pena por robo agravado?")

# Buscar en una fuente específica
resultados = manager.search_similarity("¿Cuál es la pena por robo agravado?", fuente="codigo_penal.pdf")
```

### Generación de Respuestas

```python
from llm.llm_manager import LLMManager

llm = LLMManager()
respuesta = llm.generate_response_with_context(
    prompt="¿Cuál es la pena por robo agravado?",
    context="[Contenido relevante del código penal]"
)
```

## Características del Sistema

### Gestor de Documentos

- Soporta múltiples formatos (PDF, DOCX, TXT)
- Procesamiento automático de directorios
- Manejo eficiente de codificación UTF-8

### Sistema de Embeddings

- Utiliza el modelo nomic-embed-text de Ollama
- Implementación singleton para eficiencia
- Gestión automática de recursos

### Base de Datos Vectorial

- Implementada con FAISS para búsqueda eficiente
- Soporte para filtrado por fuente
- Funciones de mantenimiento (añadir, eliminar, actualizar)
- Exportación e importación de bases de datos

### Modelo de Lenguaje

- Integración flexible con OpenAI y APIs compatibles
- Sistema de prompts optimizado
- Manejo de errores robusto

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request.

## Licencia

[MIT](https://opensource.org/licenses/MIT)
