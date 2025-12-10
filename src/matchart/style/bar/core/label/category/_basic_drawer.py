from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from matchart.style.utils.data_label.basic_labeler import (
    BasicDataLabeler,
    BDL_AlignProperties,
    BDL_LabelAnchor,
    BDL_LabelProperties,
)
from matchart.style.utils.num_formatter import (
    NumberFormat,
    ScaleType,
    NumberProperties,
    NumberFormatter,
)
from ..._utils import BarStyleHelper
from ._basic_anchor import (
    CBDL_VBar_HAlign,
    CBDL_HBar_VAlign,
    CBDL_HBar_Anchor,
    CBDL_VBar_Anchor,
)
from ._utils import CDL_Bar_Bounds, CDL_Bar_Totals


@dataclass(frozen=True)
class CBDL_Bar_LabelProperties:
    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class CBDL_Bar_AlignProperties:
    h_align: CBDL_VBar_HAlign
    v_align: CBDL_HBar_VAlign
    x_offset: float
    y_offset: float


class CBDL_Bar:

    def __init__(
        self,
        ax: Axes,
        horizontal: bool,
        help: BarStyleHelper,
        formatter: NumberFormatter,
        label: CBDL_Bar_LabelProperties,
        align: CBDL_Bar_AlignProperties,
        custom_label: dict[str, float] | None,
    ):
        self.ax = ax
        self.horizontal = horizontal
        self.help = help
        self.formatter = formatter
        self.label = label
        self.align = align
        self.custom_label = custom_label

    def draw(self) -> None:

        for category_index in self.help.get_tick_labels():

            category_bounds = CDL_Bar_Bounds.bounds(
                ax=self.ax,
                help=self.help,
                horizontal=self.horizontal,
                category_index=category_index,
            )

            if self.custom_label is None:
                category_label = CDL_Bar_Totals.totals(
                    ax=self.ax,
                    help=self.help,
                    horizontal=self.horizontal,
                    category_index=category_index,
                ).value
            else:
                category_label = self.custom_label[category_index]

            if self.horizontal:
                category_anchor = CBDL_HBar_Anchor(
                    ax=self.ax,
                    bounds=category_bounds,
                ).anchor(v_align=self.align.v_align)
            else:
                category_anchor = CBDL_VBar_Anchor(
                    ax=self.ax,
                    bounds=category_bounds,
                ).anchor(h_align=self.align.h_align)

            BasicDataLabeler(
                ax=self.ax,
                anchor=BDL_LabelAnchor(x=category_anchor.x, y=category_anchor.y),
                formatter=self.formatter,
                label=BDL_LabelProperties(
                    font=self.label.font,
                    size=self.label.size,
                    color=self.label.color,
                ),
                align=BDL_AlignProperties(
                    h_align=category_anchor.h_align,
                    v_align=category_anchor.v_align,
                    x_offset=self.align.x_offset,
                    y_offset=self.align.y_offset,
                ),
                gid="BarCategoryBasicDataLabel",
            ).draw(label=category_label)


class CBDL_Bar_Drawer:

    def __init__(self, ax: Axes, horizontal: bool) -> None:
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
        self._type: NumberFormat = "number"
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
        """
        Set the category basic data label properties.

        Parameters
        ----------
        font : FontProperties | None. Default is None.
            The font for the data label.
        size : int | None. Default is None.
            The font size for the data label.
        color : str | None. Default is None.
            The font color for the data label.

        Returns
        -------
        CBDL_Bar_Drawer
            The current instance for method chaining.
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
        """
        Set the category basic data label alignment properties.

        Parameters
        ----------
        h_align : {"left", "right", "center"}. Default is "center".
            The horizontal alignment for the data label. Valid only for vertical bars.
        v_align : {"top", "bottom", "center"}. Default is "center".
            The vertical alignment for the data label. Valid only for horizontal bars.
        x_offset : float. Default is 0.0.
            The horizontal offset for the data label.
        y_offset : float. Default is 0.0.
            The vertical offset for the data label.

        Returns
        -------
        CBDL_Bar_Drawer
            The current instance for method chaining.
        """

        self._h_align = h_align
        self._v_align = v_align
        self._x_offset = x_offset
        self._y_offset = y_offset
        return self

    def format(
        self,
        type: NumberFormat = "number",
        decimals: int = 0,
        separator: bool = False,
        currency: str | None = None,
        scale: ScaleType = "full",
    ) -> "CBDL_Bar_Drawer":
        """
        Set the category basic data label number format properties.

        Parameters
        ----------
        type : {"number", "percent"}. Default is "number".
            The number format type for the data label.
        decimals : int. Default is 0.
            The number of decimal places for the data label.
        separator : bool. Default is False.
            Whether to use a thousands separator for the data label.
        currency : str | None. Default is None.
            The currency symbol for the data label. Only used if type is "currency".
        scale : {"k", "m", "b", "t", "full", "auto"}. Default is "full".
            The scale for the data label.

        Returns
        -------
        CBDL_Bar_Drawer
            The current instance for method chaining.
        """

        self._type = type
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
        """
        Draw the category basic data label on the bars. Before calling draw(), ensure that
        all desired styling methods have been called to set up the data label appearance.

        Parameters
        ----------
        custom_label : dict[str, float] | None. Default is None.
            A dictionary mapping category indices to custom label values. If None,
            the total value for each category will be used as the label.
        clear : bool. Default is True.
            Clear existing category basic data labels before drawing new ones.
        """

        help = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "BarCategoryBasicDataLabel":
                    label.remove()

        formatter = NumberFormatter(
            properties=NumberProperties(
                type=self._type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        CBDL_Bar(
            ax=self.ax,
            horizontal=self.horizontal,
            help=help,
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
