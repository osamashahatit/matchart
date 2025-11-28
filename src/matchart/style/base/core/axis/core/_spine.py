from typing import Literal
from matplotlib.axes import Axes

type SelectSpine = (
    Literal["all", "top", "bottom", "left", "right"]
    | list[Literal["top", "bottom", "left", "right"]]
)


class AxisSpine:
    def __init__(self, ax: Axes) -> None:
        self.ax = ax

    def draw(
        self,
        select: SelectSpine,
        show: bool = True,
        color: str | None = None,
        width: float | None = None,
        style: str | None = None,
        position: float | None = None,
    ):
        """
        Draw and style the specified spines of the axis.

        Parameters
        ----------
        select : {"all", "top", "bottom", "left", "right"} | List[{"top", "bottom", "left", "right"}]
            The spine(s) to modify. "all" modifies all spines.
        show : bool. Default is True.
            Show or hide the selected spine(s).
        color : str | None. Default is None.
            The color of the selected spine(s).
        width : float | None. Default is None.
            The width of the selected spine(s).
        style : str | None. Default is None.
            The style of the selected spine(s).
        position : float | None. Default is None.
            The position of the selected spine(s) as a percentage of the axis (0 to 100). Default is None.
        """

        match select:
            case "all":
                spines = ["top", "bottom", "left", "right"]
            case str():
                spines = [select]
            case list():
                spines = list(select)
            case _:
                raise ValueError(f"Invalid select value: {select}")

        for spine in spines:
            if spine in self.ax.spines:
                spine = self.ax.spines[spine]
                spine.set_visible(show)
                if color is not None:
                    spine.set_edgecolor(color)
                if width is not None:
                    spine.set_linewidth(width)
                if style is not None:
                    spine.set_linestyle(style)
                if position is not None:
                    position_value = position / 100.0
                    spine.set_position(("axes", position_value))
