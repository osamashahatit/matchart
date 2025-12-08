from dataclasses import dataclass
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

from ..num_formatter import NumberFormatter


@dataclass(frozen=True)
class FrameDimension:
    width: float
    height: float


@dataclass(frozen=True)
class LabelDimension:
    width: float
    height: float

    def with_pad(self, pad: float) -> "LabelDimension":
        return LabelDimension(
            width=self.width + (2 * pad),
            height=self.height + (2 * pad),
        )


class FrameAutoSizer:
    """Auto-sizer for data label frames based on label size."""

    def __init__(
        self,
        fig: Figure,
        pad: float,
        font: FontProperties | None,
        size: int,
        formatter: NumberFormatter,
    ):
        self.fig = fig
        self.pad = pad
        self.font = font
        self.size = size
        self.formatter = formatter

    def label_dimension(self, label: str) -> LabelDimension:
        """Compute the label dimension in points."""

        label_path = TextPath((0, 0), label, size=self.size, prop=self.font)
        bbox = label_path.get_extents()
        width = bbox.width
        height = bbox.height
        return LabelDimension(width, height)

    def compute_dimension(
        self,
        label: float,
        custom_width: float | None,
        custom_height: float | None,
    ) -> FrameDimension:
        """Compute the frame dimension in points."""

        frame = self.label_dimension(self.formatter.format(label)).with_pad(self.pad)
        custom_width = custom_width if custom_width is not None else frame.width
        custom_height = custom_height if custom_height is not None else frame.height
        return FrameDimension(custom_width, custom_height)
