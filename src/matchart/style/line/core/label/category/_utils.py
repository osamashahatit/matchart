from dataclasses import dataclass

import numpy as np
from matplotlib.axes import Axes


@dataclass(frozen=True)
class CDL_Line_Totals:
    total: float

    @classmethod
    def compute_total(
        cls,
        ax: Axes,
        tick_label: str,
    ) -> "CDL_Line_Totals":
        tick_labels: list[str] = []
        for label in ax.get_xticklabels():
            tick_labels.append(label.get_text())

        total = 0.0
        for line in ax.lines:
            ydata = np.asarray(line.get_ydata(), dtype=float)
            for index, label in enumerate(tick_labels):
                if label == tick_label and index < len(ydata):
                    total += float(ydata[index])

        return cls(total=total)
