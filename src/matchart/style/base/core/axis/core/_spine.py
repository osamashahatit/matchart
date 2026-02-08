"""Show, hide, and style axis spines."""

from typing import Literal

from matplotlib.axes import Axes

type SelectSpine = (
    Literal["all", "top", "bottom", "left", "right"]
    | list[Literal["top", "bottom", "left", "right"]]
)


class AxisSpine:
    """Apply visibility and styling to one or more axis spines."""

    def __init__(self, ax: Axes) -> None:
        """
        Args:
            ax (Axes): Target axes whose spines will be modified.
        """
        self.ax = ax

    def draw(
        self,
        select: SelectSpine,
        show: bool = True,
        color: str | None = None,
        width: float | None = None,
        style: str | None = None,
        position: float | None = None,
    ) -> None:
        """Show, hide, and style selected axis spines.

        Args:
            select (SelectSpine): Spine selection.
                Options: "all", "top", "bottom", "left", "right",
                or a list of ["top", "bottom", "left", "right"].
            show (bool): Whether to show or hide the selected spines.
            color (str | None): Optional spine edge color.
            width (float | None): Optional spine line width.
            style (str | None): Optional spine line style.
            position (float | None): Optional spine position as a percentage
                (0–100) of the axes coordinate system.

        Returns:
            None: Spine objects are modified in place.
        """
        match select:
            case "all":
                spines = ["top", "bottom", "left", "right"]
            case str():
                spines = [select]
            case list():
                spines = list(select)

        for spine_name in spines:
            if spine_name not in self.ax.spines:
                continue

            spine = self.ax.spines[spine_name]

            spine.set_visible(show)

            if color is not None:
                spine.set_edgecolor(color)

            if width is not None:
                spine.set_linewidth(width)

            if style is not None:
                spine.set_linestyle(style)

            if position is not None:
                # Convert percentage to axes coordinates.
                position_value = position / 100.0
                spine.set_position(("axes", position_value))
