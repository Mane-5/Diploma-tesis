!pip install geopandas networkx matplotlib shapely requests
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from shapely.geometry import Polygon
import pandas as pd
#1․Հայաստանի մարզերի և Երևանի հարևանության կապերի հիման վրա Dual Graph
G = nx.Graph()
regions = [
    "Երևան", "Արագածոտն", "Արարատ", "Արմավիր",
    "Գեղարքունիք", "Կոտայք", "Լոռի", "Շիրակ",
    "Սյունիք", "Տավուշ", "Վայոց ձոր"
]

G.add_nodes_from(regions)
edges = [
    ("Երևան", "Արագածոտն"),
    ("Երևան", "Արարատ"),
    ("Երևան", "Արմավիր"),
    ("Երևան", "Կոտայք"),

    ("Արագածոտն", "Արմավիր"),
    ("Արագածոտն", "Կոտայք"),
    ("Արագածոտն", "Լոռի"),
    ("Արագածոտն", "Շիրակ"),

    ("Արարատ", "Արմավիր"),
    ("Արարատ", "Կոտայք"),
    ("Արարատ", "Գեղարքունիք"),
    ("Արարատ", "Վայոց ձոր"),

    ("Կոտայք", "Արագածոտն"),
    ("Կոտայք", "Արարատ"),
    ("Կոտայք", "Երևան"),
    ("Կոտայք", "Գեղարքունիք"),
    ("Կոտայք", "Լոռի"),
    ("Կոտայք", "Տավուշ"),

    ("Գեղարքունիք", "Կոտայք"),
    ("Գեղարքունիք", "Արարատ"),
    ("Գեղարքունիք", "Վայոց ձոր"),
    ("Գեղարքունիք", "Տավուշ"),

    ("Լոռի", "Շիրակ"),
    ("Լոռի", "Արագածոտն"),
    ("Լոռի", "Կոտայք"),
    ("Լոռի", "Տավուշ"),

    ("Շիրակ", "Լոռի"),
    ("Շիրակ", "Արագածոտն"),

    ("Վայոց ձոր", "Արարատ"),
    ("Վայոց ձոր", "Գեղարքունիք"),
    ("Վայոց ձոր", "Սյունիք"),

    ("Սյունիք", "Վայոց ձոր"),

    ("Տավուշ", "Լոռի"),
    ("Տավուշ", "Կոտայք"),
    ("Տավուշ", "Գեղարքունիք")
]
G.add_edges_from(edges)

print(f"Գրաֆը հաջողությամբ կառուցված է։")
print(f"Գագաթներ (Մարզեր) — {G.number_of_nodes()}")
print(f"Կողեր (Հարևանության կապեր) — {G.number_of_edges()}")

#2․Welsh-Powell Գրաֆի գունավորման ալգորիթմ։
def welsh_powell_coloring(graph):
    # Քայլ 1: Տեսակավորել գագաթները ըստ աստիճանի նվազման (deg(v))
    sorted_nodes = sorted(graph.nodes(), key=lambda n: graph.degree(n), reverse=True)

    color_map = {}
    current_color = 0

    for node in sorted_nodes:
        if node not in color_map:
            color_map[node] = current_color
            # Գտնում ենք մնացած չներկված գագաթները, որոնք հարևան չեն այս գույնի հետ
            for other_node in sorted_nodes:
                if other_node not in color_map:
                    has_neighbor_with_color = any(
                        graph.has_edge(other_node, neighbor) and color_map.get(neighbor) == current_color
                        for neighbor in graph.nodes()
                    )
                    if not has_neighbor_with_color:
                        color_map[other_node] = current_color
            current_color += 1

    return color_map
  
  #3․Ալգորիթմի կիրառումը  կառուցված G գրաֆի վրա
  color_assignment = welsh_powell_coloring(G)
print("--- ՄԱՐԶԵՐԻ ԵՎ ԵՐԵՎԱՆԻ ԳՈՒՆԱՎՈՐՄԱՆ ԱՐԴՅՈՒՆՔՆԵՐԸ ---")
max_color = 0
for node, color in sorted(color_assignment.items(), key=lambda x: x[1]):
    print(f"Մարզ/Քաղաք: {node:<15} | Գույն ID: {color} | Հարևանների քանակ (deg): {G.degree(node)}")
    if color > max_color:
        max_color = color

print(f"\nՕգտագործված գույների նվազագույն քանակը (Քրոմատիկ թիվ - $\chi(G)$): {max_color + 1}")

#4․Վիզուալիզացիա
plt.figure(figsize=(10, 8))
palette = ['#4CAF50', '#2196F3', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4']
geographic_pos = {
    "Շիրակ": (1.0, 7.5),
    "Լոռի": (3.5, 8.0),
    "Տավուշ": (6.0, 7.5),
    "Արագածոտն": (2.0, 5.5),
    "Կոտայք": (4.5, 5.5),
    "Երևան": (3.2, 4.2),
    "Արմավիր": (1.5, 4.0),
    "Արարատ": (3.0, 2.8),
    "Գեղարքունիք": (6.5, 5.0),
    "Վայոց ձոր": (5.5, 2.0),
    "Սյունիք": (7.0, 0.5)
}

node_colors = [palette[color_assignment[node] % len(palette)] for node in G.nodes()]
nx.draw_networkx_nodes(G, geographic_pos, node_color=node_colors, node_size=1800, edgecolors='black', linewidths=1.5)
nx.draw_networkx_edges(G, geographic_pos, width=2, alpha=0.6, edge_color='gray')
nx.draw_networkx_labels(G, geographic_pos, font_size=9, font_weight='bold', font_family='sans-serif')
plt.title("ՀՀ Մարզերի Հարևանության Գրաֆը՝ Ըստ Աշխարհագրական Դիրքերի", fontsize=13, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig('armenia_graph_coloring.png', dpi=300, bbox_inches='tight')
plt.show()
