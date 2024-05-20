class ChainLinkBox:
    def __init__(self, name: str) -> None:
        """
        Stores links in str to other boxes. Checks the line for a tokens in order.
        :param name:
        """
        self.name: str = name
        self.content: list[str] = []

    def add_to_content(self, *args: str) -> None:
        """
        add to content all links.
        :param args: str
        :return:
        """
        pass

    def is_token_in_line(self, line: str) -> tuple[bool, list[str], str]:
        """
        If each token is present in the required order in the string, return True, list of lines without tokens and
        min_line
        :param line: str
        :return: bool, list[str], str
        """
        pass

    def pop(self) -> str:
        pass

    def __len__(self) -> int:
        pass

    def __repr__(self) -> str:
        return f'CLB({self.name}, {self.content})'


class AltLinkBox(ChainLinkBox):
    def __init__(self, name: str):
        """
        Stores links in str to other boxes. Checks the line for a tokens for each token in the content.
        :param name:
        """
        super().__init__(name)

    def is_token_in_line(self, line: str):
        """
        If at least one of the tokens in the line, return True, a list of lines that don't contain these tokens and min_line
        :param line:
        :return: bool, list[str]
        """
        pass

    def __repr__(self) -> str:
        return f'ALB({self.name}, {self.content})'


class LetBox:
    def __init__(self, letter: str) -> None:
        """
        Contains a symbol. Checks line for this symbol.
        :param letter:
        """
        self.name: str = letter
        self.content: list[str] = [letter]

    def is_token_in_line(self, line: str) -> tuple[bool, list, str]:
        """
        Ignores spaces unless checked. Checks the first symbol in the line for equals and if equals returns
        True, line without this symbol at the beginning and other line for min_line
        :param line:
        :return: bool, list[str], str
        """
        pass

    def __repr__(self) -> str:
        return f'LetBox("{self.content[0]}")'


class DATA:
    """
    Stores a dict where the keys are the names of the boxes and objects of the boxes
    """
    __token_data: dict[str, AltLinkBox | ChainLinkBox | LetBox] = dict()

    @classmethod
    def change_token_data(cls, token_data: dict[str, AltLinkBox | ChainLinkBox | LetBox]) -> None:
        pass

    @classmethod
    def add_token_in(cls, *args: AltLinkBox | ChainLinkBox | LetBox) -> None:
        pass

    @classmethod
    def get_tokens(cls) -> dict[str, AltLinkBox | ChainLinkBox | LetBox]:
        pass

    @classmethod
    def __repr__(cls) -> str:
        return f'DATA({cls.__token_data})'


class BoxStack:
    def __init__(self):
        """
        Stack of ChainLinkBox  or AltLinkBox.
        """
        self.container: list[AltLinkBox | ChainLinkBox] = []

    def push(self, *args: AltLinkBox | ChainLinkBox) -> None:
        pass

    def get_last(self) -> AltLinkBox | ChainLinkBox | None:
        pass

    def pop(self) -> AltLinkBox | ChainLinkBox | None:
        pass

    def __len__(self) -> int:
        pass

    def __repr__(self) -> str:
        return f'BoxStack({self.container})'


class Brackets:
    def __init__(self):
        """
        stack of brackets
        """
        self.container: list[str] = []

    def open(self, bracket: str) -> None:
        """
        writes the bracket in the stack
        :param bracket: '(', '[', '{'
        """
        pass

    def close(self, bracket: str) -> None:
        """
        pop the bracket from the stack. If the last bracket is different, raise Exception
        :param bracket: ')', ']', '}'
        """
        pass

    def __repr__(self) -> str:
        return f'Brackets({self.container})'


class GrammarRecognizer:
    def __init__(self, token_data: dict = None) -> None:
        """
        Recognizes and remembers grammar in extended form of Bekus Naur. Saves the rules using the method
        save_rule_line and checks lines against this grammar using method is_line_right
        :param token_data: if you need to work with already saved tokens
        """
        self.__name_for_new_tokens = -1
        self.__first_token = ''
        self.__alphabet = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                           'abcdefghijklmnopqrstuvwxyz'
                           'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
                           'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                           '0123456789')

    def __get_new_token_name(self) -> str:
        pass

    @staticmethod
    def get_token_data() -> dict[str, AltLinkBox | ChainLinkBox | LetBox]:
        pass

    def save_rule_line(self, line: str) -> None:
        """
        Checks the rule for the presence of a valid name, a valid separator (->) of the left and right parts,
        for the valid use of all non-terminal symbols and processes the rule by symbol,
        divides it into tokens and saves it with the right name
        :param line: line of rule
        """
        pass

    def is_line_right(self, line: str) -> tuple[bool, int]:
        """
        Checks the line for matches the grammar. Return (True, -1) if it matches,
        otherwise return False and index wrong symbol
        :param line
        :return: bool, int
        """
        pass
