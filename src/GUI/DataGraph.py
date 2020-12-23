from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import time
import matplotlib

matplotlib.use('Qt5Agg')


###These classes were derived from https://www.learnpyqt.com/tutorials/plotting-matplotlib/
###and https://codeloop.org/pyqt5-qprogressbar-with-qthread-practical-example/ because
###having everything in the same thread was trash.

class MplCanvas(FigureCanvasQTAgg):
    """
    This class holds an individual figure for plotting.
    It was copy and pasted from https://www.learnpyqt.com/tutorials/plotting-matplotlib/
    And modified - Lauren
    """

    def __init__(self, plot_title, ylim, parent=None, width=10, height=10, dpi=100):
        """
        This creates the plot
        :param plot_title: [String] the title of the plot, ideally the sensor name
        :param ylim: [(int, int)] a tuple of ints representing the lower, upper bound of the graph's y axis
        :param parent: [IDK??] the parent of the canvas
        :param width: [Probs an int] the width of the canvas
        :param height: [Probs an int] the height of the canvas
        :param dpi: I really don't know, this was copy pasta - Lauren
        """
        fig = Figure(figsize=(width, height), dpi=dpi)
        print(plot_title)
        # If you need more params for the plot see https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html
        # and scroll down to Other Parameters: **kwargs
        # I have no idea what 111 means - Lauren
        self.axes = fig.add_subplot(111, title=str(plot_title), ylim=ylim)
        super(MplCanvas, self).__init__(fig)


class SensorGraphDataManager(QThread):
    """
    This class manages the graph data
    Basically You can't have a class inherit from QThread and other stuff
    (in my experience if you wanna google and change stuff good for you)
    SOOO we have a class just to manage the data and asks the canvas
    to update its drawing periodically
    """

    def __init__(self, canvas):
        """
        initialize stuff
        :param canvas: [MplCanvas] the canvas that will draw stuff
        """
        QThread.__init__(self)
        self.canvas = canvas

        # Holds the last 50 data points
        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [0 for i in range(n_data)]

        self._plot_ref = None  # unsure, this is copy pasta
        self.update_plot(0)

    def run(self):
        """
        this function gets called once when this class's .start function is
        called (inherited from QThread). This is where the new thread does stuff
        """
        while True:
            # This is the next data point to add to the graph
            newData = int(self.currData)
            # Drop off the first y element, append a new one.
            self.ydata = self.ydata[1:] + [newData]

            # Note: we no longer need to clear the axis.
            if self._plot_ref is None:
                # First time we have no plot reference, so do a normal plot.
                # .plot returns a list of line <reference>s, as we're
                # only getting one we can take the first element.
                plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
                self._plot_ref = plot_refs[0]
            else:
                # We have a reference, we can use it to update the data for that line.
                self._plot_ref.set_ydata(self.ydata)

            # Trigger the canvas to update and redraw.
            self.canvas.draw()
            ###MODIFY THIS TO CHANGE HOW OFTEN PLOT UPDATES
            # Tradeoff between time to load graphs and how fast they update
            time.sleep(1)

    def update_plot(self, newData):
        """
        keeps the current data up to date
        :param newData: [int?] the newest data
        """
        self.currData = newData


class DataGraph(QtWidgets.QMainWindow):
    """
    This class is a main window so the canvas can be the central widget
    and we need the canvas to draw stuff. It is in charge of holding the
    canvas and asking the data manager to update if there is new data
    """

    def __init__(self, title, ylim):
        """
        initialize stuff
        :param title: [String] the title
        :param ylim: [(int, int)] the tuple of (lower, upper) bounds of y axis
        """
        QtWidgets.QMainWindow.__init__(self)
        self.canvas = MplCanvas(title, ylim, self, width=5, height=4, dpi=100)

        self.dataManager = SensorGraphDataManager(self.canvas)
        self.dataManager.start()

        self.setCentralWidget(self.canvas)

        # set 0 as the default first data point
        self.update_plot(0)
        self.show()

    def update_plot(self, newData):
        """
        update current data for self and data manager
        :param newData: [kinda whatever as long as int() works on it] the new data point
        """
        self.currData = newData
        self.dataManager.update_plot(newData)

    def getCurrData(self):
        """
        :return: the current data point
        """
        return self.currData
