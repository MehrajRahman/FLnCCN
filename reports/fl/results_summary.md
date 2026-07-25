# Comparative Simulation Results

Evaluation of Utility-Based Federated Cache Replacement (UFCR) and Adaptive Aggregation Threshold against Epidemic and CCN-NoCache baselines.

| Scenario | Protocol | Mobility | Nodes | Rounds | Total Updates | Avg Round Latency (s) | Cache-Served Frac | Cache Lat (s) | Origin Lat (s) | Oppo Cache Hits | Total FL Cache Hits | Caching Gain Index | Useful FL Hits | Useful FL Hit Ratio | Delivery Prob | Overhead Ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Scenario A | Epidemic | RWP | 50 | 10 | 137 | 335.7 | 0.0063 | 192.7 | 104.1 | 212 | 212 | 66.75 | 1 | 0.0047 | 0.8879 | 48.0000 |
| Scenario A | Epidemic | SPMBM | 50 | 10 | 90 | 1853.5 | 0.0000 | 0.0 | 586.5 | 316 | 316 | 76.14 | 0 | 0.0000 | 0.7926 | 47.4526 |
| Scenario B | CCN-NoCache | RWP | 50 | 10 | 129 | 688.5 | 0.0000 | 0.0 | 237.3 | 0 | 0 | 52.23 | 0 | 0.0000 | 0.9574 | 28.6651 |
| Scenario B | CCN-NoCache | SPMBM | 50 | 10 | 88 | 1991.2 | 0.0000 | 0.0 | 671.0 | 0 | 0 | 61.79 | 0 | 0.0000 | 0.7970 | 20.1910 |
| Scenario D | CCN-LRU | RWP | 50 | 10 | 123 | 659.7 | 0.0789 | 475.1 | 219.2 | 638 | 638 | 77.68 | 10 | 0.0157 | 0.8551 | 15.9122 |
| Scenario D | CCN-LRU | SPMBM | 50 | 10 | 89 | 1980.9 | 0.0649 | 985.2 | 647.3 | 421 | 412 | 79.41 | 8 | 0.0194 | 0.7263 | 14.1379 |
| Scenario C | CCN-Cache | RWP | 50 | 10 | 123 | 660.9 | 0.0789 | 476.9 | 219.2 | 618 | 618 | 77.20 | 10 | 0.0162 | 0.8552 | 16.1838 |
| Scenario C | CCN-Cache | SPMBM | 50 | 10 | 89 | 1980.5 | 0.0384 | 991.1 | 580.0 | 364 | 360 | 77.23 | 5 | 0.0139 | 0.7462 | 14.8564 |
| Scenario A | Epidemic | RWP | 100 | 10 | 329 | 207.9 | 0.0281 | 89.6 | 68.4 | 397 | 397 | 64.97 | 10 | 0.0252 | 0.8970 | 98.0006 |
| Scenario A | Epidemic | SPMBM | 100 | 10 | 230 | 978.3 | 0.0344 | 747.5 | 547.0 | 301 | 301 | 60.46 | 10 | 0.0332 | 0.9358 | 97.9847 |
| Scenario B | CCN-NoCache | RWP | 100 | 10 | 228 | 502.6 | 0.0000 | 0.0 | 148.6 | 0 | 0 | 51.76 | 0 | 0.0000 | 0.9659 | 54.4741 |
| Scenario B | CCN-NoCache | SPMBM | 100 | 10 | 290 | 1552.2 | 0.0000 | 0.0 | 684.1 | 0 | 0 | 53.75 | 0 | 0.0000 | 0.8881 | 55.9370 |
| Scenario D | CCN-LRU | RWP | 100 | 10 | 235 | 418.5 | 0.1578 | 235.8 | 122.4 | 1525 | 1525 | 77.88 | 38 | 0.0249 | 0.9170 | 23.0432 |
| Scenario D | CCN-LRU | SPMBM | 100 | 10 | 214 | 1591.0 | 0.1786 | 1028.9 | 654.8 | 1175 | 1162 | 78.56 | 41 | 0.0353 | 0.7683 | 21.6322 |
| Scenario C | CCN-Cache | RWP | 100 | 10 | 244 | 397.6 | 0.1269 | 258.7 | 124.5 | 1463 | 1463 | 77.67 | 32 | 0.0219 | 0.9166 | 24.0322 |
| Scenario C | CCN-Cache | SPMBM | 100 | 10 | 207 | 1591.1 | 0.1438 | 1153.4 | 660.9 | 1079 | 1071 | 77.88 | 33 | 0.0308 | 0.7768 | 21.9931 |
