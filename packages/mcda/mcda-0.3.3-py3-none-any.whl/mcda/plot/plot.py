"""This module gathers all plotting functions.

All those functions use `matplotlib <https://matplotlib.org/>`_.
"""
from typing import Any, List, Tuple

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path as MPath
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from ..core.aliases import NumericValue


def piecewise_linear_colormap(
    colors: Any, name: str = "cmap"
) -> mcolors.LinearSegmentedColormap:
    """Create piecewise linear colormap.

    :param colors: list of any type of color accepted by :mod:`matplotlib`
    :param name: name of the created colormap
    :return: piecewise linear colormap
    """
    return mcolors.LinearSegmentedColormap.from_list(name, colors)


def radar_projection_name(num_vars: int) -> str:
    """Give projection corresponding to radar with `num_vars` axes.

    :param num_vars: number of axes of the radar plot
    :return:
    """
    return f"radar{num_vars}"


def create_radar_projection(num_vars: int, frame: str = "circle"):
    """Create a radar projection with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    :param num_vars: number of variables for radar chart
    :param frame: shape of frame surrounding axes ('circle' or 'polygon')

    Example:
        If you want to create radar projections up to a reasonable amount of
        variables. You can use the code below:

        .. code:: python

            from mcda.plot.new_plot import create_radar_projection

            for i in range(1, 12):
                create_radar_projection(i, frame="polygon")
    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = radar_projection_name(num_vars)
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location("N")

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == "circle":
                return Circle((0.5, 0.5), 0.5)
            elif frame == "polygon":
                return RegularPolygon(
                    (0.5, 0.5), num_vars, radius=0.5, edgecolor="k"
                )
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == "circle":
                return super()._gen_axes_spines()
            elif frame == "polygon":
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(
                    axes=self,
                    spine_type="circle",
                    path=MPath.unit_regular_polygon(num_vars),
                )
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(
                    Affine2D().scale(0.5).translate(0.5, 0.5) + self.transAxes
                )
                return {"polar": spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)


class Figure:
    """This class is a wrapper around :class:`matplotlib.figure.Figure`

    It plots and organizes any number of :class:`mcda.plot.new_plot.Axis`.

    If `ncols` (resp. `nrows`) is ``0``, then columns will be added (resp.
    rows) when a row is full (resp. column). If both are ``0``, the grid layout
    will be as balanced as possible.

    :param fig: matplotlib figure to use (if not provided, one will be created)
    :param figsize: figure size in inches as a tuple (`width`, `height`)
    :param ncols: number of columns for the subplot layout
    :param nrows: number of rows for the subplot layout
    :param tight_layout:
        if ``True``, matplotlib `tight_layout` function is used to organize
        axes

    .. note::
        if `ncols` or `nrows` is ``0``, an unlimited number of axes can be
        added to the figure

    .. seealso::
        `Matplotlib tight layout guide <https://matplotlib.org/stable/tutorials/intermediate/tight_layout_guide.html>`_
            Guide on tight-layout usage to fit plots within figures more cleanly
    """  # noqa E501

    def __init__(
        self,
        fig: Any = None,
        figsize: Tuple[float, float] = None,
        ncols: int = 0,
        nrows: int = 0,
        tight_layout: bool = True,
    ):
        self.fig = fig
        self.axes: List[Axis] = []
        self.figsize = figsize
        self.layout = (nrows, ncols)
        self.tight_layout = tight_layout

    def reset(self):
        """Reset `fig` attribute"""
        self.fig = (
            plt.figure()
            if self.figsize is None
            else plt.figure(figsize=self.figsize)
        )

    @property
    def max_axes(self) -> NumericValue:
        """Return maximum number of axes the figure can handle.

        :return:
        """
        if self.layout[0] == 0 or self.layout[1] == 0:
            return float("inf")
        return self.layout[0] * self.layout[1]

    def create_add_axis(self, projection: str = None) -> "Axis":
        """Create an axis and add it to figure.

        :param projection: projection ot use in created axis
        :return: created axis
        """
        axis = Axis(projection=projection)
        self.add_axis(axis)
        return axis

    def add_axis(self, axis: "Axis"):
        """Add axis to the figure.

        :param axis:
        """
        if len(self.axes) > self.max_axes:
            raise IndexError("already max number of axes")
        self.axes.append(axis)
        axis.figure = self

    def _pre_draw(self):
        """Prepare figure before drawing."""
        self.fig.clear()
        nb = len(self.axes)
        nrows, ncols = self.layout
        if self.layout[0] == 0 and self.layout[1] == 0:
            nrows = int(np.ceil(np.sqrt(nb)))
            ncols = int(np.ceil(nb / nrows))
        elif self.layout[0] == 0:
            nrows = int(np.ceil(nb / ncols))
        elif self.layout[1] == 0:
            ncols = int(np.ceil(nb / nrows))
        for i, axis in enumerate(self.axes):
            if axis.projection is None:
                ax = self.fig.add_subplot(nrows, ncols, i + 1)
            else:
                ax = self.fig.add_subplot(
                    nrows,
                    ncols,
                    i + 1,
                    projection=axis.projection,
                )
            axis.ax = ax

    def _draw(self):
        """Draw all axes."""
        for axis in self.axes:
            axis.draw()

    def _post_draw(self):
        """Apply operations after axes drawings complete."""
        if self.tight_layout:
            self.fig.tight_layout()
        self.fig.show()

    def draw(self):
        """Draw figure and all its axes content."""
        if self.fig is None:
            self.fig = (
                plt.figure()
                if self.figsize is None
                else plt.figure(figsize=self.figsize)
            )
        self._pre_draw()
        self._draw()
        self._post_draw()


class Axis:
    """This class is a wrapper around :class:`matplotlib.axes.Axes`

    It draws any number of :class:`mcda.plot.new_plot.Plot` on a same subplot.

    :param figure: figure holding the object
    :param plots: list of plots to draw
    :param ax: matplotlib axes
    :param title: title of the object
    :param xlabel: label to use for `x` axis
    :param ylabel: label to use for `y` axis
    :param projection:
        projection to use when creating `ax` attribute from scratch
    """

    def __init__(
        self,
        figure: Figure = None,
        plots: "List[Plot]" = None,
        ax: Any = None,
        title: str = None,
        xlabel: str = None,
        ylabel: str = None,
        projection: str = None,
    ):
        self.figure = figure
        self.plots = [] if plots is None else plots
        self.ax = ax
        self.title = title
        self.projection = projection
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.plots = []

    def draw(self):
        """Draw the subplot and all its plots."""
        if self.ax is None:
            fig = Figure()
            fig.add_axis(self)
            fig.draw()
            return

        for p in self.plots:
            p.draw()
        if self.title is not None:
            self.ax.set_title(self.title)
        if self.xlabel is not None:
            self.ax.set_xlabel(self.xlabel)
        if self.ylabel is not None:
            self.ax.set_ylabel(self.ylabel)

    def add_plot(self, plot: "Plot"):
        """Add a plot to the subplot.

        :param plot:
        """
        self.plots.append(plot)
        plot.axis = self


class Plot:
    """This class is the base of all plot objects of this package.

    :param axis: subplot on which to be plotted
    """

    def __init__(self, axis: Axis = None):
        self.axis = axis

    @property
    def default_axis(self) -> Axis:
        """Default subplot object on which to plot itself."""
        return Axis()

    @property
    def ax(self):
        """Matplotlib axes direct access"""
        return self.axis.ax

    def draw(self):
        """Draw this plot."""
        if self.axis is None:
            ax = self.default_axis
            ax.add_plot(self)
            ax.draw()
            return
        self._pre_draw()
        self._draw()
        self._post_draw()

    def _pre_draw(self):
        """Prepare this plot."""
        pass

    def _draw(self):
        """Do the actual drawing of this plot."""
        pass

    def _post_draw(self):
        """Apply necessary operations after plot is drawn."""
        pass


class CartesianPlot(Plot):
    """This class represents 2D cartesian plots.

    :param x: data abscissa to plot
    :param y: data ordinates to plot
    :param xticks: ticks used for `x` axis
    :param yticks: ticks used for `y` axis
    :param xticklabels: labels used to replace numeric ticks for `x` axis
    :param yticklabels: labels used to replace numeric ticks for `y` axis
    :param xticklabels_tilted:
        if ``True`` `xticklabels` are tilted to better fit
    :param axis: subplot on which to be plotted
    """

    def __init__(
        self,
        x: List[NumericValue],
        y: List[NumericValue],
        xticks: List[NumericValue] = None,
        yticks: List[NumericValue] = None,
        xticklabels: List[str] = None,
        yticklabels: List[str] = None,
        xticklabels_tilted: bool = False,
        axis: Axis = None,
    ):
        Plot.__init__(self, axis)
        self.x = x
        self.y = y
        self.xticks = xticks
        self.yticks = yticks
        self.xticklabels = xticklabels
        self.yticklabels = yticklabels
        self.xticklabels_tilted = xticklabels_tilted

    def _post_draw(self):
        """Set ticks and their labels."""
        if self.xticks is not None:
            self.ax.set_xticks(self.xticks)
            if self.xticklabels is not None:
                options = (
                    {"rotation": -45, "ha": "left", "rotation_mode": "anchor"}
                    if self.xticklabels_tilted
                    else {}
                )
                self.ax.set_xticklabels(self.xticklabels, **options)
        if self.yticks is not None:
            self.ax.set_yticks(self.yticks)
            if self.yticklabels is not None:
                self.ax.set_yticklabels(self.yticklabels)


class LinePlot(CartesianPlot):
    """This class draws a regular lines and points plot.

    :param x: data abscissa to plot
    :param y: data ordinates to plot
    :param xticks: ticks used for `x` axis
    :param yticks: ticks used for `y` axis
    :param xticklabels: labels used to replace numeric ticks for `x` axis
    :param yticklabels: labels used to replace numeric ticks for `y` axis
    :param xticklabels_tilted:
        if ``True`` `xticklabels` are tilted to better fit
    :param axis: subplot on which to be plotted
    """

    def _draw(self):
        """Draw the lines and points regular plot."""
        self.ax.plot(self.x, self.y)


class StemPlot(CartesianPlot):
    """This class draws a stem plot.

    :param x: data abscissa to plot
    :param y: data ordinates to plot
    :param xticks: ticks used for `x` axis
    :param yticks: ticks used for `y` axis
    :param xticklabels: labels used to replace numeric ticks for `x` axis
    :param yticklabels: labels used to replace numeric ticks for `y` axis
    :param xticklabels_tilted:
        if ``True`` `xticklabels` are tilted to better fit
    :param axis: subplot on which to be plotted
    """

    def _draw(self):
        """Draw the stem plot."""
        self.ax.stem(self.x, self.y)


class BarPlot(CartesianPlot):
    """This class draws a bar chart.

    :param x: data abscissa to plot
    :param y: data ordinates to plot
    :param xticks: ticks used for `x` axis
    :param yticks: ticks used for `y` axis
    :param xticklabels: labels used to replace numeric ticks for `x` axis
    :param yticklabels: labels used to replace numeric ticks for `y` axis
    :param xticklabels_tilted:
        if ``True`` `xticklabels` are tilted to better fit
    :param axis: subplot on which to be plotted
    :param width: width of the bars plotted
    """

    def __init__(
        self,
        x: List[NumericValue],
        y: List[NumericValue],
        xticks: List[NumericValue] = None,
        yticks: List[NumericValue] = None,
        xticklabels: List[str] = None,
        yticklabels: List[str] = None,
        xticklabels_tilted: bool = False,
        axis: Axis = None,
        width: NumericValue = None,
    ):
        CartesianPlot.__init__(
            self,
            x,
            y,
            xticks,
            yticks,
            xticklabels,
            yticklabels,
            xticklabels_tilted,
            axis,
        )
        self.width = width

    def _draw(self):
        """Draw the bar chart."""
        if self.width is not None:
            self.ax.bar(self.x, self.y, width=self.width)
        self.ax.bar(self.x, self.y)


class PolarPlot(Plot):
    """This class represents polar plots.

    :param x: data labels to plot
    :param y: data values to plot
    :param axis: subplot on which to be plotted
    """

    def __init__(self, x: List[str], y: List[NumericValue], axis: Axis = None):
        Plot.__init__(self, axis)
        self.x = x
        self.y = y


class PiePlot(PolarPlot):
    """This class draws a pie chart.

    :param x: data labels to plot
    :param y: data values to plot
    :param axis: subplot on which to be plotted
    """

    def _draw(self):
        """Draw the pie chart."""
        self.ax.pie(self.y, labels=self.x)


class RadarPlot(PolarPlot):
    """This class draws a radar chart (also called spider plot).

    :param x: data labels to plot
    :param y: data values to plot
    :param alpha:
        if set, surface under the plot is colored with this transparency
    :param axis: subplot on which to be plotted
    :param rlimits: limits for radial axis

    .. warning::
        This type of plot must be used with a `radar` type projection.
        The projection must exist before drawing of this chart can occur.

    .. seealso::
        Function :func:`create_radar_projection`
            This function should be called before drawing this chart so the
            radar projection (with same number of variables) is already
            registered.
    """

    def __init__(
        self,
        x: List[str],
        y: List[NumericValue],
        alpha: float = None,
        axis: Axis = None,
        rlimits: List[NumericValue] = None,
    ):
        PolarPlot.__init__(self, x, y, axis)
        self.alpha = alpha
        self.rlimits = rlimits

    @property
    def default_axis(self) -> Axis:
        """Default subplot object on which to plot itself."""
        return Axis(projection=radar_projection_name(len(self.x)))

    def _draw(self):
        # calculate evenly-spaced axis angles
        theta = np.linspace(0, 2 * np.pi, len(self.x), endpoint=False)
        if self.rlimits is not None:
            self.ax.set_ylim(self.rlimits)
        self.ax.plot(theta, self.y)
        if self.alpha is not None:
            self.ax.fill(theta, self.y, alpha=self.alpha)

    def _post_draw(self):
        self.ax.set_varlabels(self.x)
