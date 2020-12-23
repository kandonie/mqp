import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import time


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, plot_title, ylim, parent=None, width=10, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        print(plot_title)
        self.axes = fig.add_subplot(111, title=str(plot_title), ylim = ylim)
        super(MplCanvas, self).__init__(fig)


class SensorGraphDataManager(QThread):

    def __init__(self, canvas):
        QThread.__init__(self)
        self.canvas = canvas

        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [0 for i in range(n_data)]

        self._plot_ref = None
        self.update_plot(0)

    def run(self):
        while True:
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
            #Tradeoff between time to load graphs and how fast they update
            time.sleep(1)

    def update_plot(self, newData):
        self.currData = newData


class DataGraph(QtWidgets.QMainWindow):

    def __init__(self, title, ylim):
        QtWidgets.QMainWindow.__init__(self)
        self.canvas = MplCanvas(title, ylim, self, width=5, height=4, dpi=100)

        self.dataManager = SensorGraphDataManager(self.canvas)
        self.dataManager.start()

        self.setCentralWidget(self.canvas)


        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self.update_plot(0)

        self.show()

    def update_plot(self, newData):
        self.currData = newData
        self.dataManager.update_plot(newData)

    def getCurrData(self):
        return self.currData