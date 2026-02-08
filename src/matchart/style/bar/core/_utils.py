"""Utilities for bar chart stylers."""

from itertools import cycle
from typing import Iterable, Literal, TypeVar

from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.patches import Patch, Rectangle

T = TypeVar("T")


class BarStyleHelper:
    """Inspect bar artists on an Axes to support bar-specific styling."""

    def __init__(self, ax: Axes, horizontal: bool) -> None:
        """
        Args:
            ax (Axes): Axes that already contains bar artists.
            horizontal (bool): Whether the bar chart is horizontal. When
                True, widths are treated as values and y tick labels are
                used; when False, heights are treated as values and x tick
                labels are used.
        """
        self.ax = ax
        self.horizontal = horizontal

    def get_tick_labels(self) -> list[str]:
        """Return the tick labels for the bar axis.

        Returns:
            list[str]: Tick label text extracted from the active axis.
        """
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
        """Return legend labels for bar containers on the Axes.

        Returns:
            list[str]: Non-empty labels extracted from BarContainer objects.
        """
        legend_labels: list[str] = []
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                legend_label = container.get_label()
                if legend_label is not None and legend_label != "":
                    legend_labels.append(legend_label)
        return legend_labels

    def validate_tick_entry(self, mapping: dict[str, T]) -> None:
        """Validate that mapping keys match available tick labels.

        Args:
            mapping (dict[str, T]): Mapping from tick label text to a property
                value.

        Raises:
            ValueError: If any mapping keys are not present in the Axes tick
                labels. The error message includes the available labels.
        """
        tick_labels = self.get_tick_labels()
        dict_keys = set(mapping.keys())
        valid_labels = set(tick_labels)
        invalid_keys = dict_keys - valid_labels
        if invalid_keys:
            raise ValueError(
                f"Invalid tick labels in dictionary keys: {invalid_keys}. "
                f"Available tick labels are: {tick_labels}"
            )

    def validate_legend_entry(self, mapping: dict[str, T]) -> None:
        """Validate that mapping keys match available legend labels.

        Args:
            mapping (dict[str, T]): Mapping from legend label text to a property
                value.

        Raises:
            ValueError: If any mapping keys are not present in the legend
                labels discovered from BarContainer objects.
        """
        legend_labels = self.get_legend_labels()
        dict_keys = set(mapping.keys())
        valid_labels = set(legend_labels)
        invalid_keys = dict_keys - valid_labels
        if invalid_keys:
            raise ValueError(
                f"Invalid legend labels in dictionary keys: {invalid_keys}. "
                f"Available legend labels are: {legend_labels}"
            )

    def get_patch_value(self, patch: Patch) -> float:
        """Return the numeric value represented by a bar patch.

        Args:
            patch (Patch): A bar patch (expected to be a Rectangle).

        Returns:
            float: Rectangle width for horizontal bars, otherwise height.

        Raises:
            ValueError: If patch is not a Rectangle instance.
        """
        if isinstance(patch, Rectangle):
            return patch.get_width() if self.horizontal else patch.get_height()
        raise ValueError("Provided object is not a Rectangle.")

    def get_extrema_values(self) -> tuple[float, float]:
        """Return the minimum and maximum bar values found on the Axes.

        Returns:
            tuple[float, float]: (min_value, max_value) across all bar
            patches.

        Notes:
            If there are no bar patches on the Axes, this method will raise
            due to calling min()/max() on an empty sequence.
        """
        values: list[float] = []
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    values.append(self.get_patch_value(patch=patch))
        return min(values), max(values)


class BarPatchYielder:
    """Yield bar patches."""

    def __init__(self, ax: Axes, horizontal: bool) -> None:
        """
        Args:
            ax (Axes): Axes that already contains bar artists.
            horizontal (bool): Whether the bar chart is horizontal.
        """
        self.ax = ax
        self.horizontal = horizontal
        self.helper = BarStyleHelper(ax=self.ax, horizontal=self.horizontal)

    def standard(self) -> Iterable[Patch]:
        """Yield all bar patches without any associated property.

        Yields:
            Patch: Each bar patch in each BarContainer on the Axes.
        """
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    yield patch

    def cycle(self, property: list[T]) -> Iterable[tuple[Patch, T]]:
        """Yield bar patches paired with cycled values.

        Args:
            property (list[T]): Values to cycle through repeatedly as bars
                are yielded.

        Yields:
            tuple[Patch, T]: (patch, value) pairs.
        """
        property_cycle = cycle(property)
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    prop = next(property_cycle)
                    yield patch, prop

    def map_tick(self, property: dict[str, T]) -> Iterable[tuple[Patch, T]]:
        """Yield bar patches paired with values mapped by tick label.

        Args:
            property (dict[str, T]): Mapping of tick label text to a value.

        Yields:
            tuple[Patch, T]: (patch, value) for patches where a mapping
            exists for the corresponding tick label.
        """
        tick_labels = self.helper.get_tick_labels()
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for index, patch in enumerate(container.patches):
                    if index < len(tick_labels):
                        tick_label = tick_labels[index]
                        prop = property.get(tick_label)
                        if prop is not None:
                            yield patch, prop

    def map_legend(self, property: dict[str, T]) -> Iterable[tuple[Patch, T]]:
        """Yield bar patches paired with values mapped by legend label.

        Args:
            property (dict[str, T]): Mapping of legend label text to a
                value.

        Yields:
            tuple[Patch, T]: (patch, value) pairs for each bar patch in a
            container with a mapped legend label.
        """
        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                legend_label = container.get_label()
                if legend_label is not None:
                    prop = property.get(legend_label)
                    if prop is not None:
                        for patch in container.patches:
                            yield patch, prop

    def extrema(self, target: Literal["min", "max"]) -> Iterable[Patch]:
        """Yield bar patches that match the chart minimum or maximum value.

        Args:
            target (Literal["min", "max"]): Which extrema value to match.
                Options: "min", "max".

        Yields:
            Patch: Patches whose value equals the selected extrema.
        """
        min_value, max_value = self.helper.get_extrema_values()
        target_value = min_value if target == "min" else max_value

        for container in self.ax.containers:
            if isinstance(container, BarContainer):
                for patch in container.patches:
                    patch_value = self.helper.get_patch_value(patch=patch)
                    if patch_value == target_value:
                        yield patch
