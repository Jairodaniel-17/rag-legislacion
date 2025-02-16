# Documentación RAG Legislación

## Índice de Documentación

### 1. Documentación General

- [README](../README.md) - Visión general del proyecto, características principales y guía rápida de inicio

### 2. Guías

- [Instalación y Configuración](setup.md) - Guía detallada de instalación y configuración del sistema

### 3. Documentación Técnica

- [Sistema Vectorstore](vectorstore.md) - Documentación del sistema de procesamiento y búsqueda de documentos
- [Sistema LLM](llm.md) - Documentación del sistema de modelos de lenguaje

## Estructura del Sistema

```plainttext
rag-legislacion/
├── database/            # Almacenamiento de bases vectoriales
├── derecho_files/       # Documentos legales source
├── documentation/      # Documentación del proyecto
│   ├── index.md        # Este archivo
│   ├── setup.md        # Guía de instalación
│   ├── vectorstore.md  # Doc. técnica vectorstore
│   └── llm.md         # Doc. técnica LLM
├── llm/               # Módulo LLM
└── vectorstore/       # Módulo Vectorstore
    ├── document_processor.py
    ├── embeddings.py
    └── vectorstore_manager.py
```

## Guía Rápida

1. **Instalación**
   - Ver [guía de instalación](setup.md)

2. **Procesar Documentos**

   ```python
   from vectorstore.vectorstore_manager import VectorStoreManager
   manager = VectorStoreManager(path="derecho_files", name="mi_base")
   manager.create_vectorstore()
   ```

3. **Realizar Consultas**

   ```python
   # Búsqueda de documentos
   resultados = manager.search_similarity("¿Cuál es la pena por robo agravado?")
   
   # Generar respuesta con contexto
   from llm.llm_manager import LLMManager
   llm = LLMManager()
   respuesta = llm.generate_response_with_context(
       prompt="¿Cuál es la pena por robo agravado?",
       context=resultados
   )
   ```

## Enlaces Útiles

- [Repositorio del Proyecto](URL_DEL_REPOSITORIO)
- [Reporte de Issues](URL_DEL_REPOSITORIO/issues)
- [Wiki del Proyecto](URL_DEL_REPOSITORIO/wiki)

## Nota Importante

El directorio `docs/` está reservado para uso interno del VectorStoreManager. Toda la documentación del proyecto se encuentra en el directorio `documentation/`.
