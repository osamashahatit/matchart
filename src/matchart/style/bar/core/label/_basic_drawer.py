from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

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
from .._utils import BarPatchGenerator, BarStyleHelper
from ._basic_anchor import (
    HBarBDL_HAlign,
    HBarBDL_VAlign,
    VBarBDL_HAlign,
    VBarBDL_VAlign,
    BDL_BarBounds,
    BarBDL_AnchorResolver,
)


@dataclass(frozen=True)
class BarBDL_LabelProperties:
    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class BarBDL_AlignProperties:
    h_align: HBarBDL_HAlign | VBarBDL_HAlign
    v_align: HBarBDL_VAlign | VBarBDL_VAlign
    x_offset: float
    y_offset: float


class BarBasicDataLabeler:

    def __init__(
        self,
        ax: Axes,
        horizontal: bool,
        patches: BarPatchGenerator,
        help: BarStyleHelper,
        threshold: float,
        formatter: NumberFormatter,
        label: BarBDL_LabelProperties,
        align: BarBDL_AlignProperties,
    ):
        self.ax = ax
        self.horizontal = horizontal
        self.patches = patches.standard()
        self.help = help
        self.threshold = threshold
        self.formatter = formatter
        self.label = label
        self.align = align

    def draw(self) -> None:

        for patch in self.patches:
            if isinstance(patch, Rectangle):
                patch_bounds = patch.get_bbox()
                patch_label = self.help.get_patch_value(patch=patch)

                if abs(patch_label) > self.threshold:

                    anchor = BarBDL_AnchorResolver(
                        horizontal=self.horizontal,
                        bounds=BDL_BarBounds(
                            x_min=patch_bounds.x0,
                            y_min=patch_bounds.y0,
                            x_max=patch_bounds.x1,
                            y_max=patch_bounds.y1,
                        ),
                        v_align=self.align.v_align,
                        h_align=self.align.h_align,
                    ).resolve()

                    BasicDataLabeler(
                        ax=self.ax,
                        anchor=BDL_LabelAnchor(x=anchor.x, y=anchor.y),
                        align=BDL_AlignProperties(
                            h_align=anchor.h_align,
                            v_align=anchor.v_align,
                            x_offset=self.align.x_offset,
                            y_offset=self.align.y_offset,
                        ),
                        label=BDL_LabelProperties(
                            font=self.label.font,
                            size=self.label.size,
                            color=self.label.color,
                        ),
                        formatter=self.formatter,
                        gid="BarBasicDataLabel",
                    ).draw(label=patch_label)


class BarBDLDrawer:

    def __init__(self, ax: Axes, horizontal: bool) -> None:
        self.ax = ax
        self.horizontal = horizontal

        # Label properties
        self._font: FontProperties | None = None
        self._size: int | None = None
        self._color: str | None = None

        # Align properties
        self._h_align: HBarBDL_HAlign | VBarBDL_HAlign = "center"
        self._v_align: HBarBDL_VAlign | VBarBDL_VAlign = "center"
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
    ) -> "BarBDLDrawer":
        """Set the basic data label properties.

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
        BarBasicLabelDrawer
            The current instance for method chaining.
        """

        self._font = font
        self._size = size
        self._color = color
        return self

    def align(
        self,
        h_align: HBarBDL_HAlign | VBarBDL_HAlign = "center",
        v_align: HBarBDL_VAlign | VBarBDL_VAlign = "center",
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "BarBDLDrawer":
        """Set the basic data label alignment properties.

        Parameters
        ----------
        h_align : {"left", "right", "center", "outside"}. Default is "center".
            The horizontal alignment for the data label. "outside" is only valid for horizontal bars.
        v_align : {"top", "bottom", "center", "outside"}. Default is "center".
            The vertical alignment for the data label. "outside" is only valid for vertical bars.
        x_offset : float. Default is 0.0.
            The horizontal offset for the data label.
        y_offset : float. Default is 0.0.
            The vertical offset for the data label.

        Returns
        -------
        BarBasicLabelDrawer
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
    ) -> "BarBDLDrawer":
        """
        Set the data label number format properties.

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
        BarFDLDrawer
            The current instance for method chaining.
        """

        self._type = type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(self, hide_smallest: int = 0, clear: bool = True) -> None:
        """
        Draw the basic data labels on the bars. Before calling draw(), ensure that all desired
        styling methods have been called to set up the data label appearance.

        Parameters
        ----------
        hide_smallest : int. Default is 0.
            The number of smallest bars for which the data labels should be hidden
            based on their absolute values.
        clear : bool. Default is True.
            Clear existing basic data labels before drawing new ones.
        """

        help = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)
        patch_generator = BarPatchGenerator(ax=self.ax, horizontal=self.horizontal)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "BarBasicDataLabel":
                    label.remove()

        patches = list(patch_generator.standard())
        sorted_values = []
        for patch in patches:
            value = help.get_patch_value(patch)
            abs_value = abs(value)
            sorted_values.append(abs_value)
        sorted_values.sort()

        n_smallest = min(hide_smallest, len(patches))
        if n_smallest >= len(patches):
            threshold = float("inf")
        elif n_smallest == 0:
            threshold = 0
        else:
            threshold = sorted_values[n_smallest - 1]

        formatter = NumberFormatter(
            properties=NumberProperties(
                type=self._type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        BarBasicDataLabeler(
            ax=self.ax,
            horizontal=self.horizontal,
            patches=patch_generator,
            help=help,
            threshold=threshold,
            formatter=formatter,
            label=BarBDL_LabelProperties(
                font=self._font,
                size=self._size,
                color=self._color,
            ),
            align=BarBDL_AlignProperties(
                h_align=self._h_align,
                v_align=self._v_align,
                x_offset=self._x_offset,
                y_offset=self._y_offset,
            ),
        ).draw()
