import wx 

class windowClass(wx.Frame):
    def __init__(self, *args, **kwgs):
        wx.Frame.__init__(self, *args, **kwgs)
        self.Centre()
        # self.Move((800,0))#(x,y)axis
        self.basicGUI()


    def basicGUI(self):
        panel = wx.Panel(self)

        menuBar=wx.MenuBar()

        fileButton=wx.Menu()
        editButton=wx.Menu()

        exitItem=fileButton.Append(wx.ID_EXIT,'Exit','status msg ...')
        
        menuBar.Append(fileButton,'File')
        menuBar.Append(editButton,'Edit')

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU,self.Quit,exitItem)

        wx.TextCtrl(panel,pos=(10,10),size=(250,100))




        yesNoBox = wx.MessageBox('Do you enjoy wxPython?', 'Question', wx.YES_NO | wx.ICON_QUESTION)
        if yesNoBox == wx.YES:
            print("User clicked Yes")
        elif yesNoBox == wx.NO:
            print("User clicked No")
        else:
            print("User closed the dialog without clicking any button")



        self.SetTitle('Epic Window')
        self.Show(True)

    def Quit(self,e):
        self.Close()  


app=wx.App()
app1 =windowClass(None,title='my window 1')
# app2 =windowClass(None,title='my window 2')
app.MainLoop()