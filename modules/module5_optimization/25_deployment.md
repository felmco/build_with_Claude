# 5.6 Deployment Strategies

## Serverless (Lambda/Cloud Functions)
- **Pros:** Cheap for low traffic.
- **Cons:** "Cold Starts" add latency to the first request.

## Long-Running Containers (Fargate/K8s)
- **Pros:** No cold starts, better for streaming connections (WebSockets).
- **Cons:** Cost money even when idle.

## Edge Deployment
- **Not possible** for Claude itself (it runs on Anthropic servers).
- **Possible** for the *client* code (Vercel Edge Functions calling the API).

## Next Steps
- [Cloud Platform Integration](./26_cloud_integration.md).
