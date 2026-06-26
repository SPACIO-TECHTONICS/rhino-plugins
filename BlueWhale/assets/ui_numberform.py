import Rhino.UI  # type: ignore
import Eto.Drawing as drawing  # type: ignore
import Eto.Forms as forms  # type: ignore

class NumberForm(forms.Dialog):
    def __init__(self,title, *titles):
        # Set up the dialog title and size
        self.Title = title
        self.ClientSize = drawing.Size(300, 200)

        # Create a dictionary to store the number boxes
        self.number_boxes = {}

        # Create form controls dynamically based on titles
        for title in titles:
            number_box = forms.NumericUpDown()
            self.number_boxes[title] = number_box

        self.button = forms.Button()
        self.button.Text = "Submit"
        self.button.Click += self.button_Click

        # Create a layout for the controls
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)

        for title in titles:
            layout.AddRow(forms.Label(Text=title), self.number_boxes[title])

        layout.AddRow(None)  # Adds an empty row for spacing
        layout.AddRow(self.button)

        # Set the dialog content to the layout
        self.Content = layout

    def button_Click(self, sender, e):
        # Handle the button click event
        values = {}

        for title in self.number_boxes:
            value = self.number_boxes[title].Value
            values[title] = value

        self.Tag = values  # Store the form values in the dialog Tag property
        self.Close()

def show_eto_form_with_titles(*titles):
    # Create an instance of the dialog
    dialog = NumberForm(*titles)

    # Show the dialog
    dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    # Return the form values
    return dialog.Tag

