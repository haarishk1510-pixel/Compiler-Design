def demonstrate_ambiguity_elimination():
    print("\n--- Elimination of Ambiguity (Demonstration) ---")
    
    # 1. Ambiguous Grammar (Standard Arithmetic)
    # E -> E + E | E * E | (E) | id
    ambiguous_grammar = {
        'E': ['E+E', 'E*E', '(E)', 'id']
    }
    
    print(f"Original Ambiguous Grammar:\n  {ambiguous_grammar}")
    print("\n[!] Applying Precedence Rules (Manual Rewrite)...")
    print("    1. * has higher precedence than +")
    print("    2. Operators are left-associative")
    
    # 2. Unambiguous Grammar (Stratified)
    # E -> E + T | T
    # T -> T * F | F
    # F -> (E) | id
    unambiguous_grammar = {
        'E': ['E+T', 'T'],      # Lowest precedence (+)
        'T': ['T*F', 'F'],      # Higher precedence (*)
        'F': ['(E)', 'id']      # Highest precedence (parens/atoms)
    }
    
    print(f"\nResulting Unambiguous Grammar:\n  {unambiguous_grammar}")
    return unambiguous_grammar

# --- Add this to the main execution block of Exp 4 ---
if __name__ == "__main__":
    # ... (Previous Exp 4 code) ...
    
    # Run Ambiguity Demo
    demonstrate_ambiguity_elimination()