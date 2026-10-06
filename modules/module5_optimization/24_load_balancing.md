# 5.6 Load Balancing

## Keys do not add capacity
Rate limits are set per organization and workspace, so extra API keys inside one organization do not raise your limits. Separate organizations or providers are the only way to get separate quotas; check the terms before splitting traffic that way.

## Provider and Region Balancing
On Amazon Bedrock and Vertex AI, quotas are per cloud account/project and region. Global inference profiles (Bedrock `global.` prefix) route dynamically across regions for availability; regional profiles (`us.`, `eu.`, ...) keep data in a geography and cost about 10% more. A common pattern is a primary route plus a fallback to a second region or provider, with the same prompts and a model ID adapted per platform (see [Cloud Platform Integration](./26_cloud_integration.md)).

## Next Steps
- [Deployment Strategies](./25_deployment.md).
