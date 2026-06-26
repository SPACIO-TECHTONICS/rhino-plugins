# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import os
import json
import System
import System.Drawing
import System.IO
import Rhino
import Rhino.UI
import Eto.Forms as forms
import Eto.Drawing as drawing
import sys

Rhino.RhinoApp.WriteLine("--- RHINO CHARTS SYSTEM INITIALIZING v1.0.99 ---")

current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from assets.chart_display_conduit import ChartDisplayConduit


class RhinoChartsDashboard(forms.Form):
    """
    A modeless floating dashboard for RhinoCharts using Eto WebView.
    """

    def __init__(self):
        super(RhinoChartsDashboard, self).__init__()

        self.Title = "RhinoCharts Dashboard"
        self.ClientSize = drawing.Size(600, 600)
        self.WindowStyle = forms.WindowStyle.Default
        self.Topmost = True
        self.Owner = Rhino.UI.RhinoEtoApp.MainWindow

        self.setup_ui()

        self.conduit = ChartDisplayConduit()

        Rhino.RhinoDoc.SelectObjects += self.OnSelectObjects
        Rhino.RhinoDoc.DeselectObjects += self.OnSelectObjects
        Rhino.RhinoDoc.DeselectAllObjects += self.OnSelectObjects
        self.webview.DocumentTitleChanged += self.OnTitleChanged

    def setup_ui(self):
        self.webview = forms.WebView()

        assets_dir = os.path.dirname(__file__)
        plugin_dir = os.path.dirname(assets_dir)
        html_path = os.path.join(plugin_dir, "www", "index.html")

        if os.path.exists(html_path):
            self.webview.Url = System.Uri(html_path)
        else:
            Rhino.RhinoApp.WriteLine(
                "RhinoCharts ERROR: Dashboard resource not found at: " + html_path
            )

        self.Content = self.webview

    def OnShown(self, e):
        """Called when window opens"""
        super(RhinoChartsDashboard, self).OnShown(e)

    def OnClosed(self, e):
        """Unsubscribe and clear conduit when window closes"""
        super(RhinoChartsDashboard, self).OnClosed(e)
        if hasattr(self, "conduit") and self.conduit:
            self.conduit.clear()

        try:
            Rhino.RhinoDoc.SelectObjects -= self.OnSelectObjects
            Rhino.RhinoDoc.DeselectObjects -= self.OnSelectObjects
            Rhino.RhinoDoc.DeselectAllObjects -= self.OnSelectObjects
            self.webview.DocumentTitleChanged -= self.OnTitleChanged
        except:
            pass

    def OnSelectObjects(self, sender, e):
        Rhino.RhinoApp.WriteLine("RhinoCharts: Selection updated.")

        doc = Rhino.RhinoDoc.ActiveDoc
        if not doc:
            return

        obj_ids = doc.Objects.GetSelectedObjects(False, False)

        data_list = []
        for obj in obj_ids:
            try:
                data_list.append(self.extract_object_data(obj))
            except:
                pass
            if len(data_list) >= 20:
                break

        self.update_browser({"objects": data_list})

    def extract_object_data(self, obj):
        doc = Rhino.RhinoDoc.ActiveDoc
        layer_index = obj.Attributes.LayerIndex
        layer_name = doc.Layers[layer_index].FullPath

        labels = ["Area", "Volume", "Z-Height"]
        values = [0, 0, 0]

        geom = obj.Geometry
        bbox = geom.GetBoundingBox(True)
        values[2] = round(bbox.Max.Z - bbox.Min.Z, 2)

        try:
            amp = Rhino.Geometry.AreaMassProperties.Compute(geom)
            if amp:
                values[0] = round(amp.Area, 2)

            vmp = Rhino.Geometry.VolumeMassProperties.Compute(geom)
            if vmp:
                values[1] = round(vmp.Volume, 2)
        except:
            pass

        if isinstance(geom, Rhino.Geometry.Curve):
            values[0] = round(geom.GetLength(), 2)
            labels[0] = "Length"
            values[1] = 0
            labels[1] = "N/A"

        return {
            "name": obj.Attributes.Name or "Unnamed Object",
            "layer": layer_name,
            "labels": labels,
            "values": values,
        }

    def update_browser(self, data):
        """Push data to the JavaScript environment"""
        try:
            json_data = json.dumps(data)
            script = "if(window.updateChart) {{ window.updateChart({}); }}".format(
                json_data
            )
            self.webview.ExecuteScript(script)
        except Exception as ex:
            Rhino.RhinoApp.WriteLine("RhinoCharts WebView Error: {}".format(ex))

    def OnTitleChanged(self, sender, e):
        """Handle signals from JavaScript via window title"""
        new_title = str(e.Title)

        if not new_title or new_title == "RhinoCharts Dashboard Pro":
            return

        try:
            if new_title == "SET_LOCATION":
                Rhino.RhinoApp.WriteLine(
                    "RhinoCharts: Initializing HUD repositioning..."
                )
                self.pick_hud_location()
                return

            if new_title == "CLOSE_HUD":
                Rhino.RhinoApp.WriteLine(
                    "RhinoCharts: Closing HUD via Dashboard toggle..."
                )
                if "overlay_window" in sys.modules:
                    sys.modules["overlay_window"].ChartOverlay.close_instance()
                return

            if new_title.startswith("DUMP:"):
                json_data = new_title[5:]
                Rhino.RhinoApp.WriteLine(
                    "RhinoCharts v1.0.99: DUMP received ({} chars).".format(
                        len(json_data)
                    )
                )

                Rhino.RhinoApp.WriteLine("RhinoCharts: Resolving HUD Paths...")
                assets_dir = os.path.dirname(__file__)
                plugin_dir = os.path.dirname(assets_dir)
                html_path = os.path.join(plugin_dir, "www", "index.html")
                Rhino.RhinoApp.WriteLine("RhinoCharts: HTML Path: " + str(html_path))

                if not os.path.exists(html_path):
                    Rhino.RhinoApp.WriteLine(
                        "RhinoCharts ERROR: HTML file missing at " + html_path
                    )
                    return

                def launch_hud():
                    try:
                        Rhino.RhinoApp.WriteLine(
                            "RhinoCharts: Reloading and Launching Overlay Window..."
                        )
                        if "overlay_window" in sys.modules:
                            reload(sys.modules["overlay_window"])
                        import overlay_window

                        overlay_window.ChartOverlay.show_or_update(html_path, json_data)
                        Rhino.RhinoApp.WriteLine(
                            "RhinoCharts: HUD Launch Command Finished."
                        )
                    except Exception as inner_ex:
                        Rhino.RhinoApp.WriteLine(
                            "RhinoCharts HUD EXECUTION ERROR: " + str(inner_ex)
                        )

                Rhino.RhinoApp.WriteLine("RhinoCharts: Dispatching to UI Thread...")
                from System import Action

                def execute_dispatch():
                    try:
                        forms.Application.Instance.Invoke(Action(launch_hud))
                        return True
                    except:
                        try:
                            Rhino.RhinoApp.InvokeOnUiThread(Action(launch_hud))
                            return True
                        except:
                            return False

                if not execute_dispatch():
                    Rhino.RhinoApp.WriteLine(
                        "RhinoCharts: All thread jumps failed. Forcing immediate execution..."
                    )
                    launch_hud()
                else:
                    Rhino.RhinoApp.WriteLine(
                        "RhinoCharts: Dispatch command sent successfully."
                    )

            elif new_title.startswith("RELOAD"):
                Rhino.RhinoApp.WriteLine("RhinoCharts: Reloading Dashboard...")
                self.webview.Reload()
            elif new_title.startswith("ERROR:"):
                Rhino.RhinoApp.WriteLine(
                    "RhinoCharts UI Bridge Error: {}".format(new_title[6:])
                )
        except Exception as fatal_ex:
            Rhino.RhinoApp.WriteLine("RhinoCharts FATAL BRIDGE ERROR: " + str(fatal_ex))

    def pick_hud_location(self):
        """Allows the user to pick a point in the viewport and moves the HUD there."""
        try:
            from Rhino.Input import RhinoGet
            from Rhino.Commands import Result

            res, pt = RhinoGet.GetPoint(
                "Pick new HUD location (Top-Left corner)", False
            )
            if res != Result.Success:
                return

            view = Rhino.RhinoDoc.ActiveDoc.Views.ActiveView
            if not view:
                return

            client_pt = view.MainViewport.WorldToClient(pt)
            screen_pt = view.ClientToScreen(client_pt)

            def move_hud():
                try:
                    if "overlay_window" in sys.modules:
                        overlay = sys.modules["overlay_window"].ChartOverlay.instance()
                        if overlay:
                            overlay.Location = drawing.Point(screen_pt.X, screen_pt.Y)
                            Rhino.RhinoApp.WriteLine(
                                "RhinoCharts: HUD moved to [{}, {}]".format(
                                    screen_pt.X, screen_pt.Y
                                )
                            )
                        else:
                            Rhino.RhinoApp.WriteLine(
                                "RhinoCharts: HUD must be visible to move it."
                            )
                except Exception as ex:
                    Rhino.RhinoApp.WriteLine("RhinoCharts: Move Error - " + str(ex))

            from System import Action

            forms.Application.Instance.Invoke(Action(move_hud))

        except Exception as ex:
            Rhino.RhinoApp.WriteLine("RhinoCharts PICK ERROR: " + str(ex))
