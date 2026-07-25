#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
import numpy as np

# Create output directory if not present
out_dir = "/home/billy/X/FLnCCN/notes/research_paper/Figures"
os.makedirs(out_dir, exist_ok=True)

# Styling for IEEE/ACM publication standard
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

scenarios = ['Scenario A\n(Epidemic)', 'Scenario B\n(CCN-NoCache)', 'Scenario D\n(CCN-LRU)', 'Scenario C\n(CCN-UFCR)']

# --- Figure 1: Network Overhead Ratio ---
# Data for 50 nodes and 100 nodes
overhead_50_rwp   = [48.00, 28.67, 15.91, 16.18]
overhead_50_spmbm = [47.45, 20.19, 14.14, 14.86]

overhead_100_rwp   = [98.00, 54.47, 23.04, 24.03]
overhead_100_spmbm = [97.98, 55.94, 21.63, 21.99]

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)

x = np.arange(len(scenarios))
width = 0.35

# 50 Nodes
rects1 = axes[0].bar(x - width/2, overhead_50_rwp, width, label='RWP Mobility', color='#2b5c8f', edgecolor='black')
rects2 = axes[0].bar(x + width/2, overhead_50_spmbm, width, label='SPMBM Mobility', color='#d95f02', edgecolor='black')
axes[0].set_title('50-Node Network Density')
axes[0].set_xticks(x)
axes[0].set_xticklabels(scenarios, rotation=15)
axes[0].set_ylabel('Network Overhead Ratio')
axes[0].grid(axis='y', linestyle='--', alpha=0.7)
axes[0].legend()

# Annotate reduction on 50 nodes
axes[0].annotate('66.3% lower\noverhead', xy=(3, 16.18), xytext=(2.2, 35),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
            ha='center', fontsize=9, fontweight='bold', color='#1b9e77')

# 100 Nodes
rects3 = axes[1].bar(x - width/2, overhead_100_rwp, width, label='RWP Mobility', color='#2b5c8f', edgecolor='black')
rects4 = axes[1].bar(x + width/2, overhead_100_spmbm, width, label='SPMBM Mobility', color='#d95f02', edgecolor='black')
axes[1].set_title('100-Node Network Density')
axes[1].set_xticks(x)
axes[1].set_xticklabels(scenarios, rotation=15)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)
axes[1].legend()

# Annotate reduction on 100 nodes
axes[1].annotate('75.5% lower\noverhead', xy=(3, 21.99), xytext=(2.2, 70),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
            ha='center', fontsize=9, fontweight='bold', color='#1b9e77')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig_overhead_ratio.pdf'), dpi=300)
plt.savefig(os.path.join(out_dir, 'fig_overhead_ratio.png'), dpi=300)
plt.close()
print("Generated fig_overhead_ratio.pdf and png")


# --- Figure 2: Average Round Completion Latency ---
latency_50_rwp   = [335.7, 688.5, 659.7, 660.9]
latency_50_spmbm = [1853.5, 1991.2, 1980.9, 1980.5]

latency_100_rwp   = [207.9, 502.6, 418.5, 397.6]
latency_100_spmbm = [978.3, 1552.2, 1591.0, 1591.1]

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

# 50 Nodes
axes[0].bar(x - width/2, latency_50_rwp, width, label='RWP Mobility', color='#377eb8', edgecolor='black')
axes[0].bar(x + width/2, latency_50_spmbm, width, label='SPMBM Mobility', color='#e41a1c', edgecolor='black')
axes[0].set_title('50-Node Round Latency')
axes[0].set_xticks(x)
axes[0].set_xticklabels(scenarios, rotation=15)
axes[0].set_ylabel('Avg Round Completion Latency (s)')
axes[0].grid(axis='y', linestyle='--', alpha=0.7)
axes[0].legend()

# 100 Nodes
axes[1].bar(x - width/2, latency_100_rwp, width, label='RWP Mobility', color='#377eb8', edgecolor='black')
axes[1].bar(x + width/2, latency_100_spmbm, width, label='SPMBM Mobility', color='#e41a1c', edgecolor='black')
axes[1].set_title('100-Node Round Latency')
axes[1].set_xticks(x)
axes[1].set_xticklabels(scenarios, rotation=15)
axes[1].set_ylabel('Avg Round Completion Latency (s)')
axes[1].grid(axis='y', linestyle='--', alpha=0.7)
axes[1].legend()

# Annotate latency improvement on 100-node RWP
axes[1].annotate('20.9% faster\nthan NoCache', xy=(3 - width/2, 397.6), xytext=(2, 850),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
            ha='center', fontsize=9, fontweight='bold', color='#377eb8')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig_round_latency.pdf'), dpi=300)
plt.savefig(os.path.join(out_dir, 'fig_round_latency.png'), dpi=300)
plt.close()
print("Generated fig_round_latency.pdf and png")


# --- Figure 3: Useful FL Cache Hits & Useful Cache Hit Ratio ---
fig, ax1 = plt.subplots(figsize=(7, 4))

labels = ['50 Nodes\n(RWP)', '50 Nodes\n(SPMBM)', '100 Nodes\n(RWP)', '100 Nodes\n(SPMBM)']
x_c = np.arange(len(labels))

useful_hits_lru  = [10, 8, 38, 41]
useful_hits_ufcr = [10, 5, 32, 33]

rects_lru = ax1.bar(x_c - width/2, useful_hits_lru, width, label='CCN-LRU (Scenario D)', color='#984ea3', edgecolor='black')
rects_ufcr = ax1.bar(x_c + width/2, useful_hits_ufcr, width, label='CCN-UFCR (Scenario C)', color='#4daf4a', edgecolor='black')

ax1.set_ylabel('Useful FL Cache Hits (Aggregator Served)', color='black')
ax1.set_xticks(x_c)
ax1.set_xticklabels(labels)
ax1.set_title('In-Network Caching Efficiency: Useful Hits')
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.legend(loc='upper left')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig_useful_hits.pdf'), dpi=300)
plt.savefig(os.path.join(out_dir, 'fig_useful_hits.png'), dpi=300)
plt.close()
print("Generated fig_useful_hits.pdf and png")


# --- Figure 4: Delivery Probability ---
dp_50_rwp   = [0.8879, 0.9574, 0.8551, 0.8552]
dp_50_spmbm = [0.7926, 0.7970, 0.7263, 0.7462]

dp_100_rwp   = [0.8970, 0.9659, 0.9170, 0.9166]
dp_100_spmbm = [0.9358, 0.8881, 0.7683, 0.7768]

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)

axes[0].bar(x - width/2, dp_50_rwp, width, label='RWP Mobility', color='#4ba647', edgecolor='black')
axes[0].bar(x + width/2, dp_50_spmbm, width, label='SPMBM Mobility', color='#ff7f00', edgecolor='black')
axes[0].set_title('50-Node Delivery Probability')
axes[0].set_xticks(x)
axes[0].set_xticklabels(scenarios, rotation=15)
axes[0].set_ylabel('Delivery Probability')
axes[0].set_ylim(0.5, 1.0)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)
axes[0].legend()

axes[1].bar(x - width/2, dp_100_rwp, width, label='RWP Mobility', color='#4ba647', edgecolor='black')
axes[1].bar(x + width/2, dp_100_spmbm, width, label='SPMBM Mobility', color='#ff7f00', edgecolor='black')
axes[1].set_title('100-Node Delivery Probability')
axes[1].set_xticks(x)
axes[1].set_xticklabels(scenarios, rotation=15)
axes[1].set_ylim(0.5, 1.0)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)
axes[1].legend()

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'fig_delivery_prob.pdf'), dpi=300)
plt.savefig(os.path.join(out_dir, 'fig_delivery_prob.png'), dpi=300)
plt.close()
print("Generated fig_delivery_prob.pdf and png")

print("ALL FIGURES GENERATED SUCCESSFULLY IN:", out_dir)
