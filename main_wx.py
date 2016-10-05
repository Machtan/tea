import sys
import wx
import os

class Editor(wx.Frame):
    def __init__(self, parent, title, size=(500, 500), *args, **kwargs):
        super().__init__(parent, *args, title=title, size=size, **kwargs)
        self.current_directory = os.getcwd()
        self.current_file = None
        self.init_widgets()
    
    def init_widgets(self):
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        
        m_file = wx.Menu()
        i_open = m_file.Append(wx.ID_ANY, "Open")
        self.Bind(wx.EVT_MENU, self.on_open, i_open)
        
        menubar = wx.MenuBar()
        # Only add the menu if this isn't macOS (as the default items are kept in the <program name> menu item)
        #i_about = None
        if sys.platform != "darwin":
            m_program = wx.Menu()
            i_about = m_program.Append(wx.ID_ABOUT, "About", "Information about this program")
            m_program.AppendSeparator()
            i_quit = m_program.Append(wx.ID_EXIT, "Quit", "Terminate the program?")
            menubar.Append(m_program, "Program")
        else:
            i_about = m_file.Append(wx.ID_ABOUT, "About")
            i_quit = m_file.Append(wx.ID_EXIT, "Quit")
        
        self.Bind(wx.EVT_MENU, self.on_about, i_about)
        
        menubar.Append(m_file, "File")
        self.SetMenuBar(menubar)
        
        self.Show(True)
    
    def on_about(self, event):
        print("About clicked!")
        about_text = """\
        A simple code editor to hack away on
        next line\
        """
        dialog = wx.MessageDialog(self, about_text, "", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    
    def on_open(self, event):
        print("Open clicked!: ({})".format(event))
        # TODO use FD_MULTIPLE
        dialog = wx.FileDialog(
            self, defaultDir=self.current_directory, wildcard="*.*",
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST,
        )
        dialog.SetWindowStyleFlag(0)#wx.CAPTION)
        #dialog.SetTitle("")
        print([a for a in dir(dialog) if not a.startswith("__")])
        if dialog.ShowModal() == wx.ID_CANCEL:
            return
        
        self.current_file = dialog.GetFilename()
        self.current_directory = dialog.GetDirectory()
        path = os.path.join(self.current_directory, self.current_file)
        title = "{} - {}".format(
            self.current_file, os.path.basename(self.current_directory)
        )
        self.SetTitle(title)
        with open(path) as f:
            self.control.SetValue(f.read())
        
        dialog.Destroy()

def main():
    """Entry point"""
    app = wx.App(False) # Don't redirect stdout/stderr to a window
    # A frame is a top-level window
    #frame = wx.Frame(None, wx.ID_ANY, "Hello World") 
    #frame.Show(True) # Show the frame
    frame = Editor(None, "Editor test")
    app.MainLoop()

if __name__ == '__main__':
    main()