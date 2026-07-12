# Experimental Execution Plan for FL-CCN-DTN

## Phase 1: Setup & Validation (Week 1-2)

### ✅ Checklist:
- [ ] Verify all 12 configuration files run without errors
- [ ] Test with 1 run each to confirm simulator stability
- [ ] Set up output collection pipeline (parse reports)
- [ ] Create baseline measurements (Epidemic reference)

**Command Template**:
```bash
./one.sh -b 1 fl_settings/scenario_A_epidemic_50_rwp.txt
./one.sh -b 1 fl_settings/scenario_A_epidemic_100_rwp.txt
# ... etc for all 12 configs
```

---

## Phase 2: Primary Experiments (Week 3-4)

### Full Experiment Matrix

| Config # | Scenario | Nodes | Routing | Movement | Runs |
|----------|----------|-------|---------|----------|------|
| 1 | A | 50 | Epidemic | RWP | 5 |
| 2 | A | 50 | Epidemic | SPMBM | 5 |
| 3 | A | 100 | Epidemic | RWP | 5 |
| 4 | A | 100 | Epidemic | SPMBM | 5 |
| 5 | B | 50 | CCN-NoCache | RWP | 5 |
| 6 | B | 50 | CCN-NoCache | SPMBM | 5 |
| 7 | B | 100 | CCN-NoCache | RWP | 5 |
| 8 | B | 100 | CCN-NoCache | SPMBM | 5 |
| 9 | C | 50 | CCN-Cache | RWP | 5 |
| 10 | C | 50 | CCN-Cache | SPMBM | 5 |
| 11 | C | 100 | CCN-Cache | RWP | 5 |
| 12 | C | 100 | CCN-Cache | SPMBM | 5 |

**Total**: 60 simulations × 4h each = **10 days** (if run in parallel on 4-core machine)

### Run Script Template:
```bash
#!/bin/bash
# run_all_experiments.sh

RUNS=5
CONFIGS=(
    "scenario_A_epidemic_50_rwp.txt"
    "scenario_A_epidemic_50_spmbm.txt"
    "scenario_A_epidemic_100_rwp.txt"
    "scenario_A_epidemic_100_spmbm.txt"
    "scenario_B_ccn_nocache_50_rwp.txt"
    "scenario_B_ccn_nocache_50_spmbm.txt"
    "scenario_B_ccn_nocache_100_rwp.txt"
    "scenario_B_ccn_nocache_100_spmbm.txt"
    "scenario_C_ccn_cache_50_rwp.txt"
    "scenario_C_ccn_cache_50_spmbm.txt"
    "scenario_C_ccn_cache_100_rwp.txt"
    "scenario_C_ccn_cache_100_spmbm.txt"
)

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="results_$TIMESTAMP"
mkdir -p "$RESULTS_DIR"

for config in "${CONFIGS[@]}"; do
    echo "Running $config with $RUNS runs..."
    ./one.sh -b "1:$RUNS" "fl_settings/$config" > "$RESULTS_DIR/${config%.txt}.log" 2>&1
    echo "Completed: $config"
done

echo "All experiments completed. Results in: $RESULTS_DIR"
```

---

## Phase 3: Data Collection & Analysis

### Key Reports to Parse

The ONE simulator generates reports in `/reports/` folder:

1. **CCNApplicationReport**: FL-specific metrics
   - Aggregation rounds
   - Convergence time
   - Gradient delivery rates

2. **MessageStatsReport**: Network metrics
   - Messages created/relayed/delivered
   - Message delivery ratio
   - Average hop count

3. **CacheReport** (if enabled): Caching metrics
   - Cache hit rate
   - Cache utilization
   - Eviction count

### Report Processing Script:

```python
# analyze_results.py
import os
import re
import pandas as pd
from pathlib import Path

def parse_report(report_path):
    """Extract key metrics from simulator report"""
    metrics = {}
    
    with open(report_path, 'r') as f:
        content = f.read()
    
    # Extract key patterns
    patterns = {
        'total_messages': r'Total messages: (\d+)',
        'delivered': r'Delivered: (\d+)',
        'dropped': r'Dropped: (\d+)',
        'convergence_time': r'Convergence time: ([\d.]+)',
        'cache_hits': r'Cache hits: (\d+)',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            metrics[key] = float(match.group(1))
    
    return metrics

# Collect all results
results = []
for report_file in Path('reports').glob('*Report*.txt'):
    metrics = parse_report(report_file)
    config_name = report_file.stem
    
    # Extract config parameters
    if 'epidemic' in config_name.lower():
        routing = 'Epidemic'
    elif 'nocache' in config_name.lower():
        routing = 'CCN-NoCache'
    else:
        routing = 'CCN-Cache'
    
    nodes = 50 if '50' in config_name else 100
    movement = 'RWP' if 'rwp' in config_name.lower() else 'SPMBM'
    
    results.append({
        'config': config_name,
        'routing': routing,
        'nodes': nodes,
        'movement': movement,
        **metrics
    })

df = pd.DataFrame(results)

# Calculate aggregates
summary = df.groupby(['routing', 'nodes', 'movement']).agg({
    'delivered': ['mean', 'std'],
    'convergence_time': ['mean', 'std'],
    'cache_hits': ['mean', 'std'],
}).round(2)

print(summary)
df.to_csv('experimental_results.csv', index=False)
```

---

## Phase 4: Visualization & Comparison

### Figure 1: Convergence Speed Comparison
```python
import matplotlib.pyplot as plt

# Plot convergence_time across scenarios
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: By routing protocol
df_50 = df[df['nodes'] == 50]
df_50.groupby('routing')['convergence_time'].apply(list).plot(kind='box', ax=axes[0])
axes[0].set_title('Convergence Time: 50 Nodes')
axes[0].set_ylabel('Time (seconds)')

# Right: By topology size
df_ccn_cache = df[df['routing'] == 'CCN-Cache']
df_ccn_cache.groupby('nodes')['convergence_time'].apply(list).plot(kind='box', ax=axes[1])
axes[1].set_title('Convergence Time: CCN-Cache')
axes[1].set_ylabel('Time (seconds)')

plt.tight_layout()
plt.savefig('convergence_comparison.png', dpi=300)
```

### Figure 2: Message Efficiency
```python
df['delivery_ratio'] = df['delivered'] / (df['created'] + 1)  # Avoid division by zero
df['messages_per_convergence'] = df['total_messages'] / (df['convergence_rounds'] + 1)

fig, ax = plt.subplots()
for routing in ['Epidemic', 'CCN-NoCache', 'CCN-Cache']:
    data = df[df['routing'] == routing]['delivery_ratio']
    ax.bar(routing, data.mean(), yerr=data.std(), alpha=0.7)

ax.set_ylabel('Delivery Ratio')
ax.set_title('Message Delivery Efficiency by Routing Protocol')
plt.tight_layout()
plt.savefig('delivery_ratio_comparison.png', dpi=300)
```

### Figure 3: Mobility Impact (RWP vs SPMBM)
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for i, routing in enumerate(['CCN-NoCache', 'CCN-Cache']):
    subset = df[df['routing'] == routing]
    movement_groups = subset.groupby('movement')['convergence_time']
    
    x = range(len(movement_groups))
    means = [movement_groups.get_group(m).mean() for m in ['RWP', 'SPMBM']]
    stds = [movement_groups.get_group(m).std() for m in ['RWP', 'SPMBM']]
    
    axes[i].bar(['RWP', 'SPMBM'], means, yerr=stds, alpha=0.7, color=['blue', 'green'])
    axes[i].set_title(f'{routing}: Movement Model Impact')
    axes[i].set_ylabel('Convergence Time (s)')

plt.tight_layout()
plt.savefig('mobility_impact.png', dpi=300)
```

---

## Phase 5: Key Results to Extract

### For Paper:

1. **Main Finding**: Performance Improvement
   - "CCN-Cache achieves X% faster convergence than Epidemic"
   - "Message overhead reduced by Y% with intelligent caching"

2. **Secondary Finding**: Mobility Matters
   - "Road-based movement (SPMBM) stabilizes aggregation by Z%"

3. **Tertiary Finding**: Scalability
   - "50 → 100 nodes increases convergence time by ~W% (expected O(n) growth)"

4. **Cache Efficiency**:
   - "Cache hit rate: A% in 50-node, B% in 100-node topology"
   - "Bandwidth savings: C MB/node over 10 FL rounds"

---

## Phase 6: Statistical Validation

### Calculate Confidence Intervals:
```python
from scipy import stats

for routing in ['Epidemic', 'CCN-NoCache', 'CCN-Cache']:
    data = df[df['routing'] == routing]['convergence_time']
    mean = data.mean()
    ci = stats.t.interval(0.95, len(data)-1, 
                          loc=mean, 
                          scale=stats.sem(data))
    print(f"{routing}: {mean:.2f}s [CI: {ci[0]:.2f}-{ci[1]:.2f}]")
```

### Perform ANOVA:
```python
from scipy.stats import f_oneway

epidemic = df[df['routing'] == 'Epidemic']['convergence_time']
ccn_nc = df[df['routing'] == 'CCN-NoCache']['convergence_time']
ccn_c = df[df['routing'] == 'CCN-Cache']['convergence_time']

f_stat, p_value = f_oneway(epidemic, ccn_nc, ccn_c)
print(f"ANOVA F-statistic: {f_stat:.2f}, p-value: {p_value:.4f}")
# If p < 0.05: significant difference between routing protocols
```

---

## Timeline

| Week | Task |
|------|------|
| 1-2 | Setup, validation, baseline |
| 3-4 | Run 60 simulations (parallel) |
| 5 | Parse reports, analyze data |
| 6 | Generate visualizations & statistics |
| 7 | Write results section |
| 8 | Complete paper draft |

---

## Parallel Execution Strategy

**If you have 4+ CPU cores:**

```bash
# Run in background (GNU Parallel)
cat > configs.txt << EOF
scenario_A_epidemic_50_rwp.txt
scenario_A_epidemic_50_spmbm.txt
scenario_A_epidemic_100_rwp.txt
scenario_A_epidemic_100_spmbm.txt
scenario_B_ccn_nocache_50_rwp.txt
scenario_B_ccn_nocache_50_spmbm.txt
scenario_B_ccn_nocache_100_rwp.txt
scenario_B_ccn_nocache_100_spmbm.txt
scenario_C_ccn_cache_50_rwp.txt
scenario_C_ccn_cache_50_spmbm.txt
scenario_C_ccn_cache_100_rwp.txt
scenario_C_ccn_cache_100_spmbm.txt
EOF

parallel -j 4 "echo 'Running {}'; ./one.sh -b 1:5 fl_settings/{} > results/{}.log 2>&1" < configs.txt

# Wait for all to complete
wait
echo "All simulations done!"
```

This reduces 10 days to ~3 days with 4-core parallelization! 🚀
