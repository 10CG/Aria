```
feat(console): add Provider health monitoring dashboard

Add real-time Provider health monitoring with API endpoint, stats
collection, and Console dashboard:

- Add /api/providers/health endpoint returning latency, error rate,
  and availability status for all Providers (provider-health.ts)
- Add getProviderStats() method to LLM gateway for collecting
  per-provider statistics (gateway.ts)
- Add ProviderHealthDashboard Console component with live status
  table and 30-minute latency trend chart
```
