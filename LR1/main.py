########################
#
# Лабораторная работа № 1 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А. и Готиным И.А.
# Файл содержит тест для класса DNFQualifier
# Дата: 27.03.23
#
########################


from dnf_qualifier.dnf_qualifier import DNFQualifier, IncorrectFormula


if __name__ == '__main__':
    try:
        formula = r'((X1 & X3) | (X3 & (X1 & (!X2))))'
        print(f'{formula} : {DNFQualifier.is_dnf(formula)}')
    except IncorrectFormula as err:
        print(f'Error: {err}')
