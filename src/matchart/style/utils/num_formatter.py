from typing import Literal
from dataclasses import dataclass
from matplotlib.ticker import FuncFormatter

type NumberFormat = Literal["number", "percent"]
type ScaleType = Literal["k", "m", "b", "t", "full", "auto"]


@dataclass(frozen=True)
class NumberProperties:
    """Encapsulates properties for number formatting."""

    type: NumberFormat
    decimals: int
    separator: bool
    currency: str | None
    scale: ScaleType


class ScaleResolver:
    """Resolves scale factors and suffixes for number formatting."""

    _SCALES: dict[int, str] = {
        1_000_000_000_000: "t",
        1_000_000_000: "b",
        1_000_000: "m",
        1_000: "k",
    }

    @classmethod
    def identify_scale(cls, value: float) -> str:
        """Identify the appropriate scale value for a given value."""

        absolute_value = abs(value)
        for threshold, suffix in cls._SCALES.items():
            if absolute_value >= threshold:
                return suffix
        return "full"

    @classmethod
    def get_factor_and_suffix(cls, scale: str) -> tuple[float, str]:
        """Get scale factor and suffix based on scale."""

        if scale == "full":
            return 1.0, ""
        for threshold, suffix in cls._SCALES.items():
            if suffix == scale:
                return float(threshold), scale.upper()
        return 1.0, ""


class NumberFormatter:
    """Formats numbers with various styles and scales."""

    def __init__(self, properties: NumberProperties) -> None:
        self.properties = properties
        self._format_string = self.build_format_string()

    def build_format_string(self) -> str:
        """Build format string for decimals and thousands separator."""

        decimal_string = f".{self.properties.decimals}f"
        return f",{decimal_string}" if self.properties.separator else decimal_string

    def format_percent(
        self,
        value: float,
        scale_factor: float,
        scale_suffix: str,
    ) -> str:
        """Format value as percentage."""

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
        """Format value as number or currency."""

        scaled_value = value / scale_factor
        formatted_number = format(scaled_value, self._format_string)
        currency = self.properties.currency or ""
        return f"{currency}{formatted_number}{scale_suffix}"

    def format(self, value: float, position: int | None = None) -> str:
        """Format a single number value."""

        scale = (
            ScaleResolver.identify_scale(value)
            if self.properties.scale == "auto"
            else self.properties.scale
        )
        (
            scale_factor,
            scale_suffix,
        ) = ScaleResolver.get_factor_and_suffix(scale)

        if self.properties.type == "percent":
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

    def formatter(self) -> FuncFormatter:
        """Convert to matplotlib FuncFormatter."""

        return FuncFormatter(self.format)
