"""Measure text and compute auto-sized frame dimensions for data labels.

Data labels are often drawn inside a "frame" (background box) whose size
should adapt to the formatted label text. Manually choosing frame sizes
is brittle because label strings vary with values, number formats, and
font settings. This module provides lightweight geometry dataclasses and
an auto-sizer that uses Matplotlib's TextPath to measure label text in
points and returns a padded frame dimension suitable for consistent
label framing across chart types.
"""

from dataclasses import dataclass

from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

from matchart.style.utils.num_formatter import NumberFormatter


@dataclass(frozen=True)
class LabelDimension:
    """Represent a text label size in points.

    Attributes:
        width (float): Text width in points.
        height (float): Text height in points.
    """

    width: float
    height: float

    def with_pad(self, pad: float) -> "LabelDimension":
        """Return a padded label dimension.

        Padding is applied on all sides, so each dimension increases by
        2 * pad.

        Args:
            pad (float): Padding in points.

        Returns:
            LabelDimension: A new dimension including padding.
        """
        return LabelDimension(
            width=self.width + (2 * pad),
            height=self.height + (2 * pad),
        )


@dataclass(frozen=True)
class FrameDimension:
    """Represent a frame size in points.

    Attributes:
        width (float): Frame width in points.
        height (float): Frame height in points.
    """

    width: float
    height: float


class FrameAutoSizer:
    """Measure frame dimensions that fit formatted data label text."""

    def __init__(
        self,
        fig: Figure,
        pad: float,
        font: FontProperties | None,
        size: int,
        formatter: NumberFormatter,
    ):
        """
        Args:
            fig (Figure): Matplotlib figure context (currently unused).
            pad (float): Padding in points to apply around the label text.
            font (FontProperties | None): Font properties used for text
                measurement.
            size (int): Font size in points used for measurement.
            formatter (NumberFormatter): Formatter used to convert numeric
                values into display strings.
        """
        self.fig = fig
        self.pad = pad
        self.font = font
        self.size = size
        self.formatter = formatter

    def measure_label(self, label: str) -> LabelDimension:
        """Measure a text label in points.

        Args:
            label (str): Label string to measure.

        Returns:
            LabelDimension: Width/height of the text extents in points.
        """
        label_path = TextPath((0, 0), label, size=self.size, prop=self.font)
        bbox = label_path.get_extents()  # type:ignore
        return LabelDimension(bbox.width, bbox.height)

    def measure_frame(
        self,
        label: float,
        custom_width: float | None,
        custom_height: float | None,
    ) -> FrameDimension:
        """Measure a padded frame dimension for a numeric label.

        Args:
            label (float): Numeric value to format and measure.
            custom_width (float | None): Optional width override in points.
            custom_height (float | None): Optional height override in points.

        Returns:
            FrameDimension: Final frame size in points.
        """
        frame = self.measure_label(self.formatter.format(label)).with_pad(self.pad)

        width = custom_width if custom_width is not None else frame.width
        height = custom_height if custom_height is not None else frame.height

        return FrameDimension(width, height)
