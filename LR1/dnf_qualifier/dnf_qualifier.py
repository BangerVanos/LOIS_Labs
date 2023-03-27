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
    LOGICAL_OPERATIONS = {'disjunction': '|',
                          'conjunction': '&',
                          'negation': '!'}

    SPECIAL_CASES = ['1', 'T', '⊤']

    @classmethod
    def is_dnf(cls, formula: str) -> bool:
        if formula in cls.SPECIAL_CASES:
            return True
        formula_parenthesis = [sym for sym in formula if sym in ('(', ')')]
        if not cls.__check_parenthesis(formula_parenthesis):
            raise IncorrectFormula('Incorrect placement of parenthesis')
        if formula[0] == '(' and formula[-1] == ')':
            formula = formula[1:-1]
        formula = cls.__replace_special_syms(formula)
        terms = cls.__find_terms(formula)
        if not terms:
            raise IncorrectFormula('No terms founded. Looks like you have inserted empty parenthesis')
        for term in terms:
            if not cls.__is_primal_conjunction(term):
                return False
        return True

    @staticmethod
    def __check_parenthesis(parenthesis_list: list[str]):
        parenthesis_stack = []
        mapping = {')': '('}
        for parenthesis in parenthesis_list:
            if mapping.get(parenthesis):
                top_element = parenthesis_stack.pop() if parenthesis_stack else '#'
                if mapping[parenthesis] != top_element:
                    return False
            else:
                parenthesis_stack.append(parenthesis)
        return not parenthesis_stack

    @staticmethod
    def __replace_special_syms(formula: str):
        return formula.replace('\\/', '|').replace('/\\', '&').replace('¬', '!').replace(' ', '')

    @classmethod
    def __find_terms(cls, formula: str):
        terms = []
        raw_term = ''
        parenthesis_rank = 0
        for sym in formula:
            if sym == '(':
                parenthesis_rank += 1
            elif sym == ')':
                parenthesis_rank -= 1
            elif sym == '|' and parenthesis_rank == 0:
                terms.append(raw_term)
                raw_term = ''
                continue
            raw_term += sym
        if raw_term:
            terms.append(raw_term)
        return terms

    @classmethod
    def __is_primal_conjunction(cls, term: str) -> bool:
        if not term:
            raise IncorrectFormula('Empty term. Looks like you placed too many operations')
        if term[0] == '(' and term[-1] == ')':
            term = term[1:-1]
        if '!(' in term:
            return False
        literals = term.split(cls.LOGICAL_OPERATIONS['conjunction'])
        for literal in literals:
            if not cls.__is_literal(literal):
                return False
        return True

    @classmethod
    def __is_literal(cls, literal: str) -> bool:
        if not literal:
            raise IncorrectFormula('Unreadable literal. Check your formula for empty parenthesis')
        if literal in ('.L', 'T', '1', '0', '⊤', '⊥'):
            return True
        literal = literal.replace('(', '').replace(')', '')
        literal = literal.replace(cls.LOGICAL_OPERATIONS['negation'], '', 1)
        if not literal[0].isupper():
            return False
        if len(literal) > 1:
            if not (literal[1:].isdigit() and not literal[1] == '0'):
                return False
        return True
