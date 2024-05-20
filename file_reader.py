import os
from cls_grammar_recognizer import GrammarRecognizer


class Reader:
    def __init__(self, directory: str) -> None:
        self.__directory = directory

    @staticmethod
    def run_tests(file_name: str, grammar: list[str], correct: list[str], wrong: list[str]):
        GR = GrammarRecognizer()

        is_rules_valid = True
        for rule_line in grammar:
            if rule_line != '':
                try:
                    GR.save_rule_line(rule_line)
                except Exception as ex:
                    is_rules_valid = False
                    print(f'{file_name}: {rule_line}')
                    print(f'{ex}\n')

        if is_rules_valid:
            nocorrect = []
            nowrong = []
            no_right_index = []

            for line in correct:
                if line != '':
                    is_right, index = GR.is_line_right(line)
                    if not is_right:
                        nocorrect.append((line, index))

            for line in wrong:
                if line != '':
                    line, old_index = line.split(', ')
                    is_right, index = GR.is_line_right(line)
                    if is_right:
                        nowrong.append(line)

                    if int(old_index) != index:
                        no_right_index.append((line, old_index, index))

            if len(nocorrect) == 0:
                print(f'{file_name}: all correct tests is complete successful')
            else:
                for i in nocorrect:
                    print(f'{file_name}: correct test is wrong: {i[0]}, {i[1]}')

            print()

            if len(nowrong) == 0 and len(no_right_index) == 0:
                print(f'{file_name}: all wrong tests is complete successful')
            else:
                for i in nowrong:
                    print(f'{file_name}: wrong test is correct: {i}')
                for i in no_right_index:
                    print(f'{file_name}: wrong test indexes isn\'t equal: {i[0]}, old_index={i[1]}, index={i[2]}')

            print()

    def read_files(self):
        for file_name in os.listdir(self.__directory):
            if file_name != 'EXAMPLE.txt':
                with (open(f'{self.__directory}/{file_name}', 'r', encoding='utf-8') as f):
                    f = f.read()

                    gr_first, gr_sec = len('Grammar:\n'), f.index('correct:')
                    crr_first, crr_sec = gr_sec + 8, f.index('wrong:')
                    wr_first = crr_sec + 6

                    grammar = f[gr_first: gr_sec].split('\n')
                    correct = f[crr_first: crr_sec].split('\n')
                    wrong = f[wr_first:].split('\n')

                    self.run_tests(
                        file_name=file_name,
                        grammar=grammar,
                        correct=correct,
                        wrong=wrong
                    )


def main():
    Reader('./tests').read_files()


if __name__ == '__main__':
    main()
