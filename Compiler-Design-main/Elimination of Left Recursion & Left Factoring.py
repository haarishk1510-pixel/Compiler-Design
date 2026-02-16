# --- Left Recursion Elimination ---
def remove_left_recursion(grammar):
    print("\n--- Removing Left Recursion ---")
    new_grammar = {}
    
    for nt, prods in grammar.items():
        recursive = []
        non_recursive = []
        
        for p in prods:
            if p.startswith(nt): recursive.append(p[len(nt):])
            else: non_recursive.append(p)
            
        if not recursive:
            new_grammar[nt] = prods
            continue
            
        print(f"Recursion found in {nt}")
        new_nt = nt + "'"
        
        # Rule 1: A -> beta A'
        new_grammar[nt] = [beta + new_nt for beta in non_recursive]
        # Rule 2: A' -> alpha A' | ε
        new_grammar[new_nt] = [alpha + new_nt for alpha in recursive] + ['ε']
        
    return new_grammar

# --- Left Factoring ---
def left_factor(grammar):
    print("\n--- Left Factoring ---")
    new_grammar = grammar.copy()
    
    for nt in list(new_grammar.keys()):
        prods = new_grammar[nt]
        prods.sort()
        
        # Check first two productions for common prefix
        if len(prods) < 2: continue
        
        # Find Longest Common Prefix (LCP)
        p1, p2 = prods[0], prods[1]
        i = 0
        while i < len(p1) and i < len(p2) and p1[i] == p2[i]:
            i += 1
        prefix = p1[:i]
        
        if prefix:
            print(f"Factoring {nt} with prefix '{prefix}'")
            new_nt = nt + "'"
            suffixes = []
            retained = []
            
            for p in prods:
                if p.startswith(prefix):
                    suffix = p[len(prefix):]
                    suffixes.append(suffix if suffix else 'ε')
                else:
                    retained.append(p)
            
            new_grammar[nt] = [prefix + new_nt] + retained
            new_grammar[new_nt] = suffixes
            
    return new_grammar

# --- Main Execution ---
if __name__ == "__main__":
    # Grammar with Left Recursion: E -> E+T | T
    # Grammar with Left Factors: S -> iEtS | iEtSeS | a
    
    grammar = {
        'E': ['E+T', 'T'],
        'S': ['iEtS', 'iEtSeS', 'a']
    }
    
    print("Original Grammar:", grammar)
    
    # 1. Remove Recursion
    g_no_rec = remove_left_recursion(grammar)
    print("After Recursion Removal:", g_no_rec)
    
    # 2. Left Factor
    g_final = left_factor(g_no_rec)
    print("Final Grammar:", g_final)