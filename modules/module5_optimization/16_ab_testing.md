# 5.4 A/B Testing Prompts

In production, you can test improvements with real traffic.

## Setup
1. **Config:** Store prompts in a DB or feature flag system.
2. **Router:** Assign 50% traffic to Prompt A, 50% to Prompt B.
3. **Tracking:** Log which prompt was used for each request ID.

## Success Metric
How do you know which is better?
- **User Feedback:** Thumbs up/down.
- **Conversion:** Did the user copy the code? Did they buy the item?
- **Retention:** Did they come back?

## Next Steps
- [Quality Metrics](./17_quality_metrics.md).
