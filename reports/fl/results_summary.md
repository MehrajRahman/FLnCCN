# Comparative Simulation Results

Evaluation of Utility-Based Federated Cache Replacement (UFCR) and Adaptive Aggregation Threshold against Epidemic and CCN-NoCache baselines.

| Scenario | Protocol | Mobility | Rounds | Total Updates | Avg Round Latency (s) | Cache-Served Frac | Cache Lat (s) | Origin Lat (s) | Oppo Cache Hits | Total FL Cache Hits | Caching Gain Index | Useful FL Hits | Useful FL Hit Ratio | Delivery Prob | Overhead Ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Scenario A | Epidemic | RWP | 10 | 137 | 335.7 | 0.0063 | 192.7 | 104.1 | 212 | 212 | 66.75 | 1 | 0.0047 | 0.8879 | 48.0000 |
| Scenario A | Epidemic | SPMBM | 10 | 90 | 1853.5 | 0.0000 | 0.0 | 586.5 | 316 | 316 | 76.14 | 0 | 0.0000 | 0.7926 | 47.4526 |
| Scenario B | CCN-NoCache | RWP | 10 | 129 | 688.5 | 0.0000 | 0.0 | 237.3 | 0 | 0 | 52.23 | 0 | 0.0000 | 0.9574 | 28.6651 |
| Scenario B | CCN-NoCache | SPMBM | 10 | 88 | 1991.2 | 0.0000 | 0.0 | 671.0 | 0 | 0 | 61.79 | 0 | 0.0000 | 0.7970 | 20.1910 |
| Scenario D | CCN-LRU | RWP | 10 | 123 | 659.7 | 0.0789 | 475.1 | 219.2 | 638 | 638 | 77.68 | 10 | 0.0157 | 0.8551 | 15.9122 |
| Scenario D | CCN-LRU | SPMBM | 10 | 89 | 1980.9 | 0.0649 | 985.2 | 647.3 | 421 | 412 | 79.41 | 8 | 0.0194 | 0.7263 | 14.1379 |
| Scenario C | CCN-Cache | RWP | 10 | 123 | 660.9 | 0.0789 | 476.9 | 219.2 | 618 | 618 | 77.20 | 10 | 0.0162 | 0.8552 | 16.1838 |
| Scenario C | CCN-Cache | SPMBM | 10 | 89 | 1980.5 | 0.0384 | 991.1 | 580.0 | 364 | 360 | 77.23 | 5 | 0.0139 | 0.7462 | 14.8564 |
