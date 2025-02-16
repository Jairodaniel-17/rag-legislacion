# Guía de Instalación y Configuración

Esta guía proporciona instrucciones detalladas para instalar y configurar el sistema RAG de Legislación.

## Requisitos Previos

### Software Necesario

1. **Python**
   - Versión: >= 3.11
   - Verificar instalación:

     ```bash
     python --version
     ```

2. **Ollama**
   - Requerido para embeddings locales
   - [Instrucciones de instalación de Ollama](https://github.com/ollama/ollama)
   - Verificar instalación:

     ```bash
     ollama --version
     ```

3. **Git**
   - Para clonar el repositorio
   - [Descargar Git](https://git-scm.com/downloads)

### Requisitos de Hardware Recomendados

- CPU: 4 cores o más
- RAM: 8GB mínimo, 16GB recomendado
- Almacenamiento: 10GB mínimo para instalación y datos base

## Instalación

### 1. Clonar el Repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd rag-legislacion
```

### 2. Configurar Entorno Virtual

#### En Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### En macOS/Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Configuración

### 1. Variables de Entorno

Crear archivo `.env` basado en `example.env`:

```bash
cp example.env .env
```

Editar `.env` con tus configuraciones:

```env
# Configuración del LLM
LLM_MODEL_NAME=gpt4o-mini
LLM_TEMPERATURE=0.7
LLM_API_KEY=tu-api-key
LLM_BASE_URL=https://api.openai.com/v1

# Otras configuraciones según necesidad
```

### 2. Estructura de Directorios

Crear los directorios necesarios:

```bash
mkdir -p database
mkdir -p derecho_files
```

### 3. Configurar Ollama

1. Iniciar el servicio de Ollama:

   ```bash
   ollama serve
   ```

2. Descargar el modelo necesario:

   ```bash
   ollama pull nomic-embed-text
   ```

## Verificación de la Instalación

### 1. Probar el Sistema de Embeddings

```python
from vectorstore.embeddings import EmbeddingManager

embeddings = EmbeddingManager.get_embeddings()
# Debería inicializarse sin errores
```

### 2. Probar el LLM

```python
from llm.llm_manager import LLMManager

llm = LLMManager()
response = llm.generate_response("Test de funcionamiento")
print(response)
```

### 3. Probar el Vectorstore

```python
from vectorstore.vectorstore_manager import VectorStoreManager

manager = VectorStoreManager(path="derecho_files", name="test")
# Debería inicializarse sin errores
```

## Estructura de Archivos

```plainttext
rag-legislacion/
├── .env                  # Configuración del ambiente
├── database/            # Bases de datos vectoriales
├── derecho_files/       # Documentos legales
├── documentation/       # Documentación del proyecto
├── llm/                # Módulo LLM
└── vectorstore/        # Módulo Vectorstore
```

## Solución de Problemas Comunes

### 1. Error de Conexión con Ollama

Si encuentras errores de conexión con Ollama:

1. Verifica que el servicio esté corriendo:

   ```bash
   ollama serve
   ```

2. Comprueba que el modelo esté instalado:

   ```bash
   ollama list
   ```

### 2. Errores de API del LLM

Si hay problemas con la API del LLM:

1. Verifica tu API key en el archivo .env
2. Comprueba la conectividad a internet
3. Verifica los límites de tu cuenta

### 3. Problemas con los Embeddings

Si los embeddings no funcionan:

1. Reinicia el servicio de Ollama
2. Verifica la memoria disponible
3. Comprueba los logs de Ollama

## Mantenimiento

### Actualizaciones

1. Actualizar el código:

   ```bash
   git pull origin main
   ```

2. Actualizar dependencias:

   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. Actualizar modelo de embeddings:

   ```bash
   ollama pull nomic-embed-text
   ```

### Backups

1. Respaldar bases de datos vectoriales:
   - Copiar el directorio `database/`
   - Mantener respaldos de documentos originales

2. Respaldar configuración:
   - Guardar archivo `.env`
   - Documentar cambios en la configuración

## Seguridad

### Mejores Prácticas

1. No compartir claves API
2. Mantener actualizadas las dependencias
3. Revisar regularmente los logs
4. Implementar control de acceso según necesidad

## Recursos Adicionales

- [Documentación de LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Documentación de FAISS](https://github.com/facebookresearch/faiss/wiki)
- [Guía de Ollama](https://github.com/ollama/ollama)
