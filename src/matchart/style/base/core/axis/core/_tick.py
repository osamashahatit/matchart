from dataclasses import dataclass
from matplotlib.axis import Axis

from ._tick_label import MajorLabelDrawer
from ._tick_marker import MajorMarkerDrawer, MinorMarkerDrawer


@dataclass
class AxisTickMajor:
    axis: Axis

    @property
    def text(self) -> MajorLabelDrawer:
        return MajorLabelDrawer(axis=self.axis)

    @property
    def marker(self) -> MajorMarkerDrawer:
        return MajorMarkerDrawer(axis=self.axis)


@dataclass
class AxisTickMinor:
    axis: Axis

    @property
    def marker(self) -> MinorMarkerDrawer:
        return MinorMarkerDrawer(axis=self.axis)


@dataclass
class AxisTickSelector:
    axis: Axis

    @property
    def major(self) -> AxisTickMajor:
        return AxisTickMajor(axis=self.axis)

    @property
    def minor(self) -> AxisTickMinor:
        return AxisTickMinor(axis=self.axis)
