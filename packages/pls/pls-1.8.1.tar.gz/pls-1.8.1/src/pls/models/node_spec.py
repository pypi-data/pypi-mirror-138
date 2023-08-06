from __future__ import annotations

import re


class NodeSpec:
    """
    A spec describes the nature of a class of FS nodes that determine its
    presentation. This model stores attributes pertaining to a single spec. Make
    sure to massage spec entries using :py:func:`pls.data.getters.massage_specs`
    before initialising.

    Node specs are read from ``node_spec.yml``.
    """

    def __init__(
        self,
        name: str = None,
        pattern: str = None,
        extension: str = None,
        icon: str = None,
        color: str = None,
        importance: int = 0,
    ):
        identification_methods = ["name", "pattern", "extension"]
        loc = locals()

        self.name = name
        self.pattern = re.compile(pattern) if pattern else None
        self.extension = extension

        self.icon = icon
        self.color = color
        self.importance = importance

    def __repr__(self) -> str:
        """
        Get the string representation of the ``NodeSpec`` instance. This is also
        used by ``__str__`` automatically.

        :return: the string representation
        """

        if self.name:
            return self.name
        if self.extension:
            return f"*.{self.extension}"
        if self.pattern:
            return f"<{self.pattern.pattern}>"

    def match(self, name: str) -> bool:
        """
        Check whether the given file name matches this spec.

        :param name: the name of the file to match against this spec
        :return: ``True`` if the file matches this entry, ``False`` otherwise
        """

        if self.name:
            return self.name == name
        elif self.pattern:
            return re.match(self.pattern, name) is not None
        elif self.extension:
            return name.endswith(f".{self.extension}")
        else:
            return False
