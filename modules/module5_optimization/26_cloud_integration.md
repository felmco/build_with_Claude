# 5.6 Cloud Platform Integration

The SDK ships platform clients with the same `messages.create(...)` interface. What changes is authentication, the model ID format, and which features exist.

## Amazon Bedrock
- Use Claude via AWS.
- **Benefit:** Integrated billing, IAM security, PrivateLink.
- Install with `pip install -U "anthropic[bedrock]"` and use `AnthropicBedrockMantle` (the Messages-API Bedrock endpoint). Model IDs carry an `anthropic.` prefix.

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

The older `AnthropicBedrock` client (InvokeModel/Converse, ARN-versioned IDs such as `global.anthropic.claude-opus-4-6-v1`) still exists for Opus 4.6 and earlier models.

## Google Vertex AI
- Use Claude via Google Cloud.
- **Benefit:** Integration with BigQuery, Vertex Agent Builder.
- Install with `pip install -U "anthropic[vertex]"`.

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(region="us-east5", project_id="my-gcp-project")
# model IDs on Vertex can differ from first-party IDs: check the Vertex model list for the exact string
```

## Microsoft Foundry
- Use `AnthropicFoundry(resource=..., api_key=...)` (or an Azure AD token provider) and the model/deployment name from your Foundry resource.

## Claude Platform on AWS
- `from anthropic import AnthropicAWS` (`pip install -U "anthropic[aws]"`) is an Anthropic-operated service billed through AWS. It uses bare first-party model IDs and needs `AWS_REGION` and a workspace ID.

## What differs on third-party platforms
Not every feature is available everywhere. For example, Message Batches, the Files API and the Models API are first-party only; web search/fetch and code execution tools are limited or missing on Bedrock and Vertex; `inference_geo` is first-party only. Check the [feature availability table](https://platform.claude.com/docs/en/build-with-claude/overview) before choosing a platform, and never reuse a first-party model ID on Bedrock (it returns a 400).

## Conclusion
You have now completed the entire **Build with Claude** course!

You have mastered:
1. **Foundation:** API basics.
2. **Core:** Conversation & Vision.
3. **Advanced:** Tools & Caching.
4. **Apps:** Agents & RAG.
5. **Optimization:** Scaling & Production.

**Go build something amazing!**
