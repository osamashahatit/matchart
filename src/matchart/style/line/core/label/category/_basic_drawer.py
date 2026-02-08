"""Draw line chart category basic data labels."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from matchart.style.line.core._utils import LineStyleHelper
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

from ._basic_anchor import CBDL_Line_Anchor
from ._utils import CDL_Line_Totals


@dataclass(frozen=True)
class CBDL_Line_LabelProperties:
    """Configure category label font appearance for line charts."""

    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class CBDL_Line_AlignProperties:
    """Configure offsets applied to category label anchors."""

    x_offset: float
    y_offset: float


class CBDL_Line:
    """Iterate tick labels and draw one category label per tick."""

    def __init__(
        self,
        ax: Axes,
        helper: LineStyleHelper,
        formatter: NumberFormatter,
        label: CBDL_Line_LabelProperties,
        align: CBDL_Line_AlignProperties,
        custom_label: dict[str, float] | None,
    ):
        """
        Args:
            ax (Axes): Target axes that already contains line artists.
            helper (LineStyleHelper): Helper class.
            formatter (NumberFormatter): Number formatter.
            label (CBDL_Line_LabelProperties): Label appearance configuration.
            align (CBDL_Line_AlignProperties): Anchor offset configuration.
            custom_label (dict[str, float] | None): Optional mapping from tick
                label text to the numeric value to display. When None, totals
                are computed from line data via CDL_Line_Totals.
        """
        self.ax = ax
        self.helper = helper
        self.formatter = formatter
        self.label = label
        self.align = align
        self.custom_label = custom_label

    def draw(self) -> None:
        """Draw category labels for each tick label on the Axes.

        Notes:
            This method mutates the Axes by adding Text artists. It does not
            return self (not chainable).
        """
        tick_labels = self.helper.get_tick_labels()

        for tick_label in tick_labels:
            if self.custom_label is None:
                label = CDL_Line_Totals.compute_total(
                    ax=self.ax,
                    tick_label=tick_label,
                ).total
            else:
                label = self.custom_label[tick_label]

            anchor = CBDL_Line_Anchor(ax=self.ax, tick_label=tick_label)

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
                    v_align="top",
                    x_offset=self.align.x_offset,
                    y_offset=self.align.y_offset,
                ),
                gid="LineCategoryBasicDataLabel",
            ).draw(label=label)


class CBDL_Line_Drawer:
    """Configure and draw category-level labels for line charts."""

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
    ) -> "CBDL_Line_Drawer":
        """Set label font properties.

        Args:
            font (FontProperties | None): Font style. If None, Matplotlib
                defaults are used.
            size (int | None): Font size. If None, Matplotlib defaults
                are used.
            color (str | None): Font color. If None, Matplotlib defaults
                are used.

        Returns:
            CBDL_Line_Drawer: The current instance for method chaining.
        """
        self._font = font
        self._size = size
        self._color = color
        return self

    def align(
        self,
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "CBDL_Line_Drawer":
        """Set anchor offsets applied when drawing labels.

        Args:
            x_offset (float): Offset applied from anchor x coordinate.
            y_offset (float): Offset applied from anchor y coordinate.

        Returns:
            CBDL_Line_Drawer: The current instance for method chaining.
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
    ) -> "CBDL_Line_Drawer":
        """Configure numeric formatting for category labels.

        Args:
            format_type (NumberFormat): Numeric formatting mode.
                Options: "number", "percent".
            decimals (int): Number of decimal places to display.
            separator (bool): Whether to use thousands separators.
            currency (str | None): Optional currency symbol/code.
            scale (ScaleType): Scaling mode for large numbers.
                Options: "k", "m", "b", "t", "full", "auto".

        Returns:
            CBDL_Line_Drawer: The current instance for method chaining.
        """
        self._format_type = format_type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(
        self,
        custom_label: dict[str, float] | None = None,
        clear: bool = True,
    ) -> None:
        """Draw category labels onto the Axes.

        Args:
            custom_label (dict[str, float] | None): Optional mapping from tick
                label text to the numeric value to display. When None, totals
                are computed from line data via CDL_Line_Totals.
            clear (bool): If True, remove existing labels previously drawn by
                this drawer (identified by gid "LineCategoryBasicDataLabel").

        Notes:
            This method mutates the Axes by removing and adding Text artists.
            It does not return self (not chainable).
        """
        helper = LineStyleHelper(ax=self.ax)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "LineCategoryBasicDataLabel":
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

        CBDL_Line(
            ax=self.ax,
            helper=helper,
            formatter=formatter,
            label=CBDL_Line_LabelProperties(
                font=self._font,
                size=self._size,
                color=self._color,
            ),
            align=CBDL_Line_AlignProperties(
                x_offset=self._x_offset,
                y_offset=self._y_offset,
            ),
            custom_label=custom_label,
        ).draw()
