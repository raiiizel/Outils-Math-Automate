import wx
import wx.html2 as wxhtml

class MyBrowser(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self)
        self.browser = wxhtml.WebView.New(self.panel)
        self.browser.LoadURL("https://www.google.com")  # Load a web page

        # Set up sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.panel.SetSizer(sizer)

        # Set up menu bar
        self.menuBar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(wx.ID_EXIT, "E&xit", "Exit the program")
        self.menuBar.Append(self.fileMenu, "&File")
        self.SetMenuBar(self.menuBar)

        # Set up events
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        # Set window size and title
        self.SetSize((800, 600))
        self.SetTitle("Simple Web Browser")

    def OnQuit(self, event):
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    frame = MyBrowser(None, -1)
    frame.Show()
    app.MainLoop()
