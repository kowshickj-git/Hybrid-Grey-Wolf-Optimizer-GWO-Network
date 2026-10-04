# data/

No external dataset is needed: every network is generated from its configuration and seed
(`Network.deploy(config, seed)`), so the same seed always produces the same node coordinates.

To save a deployed topology (node table) for inspection or for a report:

```python
from config import SimulationConfig
from models.network import Network

cfg = SimulationConfig(n_nodes=100, seed=42)
Network.deploy(cfg).to_dataframe().to_csv("data/topology_100nodes_seed42.csv", index=False)
```

Experiment outputs (raw CSVs, figures, reports) are written to `results/`, not here.
