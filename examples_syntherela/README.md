# Datasets

Download original dataset from google drive and save into `data` folder.

So for example, the path for rossmann is `data/original/rossmann_subsampled/`.

# Installation

I am using python 3.11.9.

First install relbench.
```bash
pip install -e '.[full,example,test,dev]'
```

Then install pytorch geometric with optional dependencies [https://pytorch-geometric.readthedocs.io/en/stable/install/installation.html](https://pytorch-geometric.readthedocs.io/en/stable/install/installation.html).

# Baselines and GNN

```bash
python examples_syntherela/baseline_node.py > examples_syntherela/rossmann_historical_customers_baseline_node_results.txt

python examples_syntherela/gnn_node.py > examples_syntherela/rossmann_historical_customers_gnn_node_results.txt
```

# Comments

I set the number of epochs to 1 because I don't have cuda on mac. Default by RelBench team is 10.