from enum import Enum, auto
import networkx as nx
import random
import matplotlib.pyplot as plt
from core import automate ,Automate
from automate_render import AutomatonRenderer

class TypeGraphe(Enum):
    Simple = auto()
    Complet = auto()   
    Bipartis = auto()
    Eulerien = auto()
    Hamiltonien = auto()

class AutomatonAlphabet(Enum):
    initialization = auto()
    add_nodes = auto()   
    add_edges = auto()
    finalization = auto()


class GraphGeneratorAutomaton:

    def __init__(self, num_nodes = 10, edge_prob = 0.5, directed=True, valued=True , type = TypeGraphe.Eulerien):
        self.num_nodes = num_nodes
        self.edge_prob = edge_prob
        self.type= type
        self.directed = directed
        self.valued = valued
        self.state = 1


    def runGenerateGraph(self):
        """
        Runs the process of generating a simple graph using the AutomatonAlphabet class.

        This method iterates through different states of the AutomatonAlphabet class and performs
        specific actions based on the current state. The states include initialization, adding nodes,
        adding edges, and finalization.

        Returns:
            None
        """

        self.state = AutomatonAlphabet.initialization
        while self.state != AutomatonAlphabet.finalization:
            if self.state == AutomatonAlphabet.initialization:
                self.__initialize_graph()
            elif self.state == AutomatonAlphabet.add_nodes:
                self.__add_nodes()
            elif self.state == AutomatonAlphabet.add_edges:
                self.__add_edges()
            elif self.state == AutomatonAlphabet.finalization:      
                self.__finalize()
        if self.type == TypeGraphe.Simple:
            addEdges=f'  add_edges ( graphEdge < {self.edge_prob} )'
            endCondition=f' (pas boucle).(pas arret parrallele)'    
        if self.type == TypeGraphe.Complet:
            addEdges=f'  add_edges ( graph.number_of_edges() < { round(self.num_nodes * (self.num_nodes - 1) / 2 ) })'
            endCondition=f'    graph.number_of_edges() >= { round(self.num_nodes * (self.num_nodes - 1) / 2 ) }'
        self.automaton = self.__generateAutomaton(
            initNode=f'  init (numberNodes = {self.num_nodes})',
            addNodes=f'  add_nodes (graphNodes < {self.num_nodes})',
            graphNodes=f'  graphNodes >= {self.num_nodes}',
            addEdges=addEdges,
            endCondition=endCondition,
            finalize='  finalize' )       


    def __initialize_graph(self):
        # Step 1: Initialize the graph
        self.graph =  nx.DiGraph() if self.directed else nx.Graph()
        self.state = AutomatonAlphabet.add_nodes
    

    def __add_nodes(self):
        # Step 2: Add nodes
        self.graph.add_nodes_from(range(self.num_nodes))
        self.state = AutomatonAlphabet.add_edges
        
    def __add_edges(self):
        # Step 3: Add edges
        if self.type == TypeGraphe.Simple:
            while True:
                print(self.graph.number_of_edges() , self.num_nodes * (self.num_nodes - 1) / 2 * self.edge_prob)
                for i in range(self.num_nodes):
                    for j in range(i + 1, self.num_nodes):
                        if random.random() < self.edge_prob:
                            if not self.graph.has_edge(i, j):
                                self.graph.add_edge(i, j , weight=random.randint(1, 10) if self.valued else None)
                if self.graph.number_of_edges() >= self.num_nodes * (self.num_nodes - 1) / 2 * self.edge_prob:      
                    break          
        
        if self.type == TypeGraphe.Complet:
            self.graph : nx.Graph = nx.complete_graph(self.num_nodes , nx.DiGraph() if self.directed else nx.Graph())
            if self.valued:
                for i, j in self.graph.edges():
                    self.graph[i][j]['weight'] = random.randint(1, 10)  
        if self.type == TypeGraphe.Bipartis:
            self.graph = nx.complete_bipartite_graph(self.num_nodes, self.num_nodes) 
        if self.type == TypeGraphe.Eulerien:
            self.graph = nx.eulerian_graph(self.num_nodes)
        if self.type == TypeGraphe.Hamiltonien:
            self.graph = nx.hameltonien_graph(self.num_nodes)            

        self.state = AutomatonAlphabet.finalization
    def __finalize(self):
        # Step 4: Finalize the graph generation
        self.state = AutomatonAlphabet.finalization
        print("Graph generation is complete.")

    def __generateAutomaton(self, endCondition :str, initNode :str , addNodes :str, graphNodes :str, addEdges :str, finalize  :str) -> Automate:
        self.alphabet = [initNode, addNodes, graphNodes, addEdges, endCondition, finalize]
        self.etats = [1, 2, 3, 4, 5]
        self.etats_initiaux = [1]
        self.etats_finaux = [5]
        self.transitions = [
            (1, initNode, 2),
            (2, addNodes, 2),
            (2, graphNodes, 3),
            (3, addEdges, 3),
            (3, endCondition, 4),
            (4, finalize, 5)
        ]
        return automate(self.alphabet, self.etats, self.etats_initiaux, self.etats_finaux, self.transitions)

    def get_graph(self):
        if self.state == AutomatonAlphabet.finalization:
            return self.graph
        else:
            raise Exception("Graph generation is not yet complete.")
        

# Paramètres de génération
num_nodes = 10  # Nombre de nœuds dans le graphe
edge_prob = 0.2  # Probabilité d'ajout d'une arête entre deux nœuds

# Créer l'automate de génération de graphe
automaton = GraphGeneratorAutomaton(num_nodes, edge_prob)

# Exécuter l'automate
automaton.runGenerateGraph()

# Récupérer le graphe généré
generated_graph = automaton.get_graph()



#visualiser le graphe
pos = nx.spring_layout(generated_graph)  # positions for all nodes

nx.draw(generated_graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12, font_weight="bold", arrows=True )

edge_labels = {(u, v): d["weight"] for u, v, d in generated_graph.edges(data=True)}

print(automaton.automaton)
renderer = AutomatonRenderer(automaton.automaton)
renderer.render(output_file='automaton', format='png')

nx.draw_networkx_edge_labels(generated_graph, pos, edge_labels=edge_labels)

plt.show()




