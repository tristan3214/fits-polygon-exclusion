import numpy as np
import matplotlib
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from astropy.io import fits
import wx
import AddLinearSpacer as als
import os.path
import copy

class ImageWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "ImageWindow", size=(650,550))
        
        panel = wx.Panel(self)

        #self.image = "13461_NGC-300-OUTER-1U_F606W_drz.fits.gz"



        ## Menu
        self.menuBar = wx.MenuBar()

        # create main menus
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(1002, "Open &Image", "Open new image")
        self.fileMenu.Append(1003, "Open &Data", "Load data points")
        self.fileMenu.Append(1004, "&Save Polys", "Save the loaded polygons")
        self.fileMenu.Append(1001, "&Exit", "Quit Application")
        self.editMenu = wx.Menu()
        self.editMenu.Append(2001, "&Undo", "Undo a polygon")
        self.editMenu.Append(2002, "&Redo", "Redo a polygon")
        # add to menu bar
        self.menuBar.Append(self.fileMenu, "&File")
        self.menuBar.Append(self.editMenu, "&Edit")
        # instantiate menubar
        self.SetMenuBar(self.menuBar)

        self.editMenu.Enable(2001, False)
        self.editMenu.Enable(2002, False)
        ##


        ## Main Sizers
        self.topSizer = wx.BoxSizer(wx.VERTICAL)

        ## Minor Sizers
        self.sliderSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.im = DrawImage(self)
        self.isPlot = False
        self.polyUndo = []
        self.polyRedo = []
        self.linesUndo = []
        self.linesRedo = []
        
        #self.data = self.im.getData(self.image)

        ### Put in matplotlib imshow window
        #self.im.plotImage(self.data, 6.0, 'gray')
        
        self.devSlider = wx.Slider(self, id=-1, value=600, minValue=1, maxValue=3000, size=(250,-1), style=wx.SL_HORIZONTAL)
        self.text = wx.StaticText(self, label="Contrast:")
        self.txtCtrl = wx.TextCtrl(self, id=-1, style=wx.TE_READONLY|wx.TE_MULTILINE)


        ## Adjust sub sizers
        self.sliderSizer.Add(self.text, flag=wx.ALIGN_CENTER)
        als.AddLinearSpacer(self.sliderSizer, 10)
        self.sliderSizer.Add(self.devSlider, flag=wx.ALIGN_CENTER)

        ## Adjust main sizers
        self.topSizer.Add(self.im, proportion=-1, flag=wx.EXPAND)
        self.topSizer.Add(self.sliderSizer, flag=wx.ALIGN_CENTER)
        self.topSizer.Add(self.txtCtrl, flag=wx.ALIGN_CENTER|wx.GROW)

        ## Binds
        self.Bind(wx.EVT_MENU, self.onClose, id=1001)
        self.devSlider.Bind(wx.EVT_SCROLL_CHANGED, self.onSlide)
        self.Bind(wx.EVT_MENU, self.onImageOpen, id=1002)
        self.Bind(wx.EVT_CLOSE, self.onCloseFrame)
        self.Bind(wx.EVT_MENU, self.onDataOpen, id=1003)
        self.Bind(wx.EVT_MENU, self.onSave, id=1004)
        self.Bind(wx.EVT_MENU, self.onUndo, id=2001)
        self.Bind(wx.EVT_MENU, self.onRedo, id=2002)


        self.SetSizer(self.topSizer)
        self.Fit()

    def onSlide(self, event):
        if(self.isPlot):
            value = float(event.GetPosition()) / 100.0
            lower = self.im.median - value * self.im.mad
            upper = self.im.median + value * self.im.mad
            self.im.updateLims(lower, upper)
            self.im.refresh()

    def onClose(self, event):
        self.im.closeFig()
        self.Destroy()

    def onCloseFrame(self, event):
        self.im.closeFig()
        self.Destroy()

    def onImageOpen(self, event):
        openFileDialog = wx.FileDialog(self, "Open Image File", "", "", "Image (*.fits;*.png;*.jpg)|*.fits.*;*.fits;*.png;*.jpg", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        
        fileName = openFileDialog.GetFilename()
        fileName = fileName.split(".")
        if "fits" in fileName or "fit" in fileName:
            self.data = self.im.getData(openFileDialog.GetPath())
            self.im.clear()
            self.im.plotImage(self.data, 6.0, 'gray')
            self.isPlot = True
            self.im.refresh()
            self.devSlider.SetValue(600)
    
    def onDataOpen(self, event):
        openFileDialog = wx.FileDialog(self, "Open Data File", "", "", "Data (*.reg)|*.reg", wx.FD_OPEN| wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
            
        fileName = openFileDialog.GetFilename()
        
        if "reg" in fileName.split("."):
            shape, x, y, size = np.genfromtxt(fileName, usecols=[0,1,2,3], unpack=True)
            self.im.plotData(x, y, size, shape)
            
    def onSave(self, event):
        saveFileDialog = wx.FileDialog(self, "Save into polygon file", "", "", "poly file (*.txt)|*.txt", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        
        #fileName = saveFileDialog.GetFilename() 
        polygons = self.im.polygonStack
        
        f = open(saveFileDialog.GetPath(), "w")
        
        for poly in polygons:
            for p in poly:
                f.write("%.2f %.2f\t"%(p[0], p[1]))
            f.write("\n")

        f.close()
        
    def onUndo(self, event):
        current = self.polyUndo.pop()
        self.im.polygonStack.pop()
        self.polyRedo.append(copy.deepcopy(current))
        if(len(self.polyUndo) == 0):
            self.editMenu.Enable(2001, False)
        self.editMenu.Enable(2002, True)
        #print len(self.im.polygonStack)
        self.refreshTxt(self.im.polygonStack)
        
        lines = self.linesUndo.pop()
        self.im.lineCollection.pop()
        self.linesRedo.append(lines)
        self.im.toggleLines(lines, False)
            

    def onRedo(self, event):
        current = self.polyRedo.pop()
        self.polyUndo.append(copy.deepcopy(current))
        self.im.polygonStack.append(copy.deepcopy(current))
        if(len(self.polyRedo) == 0):
            self.editMenu.Enable(2002, False)
        self.editMenu.Enable(2001, True)
        #print len(self.im.polygonStack)
        self.refreshTxt(self.im.polygonStack)
        
        lines = self.linesRedo.pop()
        self.linesUndo.append(lines)
        self.im.lineCollection.append(lines)
        self.im.toggleLines(lines, True)
        

    def refreshTxt(self, stack):
        string = ""
        for s in stack:
            string += str(s) + "\n\n"
        self.txtCtrl.SetValue(string)
        
        

class DrawImage(wx.Panel):

    def __init__(self, parent):
        self.parent = wx.Panel.__init__(self, parent)
        
        #self.points = "outer_1u_full.reg"
        #self.writeFile = "test2.reg"
        #self.f = None
        #self.counter = 0
        self.currentPoly = []
        self.polygonStack = []
        self.currentLines = []
        self.lineCollection = []
        
        self.start = False
        self.parent = parent
        
        # Create figure, plot space, and canvas for drawing fit image
        self.figure, self.axes = plt.subplots()
        self.figure.frameon = False
        self.axes.autoscale(False)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        self.canvas.callbacks.connect("button_press_event", self.onClick)
        self.canvas.callbacks.connect("key_press_event", self.onCtrl)
        self.canvas.callbacks.connect("key_release_event", self.releaseCtrl)

        
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        self.median = 0
        self.mad = 0

        self.vertSizer = wx.BoxSizer(wx.VERTICAL)

        self.vertSizer.Add(self.canvas, proportion=1, flag=wx.LEFT | wx.TOP | wx.GROW)
        self.vertSizer.Add(self.toolbar, proportion=0, flag=wx.EXPAND)


        self.SetSizer(self.vertSizer)
        self.Fit()

    def plotImage(self, data, scale, cmap):
        
        self.median = np.median(data.flat)

        self.mad = np.median(np.abs(data.flat-self.median))
        deviation = scale * self.mad
        self.upper = self.median + deviation
        self.lower = self.median - deviation
        
        self.plot = self.axes.imshow(data, vmin=self.lower, vmax=self.upper, origin='lower')
        self.plot.set_clim(vmin=self.lower, vmax=self.upper)
        self.plot.set_cmap(cmap)
        self.figure.tight_layout()

    def plotData(self, x, y, size, shape):
        self.axes.scatter(x,y, s=size+5, marker='o', facecolor='none', edgecolors='lime')
        self.axes.autoscale(False)
        self.refresh()

    def plotLine(self, p1, p2):
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        ln, = plt.plot(x, y, color='r', linewidth=1.3)
        self.refresh()
        return ln

    def onClick(self, event):
        #print "%f %f"%(event.xdata, event.ydata)
        if self.start == True:
            if(len(self.currentPoly) > 0):
                prevPoint = self.currentPoly[-1]
            self.currentPoly.append((round(event.xdata,3), round(event.ydata,3)))
            if(len(self.currentPoly) > 1):
                newPoint = self.currentPoly[-1]
            if(len(self.currentPoly) >= 2):
                ln = self.plotLine(prevPoint, newPoint)
                self.currentLines.append(ln)
            
    

    def onCtrl(self, event):
        if event.key == "control":
            self.start = True
            del self.parent.polyRedo[:] # delete anything in the redo stack because user is initializing a new polynomial
            del self.parent.linesRedo[:] # user making new polygon delete redo references
            # turn menu redo item off now that they are cleared
            self.parent.editMenu.Enable(2002, False)

    def releaseCtrl(self, event):
        if event.key == "ctrl+control":
            #print self.currentPoly
            if len(self.currentPoly) is not 0:
                self.polygonStack.append(copy.deepcopy(self.currentPoly)) # hold polygons for when user saves
                
                if(len(self.parent.polyUndo) == 0):
                    self.parent.editMenu.Enable(2001, True)
                self.parent.polyUndo.append(copy.deepcopy(self.currentPoly)) # add to undo stack everytime a new polygon is made
                if(len(self.parent.polyRedo) > 0):
                    self.parent.editMenu.Enable(2002, False)
                #print len(self.polygonStack)
                
                self.printToScreen(self.currentPoly)
                if(len(self.currentPoly) >= 2):
                    ln = self.plotLine(self.currentPoly[-1], self.currentPoly[0])
                    self.currentLines.append(ln)
                    self.lineCollection.append(copy.copy(self.currentLines))
                    self.parent.linesUndo.append(copy.copy(self.currentLines))
                    del self.currentLines[:]

                del self.currentPoly[:]
            self.start = False
            
        
    def printToScreen(self, data):
        val = self.parent.txtCtrl.GetValue()
        self.parent.txtCtrl.SetValue(val + str(data) + "\n\n")
        self.parent.txtCtrl.SetInsertionPointEnd()

    def clear(self):
        self.axes.clear()        
    
    def refresh(self):
        self.canvas.draw()
        self.canvas.Refresh()

    def getData(self, image):
        return fits.getdata(image)

    def updateStats(self, data):
        self.median = np.median(data.flat)
    
    def toggleLines(self, lines, status):
        for ln in lines:
            ln.set_visible(status)
        self.refresh()

    def updateLims(self, min, max):
        self.plot.set_clim(vmin=min, vmax=max)

    def closeFig(self):
        plt.close('all')



if __name__ == "__main__":
    app = wx.App(False)
    app.frame = ImageWindow()
    app.frame.Show()
    app.MainLoop()
