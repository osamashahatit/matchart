"""Set explicit minimum and/or maximum limits for an axis range."""

from typing import Callable


class AxisRangeDrawer:
    """Apply explicit minimum and/or maximum bounds to an axis."""

    def __init__(
        self,
        limit_getter: Callable[[], tuple[float, float]],
        limit_setter: Callable[[float, float], tuple[float, float]],
    ) -> None:
        """
        Args:
            limit_getter (Callable[[], tuple[float, float]]): Callable that
                returns the current (min, max) axis limits.
            limit_setter (Callable[[float, float], tuple[float, float]]):
                Callable that applies new (min, max) axis limits.
        """
        self.limit_getter = limit_getter
        self.limit_setter = limit_setter

    def draw(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> None:
        """Set the axis range minimum and/or maximum.

        Args:
            min_value (float | None): New minimum value for the axis.
                If None, the current minimum is preserved.
            max_value (float | None): New maximum value for the axis.
                If None, the current maximum is preserved.

        Returns:
            None: Axis limits are updated via the setter callable.

        Raises:
            ValueError: If min_value > max_value or if both are None.
        """
        current_min, current_max = self.limit_getter()

        new_min = min_value if min_value is not None else current_min
        new_max = max_value if max_value is not None else current_max

        if min_value is None and max_value is None:
            raise ValueError("At least one of min_value or max_value must be provided.")

        if new_min >= new_max:
            raise ValueError("min_value must be less than max_value.")

        self.limit_setter(new_min, new_max)
