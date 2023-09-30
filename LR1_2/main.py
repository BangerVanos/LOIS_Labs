########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит пример использования ранее реализованных методов для нечёткого прямого вывода
# Дата: 25.09.23
#
########################


from src.fuzzy_implication_system import FuzzyImplicationSystem


if __name__ == '__main__':
    file_name = input('Give path to file: ')
    FuzzyImplicationSystem.print_conclusions_results(file_name)
