from typing import Literal
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy

type Position = Literal["center", "left", "right"]


class TitleDrawer:

    def __init__(self, ax: Axes, fig: Figure) -> None:
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
        """
        Draw and style the title of the Axes.

        Parameters
        ----------
        text : str
            The title text to be displayed.
        font : FontProperties | str | None. Default is None
            The font for the title text.
        size : int | None. Default is None
            The font size for the title text.
        color : str | None. Default is None
            The color of the title text.
        position : {"center", "left", "right"} | None. Default is None.
            The position of the title.
        pad : float | None. Default is None
            The padding between the title and the Axes.
        x_offset : float | None. Default is None
            The offset of the title along the x-axis.
        """

        title = self.ax.set_title(label=text, loc=position)

        if font is not None:
            title.set_fontproperties(font)
        if size is not None:
            title.set_fontsize(size)
        if color is not None:
            title.set_color(color)

        if pad is not None or x_offset is not None:
            offset_transform = offset_copy(
                title.get_transform(),
                fig=self.fig,
                x=x_offset if x_offset else 0,
                y=pad if pad else 0,
                units="points",
            )
            title.set_transform(offset_transform)
