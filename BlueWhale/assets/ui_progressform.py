# -*- coding: utf-8 -*-
import Rhino.UI  # type: ignore
import Eto.Drawing as drawing  # type: ignore
import Eto.Forms as forms  # type: ignore
import System.ComponentModel  # type: ignore
import osm_fetcher
reload(osm_fetcher)

class OSMDownloadDialog(forms.Dialog):
    def __init__(self, bbox):
        self.bbox = bbox
        self.result_path = None
        self.error_message = None
        
        self.Title = "OSM Online Import"
        self.ClientSize = drawing.Size(400, 120)
        self.Padding = drawing.Padding(10)
        self.WindowStyle = forms.WindowStyle.Default
        self.Resizable = False
        
        # UI Elements
        self.status_label = forms.Label(Text="Connecting to online service...")
        self.progress_bar = forms.ProgressBar()
        self.progress_bar.Indeterminate = True
        
        self.cancel_button = forms.Button(Text="Cancel")
        self.cancel_button.Click += self.on_cancel_click
        
        # Layout
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        layout.AddRow(self.status_label)
        layout.AddRow(self.progress_bar)
        layout.AddRow(None)
        layout.AddRow(self.cancel_button)
        self.Content = layout
        
        # Background Worker
        self.worker = System.ComponentModel.BackgroundWorker()
        self.worker.WorkerSupportsCancellation = True
        self.worker.DoWork += self.do_work
        self.worker.RunWorkerCompleted += self.on_worker_completed
        
        # Start immediately
        self.Shown += self.on_shown

    def on_shown(self, sender, e):
        self.worker.RunWorkerAsync()

    def do_work(self, sender, e):
        try:
            def update_status(text):
                # We need to use Invoke to update UI from background thread
                forms.Application.Instance.AsyncInvoke(lambda: self.set_status(text))
            
            def check_cancel():
                return self.worker.CancellationPending
            
            path = osm_fetcher.fetch_osm_xml(
                self.bbox, 
                update_callback=update_status,
                cancel_check=check_cancel
            )
            e.Result = path
        except Exception as ex:
            self.error_message = str(ex)
            raise ex

    def set_status(self, text):
        self.status_label.Text = text

    def on_worker_completed(self, sender, e):
        if e.Error:
            self.error_message = str(e.Error)
            self.status_label.Text = "Error: " + self.error_message
            self.progress_bar.Indeterminate = False
            self.cancel_button.Text = "Close"
        elif e.Cancelled:
            self.status_label.Text = "Cancelled."
            self.Close()
        else:
            self.result_path = e.Result
            self.Close()

    def on_cancel_click(self, sender, e):
        if self.worker.IsBusy:
            self.worker.CancelAsync()
            self.cancel_button.Enabled = False
            self.status_label.Text = "Cancelling..."
        else:
            self.Close()

class ModelCreationProgress(forms.Form):
    def __init__(self, total, message="Creating 3D Model..."):
        # Initialize internal state first
        self.total = total
        self.current = 0
        
        # UI Setup
        self.Title = "UrbanDesign 4 Rhino"
        self.ClientSize = drawing.Size(400, 100)
        self.Padding = drawing.Padding(20)
        self.WindowStyle = forms.WindowStyle.Default
        self.Topmost = True
        
        self.status_label = forms.Label(Text=message)
        self.progress_bar = forms.ProgressBar()
        self.progress_bar.MinValue = 0
        self.progress_bar.MaxValue = total
        self.progress_bar.Value = 0
        
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(10, 10)
        layout.AddRow(self.status_label)
        layout.AddRow(self.progress_bar)
        self.Content = layout
        
        # Position the window
        owner = Rhino.UI.RhinoEtoApp.MainWindow
        self.Owner = owner
        self.Location = drawing.Point(owner.Location.X + (owner.Width - self.Width) / 2,
                                     owner.Location.Y + (owner.Height - self.Height) / 2)

    def update(self, value, message=None):
        """Update the progress bar and label."""
        self.progress_bar.Value = min(value, self.total)
        if message:
            self.status_label.Text = message
        
        # Force UI update while on the main thread
        forms.Application.Instance.RunIteration()

    def show(self):
        self.Show()

    def close(self):
        self.Close()

def download_osm_with_progress(bbox):
    """
    Shows a progress dialog and downloads OSM data.
    Returns: Path to file or None.
    """
    dialog = OSMDownloadDialog(bbox)
    dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    
    if dialog.error_message and not dialog.result_path:
        import rhinoscriptsyntax as rs
        rs.MessageBox("OSM Import Failed:\n\n" + dialog.error_message, 0, "Error")
        return None
        
    return dialog.result_path
