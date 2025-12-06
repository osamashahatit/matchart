from typing import Literal, Sequence
from dataclasses import dataclass
from matplotlib.axis import Axis, XAxis, YAxis
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text
from matplotlib.transforms import Affine2D
from matplotlib.ticker import FuncFormatter, FixedLocator, FixedFormatter, Formatter

from matchart.style.utils.num_formatter import (
    NumberFormat,
    ScaleType,
    NumberProperties,
    NumberFormatter,
)

type HorizontalAlignment = Literal["left", "center", "right"]
type VerticalAlignment = Literal[
    "bottom",
    "baseline",
    "center",
    "center_baseline",
    "top",
]


@dataclass(frozen=True)
class LabelProperties:
    """Encapsulates properties for label styling."""

    font: FontProperties | None
    size: int | None
    color: str | None
    va: VerticalAlignment | None
    ha: HorizontalAlignment | None
    rotation: float | None


@dataclass(frozen=True)
class PadSettings:
    """Settings for padding tick label."""

    direction: float
    index: int


class PadResolver:
    """Resolves padding direction based on axis position."""

    def __init__(self, axis: Axis) -> None:
        self.axis = axis

    _YAXIS_PAD_MAP = {
        "left": -1,
        "right": 1,
        "both": -1,
        "none": -1,
    }

    _XAXIS_PAD_MAP = {
        "bottom": -1,
        "top": 1,
        "both": -1,
        "none": -1,
    }

    def resolve(self) -> PadSettings:
        """Resolve pad settings for an axis."""

        if isinstance(self.axis, XAxis):
            position = self.axis.get_ticks_position()
            direction = self._XAXIS_PAD_MAP.get(position, -1)
            index = 1
        elif isinstance(self.axis, YAxis):
            position = self.axis.get_ticks_position()
            direction = self._YAXIS_PAD_MAP.get(position, -1)
            index = 0
        else:
            direction = -1
            index = 0

        return PadSettings(
            direction=direction,
            index=index,
        )


class LabelStyler:
    """Applies styling to tick label."""

    def __init__(self, labels: Sequence[Text], properties: LabelProperties) -> None:
        self.labels = labels
        self.properties = properties

    def set_font_properties(self) -> None:
        """Apply font-related properties."""

        for label in self.labels:
            if self.properties.font is not None:
                label.set_fontproperties(self.properties.font)
            if self.properties.size is not None:
                label.set_fontsize(self.properties.size)
            if self.properties.color is not None:
                label.set_color(self.properties.color)
            if self.properties.rotation is not None:
                label.set_rotation(self.properties.rotation)

    def set_alignment(self) -> None:
        """Apply alignment properties."""

        if self.properties.va is not None:
            for label in self.labels:
                label.set_verticalalignment(self.properties.va)
        if self.properties.ha is not None:
            for label in self.labels:
                label.set_horizontalalignment(self.properties.ha)

    def style(self) -> None:
        """Apply styling to all labels."""

        self.set_font_properties()
        self.set_alignment()


class PadStyler:
    """Handles padding adjustments for tick labels."""

    def __init__(
        self,
        labels: Sequence[Text],
        pad: float,
        settings: PadSettings,
    ) -> None:
        self.labels = labels
        self.pad = pad
        self.settings = settings

    def set_pad(self) -> None:
        """Apply padding offset to tick labels."""

        pad_value = self.pad * 10 * self.settings.direction
        x_pad = pad_value if self.settings.index == 0 else 0
        y_pad = pad_value if self.settings.index == 1 else 0
        for label in self.labels:
            offset = Affine2D().translate(x_pad, y_pad)
            label.set_transform(label.get_transform() + offset)


class TruncateFormatter:
    """Handles truncation of tick labels."""

    def __init__(self, max_characters: int, formatter_getter: Formatter) -> None:
        self.max_characters = max_characters
        self.formatter_getter = formatter_getter

    def format(self, value: float, position: int | None = None) -> str:
        """Format and truncate tick label."""

        label = str(self.formatter_getter(value, position))
        return (
            label
            if len(label) <= self.max_characters
            else f"{label[:self.max_characters]}…"
        )

    def formatter(self) -> FuncFormatter:
        """Truncate formatter for tick labels."""

        return FuncFormatter(self.format)


class CustomLabelFormatter:
    """Handles custom tick labels and positions."""

    def __init__(self, custom_labels: Sequence[int | float | str]):
        self.custom_labels = custom_labels
        self._labels = [str(label) for label in custom_labels]
        self._positions = self.determine_positions()

    def determine_positions(self) -> list[float]:
        """Determine tick positions from labels."""

        try:
            return [float(label) for label in self.custom_labels]
        except (ValueError, TypeError):
            return list(range(len(self.custom_labels)))

    def locator(self) -> FixedLocator:
        """Locator for tick positions."""

        return FixedLocator(self._positions)

    def formatter(self) -> FixedFormatter:
        """Custom labels formatter for tick labels."""

        return FixedFormatter(self._labels)


class MajorLabelDrawer:
    """Drawer for major tick labels."""

    def __init__(self, axis: Axis) -> None:
        self.axis = axis

    def enable(self, show: bool = True) -> "MajorLabelDrawer":
        """
        Enable or disable the visibility of major tick labels.

        Parameters
        ----------
        show : bool, default=True
            Whether to display (`True`) or hide (`False`) the major tick labels.

        Returns
        -------
        MajorLabelDrawer
            The current instance for method chaining.
        """

        labels = self.axis.get_majorticklabels()
        for label in labels:
            label.set_visible(show)
        return self

    def draw(
        self,
        font: FontProperties | None = None,
        size: int | None = None,
        color: str | None = None,
        rotation: float | None = None,
        pad: float | None = None,
        va: VerticalAlignment | None = None,
        ha: HorizontalAlignment | None = None,
        truncate: int | None = None,
        custom_labels: Sequence[int | float | str] | None = None,
    ) -> "MajorLabelDrawer":
        """
        Apply label styling and customization to major tick labels.

        This method allows control over font appearance, alignment,
        padding, truncation, and the use of custom tick labels.

        Parameters
        ----------
        font : FontProperties. Default=None
            Font of the tick labels.
        size : int. Default=None
            Size of the tick labels.
        color : str. Default=None
            Color of the tick labels.
        rotation : float. Default=None
            Rotation of the tick labels.
        pad : float. Default=None
            Pad distance between tick marker and label.
        va : {"top", "center", "bottom", "baseline"}. Default=None
            Vertical alignment of the tick labels.
        ha : {"left", "center", "right"}. Default=None
            Horizontal alignment of the tick labels.
        truncate : int. Default=None
            Maximum number of characters per label before truncation.
            Longer labels are truncated and suffixed with “…” (ellipsis).
        custom_labels : sequence of int, float, or str. Default=None
            Custom tick labels.

        Returns
        -------
        MajorLabelDrawer
            The current instance for method chaining.
        """

        if custom_labels is not None:
            self.axis.set_major_locator(
                CustomLabelFormatter(custom_labels=custom_labels).locator()
            )
            self.axis.set_major_formatter(
                CustomLabelFormatter(custom_labels=custom_labels).formatter()
            )

        if truncate is not None:
            truncator = TruncateFormatter(
                max_characters=truncate,
                formatter_getter=self.axis.get_major_formatter(),
            )
            self.axis.set_major_formatter(truncator.formatter())

        labels = self.axis.get_majorticklabels()

        if pad is not None:
            settings = PadResolver(self.axis).resolve()
            PadStyler(labels=labels, pad=pad, settings=settings).set_pad()

        properties = LabelProperties(
            font=font,
            size=size,
            color=color,
            rotation=rotation,
            va=va,
            ha=ha,
        )
        LabelStyler(labels=labels, properties=properties).style()
        return self

    def format(
        self,
        type: NumberFormat = "number",
        decimals: int = 0,
        separator: bool = False,
        currency: str | None = None,
        scale: ScaleType = "full",
    ) -> "MajorLabelDrawer":
        """
        Apply number formatting for major tick labels.

        Parameters
        ----------
        type : {"number", "percent"}, default="number"
            Type of numeric format to apply.
        decimals : int, default=0
            Number of decimal places.
        separator : bool, default=False
            Whether to include a thousands separator.
        currency : str. Default=None
            Currency prefix.
        scale : ScaleType, default="full"
            Scale factor for numeric values:
            - "k": thousands
            - "m": millions
            - "b": billions
            - "t": trillions
            - "auto": automatically infer scale from data
            - "full": no scaling

        Returns
        -------
        MajorLabelDrawer
            The current instance for method chaining.
        """

        properties = NumberProperties(
            type=type,
            decimals=decimals,
            separator=separator,
            currency=currency,
            scale=scale,
        )
        self.axis.set_major_formatter(NumberFormatter(properties).formatter())
        return self
