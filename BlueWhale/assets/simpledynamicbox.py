import Rhino.UI  # type: ignore
import Eto.Drawing as drawing  # type: ignore
import Eto.Forms as forms  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

class SimpleEtoDialog(forms.Dialog):
    
    def __init__(self):
        self.Title = "Sample Eto Dialog"
        self.ClientSize = drawing.Size(500, 300)
        self.Padding = drawing.Padding(5)
        self.Resizable = False
        
        text = forms.TextArea(Text = "Lol")
        

        button = forms.Button(Tag=text)
        button.Text = "Click Me!"
        button.Click += self.OnPushPickButton
        
        layout = forms.DynamicLayout()
        layout.AddRow(text,button)
        self.Content = layout
        
    def OnPickPoint(self, sender, e):

        rs.GetPoints()
        #Rhino.Input.RhinoGet.GetPoint("Pick a point", True)
        
    def OnPushPickButton(self, sender, e):
        Rhino.UI.EtoExtensions.PushPickButton(self, self.OnPickPoint)
        button = sender
        name_box = button.Tag
        print(name_box.Text)
        
dialog = SimpleEtoDialog()
dialog.Show(Rhino.UI.RhinoEtoApp.MainWindow)