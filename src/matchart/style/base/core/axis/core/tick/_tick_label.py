"""Style and format Matplotlib tick labels."""

from dataclasses import dataclass
from typing import Literal, Sequence

from matplotlib.axis import Axis, XAxis, YAxis
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text
from matplotlib.ticker import FixedFormatter, FixedLocator, Formatter, FuncFormatter
from matplotlib.transforms import Affine2D

from matchart.style.utils.num_formatter import (
    NumberFormat,
    NumberFormatter,
    NumberProperties,
    ScaleType,
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
    """Store styling properties for tick label Text artists."""

    font: FontProperties | None
    size: int | None
    color: str | None
    v_align: VerticalAlignment | None
    h_align: HorizontalAlignment | None
    rotation: float | None


@dataclass(frozen=True)
class PadSettings:
    """Store resolved padding direction and axis index for transforms.

    Attributes:
        direction (float): Direction multiplier (typically -1 or 1).
        index (int): Which coordinate to translate:
            - 0: translate x
            - 1: translate y
    """

    direction: float
    index: int


class PadResolver:
    """Resolve padding direction/index based on whether ticks are on x or y axis."""

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

    def __init__(self, axis: Axis) -> None:
        """
        Args:
            axis (Axis): Matplotlib axis (XAxis or YAxis) to inspect.
        """
        self.axis = axis

    def resolve(self) -> PadSettings:
        """Resolve pad settings for an axis.

        Returns:
            PadSettings: Direction and index used by PadStyler to apply an
            affine translation to tick label transforms.
        """
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

        return PadSettings(direction=direction, index=index)


class LabelStyler:
    """Apply font, color, rotation, and alignment to tick label Text artists."""

    def __init__(self, labels: Sequence[Text], properties: LabelProperties) -> None:
        """
        Args:
            labels (Sequence[Text]): Tick label Text artists to style.
            properties (LabelProperties): Styling properties to apply.
        """
        self.labels = labels
        self.properties = properties

    def set_font_properties(self) -> None:
        """Apply font-related properties (font, size, color, rotation)."""
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
        """Apply alignment properties (vertical and horizontal alignment)."""
        if self.properties.v_align is not None:
            for label in self.labels:
                label.set_verticalalignment(self.properties.v_align)
        if self.properties.h_align is not None:
            for label in self.labels:
                label.set_horizontalalignment(self.properties.h_align)

    def style(self) -> None:
        """Apply all configured styling properties to the labels."""
        self.set_font_properties()
        self.set_alignment()


class PadStyler:
    """Apply padding offsets to tick labels by translating their transforms."""

    def __init__(
        self,
        labels: Sequence[Text],
        pad: float,
        settings: PadSettings,
    ) -> None:
        """
        Args:
            labels (Sequence[Text]): Tick label Text artists to adjust.
            pad (float): Padding amount (interpreted via internal scaling).
            settings (PadSettings): Resolved direction and axis index.
        """
        self.labels = labels
        self.pad = pad
        self.settings = settings

    def set_pad(self) -> None:
        """Apply the padding offset to tick labels.

        Notes:
            Padding is applied by translating the Text transform, not by
            changing Matplotlib's tick label padding settings.
        """
        pad_value = self.pad * 10 * self.settings.direction
        x_pad = pad_value if self.settings.index == 0 else 0
        y_pad = pad_value if self.settings.index == 1 else 0

        for label in self.labels:
            offset = Affine2D().translate(x_pad, y_pad)
            label.set_transform(label.get_transform() + offset)


class TruncateFormatter:
    """Wrap an existing formatter and truncate its output to a max length."""

    def __init__(self, max_characters: int, base_formatter: Formatter) -> None:
        """
        Args:
            max_characters (int): Maximum number of characters before truncation.
            base_formatter (Formatter): Callable formatter used to produce the
                original label string.
        """
        self.max_characters = max_characters
        self.base_formatter = base_formatter

    def format(self, value: float, position: int | None = None) -> str:
        """Format and truncate a tick label.

        Args:
            value (float): Tick value provided by Matplotlib.
            position (int | None): Tick position (passed through).

        Returns:
            str: Formatted label, truncated and suffixed with "…" when needed.
        """
        label = str(self.base_formatter(value, position))
        return (
            label
            if len(label) <= self.max_characters
            else f"{label[: self.max_characters]}…"
        )

    def create_formatter(self) -> FuncFormatter:
        """Create a Matplotlib FuncFormatter that truncates labels.

        Returns:
            FuncFormatter: Formatter that calls TruncateFormatter.format().
        """
        return FuncFormatter(self.format)


class CustomLabelFormatter:
    """Provide FixedLocator and FixedFormatter for custom tick labels."""

    def __init__(self, custom_labels: Sequence[int | float | str]):
        """
        Args:
            custom_labels (Sequence[int | float | str]): Sequence of labels.
                If all labels can be cast to float, those floats are used
                as tick positions; otherwise positions are 0..N-1.
        """
        self.custom_labels = custom_labels
        self._labels = [str(label) for label in custom_labels]
        self._positions = self.determine_positions()

    def determine_positions(self) -> list[float]:
        """Determine tick positions from the provided labels.

        Returns:
            list[float]: Positions for FixedLocator.
        """
        try:
            return [float(label) for label in self.custom_labels]
        except (ValueError, TypeError):
            return list(range(len(self.custom_labels)))

    def locator(self) -> FixedLocator:
        """Create a locator for the custom tick positions.

        Returns:
            FixedLocator: Locator configured with the resolved positions.
        """
        return FixedLocator(self._positions)

    def formatter(self) -> FixedFormatter:
        """Create a formatter for the custom tick labels.

        Returns:
            FixedFormatter: Formatter configured with the string labels.
        """
        return FixedFormatter(self._labels)


class MajorLabelDrawer:
    """Enable, style, truncate, and format major tick labels on an Axis."""

    def __init__(self, axis: Axis) -> None:
        """
        Args:
            axis (Axis): Matplotlib Axis (xaxis or yaxis) to modify.
        """
        self.axis = axis

    def enable(self, show: bool = True) -> "MajorLabelDrawer":
        """Enable or disable the visibility of major tick labels.

        Args:
            show (bool): Whether to display (True) or hide (False) the major
                tick labels.

        Returns:
            MajorLabelDrawer: The current instance for method chaining.
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
        v_align: VerticalAlignment | None = None,
        h_align: HorizontalAlignment | None = None,
        truncate: int | None = None,
        custom_labels: Sequence[int | float | str] | None = None,
    ) -> "MajorLabelDrawer":
        """Apply styling and customization to major tick labels.

        Args:
            font (FontProperties | None): Optional font configuration.
            size (int | None): Optional font size in points.
            color (str | None): Optional text color.
            rotation (float | None): Optional rotation in degrees.
            pad (float | None): Optional padding amount applied via a transform.
            v_align (VerticalAlignment | None): Optional vertical alignment.
                Options: "bottom", "baseline", "center", "center_baseline", "top".
            h_align (HorizontalAlignment | None): Optional horizontal alignment.
                Options: "left", "center", "right".
            truncate (int | None): Maximum number of characters per label before
                truncation. Longer labels are truncated and suffixed with "…".
            custom_labels (Sequence[int | float | str] | None): Optional custom
                tick labels. If numeric-castable, they are also used as tick
                positions; otherwise positions are 0..N-1.

        Returns:
            MajorLabelDrawer: The current instance for method chaining.
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
                base_formatter=self.axis.get_major_formatter(),
            )
            self.axis.set_major_formatter(truncator.create_formatter())

        labels = self.axis.get_majorticklabels()

        if pad is not None:
            settings = PadResolver(self.axis).resolve()
            PadStyler(labels=labels, pad=pad, settings=settings).set_pad()

        properties = LabelProperties(
            font=font,
            size=size,
            color=color,
            rotation=rotation,
            v_align=v_align,
            h_align=h_align,
        )
        LabelStyler(labels=labels, properties=properties).style()
        return self

    def format(
        self,
        format_type: NumberFormat = "number",
        decimals: int = 0,
        separator: bool = False,
        currency: str | None = None,
        scale: ScaleType = "full",
    ) -> "MajorLabelDrawer":
        """Apply numeric formatting for major tick labels.

        Args:
            format_type (NumberFormat): Numeric format mode.
                Options: "number", "percent".
            decimals (int): Number of decimal places.
            separator (bool): Whether to include a thousands separator.
            currency (str | None): Optional currency prefix (e.g., "$").
            scale (ScaleType): Scaling mode for numeric values.
                Options: "k", "m", "b", "t", "full", "auto".

        Returns:
            MajorLabelDrawer: The current instance for method chaining.
        """
        properties = NumberProperties(
            format_type=format_type,
            decimals=decimals,
            separator=separator,
            currency=currency,
            scale=scale,
        )
        self.axis.set_major_formatter(NumberFormatter(properties).create_formatter())
        return self
