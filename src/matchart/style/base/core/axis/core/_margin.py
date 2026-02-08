"""Apply axis margins around the plotted data bounds."""

from matplotlib.axes import Axes


class MarginHelpers:
    """Provide helpers for computing axis margins relative to data bounds."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Target axes used for bounds queries.
        """
        self.ax = ax

    def get_axis_limits(self) -> tuple[float, float, float, float]:
        """Return the current axes limits.

        Returns:
            tuple[float, float, float, float]:
            (x_min, x_max, y_min, y_max) from get_xlim/get_ylim.
        """
        x_axis_min, x_axis_max = self.ax.get_xlim()
        y_axis_min, y_axis_max = self.ax.get_ylim()
        return x_axis_min, x_axis_max, y_axis_min, y_axis_max

    def get_data_box_bounds(self) -> tuple[float, float, float, float]:
        """Return the data bounding box from Axes.dataLim when available.

        If Axes.dataLim has zero width and height, this falls back to the
        current axis limits.

        Returns:
            tuple[float, float, float, float]:
            (x_min, x_max, y_min, y_max) based on dataLim or axis limits.
        """
        data_box_bounds = self.ax.dataLim
        if data_box_bounds.width == 0 and data_box_bounds.height == 0:
            return self.get_axis_limits()

        return (
            data_box_bounds.x0,
            data_box_bounds.x1,
            data_box_bounds.y0,
            data_box_bounds.y1,
        )

    def convert_percent_to_data_units(
        self,
        left: float | None,
        right: float | None,
        top: float | None,
        bottom: float | None,
    ) -> tuple[float, float, float, float]:
        """Convert percent margins to data-unit distances.

        Args:
            left (float | None): Left margin as a fraction of data width.
            right (float | None): Right margin as a fraction of data width.
            top (float | None): Top margin as a fraction of data height.
            bottom (float | None): Bottom margin as a fraction of data height.

        Returns:
            tuple[float, float, float, float]:
            (left_margin, right_margin, top_margin, bottom_margin) in data
            units.
        """
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

        return left_margin, right_margin, top_margin, bottom_margin


class AxisMargin:
    """Expand axis limits by percent-based margins around the data bounds."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Target axes whose limits will be modified.
        """
        self.ax = ax

    def draw(
        self,
        left: float | None = None,
        right: float | None = None,
        top: float | None = None,
        bottom: float | None = None,
    ) -> None:
        """Apply margins around the data bounding box.

        Args:
            left (float | None): Left margin as a fraction of the data
                bounding box width.
            right (float | None): Right margin as a fraction of the data
                bounding box width.
            top (float | None): Top margin as a fraction of the data
                bounding box height.
            bottom (float | None): Bottom margin as a fraction of the data
                bounding box height.

        Returns:
            None: Axis limits are updated in place when margins are provided.
        """
        helper = MarginHelpers(self.ax)
        x_axis_min, x_axis_max, y_axis_min, y_axis_max = helper.get_axis_limits()
        data_box_min_x, data_box_max_x, data_box_min_y, data_box_max_y = (
            helper.get_data_box_bounds()
        )
        left_margin, right_margin, top_margin, bottom_margin = (
            helper.convert_percent_to_data_units(
                left=left,
                right=right,
                top=top,
                bottom=bottom,
            )
        )

        if left is not None or right is not None:
            new_data_box_min_x = (
                data_box_min_x - left_margin if left is not None else x_axis_min
            )
            new_data_box_max_x = (
                data_box_max_x + right_margin if right is not None else x_axis_max
            )
            self.ax.set_xlim(new_data_box_min_x, new_data_box_max_x)

        if top is not None or bottom is not None:
            new_data_box_min_y = (
                data_box_min_y - bottom_margin if bottom is not None else y_axis_min
            )
            new_data_box_max_y = (
                data_box_max_y + top_margin if top is not None else y_axis_max
            )
            self.ax.set_ylim(new_data_box_min_y, new_data_box_max_y)
