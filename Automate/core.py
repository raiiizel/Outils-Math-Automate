from enum import Enum, auto

""""
1.
Créer une modélisation orientée objet d’un automate et l’enrichir par les méthodes nécessaires :
"""
class TypeEtat(Enum):
    """
    bach ndefiniw les types dial les etats blast mankhdmo b'strings (puisqu'ils sont susceptibles au bugs ou fautes de frappe etc....)
    """
    Initial = auto()
    Intermediaire = auto()
    Terminal = auto()



class Etat:
    def __init__(self, label_etat : str | int, type_etat : TypeEtat = TypeEtat.Intermediaire):
        self.label_etat = label_etat
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
        self.etats_terminaux = [etat for etat in list_etats if etat.type_etat == TypeEtat.Intermediaire]


    def determiniser(self):
        ...

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

def automate(alphabet : list[str], etats : list[str | int], etats_initiaux : list[str | int], etats_finaux : list[str | int], transitions : list[tuple[int, str | int, int]]) -> Automate:
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
        aut_src = next((etat for etat in aut_etats if etat.label_etat == src))
        aut_dest = next((etat for etat in aut_etats if etat.label_etat == dest))
        aut_alph = next((aut_alph for aut_alph in aut_alphabets if aut_alph.val_alphabet == alph))
        aut_transitions.append(Transition(aut_src, aut_alph, aut_dest))

    #creation de l'automate
    return Automate(aut_alphabets, aut_etats, aut_transitions)    


