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
                returned_terminal=[]
                for state in current_set:
                    returned_terminal.extend(self.__get_target_states(state,alpha.val_alphabet))
                target_states = frozenset(returned_terminal)
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
    
    def  gerer_etat_multiple(self,returned_etat,determiniser=False):
        returned_ele=[]    
        if len(tuple(returned_etat))>1:
            if determiniser:
                returned_ele.extend(returned_etat)
            else :    
                returned_ele.append(returned_etat)
        else :
            returned_ele.append(*returned_etat) 
        return returned_ele        
    def completer(self,etat_puit):

        #definition des nouveau 
        list_transition=[]
        list_etat_initial=[]
        list_etat_final=[]
        list_etat=[]
        list_alphabets=[]


        for etat in self.list_etats:
            list_etat.append(*self.gerer_etat_multiple(etat.label_etat))
            if etat.type_etat==TypeEtat.Initial:
                list_etat_initial.append(*self.gerer_etat_multiple(etat.label_etat))
            elif etat.type_etat==TypeEtat.Terminal:  
                list_etat_final.append(*self.gerer_etat_multiple(etat.label_etat))
        for trans in self.list_transitions:
                list_alphabets.append(trans.alphabet.val_alphabet) if trans.alphabet.val_alphabet not in list_alphabets else None
                new_trans=(
                    *self.gerer_etat_multiple(trans.etat_source.label_etat),
                    trans.alphabet.val_alphabet,
                    *self.gerer_etat_multiple(trans.etat_destination.label_etat),
                )
                list_transition.append(new_trans) if new_trans not in list_transition else None
        

        #definition de etat puit
        list_etat.append(etat_puit)
        non_complet=False
        list_transition_puit=[]
        for index , etat in enumerate(list_etat):
            for alpha in list_alphabets:
                if not self.__get_target_states(etat,alpha) and etat!=etat_puit:
                    non_complet=True
                    list_transition.append([etat,alpha,etat_puit])
        #definir les transition pour etat puits
                if index == 0:
                    list_transition_puit.append([etat_puit,alpha,etat_puit]) 
        if  non_complet : 
            list_transition.extend(list_transition_puit)  
        else :
            list_etat.pop(list_etat.index(etat_puit))                   
        return automate(list_alphabets,list_etat,list_etat_initial,list_etat_final,list_transition)            
    
    
    def __get_target_states(self, from_state:int|str, alpha:str):
        returned_ele=[]
        for trans in self.list_transitions:
            if from_state in trans.etat_source.label_etat  and trans.alphabet.val_alphabet == alpha:
                added=self.gerer_etat_multiple(trans.etat_destination.label_etat,True)
                if len(added)>1:
                    returned_ele.extend(added)  
                else :
                    returned_ele.append(*added)  
        return conversion_iterable(returned_ele)
    def group_creation(self,group,partition):
        new_group=[]
        for state1 in group:
            for state2 in group:
                if state1 != state2:
                    if self.states_are_distinguishable(state1, state2, partition):
                        new_group.append(state1)
                        new_group.append(state2) 
                    else :
                        new_group.append(conversion_iterable((state1,state2,)))          
        new_group=set(new_group)
        filer_new_group=set()
        final=set()
        for ele in new_group:
            if type(ele) == tuple:
                filer_new_group.add(ele)
        for ele in new_group: 
            found=False
            if isinstance(ele,tuple): 
                    final.add(ele)
            else :
                for tup in filer_new_group:
                    if ele  in tup:       
                        found=True
            if  not found:
                final.add(ele)
        return final
    def minimiser(self):
        # init des premiers partition
         
        etat_terminaux=set([ele for etat_teminal in self.etats_terminaux for ele in etat_teminal.label_etat])
        etats_init=set([ele for etat_int in self.list_etats for ele in etat_int.label_etat if ele not in etat_terminaux])
        partition = [etat_terminaux, etats_init]
        list_alphabets=[alpha.val_alphabet for alpha in self.list_alphabets ]
        new_partition = []
        while True:

            for group in partition: 
                new_group = []
                if len(group)==1:
                    new_partition.append(group)
                    continue
                new_group=self.group_creation(group,partition)
                if new_group:
                    for ele in new_group :
                        new_partition.append(set(conversion_iterable(ele)))
            new_partition_without_unique=[]  
            new_partition_unique=[]  
            for ele in new_partition:
                if len(ele)>1:
                    new_partition_without_unique.append(ele)
                else :
                    new_partition_unique.append(ele)          
            conflicts_etat=[]
            for group in new_partition_without_unique:
                conflicts_group=set()
                conflicts_group.update(group)
                for ele in group:
                    for other_group in new_partition_without_unique :
                        if ele in other_group :
                            conflicts_group.update(other_group)
                conflicts_etat.append(conflicts_group) if conflicts_group not in conflicts_etat  else None
            new_partition=conflicts_etat+new_partition_unique

            if new_partition == partition:
                break
            partition = new_partition
            new_partition = []
        # Gather minimized states
        minimized_states = partition

        # Identify initial state(s)
        minimized_initial_states = [state for state in minimized_states if any(s in etat.label_etat for etat in self.etats_initiaux for s in state)]

        # Identify terminal state(s)
        minimized_terminal_states = [state for state in minimized_states if any(s in etat.label_etat for etat in  self.etats_terminaux for s in state)]

        # Update transitions to reflect minimized states
        minimized_transitions = self.update_transitions(minimized_states)
        print(minimized_transitions)
        return automate(list_alphabets,minimized_states,minimized_initial_states,minimized_terminal_states,minimized_transitions)

    def update_transitions(self, minimized_states):
        transitions = []
        for states in minimized_states:
            for alpha in self.list_alphabets:
                transition_dest=[]
                for etat in states:
                    transition_dest.extend(self.__get_target_states(etat, alpha.val_alphabet))
                for stats in minimized_states:     
                    if all(etat in stats for etat in transition_dest):
                        transitions.append((states, alpha.val_alphabet, stats))
                        break
        return transitions
    def states_are_distinguishable(self, state1:int, state2:int, partition:list[set[int]]):
       
        for alpha in self.list_alphabets:
            transitions1_target=self.__get_target_states(state1,alpha.val_alphabet)
            transitions2_target=self.__get_target_states(state2,alpha.val_alphabet)         
            for group in partition:  
                trans1_check = any(state in group for state in transitions1_target)
                trans2_check=any(state in group for state in transitions2_target)
                if trans1_check != trans2_check:
                    return True
        return False
    def render(self):
        ...


"""
2.
Créer une fonction qui permet la lecture d’un automate à partir d’une entrée de la forme suivante :
"""


def conversion_iterable(etat):
    returned_value = etat
    if not isinstance(etat, Iterable):
        returned_value = (etat,)
    return tuple(frozenset(returned_value))
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
        aut_src=None
        aut_dest=None  
        for etat in aut_etats :
            label=etat.label_etat
            if not isinstance(etat.label_etat,tuple):
                label = tuple(etat.label_etat)
            aut_src = etat if src == label and not aut_src else aut_src
            aut_dest = etat if dest == label and not aut_dest else aut_dest
            if aut_src is not None and aut_dest is not None:
                break
        aut_alph = next((aut_alph for aut_alph in aut_alphabets if aut_alph.val_alphabet == alph))
        aut_transitions.append(Transition(aut_src,aut_dest , aut_alph))

    #creation de l'automate
    return Automate(aut_alphabets, aut_etats, aut_transitions)    



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

# Création de l'automate
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

# Appliquer la fonction minimiser
automate_minimise_2 = exemple_automate.minimiser()

# Vérification des résultats
print("\nAutomate minimisé:")
print("Alphabets:", automate_minimise_2.return_alpha())
print("États:", automate_minimise_2.return_etat())
print("Transitions:", automate_minimise_2.return_transition())