# Energy proxy sensitivity: token/call-count vs. latency-normalized

| Provider | Avg latency | Token-count energy | Latency-normalized energy | Xk (token proxy) | Xk (latency proxy) |
| --- | --- | --- | --- | --- | --- |
| Claude Sonnet | 7871ms | 0.2 | 0.2 | 0.1698 | 0.1698 |
| Gemini 2.5 Pro | 15176ms | 0.5 | 0.369 | 0.1998 | 0.1867 |
| Qwen2.5-7B (local) | 38127ms | 0.2 | 0.9 | 0.1698 | 0.2398 |

Ranking (best/lowest Xk to worst) under token proxy: Claude Sonnet < Qwen2.5-7B (local) < Gemini 2.5 Pro

Ranking under latency proxy: Claude Sonnet < Gemini 2.5 Pro < Qwen2.5-7B (local)

Ranking changed: True
