import networkx as nx
import os
from pyvis.network import Network
from fractions import Fraction


# Optionally remove nodes with a degree lower than a specified threshold
def remove_low_degree_nodes(G, min_degree=5):
    low_degree_nodes = [node for node, degree in G.degree() if degree < min_degree]
    G.remove_nodes_from(low_degree_nodes)


# Draw network graph using Pyvis
def draw_graph_with_pyvis(X, centrality, community_map):
    net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")

    # Sort nodes in H based on centrality, only show top 100
    top_nodes = sorted((node for node in X.nodes()), key=lambda node: centrality.get(node, 0), reverse=True)[:100]

    community_colors = ["#FFA07A", "#20B2AA", "#778899", "#9370DB", "#FFD700", "#FF6347", "#3CB371", "#F08080",
                        "#00FA9A", "#BDB76B", "#FF00FF"]

    # Add top 100 nodes to Pyvis network and set colors
    for node in top_nodes:
        color = community_colors[community_map[node] % len(community_colors)]
        net.add_node(node, title=str(node), size=centrality[node] * 500, group=community_map[node], color=color)

    # Find the max weight for edges
    max_weight = max(data['weight'] for _, _, data in X.edges(data=True))

    # Add edges between the top 100 nodes, setting the edge width based on the weight relative to the maximum weight
    for source, target, data in X.edges(data=True):
        if source in top_nodes and target in top_nodes:
            weight = data.get('weight', 1)  # Default weight is 1 if not specified
            edge_width = weight / max_weight * 10  # Normalize width based on weight
            net.add_edge(source, target, width=edge_width)

    net.options.physics.barnesHut.springLength = 2000
    net.options.physics.barnesHut.springConstant = 0.02
    net.options.physics.barnesHut.damping = 0.09
    net.options.physics.barnesHut.centralGravity = 0.2
    net.options.physics.barnesHut.gravitationalConstant = -1000
    net.options.physics.maxVelocity = 5
    net.options.physics.minVelocity = 0.1

    # Enable node deletion, node add, edge add, etc
    net.show_buttons(filter_=['manipulation', 'physics'])

    filepath = os.path.join('static', 'graph.html')
    net.write_html(filepath)

    return 'graph.html'


# Draw the shortest path graph using Pyvis
def draw_shortest_path_graph(G, path):
    net = Network(height="300px", width="100%", bgcolor="#ffffff", font_color="black")

    # Add nodes and edges along the path
    previous_node = None
    for node in path:
        net.add_node(node, title=str(node), label=str(node))
        if previous_node is not None:
            weight = G[previous_node][node].get('weight', 1)  # Get the weight of the edge, defaulting to 1
            # Convert the weight to a fraction representation
            edge_weight = str(Fraction(weight).limit_denominator())
            net.add_edge(previous_node, node, title=str(edge_weight), label=str(edge_weight))
        previous_node = node

    net.options.physics.barnesHut.springLength = 200
    net.options.physics.barnesHut.springConstant = 0.05
    net.options.physics.barnesHut.damping = 0.09
    net.options.physics.barnesHut.centralGravity = 0.3
    net.options.physics.barnesHut.gravitationalConstant = -800
    net.options.physics.maxVelocity = 50
    net.options.physics.minVelocity = 0.1

    # net.show_buttons(filter_=['manipulation', 'physics'])

    unique_filename = f"shortest_path.html"
    filepath = os.path.join('static', unique_filename)
    net.write_html(filepath)

    return unique_filename


# Invert edge weights to reflect closeness instead of distance
def invert_weights(G):
    H = nx.Graph()
    for u, v, data in G.edges(data=True):
        # Ensure the weight is positive to avoid division by zero errors
        if data['weight'] > 0:
            H.add_edge(u, v, weight=1.0 / data['weight'])  # Invert the weight for closeness instead of distance
        else:
            # For edges with zero or undefined weight, assign a large weight value
            H.add_edge(u, v, weight=float('inf'))
    return H

#
# def draw_graph(G, centrality, community_map, fig_size=(5, 3), node_scale=3000, title=""):
#     fig, ax = plt.subplots(figsize=fig_size)
#     pos = nx.spring_layout(G, k=0.5, seed=4572321)
#     node_color = [community_map.get(n, 0) for n in G.nodes()]
#     node_size = [centrality.get(n, 0) * node_scale for n in G.nodes()]
#     nx.draw_networkx(
#         G,
#         pos=pos,
#         with_labels=True,
#         node_color=node_color,
#         node_size=node_size,
#         edge_color="gainsboro",
#         alpha=0.4,
#         ax=ax,
#         font_size=3
#     )
#     set_graph_title_and_legend(ax, fig, title=title)
#     return fig, ax
#
#
# def set_graph_title_and_legend(ax, fig, title=""):
#     font_title = {"color": "black", "fontweight": "bold", "fontsize": 5}
#     font_legend = {"color": "red", "fontweight": "bold", "fontsize": 3}
#     ax.set_title(title, fontdict=font_title)
#     ax.text(0.80, 0.10, "Node color = Community structure", horizontalalignment="center", transform=ax.transAxes,
#             fontdict=font_legend)
#     ax.text(0.80, 0.06, "Node size = PageRank centrality", horizontalalignment="center", transform=ax.transAxes,
#             fontdict=font_legend)
#     ax.margins(0.1, 0.05)
#     fig.tight_layout()
#     plt.axis("off")
#
#
# def save_fig_to_base64(fig):
#     img = BytesIO()
#     fig.savefig(img, format='png', dpi=300)
#     plt.close(fig)
#     img.seek(0)
#     return base64.b64encode(img.getvalue()).decode('utf8')
#
# def compute_centrality_and_communities(X):
#     centrality = nx.pagerank(X, weight='weight')
#     communities = nx.community.louvain_communities(X, weight='weight')
#     community_map = {node: i for i, community in enumerate(communities) for node in community}
#     return centrality, community_map
#
#
# def compute_betweenness_and_louvain(X):
#     centrality = nx.betweenness_centrality(X, weight='weight')
#     communities = nx.community.louvain_communities(X, weight='weight')
#     community_map = {node: i for i, community in enumerate(communities) for node in community}
#     return centrality, community_map

