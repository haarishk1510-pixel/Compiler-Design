import sys

# --- Helper Functions ---

def is_terminal(symbol):
    """Checks if a symbol is a terminal (uppercase = Non-Terminal, else Terminal)"""
    return not symbol.isupper()

def compute_first(grammar):
    first = {nt: set() for nt in grammar}
    
    def get_first(symbol):
        # 1. If terminal, FIRST(X) = {X}
        if is_terminal(symbol):
            return {symbol}
        
        # 2. If non-terminal, calculate recursively
        if symbol in first and first[symbol]:
            return first[symbol]
            
        result = set()
        for production in grammar[symbol]:
            # Case 3: X -> # (epsilon)
            if production == '#':
                result.add('#')
                continue
            
            # Case 4: X -> Y1 Y2 ... Yk
            for char in production:
                char_first = get_first(char)
                result.update(char_first - {'#'})
                
                if '#' not in char_first:
                    break
            else:
                # If we didn't break, all symbols derive epsilon
                result.add('#')
                
        first[symbol] = result
        return result

    # Compute for all Non-Terminals
    for nt in grammar:
        get_first(nt)
        
    return first

def compute_follow(grammar, first):
    follow = {nt: set() for nt in grammar}
    start_symbol = list(grammar.keys())[0]
    
    # Rule 1: FOLLOW(Start) = {$}
    follow[start_symbol].add('$')
    
    # Iterate until sets stabilize (Fixed-Point Iteration)
    while True:
        updated = False
        
        for nt, productions in grammar.items():
            for production in productions:
                # Scan production A -> alpha B beta
                for i, symbol in enumerate(production):
                    if is_terminal(symbol) or symbol == '#':
                        continue
                    
                    # We found a Non-Terminal 'B' at index i
                    # Look at what follows it (beta)
                    
                    # 1. Calculate FIRST(beta)
                    trailer = follow[nt].copy() # Default if beta is empty/null
                    
                    if i + 1 < len(production):
                        beta = production[i+1:]
                        # Compute FIRST(beta)
                        first_beta = set()
                        all_nullable = True
                        
                        for b_char in beta:
                            f = first.get(b_char, {b_char})
                            first_beta.update(f - {'#'})
                            if '#' not in f:
                                all_nullable = False
                                break
                        
                        # Rule 2: FOLLOW(B) includes FIRST(beta) - {epsilon}
                        if not follow[symbol].issuperset(first_beta):
                            follow[symbol].update(first_beta)
                            updated = True
                            
                        if all_nullable:
                            # Rule 3: If beta is nullable, FOLLOW(B) includes FOLLOW(A)
                            if not follow[symbol].issuperset(follow[nt]):
                                follow[symbol].update(follow[nt])
                                updated = True
                    else:
                        # Rule 3: A -> alpha B (beta is empty)
                        # FOLLOW(B) includes FOLLOW(A)
                        if not follow[symbol].issuperset(follow[nt]):
                            follow[symbol].update(follow[nt])
                            updated = True
                            
        if not updated:
            break
            
    return follow

# --- Main Execution ---

if __name__ == "__main__":
    # Grammar Input
    # E  -> T R
    # R  -> + T R | #
    # T  -> F Y
    # Y  -> * F Y | #
    # F  -> ( E ) | id
    
    # Note: Use single characters for Non-Terminals for simplicity
    # Use '#' for Epsilon
    grammar = {
        'E': ['TR'],
        'R': ['+TR', '#'],
        'T': ['FY'],
        'Y': ['*FY', '#'],
        'F': ['(E)', 'i'] # 'i' stands for id
    }

    print("Grammar:")
    for nt, rules in grammar.items():
        print(f"  {nt} -> {' | '.join(rules)}")
    print("-" * 30)

    # 1. Compute FIRST
    first_sets = compute_first(grammar)
    print(f"{'Non-Terminal':<15} {'FIRST Set'}")
    for nt, fset in first_sets.items():
        print(f"{nt:<15} {fset}")
    print("-" * 30)

    # 2. Compute FOLLOW
    follow_sets = compute_follow(grammar, first_sets)
    print(f"{'Non-Terminal':<15} {'FOLLOW Set'}")
    for nt, fset in follow_sets.items():
        print(f"{nt:<15} {fset}")