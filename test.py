from graphviz import Digraph

# Define your automaton
automaton = Digraph()
automaton.node('A')  # Add a state named 'A'
automaton.node('B')  # Add a state named 'B'
automaton.edge('A', 'B', label='0')  # Add a transition from 'A' to 'B' labeled '0'

# Render the automaton
automaton.render('automaton', format='png', view=True)