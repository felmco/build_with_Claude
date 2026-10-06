# 5.6 Integración con Plataforma en la Nube

El SDK incluye clientes para cada plataforma con la misma interfaz `messages.create(...)`. Lo que cambia es la autenticación, el formato del ID del modelo y qué funciones existen.

## Amazon Bedrock
- Usa Claude vía AWS.
- **Beneficio:** Facturación integrada, seguridad IAM, PrivateLink.
- Instala con `pip install -U "anthropic[bedrock]"` y usa `AnthropicBedrockMantle` (el endpoint de Bedrock para la API de Messages). Los IDs de modelo llevan el prefijo `anthropic.`.

```python
from anthropic import AnthropicBedrockMantle

client = AnthropicBedrockMantle(aws_region="us-east-1")  # AWS credentials from the default chain
response = client.messages.create(
    model="anthropic.claude-sonnet-5-5",  # not "claude-sonnet-5-5"
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.content[0].text)
```

El cliente anterior `AnthropicBedrock` (InvokeModel/Converse, IDs con versión tipo ARN como `global.anthropic.claude-opus-4-6-v1`) sigue existiendo para Opus 4.6 y modelos anteriores.

## Google Vertex AI
- Usa Claude vía Google Cloud.
- **Beneficio:** Integración con BigQuery, Vertex Agent Builder.
- Instala con `pip install -U "anthropic[vertex]"`.

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(region="us-east5", project_id="my-gcp-project")
# model IDs on Vertex can differ from first-party IDs: check the Vertex model list for the exact string
```

## Microsoft Foundry
- Usa `AnthropicFoundry(resource=..., api_key=...)` (o un proveedor de tokens de Azure AD) y el nombre del modelo/despliegue de tu recurso de Foundry.

## Claude Platform en AWS
- `from anthropic import AnthropicAWS` (`pip install -U "anthropic[aws]"`) es un servicio operado por Anthropic y facturado a través de AWS. Usa IDs de modelo de primera parte sin prefijo y requiere `AWS_REGION` y un ID de workspace.

## Qué difiere en plataformas de terceros
No todas las funciones están disponibles en todas partes. Por ejemplo, Message Batches, la API de Files y la API de Models son solo de primera parte; las herramientas de búsqueda/obtención web y de ejecución de código son limitadas o no existen en Bedrock y Vertex; `inference_geo` es solo de primera parte. Consulta la [tabla de disponibilidad de funciones](https://platform.claude.com/docs/en/build-with-claude/overview) antes de elegir una plataforma, y nunca reutilices un ID de modelo de primera parte en Bedrock (devuelve un 400).

## Conclusión
¡Ahora has completado el curso completo **Construir con Claude**!

Has dominado:
1. **Fundamentos:** Conceptos básicos de la API.
2. **Núcleo:** Conversación y Visión.
3. **Avanzado:** Herramientas y Caché.
4. **Apps:** Agentes y RAG.
5. **Optimización:** Escalado y Producción.

**¡Ve y construye algo asombroso!**
