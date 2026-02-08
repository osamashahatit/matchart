"""Draw line chart standard basic data labels."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from matchart.style.line.core._utils import LineStyleHelper, LineYielder
from matchart.style.utils.data_label.basic_labeler import (
    BasicDataLabeler,
    BDL_AlignProperties,
    BDL_LabelAnchor,
    BDL_LabelProperties,
)
from matchart.style.utils.num_formatter import (
    NumberFormat,
    NumberFormatter,
    NumberProperties,
    ScaleType,
)

from ._basic_anchor import BDL_Line_Anchor


@dataclass(frozen=True)
class BDL_Line_LabelProperties:
    """Configure font appearance for point-level line labels."""

    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class BDL_Line_AlignProperties:
    """Configure anchor offsets applied when drawing point labels."""

    x_offset: float
    y_offset: float


class BDL_Line:
    """Iterate lines and ticks to draw one label per line point."""

    def __init__(
        self,
        ax: Axes,
        lines: LineYielder,
        helper: LineStyleHelper,
        formatter: NumberFormatter,
        label: BDL_Line_LabelProperties,
        align: BDL_Line_AlignProperties,
        select: list[str] | None,
    ):
        """
        Args:
            ax (Axes): Target axes that already contains line artists.
            lines (LineYielder): Provider for line artists on the Axes.
            helper (LineStyleHelper): Helper class.
            formatter (NumberFormatter): Number formatter.
            label (BDL_Line_LabelProperties): Label appearance configuration.
            align (BDL_Line_AlignProperties): Anchor offset configuration.
            select (list[str] | None): Optional list of line labels to include.
                When provided, only lines whose Line2D.get_label() matches an
                entry are labeled.
        """
        self.ax = ax
        self.lines = lines.standard()
        self.helper = helper
        self.formatter = formatter
        self.label = label
        self.align = align
        self.select = select

    def draw(self) -> None:
        """Draw point-level labels for each (line, tick) pair.

        Notes:
            This method mutates the Axes by adding Text artists. It does not
            return self (not chainable).
        """
        tick_labels = self.helper.get_tick_labels()

        for line in self.lines:
            line_label = line.get_label()

            if self.select is not None and line_label not in self.select:
                continue

            for tick_label in tick_labels:
                anchor = BDL_Line_Anchor(ax=self.ax, line=line, tick_label=tick_label)
                point_value = self.helper.get_point_value(
                    line=line,
                    tick_label=tick_label,
                )

                BasicDataLabeler(
                    ax=self.ax,
                    anchor=BDL_LabelAnchor(x=anchor.x, y=anchor.y),
                    formatter=self.formatter,
                    label=BDL_LabelProperties(
                        font=self.label.font,
                        size=self.label.size,
                        color=self.label.color,
                    ),
                    align=BDL_AlignProperties(
                        h_align="center",
                        v_align="bottom",
                        x_offset=self.align.x_offset,
                        y_offset=self.align.y_offset,
                    ),
                    gid="LineBasicDataLabel",
                ).draw(label=point_value)


class BDL_Line_Drawer:
    """Configure and draw basic (unframed) point labels for line charts."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Target axes that already contains line artists.
        """
        self.ax = ax

        # Label properties
        self._font: FontProperties | None = None
        self._size: int | None = None
        self._color: str | None = None

        # Align properties
        self._x_offset: float = 0.0
        self._y_offset: float = 0.0

        # Format properties
        self._format_type: NumberFormat = "number"
        self._decimals: int = 0
        self._separator: bool = False
        self._currency: str | None = None
        self._scale: ScaleType = "full"

    def label(
        self,
        font: FontProperties | None = None,
        size: int | None = None,
        color: str | None = None,
    ) -> "BDL_Line_Drawer":
        """Set label font properties.

        Args:
            font (FontProperties | None): Font style. If None, Matplotlib
                defaults are used.
            size (int | None): Font size. If None, Matplotlib defaults
                are used.
            color (str | None): Font color. If None, Matplotlib defaults
                are used.

        Returns:
            BDL_Line_Drawer: The current instance for method chaining.
        """
        self._font = font
        self._size = size
        self._color = color
        return self

    def align(
        self,
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "BDL_Line_Drawer":
        """Set anchor offsets applied when drawing labels.

        Args:
            x_offset (float): Offset applied from anchor x coordinate.
            y_offset (float): Offset applied from anchor y coordinate.

        Returns:
            BDL_Line_Drawer: The current instance for method chaining.
        """
        self._x_offset = x_offset
        self._y_offset = y_offset
        return self

    def format(
        self,
        format_type: NumberFormat = "number",
        decimals: int = 0,
        separator: bool = False,
        currency: str | None = None,
        scale: ScaleType = "full",
    ) -> "BDL_Line_Drawer":
        """Configure numeric formatting for point labels.

        Args:
            format_type (NumberFormat): Numeric formatting mode.
                Options: "number", "percent".
            decimals (int): Number of decimal places to display.
            separator (bool): Whether to use thousands separators.
            currency (str | None): Optional currency symbol/code.
            scale (ScaleType): Scaling mode for large numbers.
                Options: "k", "m", "b", "t", "full", "auto".

        Returns:
            BDL_Line_Drawer: The current instance for method chaining.
        """
        self._format_type = format_type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(self, select: list[str] | None = None, clear: bool = True) -> None:
        """Draw point labels onto the Axes.

        Args:
            select (list[str] | None): Optional list of line labels to include.
                When provided, only lines whose Line2D.get_label() matches an
                entry are labeled.
            clear (bool): If True, remove existing labels previously drawn by
                this drawer (identified by gid "LineBasicDataLabel").

        Notes:
            This method mutates the Axes by removing and adding Text artists.
            It does not return self (not chainable).
        """
        helper = LineStyleHelper(ax=self.ax)
        line_yielder = LineYielder(ax=self.ax)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "LineBasicDataLabel":
                    label.remove()

        formatter = NumberFormatter(
            properties=NumberProperties(
                format_type=self._format_type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        BDL_Line(
            ax=self.ax,
            lines=line_yielder,
            helper=helper,
            formatter=formatter,
            label=BDL_Line_LabelProperties(
                font=self._font,
                size=self._size,
                color=self._color,
            ),
            align=BDL_Line_AlignProperties(
                x_offset=self._x_offset,
                y_offset=self._y_offset,
            ),
            select=select,
        ).draw()
