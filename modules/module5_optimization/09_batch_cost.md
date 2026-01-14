# 5.2 Batch Processing for Cost Reduction

## The 50% Rule
Anything that doesn't need to be answered in <10 seconds should go to Batch.

## Architecture
1. **Queue:** Accumulate non-urgent requests in a DB table.
2. **Cron Job:** Every 5 minutes, query the table.
3. **Submit:** If > 100 requests (or if oldest is > 1 hour), submit a batch.
4. **Retrieve:** Poll for results and update the DB.

## Cost Savings Example
- **Scenario:** Processing 1M documents/month with Sonnet.
- **Standard:** $3 input + $15 output / MTok.
- **Batch:** $1.50 input + $7.50 output.
- **Savings:** Thousands of dollars.

## Next Steps
- Move to [Latency Optimization](./10_latency.md).
