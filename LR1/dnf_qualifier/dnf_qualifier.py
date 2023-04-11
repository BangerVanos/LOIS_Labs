########################
#
# Лабораторная работа № 1 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А. и Готиным И.А.
# Файл содержит класс, определяющий, имеет ли строка, содержащая логическую функию, форму ДНФ
# Дата: 27.03.23
#
########################


class IncorrectFormula(Exception):
    pass


class DNFQualifier:
    MACHINERY_SYMBOLS = {'disjunction': '|',
                         'conjunction': '&',
                         'negation': '!'}  # Dictionary with logical operations (machinery ones)

    CONSTANTS = ('1', '0')  # Constants list
    ALLOWED_SYMBOLS = 'ABCDEFGHIJKMNLOPQRSTUVWXYZ0123456789\\/()!'

    @classmethod
    def is_dnf(cls, formula: str) -> bool:
        """Method checks if given formula is in DNF form"""
        formula = cls.__replace_special_syms(formula)
        try:
            initial_check = cls.__check_initial_check(formula)
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        if not initial_check:
            return False
        if cls.__is_atomic(formula) and formula != '0':
            return True
        if formula[0] == '(' and formula[-1] == ')':  # Remove formula's framing parentheses
            formula = formula[1:-1]
        formula = cls.__replace_special_syms(formula)  # Replacing some symbols for easier processing
        terms = cls.__find_terms(formula)  # Finding all terms
        if not terms:  # If there are no terms, input string is not a formula at all
            raise IncorrectFormula('No terms founded. Looks like you have inserted empty parenthesis')
        for term in terms:  # Check whether all of our terms are terms correct for DNF form
            if not cls.__is_primal_conjunction(term):
                return False
        return True

    @classmethod
    def __check_initial_check(cls, formula: str):
        """Initial check for formula"""
        if not formula:
            raise IncorrectFormula("Formula string is empty")
        if not all([sym in cls.ALLOWED_SYMBOLS for sym in formula]):  # Check if all formula's symbols are allowed
            raise IncorrectFormula('Not allowed symbol')
        try:
            if not cls.__only_atomic_negations(formula):
                return False
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        formula_parenthesis = [sym for sym in formula if sym in ('(', ')')]  # Making list of formulas parentheses
        if not cls.__check_parenthesis(formula_parenthesis):  # Check if parentheses order and amount is appropriate
            raise IncorrectFormula('Incorrect placement of parenthesis')
        operator_count = formula.count('!') + formula.count('|') + formula.count('&')
        if not len(formula_parenthesis) == operator_count * 2:
            return False
        try:
            operation_syntax = cls.__check_parenthesis_order(formula)
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        if not operation_syntax:
            return False
        return True

    @staticmethod
    def __check_parenthesis(parenthesis_list: list[str]):
        """Method checks if parenthesis order is correct and whether amount
        of close and open parentheses is the same"""
        parenthesis_stack = []  # Stack method is used
        mapping = {')': '('}
        for parenthesis in parenthesis_list:
            if mapping.get(parenthesis):  # If closing parenthesis is found
                top_element = parenthesis_stack.pop() if parenthesis_stack else '#'  # first element of stack is got
                if mapping[parenthesis] != top_element:  # If stack's top element is not opening parenthesis
                    return False  # the sequence of parentheses is not right
            else:
                parenthesis_stack.append(parenthesis)
        return not parenthesis_stack  # If parentheses stack is not empty, sequence of parentheses is not right

    @classmethod
    def __only_atomic_negations(cls, formula: str):
        while not formula.find('!') == -1:
            negation_index = formula.find('!')
            try:
                negation_subformula = formula[negation_index + 1:formula.find(')', negation_index)]
            except IndexError:
                raise IncorrectFormula('No closing parenthesis')
            if not cls.__is_atomic(negation_subformula):
                return False
            formula = formula.replace(f'!{negation_subformula}', '', 1)
        return True

    @staticmethod
    def __replace_special_syms(formula: str):
        """Replace some operation symbols for better processing"""
        return formula.replace('\\/', '|').replace('/\\', '&')

    @classmethod
    def __find_terms(cls, formula: str):
        """Find all terms in formula"""
        terms = []  # Future term's list
        raw_term = ''
        parenthesis_rank = 0  # Rank of parenthesis
        for sym in formula:  # Check all symbols from formula's string
            # if sym == '(':
            #     parenthesis_rank += 1  # Add one rank if open parenthesis is met
            # elif sym == ')':
            #     parenthesis_rank -= 1  # Remove one rank if open parenthesis is met
            if sym == '|':  # If disjunction symbol and all parentheses are compensated
                terms.append(raw_term)  # New term is appended to terms list
                raw_term = ''
                continue
            raw_term += sym  # Otherwise, symbol is added to forming term
        if raw_term:
            terms.append(raw_term)  # After iterating through all symbols, new term is added to list if not empty
        return terms

    @classmethod
    def __is_primal_conjunction(cls, term: str) -> bool:
        """Method checks if term is primal conjunction."""
        if not term:  # First we check if our term string is empty or not
            raise IncorrectFormula('Empty term. Looks like you placed too many operations')
        if term[0] == '(' and term[-1] == ')':  # Remove term's framing brackets
            term = term[1:-1]
        if cls.MACHINERY_SYMBOLS['conjunction']:
            literals = term.split(cls.MACHINERY_SYMBOLS['conjunction'])  # Split term to find hypothetical literals
        else:
            literals = term.split(cls.MACHINERY_SYMBOLS['disjunction'])
        if not len(literals) in (1, 2):
            return False
        for literal in literals:  # Check all hypothetical literals for being real literals
            if not cls.__is_literal(literal):  # If at least one hypothetical literal is not a real one
                return False  # Term string is not a term
        return True  # If all terms are real one, our term string is real term

    @classmethod
    def __is_literal(cls, literal: str) -> bool:
        """Method checks if given string is literal:
        variable or !variable. Check includes special literal like constants."""
        if not literal:  # If literal string is empty, given formula string is not a formula at all
            raise IncorrectFormula('Unreadable literal. Check your formula for empty parenthesis')
        literal = literal.replace('(', '').replace(')', '')  # Removing all parentheses
        literal = literal.replace(cls.MACHINERY_SYMBOLS['negation'], '', 1)  # Removing negation (only one)
        if not cls.__is_atomic(literal):
            return False
        return True

    @classmethod
    def __is_atomic(cls, atomic: str):
        """Method checks whether string is atomic formula"""
        if not atomic:
            raise IncorrectFormula('Empty atomic formula')
        if atomic in cls.CONSTANTS:  # Sometimes literal can be constant
            return True
        if not atomic[0].isupper():  # Variable's name can only contain upper latin letters with optional index
            return False
        if len(atomic) > 1:  # If variable's name contains index
            if not (atomic[1:].isdigit() and not atomic[1] == '0'):  # Index can only be natural number
                return False
        return True

    @classmethod
    def __check_parenthesis_order(cls, formula: str):
        if formula == '#':
            return True
        deepest_operation_index = cls.__find_index_of_deepest_operation(formula)
        close_parenthesis_index = formula[deepest_operation_index:].find(')')
        if close_parenthesis_index == -1:
            raise IncorrectFormula('No close parenthesis')
        open_parenthesis_index = formula[:deepest_operation_index].rindex('(')
        formula = formula[:open_parenthesis_index] + '#' + formula[close_parenthesis_index + 1:]
        cls.__check_parenthesis_order(formula)

    @classmethod
    def __find_index_of_deepest_operation(cls, formula: str):
        deepest_parenthesis_index = formula.rindex('(')
        for i in range(deepest_parenthesis_index, len(formula)):
            if formula[i] in cls.MACHINERY_SYMBOLS.values():
                return i
        raise IncorrectFormula('Incorrect formula')
