import networkx
import random

def setup_game(db, n_systems, avg_n_routes, civs):
    graph = create_systems_graph(n_systems, avg_n_routes)
    civs = place_civs(civs, graph)

    setup_db(db, graph, civs)


def create_systems_graph(n_systems, avg_n_routes):
    graph = networkx.Graph()
    systems = range(1, n_systems + 1)
    # Connects all systems
    minimal_edges = [(x, (x + 1)) for x in range(1, n_systems)]
    extra_edges = []
    for times in range(avg_n_routes):
        extra_edges += [((random.randrange(n_systems)), (random.randrange(n_systems)))
                        for _ in range(n_systems)]

    graph.add_nodes_from(systems)
    graph.add_edges_from(minimal_edges)
    graph.add_edges_from(extra_edges)
    return graph

def generate_system_attributes():
    return {
        "production": 1,
        "tuning": random.randrange(1_000_000)
    }

def generate_route_attributes():
    return {
        "distance": random.randrange(1, 50)
    }

def place_civs(civs, graph):
    out = []
    for name, key in civs:
        homeworld = list(graph.nodes)[random.randrange(graph.number_of_nodes())]
        out.append({
            "name": name,
            "key": key,
            "homeworld": homeworld
        })
    return out



def setup_db(db, graph, civs):
    for node in graph.nodes:
        attrs = generate_system_attributes()

        db.query_formatted("INSERT INTO systems (id, production, tuning) "
                           "VALUES (%s, %s, %s)",
                           (node, attrs["production"], attrs["tuning"]))

    for edge in graph.edges:
        origin = min(edge[0], edge[1])
        destination = max(edge[0], edge[1])
        if origin == destination:
            continue

        attrs = generate_route_attributes()
        db.query_formatted("INSERT INTO routes (origin, destination, distance) VALUES (%s, %s, %s)",
                           (origin, destination, attrs["distance"]))

    for civ in civs:
        db.query_formatted("INSERT INTO civilizations (name, homeworld, key) VALUES (%s, %s, %s)",
                           (civ["name"], civ["homeworld"], civ["key"]))