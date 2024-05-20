class UnknownRule(Exception):
    def __init__(self, *args):
        if args:
            self.unknown_rule = args[0]
        else:
            self.unknown_rule = None

    def __str__(self):
        if self.unknown_rule:
            return f'Unknown rule is {self.unknown_rule}'
        else:
            return f'Some unknown rule'


class WrongRuleLine(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Check this rule. {self.message}'
        else:
            return f'Some wrong rule line'


class EmptyTokenData(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = ''

    def __str__(self):
        return f'Have you added rules? It is empty. {self.message}'
