__all__ = ("BasePnytterException", "NoNitterInstancesDefinedError")


class BasePnytterException(Exception):
    pass


class NoNitterInstancesDefinedError(Exception):
    def __init__(self):
        super().__init__("No Nitter instances defined on the Pnytter class")
