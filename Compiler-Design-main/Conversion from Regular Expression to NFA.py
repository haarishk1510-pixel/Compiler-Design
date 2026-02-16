class State:
    def __init__(self, label=None):
        self.label = label
        self.edges = {}  # Dictionary mapping character -> list of State objects
        # Note: We use None to represent Epsilon (ε)

    def add_edge(self, char, state):
        if char not in self.edges:
            self.edges[char] = []
        self.edges[char].append(state)

    def __repr__(self):
        return f"State({self.label})"

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end  # The accepting state

# --- Builder Functions (Thompson's Construction) ---

def from_symbol(symbol):
    """Creates NFA for a single character: (start) --symbol--> (end)"""
    start = State()
    end = State()
    start.add_edge(symbol, end)
    return NFA(start, end)

def concat(nfa1, nfa2):
    """Concatenation: connects end of nfa1 to start of nfa2 with ε"""
    # Add ε-transition from nfa1's end to nfa2's start
    nfa1.end.add_edge(None, nfa2.start) 
    return NFA(nfa1.start, nfa2.end)

def union(nfa1, nfa2):
    """Union (|): New start splits to both; both end at new final"""
    start = State()
    end = State()
    
    # Split from new start
    start.add_edge(None, nfa1.start)
    start.add_edge(None, nfa2.start)
    
    # Join to new end
    nfa1.end.add_edge(None, end)
    nfa2.end.add_edge(None, end)
    
    return NFA(start, end)

def star(nfa):
    """Kleene Star (*): Zero or more repetitions"""
    start = State()
    end = State()
    
    # 1. Skip logic (Zero matches): Start -> End
    start.add_edge(None, end)
    
    # 2. Enter logic: Start -> NFA Start
    start.add_edge(None, nfa.start)
    
    # 3. Loop logic: NFA End -> NFA Start
    nfa.end.add_edge(None, nfa.start)
    
    # 4. Exit logic: NFA End -> End
    nfa.end.add_edge(None, end)
    
    return NFA(start, end)

# --- Main Logic ---

def regex_to_nfa(postfix_exp):
    stack = []
    
    for char in postfix_exp:
        if char == '*':
            # Pop 1, apply star, push back
            nfa = stack.pop()
            stack.append(star(nfa))
        elif char == '.': 
            # Concatenation operator (usually explicit in postfix)
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat(nfa1, nfa2))
        elif char == '|':
            # Union operator
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union(nfa1, nfa2))
        else:
            # Operand (character)
            stack.append(from_symbol(char))
            
    return stack.pop()

# --- Helper to Visualize ---

def print_nfa(nfa):
    visited = set()
    
    def traverse(state):
        if state in visited:
            return
        visited.add(state)
        state_id = id(state) % 1000 # Shorten ID for readability
        
        # Check if this is the end state
        label = " (ACCEPT)" if state == nfa.end else ""
        print(f"State {state_id}{label}:")
        
        for char, neighbors in state.edges.items():
            char_label = char if char is not None else "ε"
            for n in neighbors:
                print(f"  --[{char_label}]--> State {id(n) % 1000}")
                traverse(n)

    traverse(nfa.start)

# --- Test ---
# Regex: (a|b)*c
# Postfix: ab|*c. (Note: we use '.' for explicit concatenation)
postfix_regex = "ab|*c." 

print(f"Converting Postfix Regex: {postfix_regex}")
print("-" * 30)
nfa_result = regex_to_nfa(postfix_regex)
print_nfa(nfa_result)