"""Provide shared primitives for basic numeric data labels."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from matchart.style.utils.num_formatter import NumberFormatter


@dataclass(frozen=True)
class BDL_LabelAnchor:
    """Represent a data-coordinate anchor point for a label.

    Attributes:
        x (float): X coordinate in data units.
        y (float): Y coordinate in data units.
    """

    x: float
    y: float


@dataclass(frozen=True)
class BDL_LabelProperties:
    """Store text styling properties for a basic data label.

    Attributes:
        font (FontProperties | None): Optional font configuration.
        size (int | None): Optional font size in points.
        color (str | None): Optional text color.
    """

    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class BDL_AlignProperties:
    """Store alignment and offset properties for a basic data label.

    Attributes:
        h_align (str | None): Horizontal alignment passed to Matplotlib
            (e.g., "left", "center", "right").
        v_align (str | None): Vertical alignment passed to Matplotlib
            (e.g., "top", "center", "bottom", "baseline").
        x_offset (float): X offset in points (textcoords="offset points").
        y_offset (float): Y offset in points (textcoords="offset points").
    """

    h_align: str | None
    v_align: str | None
    x_offset: float
    y_offset: float


class BasicDataLabeler:
    """Add a single formatted numeric annotation to a Matplotlib Axes."""

    def __init__(
        self,
        ax: Axes,
        anchor: BDL_LabelAnchor,
        formatter: NumberFormatter,
        label: BDL_LabelProperties,
        align: BDL_AlignProperties,
        gid: str | None = None,
    ):
        """
        Args:
            ax (Axes): Target axes to annotate (no figure creation).
            anchor (BDL_LabelAnchor): Data-coordinate anchor for the label.
            formatter (NumberFormatter): Formatter used to convert numeric
                values into display strings.
            label (BDL_LabelProperties): Text styling properties.
            align (BDL_AlignProperties): Alignment and point-offset settings.
            gid (str | None): Optional Matplotlib artist group id.
        """
        self.ax = ax
        self.anchor = anchor
        self.formatter = formatter
        self.label = label
        self.align = align
        self.gid = gid

    def draw(self, label: float) -> None:
        """Draw a single data label annotation.

        Args:
            label (float): Numeric value to format and annotate.

        Returns:
            None: This method adds an annotation artist to the axes.
        """
        self.ax.annotate(  # type:ignore
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
