"""Draw bar chart category basic data labels."""

from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from matchart.style.bar.core._utils import BarStyleHelper
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

from ._basic_anchor import (
    CBDL_HBar_Anchor,
    CBDL_HBar_VAlign,
    CBDL_VBar_Anchor,
    CBDL_VBar_HAlign,
)
from ._utils import CDL_Bar_Bounds, CDL_Bar_Totals


@dataclass(frozen=True)
class CBDL_Bar_LabelProperties:
    """Configure category label font appearance."""

    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class CBDL_Bar_AlignProperties:
    """Configure category label anchoring and offsets."""

    h_align: CBDL_VBar_HAlign
    v_align: CBDL_HBar_VAlign
    x_offset: float
    y_offset: float


class CBDL_Bar:
    """Iterate tick labels and draw one label per category."""

    def __init__(
        self,
        ax: Axes,
        horizontal: bool,
        helper: BarStyleHelper,
        formatter: NumberFormatter,
        label: CBDL_Bar_LabelProperties,
        align: CBDL_Bar_AlignProperties,
        custom_label: dict[str, float] | None,
    ):
        """
        Args:
            ax (Axes): Target axes that already contains bar artists.
            horizontal (bool): Whether the bar chart is horizontal.
            helper (BarStyleHelper): Helper class.
            formatter (NumberFormatter): Number formatter.
            label (CBDL_Bar_LabelProperties): Label appearance configuration.
            align (CBDL_Bar_AlignProperties): Alignment and offset configuration.
            custom_label (dict[str, float] | None): Optional mapping from tick
                label text to the numeric value to display. When None, totals
                are computed from bar patches.
        """
        self.ax = ax
        self.horizontal = horizontal
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
        for tick_label in self.helper.get_tick_labels():
            # Aggregate span for this tick label across all bar containers.
            bounds = CDL_Bar_Bounds.bounds(
                ax=self.ax,
                helper=self.helper,
                horizontal=self.horizontal,
                tick_label=tick_label,
            )

            # Default label is the sum across containers; custom_label can
            # override this per tick.
            if self.custom_label is None:
                label = CDL_Bar_Totals.compute_total(
                    ax=self.ax,
                    helper=self.helper,
                    horizontal=self.horizontal,
                    tick_label=tick_label,
                ).total
            else:
                label = self.custom_label[tick_label]

            # Category anchors are placed at the plot edge using Axes limits.
            if self.horizontal:
                anchor = CBDL_HBar_Anchor(
                    ax=self.ax,
                    bounds=bounds,
                ).anchor(v_align=self.align.v_align)
            else:
                anchor = CBDL_VBar_Anchor(
                    ax=self.ax,
                    bounds=bounds,
                ).anchor(h_align=self.align.h_align)

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
                    h_align=anchor.h_align,
                    v_align=anchor.v_align,
                    x_offset=self.align.x_offset,
                    y_offset=self.align.y_offset,
                ),
                gid="BarCategoryBasicDataLabel",
            ).draw(label=label)


class CBDL_Bar_Drawer:
    """Configure and draw category-level labels for bar charts."""

    def __init__(self, ax: Axes, horizontal: bool) -> None:
        """
        Args:
            ax (Axes): Target axes that already contains bar artists.
            horizontal (bool): Whether the bar chart is horizontal.
        """
        self.ax = ax
        self.horizontal = horizontal

        # Label properties
        self._font: FontProperties | None = None
        self._size: int | None = None
        self._color: str | None = None

        # Align properties
        self._h_align: CBDL_VBar_HAlign = "center"
        self._v_align: CBDL_HBar_VAlign = "center"
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
    ) -> "CBDL_Bar_Drawer":
        """Set label font properties.

        Args:
            font (FontProperties | None): Font style. If None, Matplotlib
                defaults are used.
            size (int | None): Font size. If None, Matplotlib defaults
                are used.
            color (str | None): Font color. If None, Matplotlib defaults
                are used.

        Returns:
            CBDL_Bar_Drawer: The current instance for method chaining.
        """
        self._font = font
        self._size = size
        self._color = color
        return self

    def align(
        self,
        h_align: CBDL_VBar_HAlign = "center",
        v_align: CBDL_HBar_VAlign = "center",
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "CBDL_Bar_Drawer":
        """Set category anchor selection and offsets.

        Args:
            h_align (CBDL_VBar_HAlign): Horizontal alignment selection for
                vertical bar charts. Options: "left", "right", "center".
            v_align (CBDL_HBar_VAlign): Vertical alignment selection for
                horizontal bar charts. Options: "top", "bottom", "center".
            x_offset (float): Offset to apply in the x direction.
            y_offset (float): Offset to apply in the y direction.

        Returns:
            CBDL_Bar_Drawer: The current instance for method chaining.
        """
        self._h_align = h_align
        self._v_align = v_align
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
    ) -> "CBDL_Bar_Drawer":
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
            CBDL_Bar_Drawer: The current instance for method chaining.
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
                are computed from bar patches.
            clear (bool): If True, remove existing labels previously drawn by
                this drawer (identified by gid "BarCategoryBasicDataLabel").

        Notes:
            This method mutates the Axes by removing and adding Text artists.
            It does not return self (not chainable).
        """
        helper = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "BarCategoryBasicDataLabel":
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

        CBDL_Bar(
            ax=self.ax,
            horizontal=self.horizontal,
            helper=helper,
            formatter=formatter,
            label=CBDL_Bar_LabelProperties(
                font=self._font,
                size=self._size,
                color=self._color,
            ),
            align=CBDL_Bar_AlignProperties(
                h_align=self._h_align,
                v_align=self._v_align,
                x_offset=self._x_offset,
                y_offset=self._y_offset,
            ),
            custom_label=custom_label,
        ).draw()
