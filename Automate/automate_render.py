from core import automate,Automate
from graphviz import Digraph


class AutomatonRenderer:
    def __init__(self, automaton: Automate):
        self.automaton = automaton

    def fixing_format(self):
        # Convert list_etats to sets
        list_etats = self.automaton.return_etat()

        # Convert etats_initiaux to sets
        etats_initiaux =    self.automaton.return_etat_initial()

        # Convert etats_terminaux to sets
        etats_terminaux = self.automaton.return_etat_terminaux()

        # Convert transition states to sets
        displayed_transition = self.automaton.return_transition()
        return list_etats, etats_initiaux, etats_terminaux, displayed_transition

    def render(self, output_file='automaton', format='png' ):
        dot = Digraph()
        list_etats, etats_initiaux, etats_terminaux, displayed_transition = self.fixing_format()

        # Add nodes
        for etat in list_etats:
            if etat in etats_terminaux:
                dot.node(str(etat), shape='doublecircle')
            else:
                dot.node(str(etat))

        # Add transitions
        for transition in displayed_transition:
            dot.edge(str(transition[0]), str(transition[2]), label=transition[1])

        # Add initial state with arrow
        for init in etats_initiaux:
            dot.edge('', str(init), style='invis')
            dot.node('', shape='point')
            dot.edge('', str(init), label='', style='bold')

        dot.render(output_file, format=format, view=True )


# Usage example
# Exemple de données de test pour la fonction automate
alphabet = ['a', 'b']
etats = [1, 2, 3, 4, 5, 6, 7, 8]
etats_initiaux = [1]
etats_finaux = [ 6, 7, 8]
transitions =   [(1, 'a', 1),(1, 'b', 5),
                (2, 'a', 2),(2, 'b', 5),
                (3, 'a', 4),(3, 'b', 6),
                (4, 'a', 3),(4, 'b', 8),
                (5, 'b', 4), (5, 'a', 2),
                (6, 'a', 3),(6, 'b', 7),
                (7, 'b', 7),(7, 'a', 8),
                (8, 'a', 7), (8, 'b', 7),
                ]

# alphabet = ['a', 'b','c','d','e']
# etats = [1, 2, 3, 4, 5, 6]
# etats_initiaux = [1,3,6]
# etats_finaux = [6]
# transitions =   [(1, 'a', 2),(1, 'a', 3),(1, 'a', 4),
#                 (2, 'a', 2),(2, 'c', 5),
#                 (2, 'd', 5),(3, 'b', 2),(3, 'b', 4),
#                 (4, 'b', 4),(4, 'c', 5),(4, 'd', 5),(5, 'e', 6),]

# alphabet = ['a', 'b']
# etats = [1, 2, 3, 4]
# etats_initiaux = [1]
# etats_finaux = [2]
# transitions =   [(1, 'a', 1),(1, 'b', 2),(1, 'a', 3),
#                 (2, 'b', 1),(2, 'b', 4),
#                 (3, 'b', 2),(3, 'a', 4),
#                 (4, 'a', 4),(4, 'b', 2),]


# Création de l'automate
if __name__ == '__main__':
    exemple_automate = automate(alphabet, etats, etats_initiaux, etats_finaux, transitions)

    # Exemple de données de test pour la méthode determiniser
    # On peut utiliser l'automate créé précédemment comme point de départ
    automate_determinise = exemple_automate.determiniser()
    automate_completer = exemple_automate.completer(0)

    # Vérification des résultats
    print("Automate original:")
    print("Alphabets:",exemple_automate.return_alpha())
    print("États:", exemple_automate.return_etat())
    print("Transitions:",exemple_automate.return_transition())


    print("\nAutomate déterminisé:")
    print("Alphabets:",automate_determinise.return_alpha())
    print("États:", automate_determinise.return_etat())
    print("Transitions:",automate_determinise.return_transition())

    print("\nAutomate completer:")
    print("Alphabets:",automate_completer.return_alpha())
    print("États:", automate_completer.return_etat())
    print("Transitions:",automate_completer.return_transition())

    # # Appliquer la fonction minimiser
    automate_minimise_2 = exemple_automate.minimiser()

    # # Vérification des résultats
    # print("\nAutomate minimisé:")
    # print("Alphabets:", automate_minimise_2.return_alpha())
    # print("États:", automate_minimise_2.return_etat())
    # print("Transitions:", automate_minimise_2.return_transition())
    renderer = AutomatonRenderer(exemple_automate)
    renderer.render(output_file='automaton', format='png')
    renderer = AutomatonRenderer(automate_minimise_2)
    renderer.render(output_file='automaton', format='png')



