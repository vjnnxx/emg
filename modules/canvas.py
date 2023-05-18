from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 


class Canvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100,):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = fig.add_subplot(111)
        
        
        super(Canvas, self).__init__(fig)