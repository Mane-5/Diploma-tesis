import matplotlib.pyplot as plt
import networkx as nx
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

    ("Կոտայք", "Գեղարքունիք"),
    ("Կոտայք", "Լոռի"),
    ("Կոտայք", "Տավուշ"),

    ("Գեղարքունիք", "Վայոց ձոր"),
    ("Գեղարքունիք", "Տավուշ"),
    ("Գեղարքունիք", "Սյունիք"),

    ("Լոռի", "Շիրակ"),
    ("Լոռի", "Տավուշ"),

    ("Վայոց ձոր", "Սյունիք"),
]
G.add_edges_from(edges)

print("Գրաֆը հաջողությամբ կառուցված է։")
print(f"Գագաթներ (Մարզեր) — {G.number_of_nodes()}")
print(f"Կողեր (Հարևանության կապեր) — {G.number_of_edges()}")


#2․Welsh-Powell Գրաֆի գունավորման ալգորիթմ։

def welsh_powell_coloring(graph):
    # Քայլ 1: գագաթների տեսակավորում ըստ աստիճանի նվազման
    sorted_nodes = sorted(graph.nodes(), key=lambda n: graph.degree(n), reverse=True)

    color_map = {}
    current_color = 0

    for node in sorted_nodes:
        if node not in color_map:
            color_map[node] = current_color
            # Նույն գույնով ներկում ենք չներկված այն գագաթները,
            # որոնք այդ գույնի հետ ներկված հարևան չունեն
            for other in sorted_nodes:
                if other not in color_map:
                    conflict = any(
                        color_map.get(nb) == current_color
                        for nb in graph.neighbors(other)
                    )
                    if not conflict:
                        color_map[other] = current_color
            current_color += 1

    return color_map
  
  #3․Ալգորիթմի կիրառումը և արդյունքների ստուգում

  color_assignment = welsh_powell_coloring(G)

print("\n--- ՄԱՐԶԵՐԻ ԵՎ ԵՐԵՎԱՆԻ ԳՈՒՆԱՎՈՐՄԱՆ ԱՐԴՅՈՒՆՔՆԵՐԸ ---")
for node, color in sorted(color_assignment.items(), key=lambda x: x[1]):
    print(f"Մարզ/Քաղաք: {node:<15} | Գույն ID: {color} | Հարևանների քանակ (deg): {G.degree(node)}")

num_colors = max(color_assignment.values()) + 1
print(f"\nWelsh–Powell-ով օգտագործված գույների քանակը: {num_colors}")

# Ներկման ճշտության ստուգում՝ հարևանները չպետք է ունենան նույն գույնը
is_proper = all(color_assignment[u] != color_assignment[v] for u, v in G.edges())
print(f"Ներկումը ճիշտ է (հարևանները՝ տարբեր գույներ): {is_proper}")

# Ստորին գնահատական՝ մաքսիմալ կլիկի չափը (ω(G) <= χ(G))
clique_size = max(len(c) for c in nx.find_cliques(G))
print(f"Ստորին գնահատական (մաքսիմալ կլիկ ω(G)): {clique_size}")
if num_colors == clique_size:
    print(f"Ներկումը օպտիմալ է՝ χ(G) = {clique_size}")
    
#4.Համեմատության համար՝ DSATUR 
dsatur = nx.coloring.greedy_color(G, strategy="DSATUR")
print(f"DSATUR-ով օգտագործված գույների քանակը: {max(dsatur.values()) + 1}")


#5․Վիզուալիզացիա

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

node_colors = [palette[color_assignment[n] % len(palette)] for n in G.nodes()]
nx.draw_networkx_nodes(G, geographic_pos, node_color=node_colors,
                       node_size=1800, edgecolors='black', linewidths=1.5)
nx.draw_networkx_edges(G, geographic_pos, width=2, alpha=0.6, edge_color='gray')
nx.draw_networkx_labels(G, geographic_pos, font_size=9, font_weight='bold',
                        font_family='sans-serif')
plt.title("ՀՀ Մարզերի Հարևանության Գրաֆը՝ Ըստ Աշխարհագրական Դիրքերի",
          fontsize=13, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig('armenia_graph_coloring.png', dpi=300, bbox_inches='tight')
plt.show()
