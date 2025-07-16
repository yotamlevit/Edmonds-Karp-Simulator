# Edmonds-Karp Simulator

This project provides a simple Streamlit application to visualise the Edmonds-Karp maximum flow algorithm. You can build a custom directed graph, set edge capacities and run the algorithm either step by step or to completion.

The graph can be manipulated with the mouse: drag nodes to reposition them or use the built in editor to create connections. The sidebar lists all edges so their weights can be adjusted easily.

## Requirements

Install the Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Use the web interface to add nodes and edges, select source and sink nodes and then execute the algorithm.
