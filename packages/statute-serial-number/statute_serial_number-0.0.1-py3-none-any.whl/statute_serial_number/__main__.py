from enum import Enum, unique
from pathlib import Path
from typing import Optional

from lawsql_utils.files import STATUTES_PATH

_NUMBER = "No."
_BILANG = "Blg."
_DATED = "dated"
_DASHED = "-"


@unique
class StatuteID(Enum):
    """
    Decoding & encoding of statutory identifiers.

    Each member of this enumeration contains:

    1. a `name`: shortcut folder source of raw statutory yaml files as found in `STATUTES_PATH`.
    2. a `value`: a tuple:
        1. `value[0]` is the "formal category name"
        2. `value[1]`, if applicable, is the manner it is serialized in numbered format.

    Example: `1987 Constitution`

    1. name: `CONST`
    2. value: ("Constitution", None)

    Example: `Republic Act No. 386`

    1. name: `RA`
    2. value: ("Republic Act", "No.")

    The uniform use of names enables the grouping of related files in the same folder. See `STATUTES_PATH`.

    The formal names are utilized in the `*.yaml` files contained in these folders.
    """

    # Note that `Republic Act` and `Commonwealth Act` must precede Act
    # name = (value[0], value[1])
    RA = ("Republic Act", _NUMBER)
    CA = ("Commonwealth Act", _NUMBER)
    ACT = ("Act", _NUMBER)
    CONST = ("Constitution", None)
    SPAIN = ("Spanish", None)
    BP = ("Batas Pambansa", _BILANG)
    PD = ("Presidential Decree", _NUMBER)
    EO = ("Executive Order", _NUMBER)
    VETO = ("Veto Message", _DASHED)
    RULE_ROC = ("Rules of Court", None)
    RULE_BM = ("Bar Matter", _NUMBER)
    RULE_AM = ("Administrative Matter", _NUMBER)
    RULE_RESO = ("Resolution of the Court En Banc", _DATED)

    @property
    def parts(self) -> str:
        """Remove `None` values when joining the tuple value"""
        return " ".join(elem for elem in self.value if elem)

    @property
    def meta_folder(self) -> Path:
        """Assuming a base path `statutes` folder, determine if a subfolder therein exists which match the member's name"""
        return STATUTES_PATH.joinpath(self.name)

    def data_source_folder(self, idx: str) -> Optional[Path]:
        """Get the associated folder, subfolder of an existing `meta_folder`"""
        return (
            subfolder
            if self.meta_folder.exists()
            and (subfolder := self.meta_folder.joinpath(idx))
            and subfolder.exists()
            and subfolder.is_dir()
            else None
        )

    def get_spanish_id_code(self, text: str):
        """Legacy docs don't have serialized identifiers"""
        remainder = text.removeprefix("Spanish ").lower()
        if "civil" in remainder:
            return "civil"
        elif "commerce" in remainder:
            return "commerce"
        elif "penal" in remainder:
            return "penal"

    def get_idx(self, txt: str) -> str:
        """Given text e.g. `Spanish Civil Code` or `Executive Order No. 111`, get the serial number"""
        if self.name == "SPAIN" and (code := self.get_spanish_id_code(txt)):
            return code  # special case
        return txt.replace(self.parts, "").strip()  # regular

    def search_pair(self, txt: str) -> Optional[tuple[str, str]]:
        """Return shortcut tuple of member name and identifier, if found."""
        return (self.name, self.get_idx(txt)) if self.value[0] in txt else None

    def make_title(self, idx: str) -> str:
        """Return full title; notice inverted order for Rules of Court, Constitution"""
        if self.name in ["RULE_ROC", "CONST"]:
            return f"{idx} {self.parts}"  # e.g. 1987 Constitution
        elif self.name == "SPAIN":
            if code := self.get_spanish_id_code(f"Spanish {idx}"):
                if code == "civil" or code == "penal":
                    return f"Spanish {code.title()} Code"
                elif code == "commerce":
                    return "Spanish Code of Commerce"
        return f"{self.parts} {idx}"  # e.g. Republic Act No. 1231


def get_statute_choices() -> list[tuple[str, str]]:
    return [
        (name, member.value[0])
        for name, member in StatuteID.__members__.items()
    ]


def get_member(query: str) -> Optional[StatuteID]:
    for name, member in StatuteID.__members__.items():
        if query == name:
            return member
    return None


def extract_category_and_identifier_from_text(
    text: str,
) -> Optional[tuple[str, str]]:
    """Given statutory text, e.g. "Republic Act No. 386", get a matching category ("RA") and identifier ("386") by going through each member of the `StatuteID` enumeration"""
    for member in StatuteID:
        if pair := member.search_pair(text):
            return pair
    return None
