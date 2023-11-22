from src.backward_conclusion_parser import BackwardConclusionParser


if __name__ == '__main__':
    result = BackwardConclusionParser.parse('program.txt')
    print(result)
