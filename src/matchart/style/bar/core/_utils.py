from itertools import cycle
from typing import Iterable, Literal, TypeVar
from matplotlib.axes import Axes
from matplotlib.patches import Patch, Rectangle
from matplotlib.container import BarContainer

T = TypeVar("T")


class BarStyleHelper:

    def __init__(self, ax: Axes, horizontal: bool) -> None:
        self.ax = ax
        self.horizontal = horizontal

    def get_tick_labels(self) -> list[str]:
        """Get tick labels based on orientation."""

        label_getter = (
            self.ax.get_yticklabels()
            if self.horizontal is True
            else self.ax.get_xticklabels()
        )
        tick_labels: list[str] = []
        for tick_label in label_getter:
            tick_labels.append(tick_label.get_text())
        return tick_labels

    def get_legend_labels(self) -> list[str]:
        """Get legend labels."""

        legend_labels: list[str] = []
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                legend_label = container.get_label()
                if legend_label is not None and legend_label != "":
                    legend_labels.append(legend_label)
        return legend_labels

    def validate_tick_entry(self, dict: dict[str, T]) -> None:
        """Validate that dictionary keys match tick labels."""

        tick_labels = self.get_tick_labels()
        dict_keys = set(dict.keys())
        valid_labels = set(tick_labels)
        invalid_keys = dict_keys - valid_labels
        if invalid_keys:
            raise ValueError(
                f"Invalid tick labels in dictionary keys: {invalid_keys}. "
                f"Available tick labels are: {tick_labels}"
            )

    def validate_legend_entry(self, dict: dict[str, T]) -> None:
        """Validate that dictionary keys match legend labels."""

        legend_labels = self.get_legend_labels()
        dict_keys = set(dict.keys())
        valid_labels = set(legend_labels)
        invalid_keys = dict_keys - valid_labels
        if invalid_keys:
            raise ValueError(
                f"Invalid legend labels in dictionary keys: {invalid_keys}. "
                f"Available legend labels are: {legend_labels}"
            )

    def get_patch_value(self, patch: Patch) -> float:
        """Get the value of a bar patch."""

        if isinstance(patch, Rectangle):
            return patch.get_width() if self.horizontal else patch.get_height()
        raise ValueError("Provided object is not a Rectangle.")

    def get_extrema_values(self) -> tuple[float, float]:
        """Get min and max bar values."""

        values: list[float] = []
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    values.append(self.get_patch_value(patch=patch))
        return min(values), max(values)


class BarPatchGenerator:

    def __init__(self, ax: Axes, horizontal: bool) -> None:
        self.ax = ax
        self.horizontal = horizontal
        self.help = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

    def standard(self) -> Iterable[Patch]:
        """Generate standard patches without any properties."""

        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    yield patch

    def cycle(self, property: list[T]) -> Iterable[tuple[Patch, T]]:
        """Generate patches with cycled properties."""

        property_cycle = cycle(property)
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    prop = next(property_cycle)
                    yield patch, prop

    def map_tick(self, property: dict[str, T]) -> Iterable[tuple[Patch, T]]:
        """Generate patches with properties mapped to tick labels."""

        tick_labels = self.help.get_tick_labels()
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for index, patch in enumerate(container.patches):
                    if index < len(tick_labels):
                        tick_label = tick_labels[index]
                        prop = property.get(tick_label)
                        if prop is not None:
                            yield patch, prop

    def map_legend(self, property: dict[str, T]) -> Iterable[tuple[Patch, T]]:
        """Generate patches with properties mapped to legend labels."""

        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                legend_label = container.get_label()
                if legend_label is not None:
                    prop = property.get(legend_label)
                    if prop is not None:
                        for patch in container.patches:
                            yield patch, prop

    def extrema(self, target: Literal["min", "max"]) -> Iterable[Patch]:
        """Generate patches with properties mapped to extrema (min or max) values."""

        min_value, max_value = self.help.get_extrema_values()
        target_value = min_value if target == "min" else max_value

        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    patch_value = self.help.get_patch_value(patch=patch)
                    if patch_value == target_value:
                        yield patch
