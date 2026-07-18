# Comparative Simulation Results

Evaluation of Utility-Based Federated Cache Replacement (UFCR) and Adaptive Aggregation Threshold against Epidemic and CCN-NoCache baselines.

| Scenario | Protocol | Mobility | Rounds | Total Updates | Avg Round Latency (s) | Useful Cache Hits | Useful Cache Hit Ratio | Delivery Prob | Overhead Ratio |
|---|---|---|---|---|---|---|---|---|---|
| Scenario A | Epidemic | RWP | 10 | 0 | 0.0 | 0 | 0.0000 | 0.0000 | 0.0000 |
| Scenario A | Epidemic | SPMBM | 10 | 91 | 1848.2 | 4 | 0.0025 | 0.5305 | 47.6242 |
| Scenario B | CCN-NoCache | RWP | 10 | 129 | 688.5 | 0 | 0.0000 | 0.9574 | 28.6651 |
| Scenario B | CCN-NoCache | SPMBM | 10 | 88 | 1991.2 | 0 | 0.0000 | 0.7970 | 20.1910 |
| Scenario C | CCN-Cache | RWP | 10 | 127 | 628.4 | 14 | 0.0211 | 0.8550 | 15.5009 |
| Scenario C | CCN-Cache | SPMBM | 10 | 87 | 1903.6 | 8 | 0.0203 | 0.7568 | 13.9460 |
