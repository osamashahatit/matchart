"""Style axes titles."""

from typing import Literal

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy

type Position = Literal["center", "left", "right"]


class TitleDrawer:
    """Draw and style an Axes title."""

    def __init__(self, ax: Axes, fig: Figure) -> None:
        """
        Args:
            ax (Axes): Axes whose title will be set/styled.
            fig (Figure): Figure used for points-based offset transforms.
        """
        self.ax = ax
        self.fig = fig

    def draw(
        self,
        text: str,
        font: FontProperties | str | None = None,
        size: int | None = None,
        color: str | None = None,
        position: Position | None = None,
        pad: float | None = None,
        x_offset: float | None = None,
    ) -> None:
        """Set and style the Axes title text.

        Args:
            text (str): Title text to display.
            font (FontProperties | str | None): Font configuration for the
                title. When provided as a string, it is passed through to
                Text.set_fontproperties(). A common usage is a font family
                name (e.g., "DejaVu Sans").
            size (int | None): Font size in points.
            color (str | None): Title text color.
            position (Position | None): Title alignment on the Axes.
                Options: "center", "left", "right".
            pad (float | None): Additional vertical offset in points applied
                via a transform (positive moves up).
            x_offset (float | None): Additional horizontal offset in points
                applied via a transform (positive moves right).

        Returns:
            None: The Axes title Text artist is modified in place.
        """
        title = self.ax.set_title(label=text, loc=position)  # type:ignore

        if font is not None:
            title.set_fontproperties(font)
        if size is not None:
            title.set_fontsize(size)
        if color is not None:
            title.set_color(color)

        if pad is not None or x_offset is not None:
            # Use a points-based transform offset so layout is consistent
            # regardless of data limits and figure size.
            offset_transform = offset_copy(
                title.get_transform(),
                fig=self.fig,
                x=x_offset if x_offset else 0,
                y=pad if pad else 0,
                units="points",
            )
            title.set_transform(offset_transform)
