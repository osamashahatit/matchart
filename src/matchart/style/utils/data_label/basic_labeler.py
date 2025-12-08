from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from ..num_formatter import NumberFormatter


@dataclass(frozen=True)
class BDL_LabelAnchor:
    x: float
    y: float


@dataclass(frozen=True)
class BDL_LabelProperties:
    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class BDL_AlignProperties:
    h_align: str | None
    v_align: str | None
    x_offset: float
    y_offset: float


class BasicDataLabeler:
    """Adds chart basic data labels."""

    def __init__(
        self,
        ax: Axes,
        anchor: BDL_LabelAnchor,
        formatter: NumberFormatter,
        label: BDL_LabelProperties,
        align: BDL_AlignProperties,
        gid: str | None = None,
    ):
        self.ax = ax
        self.anchor = anchor
        self.formatter = formatter
        self.label = label
        self.align = align
        self.gid = gid

    def draw(self, label: float) -> None:

        self.ax.annotate(
            text=self.formatter.format(label),
            xy=(self.anchor.x, self.anchor.y),
            fontproperties=self.label.font,
            fontsize=self.label.size,
            color=self.label.color,
            ha=self.align.h_align,
            va=self.align.v_align,
            xytext=(self.align.x_offset, self.align.y_offset),
            xycoords="data",
            textcoords="offset points",
            gid=self.gid,
        )
