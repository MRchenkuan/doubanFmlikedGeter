import wx
from MyFrame1 import MyFrame1

app = wx.App(False) 
frame = MyFrame1(None)
frame.Show(True) 
app.MainLoop()