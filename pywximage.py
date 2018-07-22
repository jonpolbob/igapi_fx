from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        self.setImage( r"C:\Users\cagibi\Pictures\2016-04-03\114.jpg" )
       

    def setImage(self, pathToImage):
        '''Sets the background image of the canvas'''

        import matplotlib.image as mpimg

        # Load the image into matplotlib
        image = matplotlib.image.imread(pathToImage)
        
        # left in as anchor for image size
        self.imageSize = image.shape[0:2]
        
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(image, interpolation="quadric", aspect='auto')
        self.canvas.draw()

if __name__ == "__main__":
    app = wx.App()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    fr.Show()
    app.MainLoop()
