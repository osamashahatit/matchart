"""Draw bar chart standard basic data labels."""

from dataclasses import dataclass
from typing import cast

from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

from matchart.style.bar.core._utils import BarPatchYielder, BarStyleHelper
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
    BDL_Bar_Bounds,
    BDL_HBar_Anchor,
    BDL_HBar_HAlign,
    BDL_HBar_VAlign,
    BDL_VBar_Anchor,
    BDL_VBar_HAlign,
    BDL_VBar_VAlign,
)


@dataclass(frozen=True)
class BDL_Bar_LabelProperties:
    """Configure bar label font appearance."""

    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class BDL_Bar_AlignProperties:
    """Configure bar label alignment and offsets."""

    h_align: BDL_HBar_HAlign | BDL_VBar_HAlign
    v_align: BDL_HBar_VAlign | BDL_VBar_VAlign
    x_offset: float
    y_offset: float


class BDL_Bar:
    """Iterate bar patches on an Axes and draw numeric labels.

    This class is the internal worker used by BDL_Bar_Drawer. It computes
    bounds/anchors per bar and delegates text creation to BasicDataLabeler.
    """

    def __init__(
        self,
        ax: Axes,
        horizontal: bool,
        patches: BarPatchYielder,
        helper: BarStyleHelper,
        threshold: float,
        formatter: NumberFormatter,
        label: BDL_Bar_LabelProperties,
        align: BDL_Bar_AlignProperties,
    ):
        """
        Args:
            ax (Axes): Target axes that already contains bar artists.
            horizontal (bool): Whether the bar chart is horizontal.
            patches (BarPatchYielder): Patch yielder for bar patches.
            helper (BarStyleHelper): Helper class.
            threshold (float): Minimum absolute bar value required for a label
                to be drawn. A label is drawn only when abs(value) > threshold.
            formatter (NumberFormatter): Number formatter.
            label (BDL_Bar_LabelProperties): Label appearance configuration.
            align (BDL_Bar_AlignProperties): Alignment and offset configuration.
        """
        self.ax = ax
        self.horizontal = horizontal
        self.patches = patches.standard()
        self.helper = helper
        self.threshold = threshold
        self.formatter = formatter
        self.label = label
        self.align = align

    def draw(self) -> None:
        """Draw labels for bars that exceed the configured threshold.

        Notes:
            This method mutates the Axes by adding Text artists. It does not
            return self (not chainable).
        """
        for patch in self.patches:
            if isinstance(patch, Rectangle):
                patch_value = self.helper.get_patch_value(patch=patch)

                # Skip small bars using absolute-value thresholding.
                if abs(patch_value) > self.threshold:
                    bbox = patch.get_bbox()
                    bounds = BDL_Bar_Bounds(
                        x_min=bbox.x0,
                        y_min=bbox.y0,
                        x_max=bbox.x1,
                        y_max=bbox.y1,
                    )

                    # Compute anchor differently for horizontal vs. vertical
                    # bars so alignment literals stay correct for each mode.
                    if self.horizontal:
                        anchor = BDL_HBar_Anchor(bounds=bounds).anchor(
                            h_align=self.align.h_align,
                            v_align=cast(BDL_HBar_VAlign, self.align.v_align),
                        )
                    else:
                        anchor = BDL_VBar_Anchor(bounds=bounds).anchor(
                            h_align=cast(BDL_VBar_HAlign, self.align.h_align),
                            v_align=self.align.v_align,
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
                            h_align=anchor.h_align,
                            v_align=anchor.v_align,
                            x_offset=self.align.x_offset,
                            y_offset=self.align.y_offset,
                        ),
                        gid="BarBasicDataLabel",
                    ).draw(label=patch_value)


class BDL_Bar_Drawer:
    """Configure and draw basic data labels for bar charts.

    This is the user-facing builder used by higher-level bar chart APIs.

    The drawer reads bar patches from the provided Axes and draws labels
    using BasicDataLabeler. It can optionally clear previously drawn bar
    labels (identified by gid) before drawing new ones.
    """

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
        self._h_align: BDL_HBar_HAlign | BDL_VBar_HAlign = "center"
        self._v_align: BDL_HBar_VAlign | BDL_VBar_VAlign = "center"
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
    ) -> "BDL_Bar_Drawer":
        """Set label font properties.

        Args:
            font (FontProperties | None): Font style. If None, Matplotlib
                defaults are used.
            size (int | None): Font size. If None, Matplotlib defaults
                are used.
            color (str | None): Font color. If None, Matplotlib defaults
                are used.

        Returns:
            BDL_Bar_Drawer: The current instance for method chaining.
        """
        self._font = font
        self._size = size
        self._color = color
        return self

    def align(
        self,
        h_align: BDL_HBar_HAlign | BDL_VBar_HAlign = "center",
        v_align: BDL_HBar_VAlign | BDL_VBar_VAlign = "center",
        x_offset: float = 0.0,
        y_offset: float = 0.0,
    ) -> "BDL_Bar_Drawer":
        """Set label alignment and offsets.

        Args:
            h_align (BDL_HBar_HAlign | BDL_VBar_HAlign): Horizontal alignment.
                Options: "left", "right", "center", "outside".
            v_align (BDL_HBar_VAlign | BDL_VBar_VAlign): Vertical alignment.
                Options: "top", "bottom", "center", "outside".
            x_offset (float): Offset applied from anchor x coordinate.
            y_offset (float): Offset applied from anchor y coordinate.

        Returns:
            BDL_Bar_Drawer: The current instance for method chaining.
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
    ) -> "BDL_Bar_Drawer":
        """Configure numeric formatting for bar labels.

        Args:
            format_type (NumberFormat): Numeric formatting mode.
                Options: "number", "percent".
            decimals (int): Number of decimal places to display.
            separator (bool): Whether to use thousands separators.
            currency (str | None): Optional currency symbol/code.
            scale (ScaleType): Scaling mode for large numbers.
                Options: "k", "m", "b", "t", "full", "auto".

        Returns:
            BDL_Bar_Drawer: The current instance for method chaining.
        """
        self._format_type = format_type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(self, hide_smallest: int = 0, clear: bool = True) -> None:
        """Draw bar value labels onto the Axes.

        Args:
            hide_smallest (int): Number of smallest bars (by absolute value)
                to omit labels for. If 0, no bars are omitted.
            clear (bool): If True, remove existing labels previously drawn by
                this drawer (identified by gid "BarBasicDataLabel").

        Notes:
            This method mutates the Axes by removing and adding Text artists.
            It does not return self (not chainable).
        """
        helper = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)
        patch_yielder = BarPatchYielder(ax=self.ax, horizontal=self.horizontal)

        if clear:
            # Only remove labels created by this helper (identified by gid).
            for label in self.ax.texts[:]:
                if label.get_gid() == "BarBasicDataLabel":
                    label.remove()

        patches = list(patch_yielder.standard())

        # Determine the absolute-value threshold implied by hide_smallest.
        sorted_values: list[float] = []
        for patch in patches:
            value = helper.get_patch_value(patch)
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
                format_type=self._format_type,
                decimals=self._decimals,
                separator=self._separator,
                currency=self._currency,
                scale=self._scale,
            )
        )

        BDL_Bar(
            ax=self.ax,
            horizontal=self.horizontal,
            patches=patch_yielder,
            helper=helper,
            threshold=threshold,
            formatter=formatter,
            label=BDL_Bar_LabelProperties(
                font=self._font,
                size=self._size,
                color=self._color,
            ),
            align=BDL_Bar_AlignProperties(
                h_align=self._h_align,
                v_align=self._v_align,
                x_offset=self._x_offset,
                y_offset=self._y_offset,
            ),
        ).draw()
