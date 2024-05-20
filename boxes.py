from data import DATA
from exceptions import UnknownRule


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
        :param args:
        :return:
        """
        for link in args:
            self.content.append(link)

    def is_token_in_line(self, line: str) -> tuple[bool, list[str], str]:
        """
        If each token is present in the required order in the string, return True, list of lines without tokens and
        min_line
        :param line: str
        :return: bool, list[str], str
        """
        min_line = line
        results = [line]
        for token_link in self.content:
            try:
                token = DATA.get_tokens()[token_link]
            except KeyError:
                raise UnknownRule(token_link)

            new_results = []
            for one_line in results:
                result = token.is_token_in_line(one_line)
                min_line = min(min_line, result[2], key=len)
                if result[0]:
                    new_results += result[1]

            if len(new_results) != 0:
                results = new_results.copy()
            else:
                return False, [line], min_line
        return True, results, min_line

    def pop(self) -> str:
        return self.content.pop()

    def __len__(self) -> int:
        return len(self.content)

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
        min_line = line
        results = []
        for token_link in self.content:
            try:
                token = DATA.get_tokens()[token_link]
            except KeyError:
                raise UnknownRule(token_link)

            result = token.is_token_in_line(line)
            min_line = min(min_line, result[2], key=len)
            if result[0]:
                results += result[1]

        if len(results) != 0:
            return True, results, min_line
        else:
            return False, [line], min_line

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
        if self.content[0] in ['∅', 'Ø']:
            return True, [line], line
        elif len(line) > 0:
            if self.content[0] != ' ':
                line = line.strip()
            if line[0] == self.content[0]:
                return True, [line[1:]], line[1:]

        return False, [line], line

    def __repr__(self) -> str:
        return f'LetBox("{self.content[0]}")'
