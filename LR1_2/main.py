########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит пример использования ранее реализованных методов для нечёткого прямого вывода
# Дата: 25.09.23
#
########################


from src.fuzzy_implication import FuzzyOutput
from src.fuzzy_set_parser import FuzzySetParser


if __name__ == '__main__':
    fuzzy_sets = FuzzySetParser.parse_read_fuzzy_sets(FuzzySetParser.read_file_for_fuzzy_sets('facts', 'premises'))
    facts = fuzzy_sets['facts']
    premises = fuzzy_sets['premises']
    implication_matrix = FuzzyOutput.make_dataframe(facts['A'], facts['B'])
    print(implication_matrix)
    print(FuzzyOutput.fuzzy_set_dict_to_str(FuzzyOutput.fuzzy_conclusion(premises['C'], implication_matrix)))
