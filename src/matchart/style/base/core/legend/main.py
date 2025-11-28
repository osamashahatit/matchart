from typing import Literal
from matplotlib.axes import Axes
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D

from .core._frame import FrameProperties, FrameDrawer
from .core._title import TitleProperties, TitleDrawer
from .core._marker import MarkerProperties, MarkerDrawer

type Orientation = Literal["horizontal", "vertical"]
type Alignment = Literal["left", "center", "right"]
type Position = Literal[
    "best",
    "upper right",
    "upper left",
    "lower left",
    "lower right",
    "right",
    "center left",
    "center right",
    "lower center",
    "upper center",
    "center",
]


class LegendStyler:

    def __init__(self, ax: Axes) -> None:
        self.ax = ax

        # Frame properties
        self._frame_show: bool = True
        self._frame_properties: FrameProperties | None = None

        # Label properties
        self._label_font: FontProperties | str | None = None
        self._label_size: int | None = None
        self._label_color: str | None = None

        # Layout properties
        self._marker_first: bool = True
        self._v_pad: float | None = None
        self._h_pad: float | None = None
        self._box_pad: float | None = None
        self._marker_pad: float | None = None
        self._align: Alignment = "left"

        # Marker properties
        self._marker_properties: MarkerProperties | None = None
        self._custom_markers: list[Line2D] | None = None
        self._custom_labels: list[str] | None = None

        # Position properties
        self._position: Position | None = "upper right"
        self._bbox_to_anchor: tuple[float, float] | None = None

        # Title properties
        self._title_text: str | None = None
        self._title_properties: TitleProperties | None = None

    def frame(
        self,
        show: bool = True,
        face_color: str | None = None,
        face_alpha: float | None = None,
        border_color: str | None = None,
        border_alpha: float | None = None,
        border_style: str | None = None,
        border_width: float | None = None,
        border_radius: float | None = None,
    ) -> "LegendStyler":
        """
        Set the style of the legend frame.

        Parameters
        ----------
        face_color : str or None. Default is None.
            The face (background) color of the legend frame.
        face_alpha : float or None. Default is None.
            The transparency (alpha) of the legend frame's face color.
        border_color : str or None. Default is None.
            The border (border) color of the legend frame.
        border_alpha : float or None. Default is None.
            The transparency (alpha) of the legend frame's border color.
        border_style : str or None. Default is None.
            The line style of the legend frame's border (e.g., 'solid', 'dashed').
        border_width : float or None. Default is None.
            The line width of the legend frame's border.
        border_radius : float or None. Default is None.
            The corner radius for rounded borders of the legend frame.

        Returns
        -------
        LegendStyler
            The current instance for method chaining.
        """

        self._frame_show = show
        self._frame_properties = FrameProperties(
            face_color=face_color,
            face_alpha=face_alpha,
            border_color=border_color,
            border_alpha=border_alpha,
            border_style=border_style,
            border_width=border_width,
            border_radius=border_radius,
        )
        return self

    def label(
        self,
        font: FontProperties | str | None = None,
        size: int | None = None,
        color: str | None = None,
    ) -> "LegendStyler":
        """
        Set the style of the legend labels.

        Parameters
        ----------
        font : str or FontProperties or None. Default is None.
            The font family or FontProperties object of the legend labels.
        size : int or None. Default is None.
            The size of the legend labels.
        color : str or None. Default is None.
            The color of the legend labels.

        Returns
        -------
        LegendStyler
            The current instance for method chaining.
        """

        if isinstance(font, str):
            self._label_font = FontProperties(family=font, size=size)
        if isinstance(font, FontProperties):
            self._label_font = FontProperties(fname=str(font.get_file()), size=size)
        self._label_size = size
        self._label_color = color
        return self

    def layout(
        self,
        marker_first: bool = True,
        v_pad: float | None = None,
        h_pad: float | None = None,
        box_pad: float | None = None,
        marker_pad: float | None = None,
        align: Alignment = "left",
    ) -> "LegendStyler":
        """
        Set the layout of the legend.

        Parameters
        ----------
        marker_first : bool. Default is True.
            Whether to draw the marker before the label.
        v_pad : float or None. Default is None.
            The vertical padding between legend entries.
        h_pad : float or None. Default is None.
            The horizontal padding between legend entries.
        box_pad : float or None. Default is None.
            The padding between the legend content and the legend box.
        marker_pad : float or None. Default is None.
            The padding between the marker and the label.
        align : {"left", "center", "right"}. Default is "left".
            The alignment of the legend entries.

        Returns
        -------
        LegendStyler
            The current instance for method chaining.
        """

        self._marker_first = marker_first
        self._v_pad = v_pad
        self._h_pad = h_pad
        self._box_pad = box_pad
        self._marker_pad = marker_pad
        self._align = align
        return self

    def marker(
        self,
        marker: str | None = None,
        size: float | None = None,
    ) -> "LegendStyler":
        """
        Set custom markers for the legend.

        Parameters
        ----------
        marker : str or None. Default is None.
            The marker style to use for the legend entries. If None, default markers are used.
        size : float or None. Default is None.
            The size of the custom markers.

        Returns
        -------
        LegendStyler
            The current instance for method chaining.
        """

        self._marker_properties = MarkerProperties(marker=marker, size=size)
        return self

    def position(
        self,
        position: Position = "upper right",
        x_offset: float | None = None,
        y_offset: float | None = None,
    ) -> "LegendStyler":
        """
        Set the position of the legend.

        Parameters
        ----------
        position : {"best", "upper right", "upper left", "lower left", "lower right",
                    "right", "center left", "center right", "lower center", "upper center",
                    "center"}. Default is "best".
            The position of the legend.
        x_offset : float or None. Default is None.
            The horizontal offset for the legend position.
        y_offset : float or None. Default is None.
            The vertical offset for the legend position.

        Returns
        -------
        LegendStyler
            The current instance for method chaining.
        """

        _ANCHOR_MAP = {
            "upper right": (1.0, 1.0),
            "upper left": (0.0, 1.0),
            "lower left": (0.0, 0.0),
            "lower right": (1.0, 0.0),
            "right": (1.0, 0.5),
            "center left": (0.0, 0.5),
            "center right": (1.0, 0.5),
            "lower center": (0.5, 0.0),
            "upper center": (0.5, 1.0),
            "center": (0.5, 0.5),
        }

        self._position = position
        if x_offset is not None or y_offset is not None:
            base_x, base_y = _ANCHOR_MAP.get(position, (0.5, 0.5))
            self._bbox_to_anchor = (
                base_x + (x_offset or 0.0),
                base_y + (y_offset or 0.0),
            )
        return self

    def title(
        self,
        text: str | None = None,
        font: FontProperties | str | None = None,
        color: str | None = None,
        size: int | None = None,
    ) -> "LegendStyler":
        """
        Set the title of the legend.

        Parameters
        ----------
        text : str or None. Default is None.
            The title text of the legend.
        font : FontProperties or None. Default is None.
            The FontProperties object for the legend title.
        color : str or None. Default is None.
            The color of the legend title.
        size : int or None. Default is None.
            The font size of the legend title.

        Returns
        -------
        LegendStyler
            The current instance for method chaining.
        """

        self._title_text = text
        self._title_properties = TitleProperties(font=font, size=size, color=color)
        return self

    def draw(self, orientation: Orientation = "vertical") -> None:
        """
        Draw the legend on the Axes. Before calling draw(), ensure that all desired
        styling methods have been called to set up the legend appearance. The styling
        methods can be chained for convenience and include:
        - frame()
        - label()
        - layout()
        - marker()
        - position()
        - title()

        Parameters
        ----------
        orientation : {"vertical", "horizontal"}. Default is "vertical".
            The orientation of the legend (horizontal or vertical).
        """

        handles, labels = self.ax.get_legend_handles_labels()

        for ax in self.ax.figure.axes:
            if ax != self.ax and (ax.bbox.bounds == self.ax.bbox.bounds):
                handle, label = ax.get_legend_handles_labels()
                handles.extend(handle)
                labels.extend(label)

        if self._marker_properties is not None:
            self._custom_markers = MarkerDrawer(handles).draw(self._marker_properties)
            self._custom_labels = labels

        self.ax.legend(
            handles=self._custom_markers if self._custom_markers else handles,
            labels=self._custom_labels if self._custom_markers else labels,
            ncol=len(labels) if orientation == "horizontal" else 1,
            loc=self._position,
            markerfirst=self._marker_first,
            prop=self._label_font,
            labelcolor=self._label_color,
            fontsize=self._label_size,
            labelspacing=self._v_pad,
            columnspacing=self._h_pad,
            borderpad=self._box_pad,
            handletextpad=self._marker_pad,
            bbox_to_anchor=self._bbox_to_anchor,
            alignment=self._align,
        )

        legend = self.ax.get_legend()

        if legend is not None:
            if self._frame_show is not False:
                legend.set_frame_on(True)
                if self._frame_properties:
                    FrameDrawer(legend).draw(properties=self._frame_properties)

        if legend is not None:
            if self._title_text is not None:
                legend.set_title(self._title_text)
                if self._title_properties is not None:
                    TitleDrawer(legend).draw(properties=self._title_properties)
