# FL-CCN-DTN: Federated Learning over Content-Centric Delay Tolerant Networks

## Architecture Diagram

```mermaid
graph TB
    subgraph "Simulation Environment (The ONE)"
        SIM["DTN Simulator<br/>4h simulation<br/>2500x2500m world"]
    end

    subgraph "Network Layer"
        EPIDEMIC["Scenario A<br/>EpidemicRouter<br/>(Flood-based)"]
        CCN_NC["Scenario B<br/>CCNRouter<br/>(No Cache)"]
        CCN_C["Scenario C<br/>CCNRouter<br/>(With Cache)"]
        
        EPIDEMIC -.->|Baseline| SIM
        CCN_NC -.->|Comparison| SIM
        CCN_C -.->|Optimized| SIM
    end

    subgraph "Transport Properties"
        BT["Bluetooth Interface<br/>Speed: 2Mbps<br/>Range: 200m"]
        MOVE["Movement Models<br/>RWP: Random Waypoint<br/>SPMBM: Road-based"]
        
        BT --> SIM
        MOVE --> SIM
    end

    subgraph "Application Layer (CCN_application)"
        AGG["🎯 Aggregator<br/>Mode=1<br/>Stationary<br/>1 node<br/><br/>Tasks:<br/>• Send FL Interests<br/>• Collect gradients<br/>• Compute aggregation<br/>• FL Threshold: 0.50"]
        
        WORKER["⚙️ FL Workers<br/>Mode=2<br/>Mobile<br/>69 nodes<br/><br/>Tasks:<br/>• Compute locally<br/>• Generate gradients<br/>• Respond to Interests<br/>• Cache results"]
        
        RELAY["🔄 Relay Nodes<br/>Mode=3<br/>Mobile<br/>30 nodes<br/><br/>Tasks:<br/>• Cache & forward<br/>• Increase coverage<br/>• Support connectivity"]
    end

    subgraph "Caching & Memory"
        CACHE["Opportunistic Cache<br/>Node-level LRU<br/>Capacity varies:<br/>• Aggregator: 5000<br/>• Workers: 500<br/>• Relays: 1000"]
        
        PIT["Pending Interest<br/>Table (PIT)<br/>Tracks pending<br/>Interests"]
        
        CACHE --> WORKER
        CACHE --> RELAY
        PIT --> AGG
    end

    subgraph "Federated Learning Logic"
        FL["FL Protocol<br/>Rounds: 10<br/>Nodes: 69 workers<br/>Threshold: 0.50<br/>Content Size: 512KB<br/><br/>Per Round:<br/>1. Aggregator broadcasts Interest<br/>2. Workers reply with gradients<br/>3. Aggregator aggregates (threshold-based)<br/>4. Next round or convergence"]
    end

    subgraph "Test Scenarios"
        T50["50-node setup<br/>1 Agg + 30 Workers<br/>+ 19 Relays"]
        T100["100-node setup<br/>1 Agg + 69 Workers<br/>+ 30 Relays"]
    end

    AGG --> FL
    WORKER --> FL
    RELAY --> FL
    
    FL --> T50
    FL --> T100
    
    T50 -.->|Run Experiments| EPIDEMIC
    T100 -.->|Run Experiments| EPIDEMIC

    style AGG fill:#ff9999
    style WORKER fill:#99ccff
    style RELAY fill:#99ff99
    style FL fill:#ffcc99
