from types_ import AltLinkBox, ChainLinkBox, LetBox


class DATA:
    """
    Stores a dict where the keys are the names of the boxes and objects of the boxes
    """
    __token_data = dict()

    @classmethod
    def change_token_data(cls, token_data: dict[str, AltLinkBox | ChainLinkBox | LetBox]) -> None:
        cls.__token_data = token_data

    @classmethod
    def add_token_in(cls, *args: AltLinkBox | ChainLinkBox | LetBox) -> None:
        for lb in args:
            cls.__token_data[lb.name] = lb

    @classmethod
    def get_tokens(cls) -> dict[str, AltLinkBox | ChainLinkBox | LetBox]:
        return cls.__token_data

    @classmethod
    def __repr__(cls):
        return f'DATA({cls.__token_data})'
