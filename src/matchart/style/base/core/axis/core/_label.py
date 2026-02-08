"""Draw and style axis labels."""

from matplotlib.axis import Axis
from matplotlib.font_manager import FontProperties


class AxisLabelDrawer:
    """Apply text and styling to a Matplotlib axis label."""

    def __init__(self, axis: Axis) -> None:
        """
        Args:
            axis (Axis): Matplotlib Axis instance (e.g., ax.xaxis or
                ax.yaxis) whose label will be styled.
        """
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
        """Draw and style the axis label.

        Args:
            text (str): Label text to display.
            font (FontProperties | None): Optional font configuration.
            size (int | None): Optional font size.
            color (str | None): Optional text color.
            rotation (float | None): Optional text rotation in degrees.
            pad (float | None): Optional padding from the axis.

        Returns:
            None: The axis label is modified in place.
        """
        # Label text is always updated.
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
