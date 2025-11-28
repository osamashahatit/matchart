from matplotlib.axes import Axes


class MarginHelpers:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def get_axis_limits(self) -> tuple[float, float, float, float]:
        """Get the current axis limits of the Axes object."""

        x_axis_min, x_axis_max = self.ax.get_xlim()
        y_axis_min, y_axis_max = self.ax.get_ylim()
        return (
            x_axis_min,
            x_axis_max,
            y_axis_min,
            y_axis_max,
        )

    def get_data_box_bounds(self) -> tuple[float, float, float, float]:
        """Get the data bounding box limits of the Axes object."""

        data_box_bounds = self.ax.dataLim
        if data_box_bounds.width == 0 and data_box_bounds.height == 0:
            return self.get_axis_limits()

        data_box_min_x = data_box_bounds.x0
        data_box_max_x = data_box_bounds.x1
        data_box_min_y = data_box_bounds.y0
        data_box_max_y = data_box_bounds.y1
        return (
            data_box_min_x,
            data_box_max_x,
            data_box_min_y,
            data_box_max_y,
        )

    def convert_percent_to_data_units(
        self,
        left: float | None,
        right: float | None,
        top: float | None,
        bottom: float | None,
    ) -> tuple[float, float, float, float]:
        """Convert relative percentage margins into absolute data-unit margins."""

        (
            data_box_min_x,
            data_box_max_x,
            data_box_min_y,
            data_box_max_y,
        ) = self.get_data_box_bounds()
        x_data_box_range = (
            data_box_max_x - data_box_min_x if data_box_max_x != data_box_min_x else 1.0
        )
        y_data_box_range = (
            data_box_max_y - data_box_min_y if data_box_max_y != data_box_min_y else 1.0
        )

        left_margin = (left or 0.0) * x_data_box_range
        right_margin = (right or 0.0) * x_data_box_range
        top_margin = (top or 0.0) * y_data_box_range
        bottom_margin = (bottom or 0.0) * y_data_box_range
        return (
            left_margin,
            right_margin,
            top_margin,
            bottom_margin,
        )


class AxisMargin:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def draw(
        self,
        left: float | None = None,
        right: float | None = None,
        top: float | None = None,
        bottom: float | None = None,
    ):
        """
        Draw margins around the data bounding box of the Matplotlib Axes object.

        Parameters
        ----------
        left : float or None. Default is None.
            Left margin as a fraction of the data bounding box width.
        right : float or None. Default is None.
            Right margin as a fraction of the data bounding box width.
        top : float or None. Default is None.
            Top margin as a fraction of the data bounding box height.
        bottom : float or None. Default is None.
            Bottom margin as a fraction of the data bounding box height.
        """

        help = MarginHelpers(self.ax)
        (
            x_axis_min,
            x_axis_max,
            y_axis_min,
            y_axis_max,
        ) = help.get_axis_limits()
        (
            data_box_min_x,
            data_box_max_x,
            data_box_min_y,
            data_box_max_y,
        ) = help.get_data_box_bounds()
        (
            left_margin,
            right_margin,
            top_margin,
            bottom_margin,
        ) = help.convert_percent_to_data_units(
            left=left,
            right=right,
            top=top,
            bottom=bottom,
        )

        if left is not None or right is not None:
            new_data_box_min_x = (
                data_box_min_x - left_margin if left is not None else x_axis_min
            )
            new_data_box_max_x = (
                data_box_max_x + right_margin if right is not None else x_axis_max
            )
            self.ax.set_xlim(
                new_data_box_min_x,
                new_data_box_max_x,
            )

        if top is not None or bottom is not None:
            new_data_box_min_y = (
                data_box_min_y - bottom_margin if bottom is not None else y_axis_min
            )
            new_data_box_max_y = (
                data_box_max_y + top_margin if top is not None else y_axis_max
            )
            self.ax.set_ylim(
                new_data_box_min_y,
                new_data_box_max_y,
            )
