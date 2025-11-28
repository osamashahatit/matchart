from typing import Callable


class AxisRangeDrawer:
    def __init__(
        self,
        limit_getter: Callable[[], tuple[float, float]],
        limit_setter: Callable[[float, float], tuple[float, float]],
    ) -> None:
        self.limit_getter = limit_getter
        self.limit_setter = limit_setter

    def draw(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> None:
        """
        Draw the axis range by setting new minimum and/or maximum values.

        Parameters
        ----------
        min_value : float or None. Default is None.
            The new minimum value for the axis range.
        max_value : float or None. Default is None.
            The new maximum value for the axis range.
        """

        current_min, current_max = self.limit_getter()
        new_min = min_value if min_value is not None else current_min
        new_max = max_value if max_value is not None else current_max
        self.limit_setter(new_min, new_max)
