from matplotlib.axis import Axis
from matplotlib.font_manager import FontProperties


class AxisLabelDrawer:
    def __init__(self, axis: Axis) -> None:
        self.axis = axis

    def draw(
        self,
        text: str,
        font: FontProperties | None = None,
        size: int | None = None,
        color: str | None = None,
        rotation: float | None = None,
        pad: float | None = None,
    ) -> None:
        """
        Draw the axis label of the Matplotlib axis object.

        Parameters
        ----------
        text : str
            The text of the axis label.
        font : FontProperties | None. Default is None.
            The text font.
        size : int | None. Default is None.
            The text size.
        color : str | None. Default is None.
            The text color.
        rotation : float | None. Default is None.
            The text rotation.
        pad : float | None. Default is None.
            The text padding from the axis.
        """

        self.axis.label.set_text(text)
        if font is not None:
            self.axis.label.set_fontproperties(font)
        if size is not None:
            self.axis.label.set_fontsize(size)
        if color is not None:
            self.axis.label.set_color(color)
        if rotation is not None:
            self.axis.label.set_rotation(rotation)
        if pad is not None:
            self.axis.labelpad = pad
