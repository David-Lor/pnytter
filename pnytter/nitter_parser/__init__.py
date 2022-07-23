from .profiles import NitterProfilesParser
from .tweets import NitterTweetsParser

__all__ = ("NitterParser",)


class NitterParser(NitterProfilesParser, NitterTweetsParser):
    """The NitterParser object is initialized once for each Nitter page to parse. The object is initialized with the
    Nitter page HTML source. The methods exposed allows parsing the desired data. The given webpage source must contain
    the information wanted (for example, we cannot parse a profile data from a tweet page).

    Internally, the NitterParser has no logic, while inheriting from different Parser classes, splitting the logic
    for the different kinds of Twitter objects supported.
    """
