from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties

from matchart.style.utils.data_label.basic_labeler import (
    BDL_AlignProperties,
    BDL_LabelAnchor,
    BDL_LabelProperties,
    BasicDataLabeler,
)

from matchart.style.utils.num_formatter import (
    ScaleType,
    NumberFormat,
    NumberProperties,
    NumberFormatter,
)

from ..._utils import LineGenerator
from ._basic_anchor import BDL_Line_Anchor


@dataclass(frozen=True)
class BDL_Line_LabelProperties:
    font: FontProperties | None
    size: int | None
    color: str | None


@dataclass(frozen=True)
class BDL_Line_AlignProperties:
    x_offset: float
    y_offset: float


class BDL_Line:
    def __init__(
        self,
        ax: Axes,
        lines: LineGenerator,
        formatter: NumberFormatter,
        label: BDL_Line_LabelProperties,
        align: BDL_Line_AlignProperties,
        select: list[str] | None,
    ):
        self.ax = ax
        self.lines = lines.standard()
        self.formatter = formatter
        self.label = label
        self.align = align
        self.select = select

    def draw(self) -> None:
        for line in self.lines:
            line_label = line.get_label()
            if self.select is not None:
                if line_label not in self.select:
                    continue
            anchor = BDL_Line_Anchor(line=line).anchor()
            for point in anchor:
                x, y = point
                BasicDataLabeler(
                    ax=self.ax,
                    anchor=BDL_LabelAnchor(x=x, y=y),
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
                ).draw(label=y)


class BDL_Line_Drawer:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

        # Label Propertoes
        self._font: FontProperties | None = None
        self._size: int | None = None
        self._color: str | None = None

        # Align properties
        self._x_offset: float = 0.0
        self._y_offset: float = 5.0

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
    ) -> "BDL_Line_Drawer":
        """
        Set the basic data label properties.

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
        BDL_Line_Drawer
            The current instance for method chaining.
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
        """
        Set the basic data label alignment properties.

        Parameters
        ----------
        x_offset : float. Default is 0.0.
            The horizontal offset for the data label.
        y_offset : float. Default is 0.0.
            The vertical offset for the data label.

        Returns
        -------
        BDL_Line_Drawer
            The current instance for method chaining.
        """

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
    ) -> "BDL_Line_Drawer":
        """
        Set the basic data label number format properties.

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
        BDL_Line_Drawer
            The current instance for method chaining.
        """

        self._type = type
        self._decimals = decimals
        self._separator = separator
        self._currency = currency
        self._scale = scale
        return self

    def draw(self, select: list[str] | None = None, clear: bool = True) -> None:
        """
        Draw the basic data label on the lines. Before calling draw(), ensure that
        all desired styling methods have been called to set up the data label appearance.

        Parameters
        ----------
        select : list[str] | None. Default is None.
            A list of line labels to draw data labels for. If None, data labels will be drawn.
        clear : bool. Default is True.
            Clear existing basic data labels before drawing new ones.
        """

        line_generator = LineGenerator(ax=self.ax)

        if clear:
            for label in self.ax.texts[:]:
                if label.get_gid() == "LineBasicDataLabel":
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

        BDL_Line(
            ax=self.ax,
            lines=line_generator,
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
