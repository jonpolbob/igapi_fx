


#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#from scipy import misc
import wx
#­import wxmplot


class simpleapp_wx(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title)
        self.parent = parent
        
        
        #on cree un panel dans un frame
        self.frame = wx.Frame(None, title='Photo Control')
        self.panel = wx.Panel(self.frame)
        
        #on cree un conrole image
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                                 wx.BitmapFromImage(img))
        
        #creation d'un sizer pour y metre l'image        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        
        #on charge un image
        self.loadimage()
        self.frame.Show()
        


    def loadimage(self):
        filepath =r"C:\Users\cagibi\Pictures\2016-04-03\114.jpg"        
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        img = img.Scale(240,240)
        
        #self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))        
        self.imageCtrl = self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))        
        
        
if __name__ == "__main__":
    app = wx.App()
    frame = simpleapp_wx(None,-1,'my application')
app.MainLoop()


