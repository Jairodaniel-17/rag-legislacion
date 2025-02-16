# Documentación del Sistema LLM

## LLMManager

El `LLMManager` es el componente responsable de la interacción con modelos de lenguaje grandes (LLMs). Proporciona una interfaz unificada para generar respuestas utilizando diferentes modelos de lenguaje.

### Configuración

El sistema utiliza variables de entorno para su configuración:

```env
LLM_MODEL_NAME=gpt4o-mini    # Modelo a utilizar
LLM_TEMPERATURE=0.7             # Temperatura para generación (0.0-1.0)
LLM_API_KEY=tu-api-key         # Clave API del proveedor
LLM_BASE_URL=https://api.openai.com/v1  # URL base del API
```

### Inicialización

```python
from llm.llm_manager import LLMManager

llm = LLMManager()
```

El constructor:

1. Carga las variables de entorno
2. Inicializa la conexión con el LLM
3. Configura los parámetros del modelo

### Métodos Principales

#### generate_response(prompt: str) -> str

Genera una respuesta directa del modelo.

```python
response = llm.generate_response("¿Cuál es el propósito del habeas corpus?")
```

- Parámetros:
  - `prompt`: Texto de la pregunta o instrucción
- Retorna: Respuesta generada por el modelo
- Manejo de errores incluido

#### generate_response_with_context(prompt: str, context: str) -> str

Genera una respuesta considerando un contexto específico.

```python
response = llm.generate_response_with_context(
    prompt="¿Cuál es la pena por este delito?",
    context="Artículo 189.- Robo agravado: La pena será..."
)
```

- Parámetros:
  - `prompt`: Pregunta del usuario
  - `context`: Contexto relevante para la respuesta
- Retorna: Respuesta generada considerando el contexto
- Utiliza un prompt template optimizado

### Prompt Template

El sistema utiliza un template predefinido para estructurar las consultas:

```python
PROMPT_TEMPLATE = ChatPromptTemplate([
    ("system", "Answer the user's question, using the context provided."),
    ("user", "User query: '{user question}' context to answer user question: '{context}'"),
])
```

Este template:

- Proporciona instrucciones claras al modelo
- Mantiene consistencia en las respuestas
- Facilita la incorporación de contexto

### Consideraciones Técnicas

#### Manejo de Errores

- Captura y manejo de excepciones en todas las operaciones
- Retroalimentación clara sobre errores
- Prevención de fallos en cadena

#### Optimización

- Reutilización de conexiones
- Validación de parámetros
- Gestión eficiente de recursos

#### Extensibilidad

- Diseño modular para soportar diferentes modelos
- Fácil adaptación a nuevos proveedores
- Configuración flexible mediante variables de entorno

### Integración con Vectorstore

El LLMManager está diseñado para trabajar en conjunto con el sistema de vectorstore:

1. El vectorstore encuentra documentos relevantes
2. Los documentos se proporcionan como contexto
3. El LLM genera respuestas informadas por este contexto

### Mejores Prácticas

1. **Configuración**
   - Mantener las variables de entorno actualizadas
   - Verificar la disponibilidad del API antes de operaciones
   - Monitorear el uso de tokens

2. **Uso**
   - Proporcionar contexto relevante cuando sea posible
   - Validar las respuestas para casos críticos
   - Implementar retry logic para fallos temporales

3. **Mantenimiento**
   - Actualizar regularmente las dependencias
   - Monitorear el rendimiento del modelo
   - Mantener logs de errores y uso

### Ejemplos de Uso

#### Consulta Simple

```python
llm = LLMManager()
response = llm.generate_response("Explica el concepto de debido proceso")
print(response)
```

#### Consulta con Contexto

```python
context = """
Artículo 139.- Son principios y derechos de la función jurisdiccional:
3. La observancia del debido proceso y la tutela jurisdiccional...
"""

response = llm.generate_response_with_context(
    "¿Qué establece la constitución sobre el debido proceso?",
    context
)
print(response)
```

### Limitaciones Conocidas

1. Dependencia de conectividad a internet
2. Límites de tokens por request
3. Costos asociados al uso del API
4. Posibles sesgos en las respuestas del modelo

### Futuras Mejoras

- Implementación de cache local
- Soporte para más proveedores de LLM
- Sistema de retry con backoff exponencial
- Métricas detalladas de uso y rendimiento
