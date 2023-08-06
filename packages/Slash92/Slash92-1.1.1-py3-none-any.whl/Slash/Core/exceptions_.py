class SlashTypeError(Exception):
    def __init__(self, text): ...


class SlashRulesError(Exception):
    def __init__(self, text): ...


class SlashBadColumnNameError(Exception):
    def __init__(self, text): ...


class SlashBadAction(Exception):
    def __init__(self, text): ...


class SlashPatternMismatch(Exception):
    def __init__(self, text): ...


class SlashLenMismatch(Exception):
    def __init__(self, text) -> None: ...


class SlashOneTableColumn(Exception):
    def __init__(self, text) -> None: ...

class SlashNoResultToFetch(Exception):
    def __init__(self, text) -> None: ...


class SlashUnexpectedError(Exception):
    def __init__(self, text) -> None: ...


class SlashNotTheSame(Exception):
    def __init__(self, text) -> None: ...
