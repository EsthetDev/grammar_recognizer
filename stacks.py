from types_ import AltLinkBox, ChainLinkBox


class BoxStack:
    def __init__(self):
        """
        Stack of ChainLinkBox  or AltLinkBox.
        """
        self.container: list[AltLinkBox | ChainLinkBox] = []

    def push(self, *args: AltLinkBox | ChainLinkBox) -> None:
        for lb in args:
            self.container.append(lb)

    def get_last(self) -> AltLinkBox | ChainLinkBox | None:
        if len(self.container) >= 1:
            return self.container[-1]
        return None

    def pop(self) -> AltLinkBox | ChainLinkBox | None:
        return self.container.pop()

    def __len__(self) -> int:
        return len(self.container)

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
        self.container.append(bracket)

    def close(self, bracket: str) -> None:
        """
        pop the bracket from the stack. If the last bracket is different, raise Exception
        :param bracket: ')', ']', '}'
        """
        brackets = self.container[-1] + bracket
        if brackets in ['()', '[]', '{}']:
            self.container.pop()
        else:
            raise Exception('Wrong bracket')

    def __repr__(self) -> str:
        return f'Brackets({self.container})'
