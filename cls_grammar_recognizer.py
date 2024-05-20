from boxes import AltLinkBox, ChainLinkBox, LetBox
from stacks import BoxStack, Brackets
from data import DATA
from exceptions import EmptyTokenData, WrongRuleLine


class GrammarRecognizer:
    def __init__(self, token_data: dict = None):
        """
        Recognizes and remembers grammar in extended form of Bekus Naur. Saves the rules using the method
        save_rule_line and checks lines against this grammar using method is_line_right
        :param token_data: if you need to work with already saved tokens
        """
        self.__name_for_new_tokens = -1
        self.__first_token = ''
        if token_data:
            DATA.change_token_data(token_data)

        self.__alphabet = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                           'abcdefghijklmnopqrstuvwxyz'
                           'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
                           'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                           '0123456789')

    def __get_new_token_name(self) -> str:
        self.__name_for_new_tokens += 1
        return f'_{self.__name_for_new_tokens}'

    @staticmethod
    def get_token_data():
        return DATA.get_tokens()

    def save_rule_line(self, line: str):
        """
        Checks the rule for the presence of a valid name, a valid separator (->) of the left and right parts,
        for the valid use of all non-terminal symbols and processes the rule by symbol,
        divides it into tokens and saves it with the right name
        :param line: line of rule
        :return:
        """
        old_token_data = DATA.get_tokens().copy()
        box_stack = BoxStack()
        brackets = Brackets()

        if '->' not in line:
            raise WrongRuleLine('The rule doesn\'t have "->"')

        rule_name, content = line.split('->')

        if ('<' != rule_name.strip()[0]) or ('>' != rule_name.strip()[-1]):
            raise WrongRuleLine('The rule name doesn\'t have "< >" in the right place')

        token_name = f'_{rule_name.strip()[1:-1]}'

        if not self.__first_token:
            self.__first_token = token_name
        clb = ChainLinkBox(token_name)
        box_stack.push(clb)
        DATA.add_token_in(clb)

        ind_let = 0
        while ind_let < len(content):
            match content[ind_let]:
                case '<':
                    ind_start = ind_let + 1
                    if '>' not in content[ind_start:]:
                        raise WrongRuleLine(f'The nonterminal doesn\'t have ">" by index={len(rule_name)+2+ind_let}')

                    while content[ind_let] != '>':
                        ind_let += 1

                    token_name = f'_{content[ind_start: ind_let]}'
                    box_stack.get_last().add_to_content(token_name)

                case '|':
                    lb = box_stack.pop()
                    if len(lb.content) == 0:
                        raise WrongRuleLine(f'The "|" used incorrectly by index={len(rule_name)+2+ind_let}')

                    alb = AltLinkBox(self.__get_new_token_name())
                    alb.name, lb.name = lb.name, alb.name

                    clb = ChainLinkBox(self.__get_new_token_name())

                    alb.add_to_content(lb.name, clb.name)

                    box_stack.push(clb)
                    DATA.add_token_in(lb, alb, clb)

                case '(':
                    brackets.open('(')
                    clb = ChainLinkBox(self.__get_new_token_name())
                    box_stack.get_last().add_to_content(clb.name)

                    box_stack.push(clb)
                    DATA.add_token_in(clb)

                case ')':
                    try:
                        brackets.close(')')
                    except Exception:
                        raise WrongRuleLine(f'")" found without "(" by index={len(rule_name)+2+ind_let}. Remove it')
                    lb = box_stack.pop()
                    if len(lb) == 0:
                        raise WrongRuleLine(f'The "(...)" used incorrectly by index={len(rule_name)+2+ind_let}')

                case '[':
                    brackets.open('[')
                    alb = AltLinkBox(self.__get_new_token_name())
                    box_stack.get_last().add_to_content(alb.name)

                    clb = ChainLinkBox(self.__get_new_token_name())
                    box_stack.push(clb)

                    alb.add_to_content('∅', clb.name)

                    DATA.add_token_in(alb, clb, LetBox('∅'))

                case ']':
                    try:
                        brackets.close(']')
                    except Exception:
                        raise WrongRuleLine(f'"]" found without "[" by index={len(rule_name)+2+ind_let}. Remove it')
                    lb = box_stack.pop()
                    if len(lb) == 0:
                        raise WrongRuleLine(f'The "[...]" used incorrectly by index={len(rule_name)+2+ind_let}')

                case '{':
                    brackets.open('{')
                    alb = AltLinkBox(self.__get_new_token_name())
                    box_stack.get_last().add_to_content(alb.name)

                    clb1 = ChainLinkBox(self.__get_new_token_name())
                    clb2 = ChainLinkBox(self.__get_new_token_name())

                    clb1.add_to_content(clb2.name, alb.name)
                    alb.add_to_content('∅', clb1.name)

                    box_stack.push(alb, clb1, clb2)
                    DATA.add_token_in(LetBox('∅'), alb, clb1, clb2)

                case '}':
                    try:
                        brackets.close('}')
                    except Exception:
                        raise WrongRuleLine('"}" found without "{"'+f' by index={len(rule_name)+2+ind_let}. Remove it')
                    lb = box_stack.pop()
                    if len(lb) == 0:
                        raise WrongRuleLine('The "{...}" used '+f'incorrectly by index={len(rule_name)+2+ind_let}')

                    clb = box_stack.pop()
                    alb = box_stack.pop()
                    if ind_let + 1 < len(content):
                        ind_let += 1
                        if content[ind_let] == '*':
                            clb.name, alb.name = alb.name, clb.name
                            clb.content[-1], alb.content[-1] = alb.name, clb.name

                            DATA.add_token_in(alb, clb)
                        else:
                            ind_let -= 1

                case '-':
                    try:
                        box_stack.get_last().pop()
                        first_let, sec_let = content[ind_let-1], content[ind_let+1]
                        ind_let += 1

                        ind_first, ind_sec = self.__alphabet.index(first_let), self.__alphabet.index(sec_let)
                    except Exception:
                        raise WrongRuleLine(f'The "-" used incorrectly by index={len(rule_name)+2+ind_let-1}')

                    alb = AltLinkBox(self.__get_new_token_name())
                    box_stack.get_last().add_to_content(alb.name)
                    DATA.add_token_in(alb)

                    for letter in self.__alphabet[ind_first: ind_sec+1]:
                        alb.add_to_content(letter)
                        DATA.add_token_in(LetBox(letter))

                case "'":
                    ind_let += 1
                    if "'" not in content[ind_let:]:
                        raise WrongRuleLine(f'" \' " found without other by index={len(rule_name)+2+ind_let-1}. Remove it')

                    while content[ind_let] != "'":
                        letter = content[ind_let]
                        box_stack.get_last().add_to_content(letter)
                        DATA.add_token_in(LetBox(letter))
                        ind_let += 1

                case ' ':
                    pass

                case '>':
                    raise WrongRuleLine(f'">" found without "<" by index={len(rule_name)+2+ind_let}. Remove it')

                case '*':
                    raise WrongRuleLine('"*" found without "{...}" by index=' + f'{len(rule_name)+2+ind_let}. Remove it')

                case letter:
                    box_stack.get_last().add_to_content(letter)
                    DATA.add_token_in(LetBox(letter))

            ind_let += 1

        box_stack.pop()
        if len(box_stack) != 0:
            DATA.change_token_data(old_token_data)
            raise WrongRuleLine(f'Brackets were never closed by index={len(rule_name)+2+ind_let}')

    def is_line_right(self, line: str) -> tuple[bool, int]:
        """
        Checks the line for matches the grammar. Return (True, -1) if it matches,
        otherwise return False and index wrong symbol
        :param line
        :return: bool, int
        """
        if self.__first_token is None:
            raise EmptyTokenData()
        token = DATA.get_tokens()[self.__first_token]

        is_right, lines, min_line = token.is_token_in_line(line)

        if is_right and '' in lines:
            return True, -1
        else:
            index = len(line) - len(min_line)
        return False, index

