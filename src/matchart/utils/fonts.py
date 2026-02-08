"""Utilities for font management."""

from pathlib import Path

import matplotlib.font_manager as fm


class Fonts:
    """Utility class to load and register custom fonts for Matplotlib."""

    def __init__(self) -> None:
        """Initialize an empty font registry."""
        self.properties: dict[str, fm.FontProperties] = {}

    @classmethod
    def load(cls, path: str, fonts: dict[str, str]) -> "Fonts":
        """Load and register multiple font files from a directory.

        Args:
            path: Path to the directory containing font files.
            fonts: Mapping of font names to font filenames.

        Returns:
            Fonts: A populated ``Fonts`` instance with registered fonts.
        """
        instance = cls()
        base_path = Path(path)

        for name, filename in fonts.items():
            instance._add(name=name, path=base_path / filename)

        return instance

    def _add(self, name: str, path: Path) -> fm.FontProperties:
        """Register a single font file under a given name.

        Args:
            name: User-facing font name.
            path: Full path to the font file.

        Returns:
            matplotlib.font_manager.FontProperties: Registered font properties.
        """
        path = Path(path)

        fm.fontManager.addfont(str(path))  # type: ignore[attr-defined]
        font_properties = fm.FontProperties(fname=path)

        self.properties[name] = font_properties
        setattr(self, name, font_properties)

        return font_properties

    def __getattr__(self, name: str) -> fm.FontProperties:
        """Retrieve font properties by attribute access.

        Args:
            name: Font name.

        Returns:
            matplotlib.font_manager.FontProperties: Font properties for the
            requested font.

        Raises:
            AttributeError: If the font name does not exist.
        """
        try:
            return self.properties[name]
        except KeyError as exc:
            raise AttributeError(
                f"No such font name: {name!r}. Available: {list(self.properties)}"
            ) from exc
