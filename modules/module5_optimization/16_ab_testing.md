# 5.4 A/B Testing Prompts

In production, you can test improvements with real traffic.

## Setup
1. **Config:** Store prompts in a DB or feature flag system.
2. **Router:** Assign 50% traffic to Prompt A, 50% to Prompt B. Assign by a stable hash of the user ID so a user always sees the same variant:

```python
import hashlib

def pick_variant(user_id: str, split: float = 0.5) -> str:
    bucket = int(hashlib.sha256(user_id.encode()).hexdigest(), 16) % 100
    return "A" if bucket < split * 100 else "B"
```
3. **Tracking:** Log which prompt was used for each request ID.

## Success Metric
How do you know which is better?
- **User Feedback:** Thumbs up/down.
- **Conversion:** Did the user copy the code? Did they buy the item?
- **Retention:** Did they come back?

## Before declaring a winner
Run both variants on the same model version and enough traffic to reach statistical significance. Model output is non-deterministic, so small differences on a few hundred samples are often noise. Run the prompt through your offline eval set first ([Evaluation](./14_evaluation.md)) so that production traffic only tests candidates that already pass.

## Next Steps
- [Quality Metrics](./17_quality_metrics.md).
