from enum import Enum, auto
import networkx as nx 
import random
import matplotlib.pyplot as plt
from core import automate ,Automate
from automate_render import AutomatonRenderer
from math import floor
class TypeGraphe(Enum):
    Simple = auto()
    Complet = auto()   
    CompletBipartis = auto()
    Eulerien = auto()
    Hamiltonien = auto()

class AutomatonAlphabet(Enum):
    initialization = auto()
    add_nodes = auto()   
    add_edges = auto()
    finalization = auto()


class GraphGeneratorAutomaton:
    def __init__(self, num_nodes = 10, edge_prob = 0.5, directed=True, valued=False , type = TypeGraphe.Hamiltonien):
       
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

        removeEdges=''
        endCondition2=''
        if self.type == TypeGraphe.Simple or self.type == TypeGraphe.Hamiltonien:
            initNode=f'  init (numberNodes = {self.num_nodes})'
            if self.valued:
                addEdges=f'  add_valued_edges ( graphEdge < {self.edge_prob} )'
            else :
                addEdges=f'  add_edges ( graphEdge < {self.edge_prob} )'    
            endCondition=f' (pas boucle).(pas arret parrallele)'    
        if self.type == TypeGraphe.Complet:
            initNode=f'  init (numberNodes = {self.num_nodes})'
            if self.valued:
                addEdges=f'  add_valued_edges ( graph.number_of_edges() < { round(self.num_nodes * (self.num_nodes - 1) / 2 ) })'
            else :
                addEdges=f'  add_edges ( graph.number_of_edges() < { round(self.num_nodes * (self.num_nodes - 1) / 2 ) })'  
            endCondition=f'    graph.number_of_edges() == { round(self.num_nodes * (self.num_nodes - 1) / 2 ) }'
        if self.type == TypeGraphe.CompletBipartis:
            initNode=f'  init . (numberNodes = {self.num_nodes}) . (topNodes et bottomNodes)'
            if self.valued:
                addEdges=f'  add_valued_edges. (graph.number_of_edges() < { round(self.top_nodes * self.bottom_nodes) }) . (topNodes liee avec bottomNodes)'
            else :
                addEdges=f'  add_edges .(graph.number_of_edges() < {round(self.top_nodes * self.bottom_nodes) }).(topNodes liee avec bottomNodes)'  
            endCondition=f'    graph.number_of_edges() == {self.bottom_nodes * self.top_nodes}'
        if self.type == TypeGraphe.Eulerien:
            initNode=f'  init (numberNodes = {self.num_nodes})'
            addEdges=f'  add_edges ( graph.number_of_edges() < { round(self.num_nodes * (self.num_nodes - 1) / 2 ) })'  
            endCondition=f'    graph.number_of_edges() == { round(self.num_nodes * (self.num_nodes - 1) / 2 ) }'
            if self.directed == False:
                removeEdges= f' remove_edges( Node_Degree1 % 2 != 0 && Node_Degree2 % 2 != 0)'
                endCondition2= f' Nodes_Degree % 2 == 0'
            else:
                removeEdges= f' remove_edges ( Node_in_Degree != Node_out_degree )'
                endCondition2= f' Nodes_in_Degree == Nodes_out_degree '
            
        self.automaton = self.__generateAutomaton(
            initNode=initNode,
            addNodes= f'  add_nodes (graphNodes < {self.num_nodes})',
            graphNodes=f'  graphNodes == {self.num_nodes}',
            addEdges=addEdges,
            endCondition=endCondition,
            finalize='  finalize',
            removeEdges=removeEdges,
            endCondition2=endCondition2
            )


    def __initialize_graph(self):
        # Step 1: Initialize the graph
        self.graph =  nx.DiGraph() if self.directed else nx.Graph()
        self.state = AutomatonAlphabet.add_nodes  

    def __add_nodes(self):
        # Step 2: Add nodes
        if self.type == TypeGraphe.Simple or self.type == TypeGraphe.Complet or self.type == TypeGraphe.Eulerien : 
            self.graph.add_nodes_from(range(self.num_nodes))
            
        if self.type == TypeGraphe.CompletBipartis:
            if self.num_nodes % 2 == 0:
                self.top_nodes = int(self.num_nodes/2) 
                self.bottom_nodes = int(self.num_nodes/2)
            else :
                self.top_nodes = floor(self.num_nodes/2)
                self.bottom_nodes =  floor(self.num_nodes/2)+1
            self.top = list(range(self.top_nodes))
            self.bottom = list(range(self.top_nodes, self.top_nodes + self.bottom_nodes))
            
            self.graph.add_nodes_from(self.top, bipartite=0)
            self.graph.add_nodes_from(self.bottom, bipartite=1)       
        self.state = AutomatonAlphabet.add_edges
             
    def __add_edges(self):
        #ADD EDGES FOR A SIMPLE GRAPH
        if self.type == TypeGraphe.Simple:
            while True:
                for i in range(self.num_nodes):
                    for j in range(i + 1, self.num_nodes):
                        if random.random() < self.edge_prob:
                            if not self.graph.has_edge(i, j):
                                if self.valued:
                                    self.graph.add_edge(i, j , weight=random.randint(1, 10))
                                else :
                                    self.graph.add_edge(i, j)    
                if self.graph.number_of_edges() >= self.num_nodes * (self.num_nodes - 1) / 2 * self.edge_prob:      
                    break          
        
        #ADD EDGES FOR A COMPLETE GRAPH
        if self.type == TypeGraphe.Complet:
            self.graph : nx.Graph = nx.complete_graph(self.num_nodes , nx.DiGraph() if self.directed else nx.Graph())
            if self.valued:
                for i, j in self.graph.edges():
                    self.graph[i][j]['weight'] = random.randint(1, 10) 
        


        #ADD EDGES FOR A BIPARTITE GRAPH 
        if self.type == TypeGraphe.CompletBipartis:
            for u in self.top:
                for v in self.bottom:
                    if self.valued:
                        value = random.randint(1, 10)
                        if random.random() < 0.5:
                            self.graph.add_edge(v, u, weight=value)
                        else :
                            self.graph.add_edge(u, v, weight=value)    
                    else:
                        self.graph.add_edge(u, v)

        #ADD EDGES FOR AN EULERIEN GRAPH 
        if self.type == TypeGraphe.Eulerien:
            self.graph.add_edges_from([(i, j) for i in range(self.num_nodes) 
                                    for j in range(self.num_nodes) 
                                    if not self.graph.has_edge(i, j) and i!= j 
                                    ]) 

            # Create a list to store nodes with odd degree
            odd_degree_nodes = []

            # Connect nodes to make the graph Eulerian
            for node in self.graph.nodes():
                degree = self.graph.degree(node)
                if degree % 2 != 0:
                    odd_degree_nodes.append(node)

            while len(odd_degree_nodes) > 1:
                node1 = odd_degree_nodes.pop()
                node2 = odd_degree_nodes.pop()
                self.graph.remove_edge(node1, node2)

        #ADD EDGES FOR AN HAMELTONIEN GRAPH 
        if self.type == TypeGraphe.Hamiltonien:
            hamiltonian_path = list(range(self.num_nodes))
            random.shuffle(hamiltonian_path)
            hamiltonian_path.append(hamiltonian_path[0])
            
            # Add edges to form the Hamiltonian cycle
            for index in range(self.num_nodes-1):
                print(index)
                self.graph.add_edge(hamiltonian_path[index], hamiltonian_path[index+1] , weight = index )
            
            # Optionally add additional edges
            for i in range(self.num_nodes):
                for j in range(i + 1, self.num_nodes):
                    if random.random() > self.edge_prob and not self.graph.has_edge(i, j)  and not self.graph.has_edge(j,i) :
                        self.graph.add_edge(i, j , weight= -1)


        self.state = AutomatonAlphabet.finalization
    def __finalize(self):
        # Step 4: Finalize the graph generation
        self.state = AutomatonAlphabet.finalization
        print("Graph generation is complete.")

    def __generateAutomaton(self, endCondition :str, 
                            initNode :str ,
                            addNodes :str, 
                            graphNodes :str, 
                            addEdges :str,
                            removeEdges :str,
                            endCondition2:str, 
                            finalize  :str) -> Automate:
        self.alphabet = [initNode, addNodes, graphNodes, addEdges, endCondition,removeEdges,endCondition2, finalize]
        self.etats = [1, 2, 3, 4, 5]
        self.etats_initiaux = [1]
        if self.type == TypeGraphe.Eulerien:
            self.etats_finaux = [6]
            self.transitions = [
                (1, initNode, 2),
                (2, addNodes, 2),
                (2, graphNodes, 3),
                (3, addEdges, 3),
                (3, endCondition, 4),
                (4, removeEdges, 4),
                (4, endCondition2, 5),
                (5, finalize, 6)
            ]
        else:
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
    
    def draw_graph(self):

        generated_graph = self.get_graph()
        pos = nx.spring_layout(generated_graph) 

        #rendering a bipartite graph
        if self.type == TypeGraphe.CompletBipartis:
            pos = nx.bipartite_layout(self.graph, self.top, align='horizontal')  
            
        nx.draw(generated_graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=12, font_weight="bold", arrows=True )
        renderer = AutomatonRenderer(self.automaton)
        renderer.render(output_file='automaton', format='png')

        if self.valued or self.type == TypeGraphe.Eulerien  or self.type == TypeGraphe.Hamiltonien:
            if self.type == TypeGraphe.Eulerien: 
                circuit = list(nx.eulerian_circuit(self.graph))
                edge_labels = {edge: i for i, edge in enumerate(circuit)}  
                print("Eulerian Circuit:", circuit)   
            else:
                edge_labels = {(u, v): d["weight"] for u, v, d in generated_graph.edges(data=True)}
            nx.draw_networkx_edge_labels(generated_graph, pos, edge_labels=edge_labels)
        plt.show()



# Paramètres de génération
num_nodes = 5 # Nombre de nœuds dans le graphe
edge_prob = 0.2  # Probabilité d'ajout d'une arête entre deux nœuds

# Créer l'automate de génération de graphe
automaton = GraphGeneratorAutomaton(num_nodes, edge_prob)

# Exécuter l'automate
automaton.runGenerateGraph()

automaton.draw_graph()





