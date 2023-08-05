from pathlib import Path
from typing import *

from .. import IOUtils, LoggingUtils
from .Macro import Macro
from .Table import Table


class File:

    logger = LoggingUtils.get_logger("latex.File")

    def __init__(self, path: Path, is_append: bool = False):
        """
        Creates a latex file, currently for numbers/macros or tables.
        :param path: the path to the file.
        :param is_append: if set to true, then append to any existing file; otherwise overwrite the file.
        """
        self.path: Path = path
        self.is_append: bool = is_append

        self.old_content: str = ""
        if self.is_append:
            if path.is_file():
                self.old_content = IOUtils.load(path, "txt")
        # end if, if

        # Contents
        self.items: List[Union[str, Macro, Table]] = list()
        self.macros_indexed: Dict[str, Macro] = dict()
        return

    def append(self, line: str) -> "File":
        """
        Appends one line of text into the file.
        """
        self.items.append(line)
        return self

    def append_macro(self, macro: Macro) -> "File":
        if macro.key in self.macros_indexed:
            self.logger.warning(f"Redefining macro {macro.key}")
        # end if
        self.macros_indexed[macro.key] = macro
        self.items.append(macro)
        return self

    def append_comment(self, line: str) -> "File":
        self.items.append("%% " + line)
        return self

    def save(self) -> None:
        content = self.old_content + "\n" + self.eval_content()
        IOUtils.dump(self.path, content, "txt")
        return

    def eval_content(self) -> str:
        content_lines: List[str] = list()
        if not self.is_append:
            content_lines.append(self.autogen_notice())
        # end if
        for item in self.items:
            if isinstance(item, str):
                content_lines.append(item)
            elif isinstance(item, Macro):
                content_lines.append(item.eval_content(self.macros_indexed))
            else:
                self.logger.warning("Skipping unsupported item")
            # end if
        # end for
        return "\n".join(content_lines)+"\n"

    def load_macros_from_file(self, file: Path) -> "File":
        self.macros_indexed.update(Macro.load_from_file(file))
        return self

    def __iadd__(self, other: Union[str, Macro]):
        if isinstance(other, str):
            self.append(other)
        elif isinstance(other, Macro):
            self.append_macro(other)
        else:
            self.logger.warning("Skipping unsupported item")
        # end if
        return self

    @classmethod
    def autogen_notice(cls) -> str:
        return "%% Automatically generated by pyutil.latex \n"
