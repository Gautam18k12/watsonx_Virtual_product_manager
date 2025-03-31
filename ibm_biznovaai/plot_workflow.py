import matplotlib.pyplot as plt
import networkx as nx
from langgraph.graph import StateGraph, END
from typing import Dict
from ibm_biznovaai.query_interpreter import interpret_query
from ibm_biznovaai.department_processor import process_departments
from ibm_biznovaai.response_generator import generate_response

# Define a simple GraphState type as a dictionary.
GraphState = Dict

# Build your workflow graph.
workflow = StateGraph(GraphState)
workflow.add_node("interpret", interpret_query)
workflow.add_node("process", process_departments)
workflow.add_node("respond", generate_response)
workflow.add_edge("interpret", "process")
workflow.add_edge("process", "respond")
workflow.add_edge("respond", END)
workflow.set_entry_point("interpret")

# Compile the workflow.
app = workflow.compile()

def plot_workflow_with_networkx(wf: StateGraph):
    """
    Plot the workflow diagram using NetworkX and Matplotlib.
    This function uses the public properties 'nodes' and 'edges' of the StateGraph.
    """
    G = nx.DiGraph()

    # Add nodes.
    for node in wf.nodes.keys():
        G.add_node(node)

    # Add edges.
    for edge in wf.edges:
        if isinstance(edge, dict):
            src = edge.get("from")
            tgt = edge.get("to")
        else:
            src, tgt = edge
        G.add_edge(src, tgt)

    # Use a layout for the nodes.
    pos = nx.spring_layout(G)
    
    # Draw the nodes, edges, and labels.
    nx.draw_networkx_nodes(G, pos, node_color="skyblue", node_size=2000)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    
    plt.title("Workflow Diagram")
    plt.axis("off")
    plt.show()

# Plot the workflow using NetworkX.
plot_workflow_with_networkx(workflow)
