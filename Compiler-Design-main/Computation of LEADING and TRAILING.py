from collections import defaultdict

# --- 1. Define Grammar ---
# Operator Precedence Grammar (No epsilon, no adjacent non-terminals)
grammar = {
    'E': ['E+T', 'T'],
    'T': ['T*F', 'F'],
    'F': ['(E)', 'i']
}

# --- 2. Logic for LEADING Sets ---
def compute_leading(grammar):
    leading = defaultdict(set)
    
    # Iterate until sets stabilize (Fixed-Point Algorithm)
    while True:
        updated = False
        
        for nt, prods in grammar.items():
            for prod in prods:
                # Rule 1: A -> a... (Terminal at start)
                if not prod[0].isupper():
                    if prod[0] not in leading[nt]:
                        leading[nt].add(prod[0])
                        updated = True
                else:
                    # Rule 2: A -> B... (Non-Terminal at start)
                    # Add LEADING(B) to LEADING(A)
                    B = prod[0]
                    if not leading[nt].issuperset(leading[B]):
                        leading[nt].update(leading[B])
                        updated = True
                    
                    # Rule 3: A -> B a... (Terminal after first NT)
                    if len(prod) > 1 and not prod[1].isupper():
                        if prod[1] not in leading[nt]:
                            leading[nt].add(prod[1])
                            updated = True
                            
        if not updated:
            break
            
    return leading

# --- 3. Logic for TRAILING Sets ---
def compute_trailing(grammar):
    trailing = defaultdict(set)
    
    while True:
        updated = False
        
        for nt, prods in grammar.items():
            for prod in prods:
                # Rule 1: A -> ...a (Terminal at end)
                if not prod[-1].isupper():
                    if prod[-1] not in trailing[nt]:
                        trailing[nt].add(prod[-1])
                        updated = True
                else:
                    # Rule 2: A -> ...B (Non-Terminal at end)
                    # Add TRAILING(B) to TRAILING(A)
                    B = prod[-1]
                    if not trailing[nt].issuperset(trailing[B]):
                        trailing[nt].update(trailing[B])
                        updated = True
                        
                    # Rule 3: A -> ...a B (Terminal before last NT)
                    if len(prod) > 1 and not prod[-2].isupper():
                        if prod[-2] not in trailing[nt]:
                            trailing[nt].add(prod[-2])
                            updated = True

        if not updated:
            break
            
    return trailing

# --- 4. Main Execution ---
if __name__ == "__main__":
    print(f"Grammar: {grammar}\n")
    
    # Compute
    leading_sets = compute_leading(grammar)
    trailing_sets = compute_trailing(grammar)
    
    # Display Results
    print(f"{'Non-Terminal':<15} {'LEADING Set':<20} {'TRAILING Set'}")
    print("-" * 60)
    
    for nt in grammar.keys():
        l_set = str(leading_sets[nt])
        t_set = str(trailing_sets[nt])
        print(f"{nt:<15} {l_set:<20} {t_set}")