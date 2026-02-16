from collections import defaultdict

# --- 1. Define the Grammar ---
# Rules: 
# - Uppercase for Non-Terminals
# - Lowercase/Symbols for Terminals
# - '#' represents Epsilon (ε)

grammar = {
    'E': ['TR'],
    'R': ['+TR', '#'],
    'T': ['FY'],
    'Y': ['*FY', '#'],
    'F': ['(E)', 'i']  # 'i' represents 'id'
}

# --- 2. Helper Functions (FIRST & FOLLOW) ---

def compute_first(grammar):
    first = defaultdict(set)
    
    def get_first(symbol):
        # If terminal, FIRST is the symbol itself
        if not symbol.isupper():
            return {symbol}
        
        # If already computed, return it
        if symbol in first and first[symbol]:
            return first[symbol]
            
        for production in grammar[symbol]:
            if production == '#':
                first[symbol].add('#')
                continue
                
            # Iterate through symbols in the production
            for char in production:
                char_first = get_first(char)
                # Add everything except epsilon
                first[symbol].update(char_first - {'#'})
                
                # If this symbol doesn't produce epsilon, stop
                if '#' not in char_first:
                    break
            else:
                # If loop completed (all symbols nullable), add epsilon
                first[symbol].add('#')
                
        return first[symbol]

    for nt in grammar:
        get_first(nt)
    return first

def compute_follow(grammar, first):
    follow = defaultdict(set)
    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add('$') # Rule 1
    
    while True:
        updated = False
        for nt, productions in grammar.items():
            for production in productions:
                # Scan: A -> alpha B beta
                for i, symbol in enumerate(production):
                    if not symbol.isupper(): continue
                    
                    # Everything after current symbol is 'beta'
                    beta = production[i+1:]
                    
                    # Calculate FIRST(beta)
                    trailer = follow[nt].copy()
                    
                    if beta:
                        first_beta = set()
                        all_nullable = True
                        for b_char in beta:
                            f = first[b_char] if b_char.isupper() else {b_char}
                            first_beta.update(f - {'#'})
                            if '#' not in f:
                                all_nullable = False
                                break
                        
                        # Rule 2: FOLLOW(B) += FIRST(beta) - {ε}
                        if not follow[symbol].issuperset(first_beta):
                            follow[symbol].update(first_beta)
                            updated = True
                        
                        # Rule 3: If beta is nullable, FOLLOW(B) += FOLLOW(A)
                        if all_nullable:
                            if not follow[symbol].issuperset(trailer):
                                follow[symbol].update(trailer)
                                updated = True
                    else:
                        # Rule 3: A -> alpha B (beta is empty)
                        if not follow[symbol].issuperset(trailer):
                            follow[symbol].update(trailer)
                            updated = True
        if not updated: break
    return follow

# --- 3. Main Logic: Construct Table ---

def build_parsing_table(grammar, first, follow):
    # Table structure: { NonTerminal: { Terminal: Production } }
    table = defaultdict(dict)
    
    for nt, productions in grammar.items():
        for production in productions:
            # Calculate FIRST(alpha) for this specific production
            first_alpha = set()
            if production == '#':
                first_alpha.add('#')
            else:
                # simplified FIRST logic for a string
                for char in production:
                    f = first[char] if char.isupper() else {char}
                    first_alpha.update(f - {'#'})
                    if '#' not in f: break
                else:
                    first_alpha.add('#')
            
            # Rule 1: For each terminal 'a' in FIRST(alpha), add A->alpha to Table
            for term in first_alpha:
                if term != '#':
                    table[nt][term] = production
            
            # Rule 2: If ε in FIRST(alpha), add A->alpha to Table for each 'b' in FOLLOW(A)
            if '#' in first_alpha:
                for term in follow[nt]:
                    table[nt][term] = production

    return table

# --- 4. Display ---

def print_table(table):
    # Get all terminals
    terminals = set()
    for row in table.values():
        terminals.update(row.keys())
    terminals = sorted(list(terminals))
    
    print("\n" + "="*60)
    print(f"{'PREDICTIVE PARSING TABLE':^60}")
    print("="*60)
    
    # Print Header
    print(f"{'NT':<5} | ", end="")
    for t in terminals:
        print(f"{t:<10}", end="")
    print("\n" + "-"*60)
    
    # Print Rows
    for nt, row in table.items():
        print(f"{nt:<5} | ", end="")
        for t in terminals:
            prod = row.get(t, "")
            cell = f"{nt}->{prod}" if prod else ""
            print(f"{cell:<10}", end="")
        print()

# --- Execution ---
if __name__ == "__main__":
    # Compute prerequisites
    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, first_sets)
    
    # Build Table
    parsing_table = build_parsing_table(grammar, first_sets, follow_sets)
    
    # Output
    print_table(parsing_table)