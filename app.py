import streamlit as st
import networkx as nx
from pyvis.network import Network
from algorithm import EdmondsKarp

"""Streamlit app to build a graph and run Edmonds-Karp."""

st.set_page_config(page_title="Edmonds-Karp Simulator")

st.title("Edmonds-Karp Algorithm Simulator")

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = nx.DiGraph()
if 'ek' not in st.session_state:
    st.session_state.ek = None
if 'steps' not in st.session_state:
    st.session_state.steps = []

st.sidebar.header("Nodes")
new_node = st.sidebar.text_input("New node name", key="new_node")
if st.sidebar.button("Add node") and new_node:
    st.session_state.graph.add_node(new_node)
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

st.sidebar.header("Edges")
if st.session_state.graph.nodes:
    src = st.sidebar.selectbox("Source", list(st.session_state.graph.nodes), key="src")
    dst = st.sidebar.selectbox("Target", list(st.session_state.graph.nodes), key="dst")
    cap = st.sidebar.number_input("Capacity", min_value=1, value=1, key="cap")
    if st.sidebar.button("Add edge"):
        st.session_state.graph.add_edge(src, dst, capacity=cap)

st.sidebar.subheader("Current edges")
for u, v, data in list(st.session_state.graph.edges(data=True)):
    key = f"{u}-{v}"
    weight = st.sidebar.number_input(f"{u} -> {v}", value=int(data.get('capacity', 1)), key=key)
    st.session_state.graph[u][v]['capacity'] = weight
    if st.sidebar.button("Remove", key=f"remove-{key}"):
        st.session_state.graph.remove_edge(u, v)
        if hasattr(st, "rerun"):
            st.rerun()
        elif hasattr(st, "experimental_rerun"):
            st.experimental_rerun()

st.header("Graph editor")
if st.session_state.graph.nodes:
    nt = Network(height="500px", width="100%", directed=True)
    nt.set_options("""var options = {interaction:{dragNodes:true}, manipulation:{enabled:true}};""")
    for node in st.session_state.graph.nodes:
        nt.add_node(node, label=str(node))
    for u, v, data in st.session_state.graph.edges(data=True):
        nt.add_edge(u, v, label=str(data.get('capacity', 1)))
    nt.save_graph("graph.html")
    st.components.v1.html(open("graph.html").read(), height=520)
else:
    st.info("Use the sidebar to add nodes")

st.header("Algorithm")
if st.session_state.graph.nodes:
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
