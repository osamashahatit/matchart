"""Format numeric labels.

Matplotlib exposes flexible formatter hooks, but writing consistent
number formatting logic (decimals, thousands separators, currency, and
human-friendly scaling like K/M/B/T) is repetitive and error-prone. This
module provides a small, reusable formatter that converts numeric values
into display strings and exposes a Matplotlib FuncFormatter for easy
integration in axis styling across matchart.
"""

from dataclasses import dataclass
from typing import Literal

from matplotlib.ticker import FuncFormatter

type NumberFormat = Literal["number", "percent"]
type ScaleType = Literal["k", "m", "b", "t", "full", "auto"]


@dataclass(frozen=True)
class NumberProperties:
    """Store configuration for number formatting.

    Attributes:
        format_type (NumberFormat): Whether to format as a number or percent.
        decimals (int): Number of decimal places to display.
        separator (bool): Whether to include thousands separators.
        currency (str | None): Optional currency prefix (e.g., "$").
        scale (ScaleType): Scaling mode ("full", fixed suffix, or "auto").
    """

    format_type: NumberFormat
    decimals: int
    separator: bool
    currency: str | None
    scale: ScaleType


class ScaleResolver:
    """Resolve scale suffixes and factors used for number formatting."""

    _SCALES: dict[int, str] = {
        1_000_000_000_000: "t",
        1_000_000_000: "b",
        1_000_000: "m",
        1_000: "k",
    }

    @classmethod
    def detect_scale(cls, value: float) -> str:
        """Detect the appropriate scale suffix for a value.

        Args:
            value (float): Numeric value to inspect.

        Returns:
            str: One of "t", "b", "m", "k", or "full".
        """
        absolute_value = abs(value)
        for threshold, suffix in cls._SCALES.items():
            if absolute_value >= threshold:
                return suffix
        return "full"

    @classmethod
    def get_factor_and_suffix(cls, scale: str) -> tuple[float, str]:
        """Return scale factor and display suffix for a scale key.

        Args:
            scale (str): Scale key such as "k", "m", "b", "t", or "full".

        Returns:
            tuple[float, str]: (scale_factor, scale_suffix) where scale_factor
            is the divisor applied to the raw value and scale_suffix is the
            display suffix (e.g., "K", "M").
        """
        if scale == "full":
            return 1.0, ""

        for threshold, suffix in cls._SCALES.items():
            if suffix == scale:
                return float(threshold), scale.upper()

        return 1.0, ""


class NumberFormatter:
    """Format numbers for display and expose a Matplotlib FuncFormatter."""

    def __init__(self, properties: NumberProperties) -> None:
        """
        Args:
            properties (NumberProperties): Formatting configuration.
        """
        self.properties = properties
        self._format_string = self.build_format_string()

    def build_format_string(self) -> str:
        """Build a Python format specifier for decimals and separators.

        Returns:
            str: A format specifier compatible with format(value, spec).
        """
        decimal_string = f".{self.properties.decimals}f"
        return f",{decimal_string}" if self.properties.separator else decimal_string

    def format_percent(
        self,
        value: float,
        scale_factor: float,
        scale_suffix: str,
    ) -> str:
        """Format a value as a percentage.

        Args:
            value (float): Raw numeric value (e.g., 0.25 for 25%).
            scale_factor (float): Divisor applied after converting to percent.
            scale_suffix (str): Display suffix (e.g., "K").

        Returns:
            str: Formatted percent string.
        """
        percent_value = value * 100.0
        scaled_value = percent_value / scale_factor
        formatted_number = format(scaled_value, self._format_string)
        return f"{formatted_number}{scale_suffix}%"

    def format_number(
        self,
        value: float,
        scale_factor: float,
        scale_suffix: str,
    ) -> str:
        """Format a value as a number or currency.

        Args:
            value (float): Raw numeric value.
            scale_factor (float): Divisor applied for scaling.
            scale_suffix (str): Display suffix (e.g., "M").

        Returns:
            str: Formatted number string, optionally prefixed with currency.
        """
        scaled_value = value / scale_factor
        formatted_number = format(scaled_value, self._format_string)
        currency = self.properties.currency or ""
        return f"{currency}{formatted_number}{scale_suffix}"

    def format(self, value: float, _: int | None = None) -> str:
        """Format a single numeric value.

        This signature matches Matplotlib's formatter callback convention.

        Args:
            value (float): Tick value provided by Matplotlib.
            _ (int | None): Tick position (ignored).

        Returns:
            str: Formatted tick label string.
        """
        scale = (
            ScaleResolver.detect_scale(value)
            if self.properties.scale == "auto"
            else self.properties.scale
        )
        scale_factor, scale_suffix = ScaleResolver.get_factor_and_suffix(scale)

        if self.properties.format_type == "percent":
            return self.format_percent(
                value=value,
                scale_factor=scale_factor,
                scale_suffix=scale_suffix,
            )

        return self.format_number(
            value=value,
            scale_factor=scale_factor,
            scale_suffix=scale_suffix,
        )

    def create_formatter(self) -> FuncFormatter:
        """Create a Matplotlib FuncFormatter for the NumberFormatter.

        Returns:
            FuncFormatter: Formatter that calls NumberFormatter.format.
        """
        return FuncFormatter(self.format)
