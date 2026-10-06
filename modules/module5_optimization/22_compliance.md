# 5.6 Compliance and Data Privacy

## Anthropic's Data Policy
- **Standard API:** Data is not used for training by default (check the latest commercial terms).
- **Retention:** Inputs and outputs are retained for a limited period (30 days at the time of writing); zero data retention is available by agreement. Verify current terms for your organization, and note that Bedrock, Vertex and Foundry follow the cloud provider's policies.

## GDPR / CCPA
If a user asks to be deleted, you must delete their data from your logs.
- Claude doesn't store user data long-term, but *you* do (in logs/DB).

## Next Steps
- Move to [Scaling and Deployment](./23_scaling.md).
