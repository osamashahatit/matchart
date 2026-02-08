"""Provide a small facade for accessing major/minor tick styling helpers."""

from dataclasses import dataclass

from matplotlib.axis import Axis

from .tick._tick_label import MajorLabelDrawer
from .tick._tick_marker import MajorMarkerDrawer, MinorMarkerDrawer


@dataclass
class AxisTickMajor:
    """Group accessors for major tick styling helpers.

    Attributes:
        axis (Axis): Matplotlib axis (xaxis or yaxis) to be styled.
    """

    axis: Axis

    @property
    def text(self) -> MajorLabelDrawer:
        """Return a helper for styling major tick labels.

        Returns:
            MajorLabelDrawer: Drawer for major tick label styling.
        """
        return MajorLabelDrawer(axis=self.axis)

    @property
    def marker(self) -> MajorMarkerDrawer:
        """Return a helper for styling major tick markers.

        Returns:
            MajorMarkerDrawer: Drawer for major tick marker styling.
        """
        return MajorMarkerDrawer(axis=self.axis)


@dataclass
class AxisTickMinor:
    """Group accessors for minor tick styling helpers.

    Attributes:
        axis (Axis): Matplotlib axis (xaxis or yaxis) to be styled.
    """

    axis: Axis

    @property
    def marker(self) -> MinorMarkerDrawer:
        """Return a helper for styling minor tick markers.

        Returns:
            MinorMarkerDrawer: Drawer for minor tick marker styling.
        """
        return MinorMarkerDrawer(axis=self.axis)


@dataclass
class AxisTickSelector:
    """Expose major/minor tick styling groups for a Matplotlib Axis.

    Attributes:
        axis (Axis): Matplotlib axis (xaxis or yaxis) to be styled.
    """

    axis: Axis

    @property
    def major(self) -> AxisTickMajor:
        """Return the major tick styling group.

        Returns:
            AxisTickMajor: Accessors for major tick label/marker helpers.
        """
        return AxisTickMajor(axis=self.axis)

    @property
    def minor(self) -> AxisTickMinor:
        """Return the minor tick styling group.

        Returns:
            AxisTickMinor: Accessor for minor tick marker helper.
        """
        return AxisTickMinor(axis=self.axis)
