def is_dnf(s):
    # Remove parentheses and split into clauses
    s = s.replace("(", "").replace(")", "")
    clauses = s.split("\\/")

    for clause in clauses:
        # Split each clause into literals
        literals = clause.split("/\\")

        for literal in literals:
            # Check if the literal is a variable or its negation
            if not (literal.isalpha() or
                    (literal.startswith("!") and literal[1:].isalpha())):
                return False
    return True


print(is_dnf('(D\/(A/\(!B))\/(A/\(!C)))'))
