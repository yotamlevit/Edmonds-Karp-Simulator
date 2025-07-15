import streamlit as st
import networkx as nx
from pyvis.network import Network
from algorithm import EdmondsKarp

st.set_page_config(page_title="Edmonds-Karp Simulator")

st.title("Edmonds-Karp Algorithm Simulator")

# Session state setup
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
if 'ek' not in st.session_state:
    st.session_state.ek = None
if 'steps' not in st.session_state:
    st.session_state.steps = []

st.header("Build Graph")
node_input = st.text_input("Add node label", "")
if st.button("Add Node") and node_input:
    st.session_state.graph.add_node(node_input)
    # Rerun the script to refresh widgets. ``st.rerun`` is available in newer
    # versions of Streamlit, while older releases provide ``experimental_rerun``.
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

if st.session_state.graph.nodes:
    col1, col2 = st.columns(2)
    with col1:
        src = st.selectbox("Edge source", list(st.session_state.graph.nodes))
    with col2:
        dst = st.selectbox("Edge target", list(st.session_state.graph.nodes))
    cap = st.number_input("Capacity", min_value=1, value=1)
    if st.button("Add Edge"):
        st.session_state.graph.add_edge(src, dst, capacity=cap)

st.subheader("Current Graph")
# display graph using pyvis
if st.session_state.graph.nodes:
    nt = Network(height="400px", directed=True)
    for node in st.session_state.graph.nodes:
        nt.add_node(node, label=str(node))
    for u, v, data in st.session_state.graph.edges(data=True):
        nt.add_edge(u, v, label=str(data.get('capacity', '')))
    nt.save_graph("graph.html")
    st.components.v1.html(open("graph.html").read(), height=420)
else:
    st.info("Add nodes to begin")

st.header("Algorithm")
source_node = st.selectbox("Source", list(st.session_state.graph.nodes), key="source")
sink_node = st.selectbox("Sink", list(st.session_state.graph.nodes), key="sink")
if st.button("Initialize"):
    st.session_state.ek = EdmondsKarp(st.session_state.graph, source_node, sink_node)
    st.session_state.steps = []

if st.session_state.ek:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Step"):
            result = st.session_state.ek.step()
            if result:
                st.session_state.steps.append(result)
            else:
                st.info("No more augmenting paths.")
    with col2:
        if st.button("Run to completion"):
            st.session_state.steps.extend(st.session_state.ek.run())

    st.subheader("Steps")
    for i, step in enumerate(st.session_state.steps, 1):
        st.write(f"Step {i}: Path {step['path']} capacity {step['path_capacity']} total flow {step['total_flow']}")
