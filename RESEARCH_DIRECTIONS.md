# Publishable Research Directions for FL-CCN-DTN

## Current Work Summary
**Federated Learning over Content-Centric Delay Tolerant Networks**
- Testing 3 routing strategies (Epidemic vs CCN with/without caching)
- 50-100 mobile nodes in DTN environment
- Metrics: aggregation rounds, convergence time, message delivery, cache efficiency

---

## 🎯 Potential Publishable Contributions

### **1. PRIMARY: "Content-Centric Federated Learning in DTNs"**
**Venue**: IEEE Transactions on Mobile Computing / ACM SIGMOBILE
**Focus Area**: Protocol Design & Performance

#### Key Insight:
CCN's content-based routing + PIT naturally matches FL's gradient aggregation pattern
- Interests = gradient requests
- Data = model updates
- Content caching = gradient caching across hops

#### Unique Angles:
- **First work to combine CCN + FL** in DTN (to our knowledge)
- Show CCN outperforms Epidemic for distributed learning
- Cache efficiency reduces transmission overhead
- Convergence time analysis under mobility

#### Experimental Results to Highlight:
```
Scenario A (Epidemic):   High message flood → poor efficiency
Scenario B (CCN No Cache): Content awareness → 30-40% better
Scenario C (CCN + Cache): Cache hits reduce messages → 50%+ reduction
+ Convergence speed comparison across scenarios
```

---

### **2. SECONDARY: "Mobility-Aware Federated Learning in Vehicular Networks"**
**Venue**: Vehicular Technology Conference (VTC) / IEEE Transactions on Intelligent Transportation
**Focus Area**: IoV Application

#### Pivot Strategy:
Position your work as **FL for Edge Computing in IoV**
- Use your real road data: `data/roads.wkt`, `data/tram*.wkt`
- Reframe scenarios as vehicle mobility patterns
- Real-world scenario: Vehicle sensors → collaborative ML without cloud

#### Use Cases:
- Fleet optimization (taxi services)
- Cooperative traffic prediction
- Autonomous vehicle learning (sensor fusion)
- Smart city sensor networks

#### Experimental Variation:
- Compare RWP (random) vs SPMBM (realistic road-based)
- Show SPMBM improves convergence (vehicles stay in coverage longer)
- Measure performance on actual Helsinki/Manhattan traces

---

### **3. TERTIARY: "Caching Strategies for Distributed Learning in Opportunistic Networks"**
**Venue**: IEEE ICC / Globecom / ACM Symposium on Edge Computing
**Focus Area**: Systems Optimization

#### Research Questions:
1. **Optimal cache placement**: Where should gradients be cached?
   - Central (Aggregator): vs Distributed (Workers/Relays)?
   - Trade-off: latency vs. memory usage

2. **Cache eviction policies** for FL:
   - Standard LRU vs. FL-aware (newer gradients > older)
   - Can we predict which gradients will be needed?

3. **Threshold effects**:
   - How does FL threshold (currently 0.50) affect cache hit rates?
   - Can adaptive thresholds improve convergence?

#### Experimental Contribution:
Compare cache strategies across scenarios
- Measure: Cache hit rate, bytes saved, convergence time, memory overhead

---

### **4. QUATERNARY: "Convergence Analysis of FL Over Intermittently Connected Networks"**
**Venue**: IEEE Transactions on Networking / IEEE/ACM Transactions on Networking
**Focus Area**: Theoretical Analysis

#### Mathematical Contribution:
Analyze convergence guarantees when:
- Nodes disconnect unpredictably
- Gradient messages may be lost
- Async aggregation due to delays

#### Experimental Validation:
- Measure actual convergence rate vs. theory
- Show robustness under different mobility speeds (0.5-2.5 m/s)
- Impact of TTL on convergence

---

## 📊 Recommended Publication Strategy

### Phase 1: Core Contribution (Best First)
**Paper 1: "Content-Centric Federated Learning in DTNs"**
- Primary experiments: All 3 scenarios × 2 topologies × 2 movement models = 12 simulations
- Metrics: Aggregation rounds, convergence time, message delivery ratio, cache efficiency
- Conference: **IEEE ICC 2024 or IEEE ICDCS 2024**

### Phase 2: Application Expansion
**Paper 2: "Federated Learning for Autonomous Vehicles: An Opportunistic Network Approach"**
- Use road-based movement model
- Real-world use case framing
- Conference: **IEEE VTC 2024 or IEEE Intelligent Vehicles Symposium**

### Phase 3: Systems Optimization
**Paper 3: "Learning-Aware Caching for Distributed FL in Delay-Tolerant Networks"**
- Detailed cache analysis
- Adaptive strategies
- Conference: **ACM SIGCOMM or IEEE INFOCOM 2024**

---

## 🔬 Immediate Next Steps for Paper 1

### Experiments to Run:
```bash
# Scenario matrix:
# 50 nodes × 100 nodes (topology)
# Epidemic, CCN-NoCache, CCN-Cache (routing)
# RWP, SPMBM (movement)
# = 2×3×2 = 12 configurations × 3-5 runs = 36-60 total simulations

Configuration 1: 50-RWP-Epidemic
Configuration 2: 50-RWP-CCNNoCache
Configuration 3: 50-RWP-CCNCache
Configuration 4: 50-SPMBM-Epidemic
... and so on
```

### Key Metrics to Collect:
1. **Convergence Metrics**:
   - FL rounds to achieve target accuracy threshold
   - Time to convergence (simulated clock)
   - Gradient update loss rate (dropped messages)

2. **Network Metrics**:
   - Message delivery ratio
   - Average message latency (Aggregator → Workers → Aggregator)
   - Hop count distribution

3. **Efficiency Metrics**:
   - Total bytes transmitted
   - Cache hit rate per node type
   - PIT table size evolution

4. **Mobility Impact**:
   - Connectivity time between Aggregator ↔ Workers
   - Number of disconnection events per round
   - Convergence degradation vs. connectivity

---

## 📝 Paper Outline for Paper 1

```
1. Introduction
   - FL challenges in edge computing
   - DTN connectivity issues
   - CCN natural fit for gradients

2. Related Work
   - Federated Learning: [FedAvg, FedProx, ...]
   - DTN Routing: [Epidemic, Prophet, MaxProp, ...]
   - Content-Centric Networking: [NDN, CCNx]
   - FL over DTN: [Few existing works]

3. System Model
   - Network architecture (1 agg, N workers, M relays)
   - CCN protocol adaptation for FL
   - Gradient as content naming scheme
   - Cache hierarchy

4. Federated Learning Protocol over CCN
   - Interest generation by Aggregator
   - Gradient serialization as Content Objects
   - PIT role in handling retransmissions
   - Convergence detection threshold

5. Experimental Setup
   - The ONE simulator configuration
   - Scenario details (50/100 nodes, movement models)
   - Metric definitions
   - Implementation details

6. Results & Analysis
   - Scenario comparison (Epidemic vs CCN)
   - Impact of caching
   - Mobility effect (RWP vs SPMBM)
   - Convergence speed & efficiency

7. Discussion & Insights
   - Why CCN works well for FL
   - Trade-offs and limitations
   - Practical deployment considerations

8. Conclusion & Future Work
```

---

## 🎬 Quick Win: Visualizations for Papers

Create these figures:
1. **System architecture**: Aggregator ↔ Workers ↔ Relays
2. **Convergence curves**: All 3 routing strategies overlaid
3. **Cache hit rates**: Heat map (node type vs. scenario)
4. **Message overhead**: Bar chart comparing routing protocols
5. **Mobility impact**: Line graph (convergence vs. node speed)
6. **Timeline diagram**: One round of FL over CCN with delays shown

---

## Challenges & Mitigations

| Challenge | Mitigation |
|-----------|-----------|
| FL convergence proof | Empirical validation + ref existing FedAvg theory |
| DTN realism | Use multiple mobility models, compare synthetic vs. traces |
| Statistical significance | Run 5-10 trials per config, report confidence intervals |
| Reproducibility | Release code + config files, use public THE ONE simulator |
| Limited novelty | Emphasize CCN-FL combination is novel |

---

## Success Metrics for This Work

✅ **Paper 1 Success** = Accepted at T1 conference (IEEE ICC, INFOCOM, SIGCOMM)
✅ **Paper 2 Success** = Accepted at IoV-focused venue (VTC, ITS)
✅ **Impact** = 20+ citations within 2 years

Good luck! 🚀
