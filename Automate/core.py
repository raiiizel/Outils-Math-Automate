from enum import Enum, auto


class TypeEtat(Enum):
    """
    bach ndefiniw les types dial les etats blast mankhdmo b'strings (puisqu'ils sont susceptibles au bugs ou fautes de frappe etc....)
    """
    Initial = auto()
    Intermediaire = auto()
    Terminal = auto()



class Etat:
    def __init__(self, label_etat : str, type_etat : TypeEtat = TypeEtat.Intermediaire):
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

    def determiniser(self):
        ...

    def completer(self):
        ...

    def minimiser(self):
        ...

    def render(self):
        ...