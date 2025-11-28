import matplotlib.font_manager as fm
from pathlib import Path


class Fonts:
    """
    Utility class to load and register custom fonts for Matplotlib.

    This class simplifies loading and managing custom font files using
    Matplotlib's `font_manager`. Fonts can be added from a directory and
    accessed later via named attributes or through the `properties` dictionary.
    """

    def __init__(self) -> None:
        self.properties: dict[str, fm.FontProperties] = {}

    @classmethod
    def load(cls, path: str, fonts: dict[str, str]) -> "Fonts":
        """
        Load and register custom fonts from a directory.

        Parameters
        ----------
        path : str
            Path to the directory containing font files.
        fonts : dict[str, str]
            Mapping of font names to font filenames. Each key represents a
            user-defined font name, and each value is the corresponding filename.

        Returns
        -------
        Fonts
            A Fonts instance with loaded font properties.
        """
        instance = cls()
        for name, file in fonts.items():
            instance._add(name, Path(path) / file)
        return instance

    def _add(self, name: str, path: Path) -> fm.FontProperties:
        """Register a single font file under a name and return its properties."""

        path = Path(path)
        fm.fontManager.addfont(str(path))
        property = fm.FontProperties(fname=path)
        self.properties[name] = property
        setattr(self, name, property)
        return property

    def __getattr__(self, name: str) -> fm.FontProperties:
        """Get font properties by name, raising AttributeError if not found."""

        try:
            return self.properties[name]
        except KeyError:
            raise AttributeError(
                f"No such font name: {name!r}. Available: {list(self.properties)}"
            )
