# --- Grammar Definition ---
# format: (LHS, RHS)
# Note: Order matters for conflict resolution in this simple parser!
# We put longer rules first to prefer "longest match" (greedy reduction).
GRAMMAR = [
    ("E", "E+E"),
    ("E", "E*E"),
    ("E", "(E)"),
    ("E", "id")
]

def shift_reduce_parser(input_string):
    # 1. Initialization
    stack = ""
    input_buffer = input_string
    step = 1
    
    print(f"{'Step':<5} {'Stack':<15} {'Input':<15} {'Action'}")
    print("-" * 50)
    
    while True:
        # Check if we reached the goal (Stack = Start Symbol 'E' and Input is empty)
        if stack == "E" and input_buffer == "":
            print(f"{step:<5} {stack:<15} {input_buffer:<15} ACCEPT")
            break
            
        # --- Reduction Phase ---
        # Try to match the top of the stack with a RHS from the grammar
        reduced = False
        for lhs, rhs in GRAMMAR:
            # Check if stack ends with this RHS
            if stack.endswith(rhs):
                # Found a handle! Reduce it.
                
                # Special Case: Don't reduce 'id' to 'E' immediately if we just shifted it?
                # Actually, in simple Shift-Reduce, we reduce whenever possible.
                
                # However, to handle precedence (e.g. id+id*id), a simple parser
                # without lookahead will struggle. 
                # For this lab, we use a standard "reduce if handle found" logic.
                
                # Perform reduction: remove RHS, add LHS
                stack = stack[:-len(rhs)] + lhs
                print(f"{step:<5} {stack:<15} {input_buffer:<15} Reduce {lhs}->{rhs}")
                step += 1
                reduced = True
                break # Restart loop to check for further reductions
        
        if reduced:
            continue

        # --- Shift Phase ---
        # If no reduction was possible, try to shift
        if input_buffer:
            # Shift the next character (or token)
            # Here we assume 'id' is 2 chars, others are 1 char.
            
            if input_buffer.startswith("id"):
                token = "id"
                input_buffer = input_buffer[2:]
            else:
                token = input_buffer[0]
                input_buffer = input_buffer[1:]
                
            stack += token
            print(f"{step:<5} {stack:<15} {input_buffer:<15} Shift")
            step += 1
        else:
            # No input left and no reductions possible -> Error
            print(f"{step:<5} {stack:<15} {input_buffer:<15} REJECT (Error)")
            break

# --- Main Execution ---
if __name__ == "__main__":
    # Input string to parse
    # Try: id+id*id
    user_input = "id+id*id"
    
    print(f"Grammar:\n  E -> E+E\n  E -> E*E\n  E -> (E)\n  E -> id\n")
    print(f"Parsing Input: {user_input}\n")
    
    shift_reduce_parser(user_input)