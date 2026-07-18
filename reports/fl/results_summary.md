# Comparative Simulation Results

Evaluation of Utility-Based Federated Cache Replacement (UFCR) and Adaptive Aggregation Threshold against Epidemic and CCN-NoCache baselines.

| Scenario | Protocol | Mobility | Rounds | Total Updates | Avg Round Latency (s) | Useful Cache Hits | Useful Cache Hit Ratio | Delivery Prob | Overhead Ratio |
|---|---|---|---|---|---|---|---|---|---|
| Scenario A | Epidemic | RWP | 10 | 121 | 379.7 | 2 | 0.0024 | 0.6590 | 44.9066 |
| Scenario A | Epidemic | SPMBM | 10 | 17 | 2205.6 | 0 | 0.0000 | 0.5695 | 39.0291 |
| Scenario B | CCN-NoCache | RWP | 10 | 71 | 704.4 | 0 | 0.0000 | 0.8066 | 20.8459 |
| Scenario B | CCN-NoCache | SPMBM | 10 | 17 | 2249.1 | 0 | 0.0000 | 0.6667 | 18.6489 |
| Scenario C | CCN-Cache | RWP | 10 | 81 | 595.8 | 9 | 0.0443 | 0.7624 | 15.6502 |
| Scenario C | CCN-Cache | SPMBM | 10 | 17 | 2249.3 | 3 | 0.0536 | 0.6548 | 14.2481 |
