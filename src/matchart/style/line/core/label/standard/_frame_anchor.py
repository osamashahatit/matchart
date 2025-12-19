import numpy as np
from matplotlib.lines import Line2D


class FDL_Line_Anchor:
    def __init__(self, line: Line2D):
        self.line = line

    def get_x(self) -> list[int]:
        x_data = np.asarray(self.line.get_xdata())
        return list(range(len(x_data)))

    def get_y(self) -> list[float]:
        y_data = np.asarray(self.line.get_ydata(), dtype=float)
        return y_data.tolist()

    def anchor(self) -> list[tuple[int, float]]:
        x_values = self.get_x()
        y_values = self.get_y()
        return list(zip(x_values, y_values))
