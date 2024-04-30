from enum import Enum, auto
from collections.abc import Iterable
""""
1.
Créer une modélisation orientée objet d’un automate et l’enrichir par les méthodes nécessaires :
"""
# class frozenset(frozenset):
#     def __str__(self):
#         # Convert the elements to a string representation and join them with commas
#         elements_str = ", ".join(str(ele) for ele in self)
#         return "{" + elements_str + "}"


class TypeEtat(Enum):
    """
    bach ndefiniw les types dial les etats blast mankhdmo b'strings (puisqu'ils sont susceptibles au bugs ou fautes de frappe etc....)
    """
    Initial = auto()
    Intermediaire = auto()
    Terminal = auto()



class Etat:
    def __init__(self, label_etat : list[str | int], type_etat : TypeEtat = TypeEtat.Intermediaire):
        self.label_etat = frozenset(label_etat)
        self.type_etat = type_etat


class Alphabet:
    def __init__(self, val_alphabet : str):
        self.val_alphabet = val_alphabet

class Transition:
    def __init__(self, etat_source : Etat, etat_destination : Etat, alphabet : Alphabet):
        self.etat_source = etat_source
        self.etat_destination = etat_destination
        self.alphabet = alphabet



class Automate:
    
    def __init__(self, list_alphabets : list[Alphabet], list_etats : list[Etat], list_transitions : list[Transition]):
        """"
        madrtch list initiaux w terminaux, 7itach kayna type d'etat fl'etat, n9do n'segregiw bih
        """
        self.list_alphabets = list_alphabets
        self.list_etats = list_etats
        self.list_transitions = list_transitions
        self.etats_initiaux = [etat for etat in list_etats if etat.type_etat == TypeEtat.Initial]
        self.etats_terminaux = [etat for etat in list_etats if etat.type_etat == TypeEtat.Terminal]
    
    def __process_data(self,list_modifier):
        initial_closure=[]
        
        for ele in list_modifier:
            element=ele
            if not isinstance(ele.label_etat,tuple):
                element=(ele,)
            for num in element:
                initial_closure.append(*tuple(num.label_etat))   
        return  initial_closure 
    
    def return_alpha(self):
        return  [alpha.val_alphabet for alpha in self.list_alphabets]
    
    def return_etat(self)-> list[tuple[set[str | int], str, set[str | int]]]:
        return [set(etat.label_etat)  for etat in self.list_etats]
    
    def return_transition(self)-> list[tuple[set[str | int], str, set[str | int]]]:
        return [(set(trans.etat_source.label_etat), trans.alphabet.val_alphabet, set(trans.etat_destination.label_etat)) for trans in self.list_transitions]
    
    
    def determiniser(self):
        new_states = {}
        unprocessed = []
        new_transitions = []

        initial_closure=self.__process_data(self.etats_initiaux)    
        initial_closure = frozenset(initial_closure)
        
        new_initial_state = Etat(label_etat=initial_closure, type_etat=TypeEtat.Initial)
        new_states[initial_closure] = new_initial_state
        unprocessed.append(initial_closure)


        while unprocessed:
            current_set = unprocessed.pop(0)
            current_new_state = new_states[current_set]

            for alpha in self.list_alphabets:
                target_states = frozenset(
                    sum([self.__get_target_states(state, alpha) for state in current_set], [])
                )
                if not target_states :
                    continue
                if target_states not in new_states:
                    target_state_type = TypeEtat.Terminal if any(s in self.etats_terminaux for s in target_states) else TypeEtat.Intermediaire
                    new_state = Etat(label_etat=target_states, type_etat=target_state_type)
                    new_states[target_states] = new_state
                    unprocessed.append(target_states)

                new_transitions.append(Transition(current_new_state, new_states[target_states], alpha))

        new_list_states = list(new_states.values())
        return Automate(self.list_alphabets, new_list_states, new_transitions)
    
    
    def __get_target_states(self, from_state, alpha):
        returned_ele=[]
        for trans in self.list_transitions:
            if from_state in trans.etat_source.label_etat  and trans.alphabet == alpha:
                returned_ele.append(*tuple(trans.etat_destination.label_etat))
        return returned_ele
    
    def completer(self):
        ...

    def minimiser(self):
        ...

    def render(self):
        ...


"""
2.
Créer une fonction qui permet la lecture d’un automate à partir d’une entrée de la forme suivante :
"""
def conversion_iterable(etat):
    if isinstance(etat, Iterable):
        return etat
    return (etat,)
def automate(alphabet : list[str], etats : list[str | int], etats_initiaux : list[str | int], etats_finaux : list[str | int], transitions : list[tuple[int, str | int, int]]) -> Automate:
    #coversion_en_frozen_set
    etats_initiaux = [conversion_iterable(label) for label in etats_initiaux]
    etats_finaux = [conversion_iterable(label) for label in etats_finaux]
    etats = [conversion_iterable(label) for label in etats]
    transitions = [(conversion_iterable(src),alph,conversion_iterable(dest)) for src, alph, dest in transitions]

    #creation des alphabets
    aut_alphabets = [Alphabet(alph) for alph in alphabet]

    #creation des etats 
    aut_etats_initiaux = [Etat(label, TypeEtat.Initial) for label in etats_initiaux]
    aut_etats_terminaux = [Etat(label, TypeEtat.Terminal) for label in etats_finaux]
    aut_etats_intermediaires = [Etat(label) for label in etats if label not in etats_initiaux and label not in etats_finaux]
    aut_etats = aut_etats_initiaux + aut_etats_intermediaires + aut_etats_terminaux
    
    #creation des transitions
    aut_transitions = []
    for src, alph, dest in transitions:                
        aut_src = next((etat for etat in aut_etats if src == tuple(etat.label_etat)))
        aut_dest = next((etat for etat in aut_etats if dest == tuple(etat.label_etat)))
        aut_alph = next((aut_alph for aut_alph in aut_alphabets if aut_alph.val_alphabet == alph))
        aut_transitions.append(Transition(aut_src,aut_dest , aut_alph))

    #creation de l'automate
    return Automate(aut_alphabets, aut_etats, aut_transitions)    



# Exemple de données de test pour la fonction automate
alphabet = ['a', 'b']
etats = [1, 2, 3]
etats_initiaux = [1]
etats_finaux = [3]
transitions = [(1, 'a', 2), (2, 'b', 3),(2, 'b', 2)]

# Création de l'automate
exemple_automate = automate(alphabet, etats, etats_initiaux, etats_finaux, transitions)

# Exemple de données de test pour la méthode determiniser
# On peut utiliser l'automate créé précédemment comme point de départ
automate_determinise = exemple_automate.determiniser()

# Vérification des résultats
print("Automate original:")
print("Alphabets:",exemple_automate.return_alpha())
print("États:", exemple_automate.return_etat())
print("Transitions:",exemple_automate.return_transition())


print("\nAutomate déterminisé:")
print("Alphabets:",automate_determinise.return_alpha())
print("États:", automate_determinise.return_etat())
print("Transitions:",automate_determinise.return_transition())