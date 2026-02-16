# Import the State, NFA classes and nfa_result from the Regular Expression to NFA file
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
regex_nfa_module = import_module('Conversion from Regular Expression to NFA')
State = regex_nfa_module.State
NFA = regex_nfa_module.NFA
nfa_result = regex_nfa_module.nfa_result
regex_to_nfa = regex_nfa_module.regex_to_nfa

def get_epsilon_closure(nfa_states):
    """
    Finds all states reachable from a set of states using only ε-transitions.
    """
    stack = list(nfa_states)
    closure = set(nfa_states)
    
    while stack:
        state = stack.pop()
        # In our NFA implementation, None represents Epsilon
        if None in state.edges:
            for next_state in state.edges[None]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return frozenset(closure)

def move(nfa_states, symbol):
    """
    Finds all states reachable from a set of states by consuming 'symbol'.
    """
    reachable = set()
    for state in nfa_states:
        if symbol in state.edges:
            for next_state in state.edges[symbol]:
                reachable.add(next_state)
    return reachable

def nfa_to_dfa(nfa, alphabet):
    """
    Converts an NFA to a DFA using Subset Construction.
    Returns: 
      - dfa_transitions: dict { dfa_state_id : { char: next_dfa_state_id } }
      - dfa_start_state: ID of the start state
      - dfa_accept_states: Set of IDs of accept states
    """
    # 1. Start State = Epsilon Closure of NFA start
    start_closure = get_epsilon_closure({nfa.start})
    
    # We need to map these sets of NFA states to simple IDs (0, 1, 2...)
    states_map = {start_closure: 0} # { frozenset(nfa_states) : dfa_id }
    unmarked_states = [start_closure] # Queue of states to process
    
    dfa_transitions = {} # { 0: {'a': 1, 'b': 2}, ... }
    dfa_accept_states = set()
    
    state_counter = 0

    while unmarked_states:
        # Get current DFA state (which is a set of NFA states)
        current_nfa_set = unmarked_states.pop()
        current_id = states_map[current_nfa_set]
        
        # Check if this DFA state is an accepting state
        # (It is accepting if ANY of its NFA states is the NFA end state)
        if nfa.end in current_nfa_set:
            dfa_accept_states.add(current_id)
        
        dfa_transitions[current_id] = {}
        
        for symbol in alphabet:
            # 2. Calculate Move(S, symbol)
            moved_states = move(current_nfa_set, symbol)
            
            if not moved_states:
                continue
                
            # 3. Calculate Epsilon Closure of the result
            closure = get_epsilon_closure(moved_states)
            
            # 4. Check if we've seen this new state before
            if closure not in states_map:
                state_counter += 1
                states_map[closure] = state_counter
                unmarked_states.append(closure)
            
            # Record transition
            target_id = states_map[closure]
            dfa_transitions[current_id][symbol] = target_id

    return dfa_transitions, 0, dfa_accept_states

# --- Testing the Conversion ---

# Option A: Use the imported nfa_result from the regex file
# Option B: Create a new NFA here if the import fails
try:
    # Try to use the imported nfa_result
    test_nfa = nfa_result
    print("Using NFA from 'Conversion from Regular Expression to NFA.py'")
except NameError:
    # If nfa_result is not available, create a new one
    print("Creating a new NFA for testing: (a|b)*c")
    postfix_regex = "ab|*c."
    test_nfa = regex_to_nfa(postfix_regex)

# Define the alphabet used in the regex
alphabet = ['a', 'b', 'c']

print("\nConverting NFA to DFA...")
print("-" * 30)

transitions, start_id, accept_ids = nfa_to_dfa(test_nfa, alphabet)

print(f"Start State: {start_id}")
print(f"Accept States: {accept_ids}")
print("Transitions:")
for state_id, trans in transitions.items():
    state_label = " (ACCEPT)" if state_id in accept_ids else ""
    print(f"  State {state_id}{state_label}:")
    for char, next_id in trans.items():
        print(f"    --[{char}]--> State {next_id}")