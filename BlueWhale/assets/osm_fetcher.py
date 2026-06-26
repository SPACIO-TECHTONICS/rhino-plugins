# -*- coding: utf-8 -*-
import System.Net  # type: ignore
import tempfile
import os

class TimeoutWebClient(System.Net.WebClient):
    """ Custom WebClient with longer timeout """
    def GetWebRequest(self, uri):
        w = System.Net.WebClient.GetWebRequest(self, uri)
        w.Timeout = 300000 # 5 minutes in milliseconds
        return w

def fetch_osm_xml(bbox, update_callback=None, cancel_check=None):
    """
    Fetches OSM XML data from Overpass API for a given bounding box.
    bbox: tuple (min_lat, min_lon, max_lat, max_lon)
    update_callback: function to call with status updates
    cancel_check: function that returns True if we should stop
    Returns: Path to a temporary XML file containing the data.
    """
    # Overpass QL query with a 180-second server-side timeout
    query = '[out:xml][timeout:180];(node({0});way({0});relation({0}););out body;>;out skel qt;'.format(
        ",".join(map(str, bbox))
    )
    
    url = "https://overpass-api.de/api/interpreter?data=" + System.Uri.EscapeDataString(query)
    
    # Configure TLS 1.2
    System.Net.ServicePointManager.SecurityProtocol = System.Net.SecurityProtocolType.Tls12
    
    web_client = TimeoutWebClient()
    web_client.Headers.Add("User-Agent", "UrbanDesign4Rhino-RhinoPlugin")
    
    # Handle cancellation
    if cancel_check and cancel_check():
        return None

    try:
        # Create a temporary file path
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "overpass_query_result.osm")
        
        # Perform the download
        try:
            if update_callback: update_callback("Fetching model...")
            web_client.DownloadFile(url, temp_path)
            return temp_path
        except System.Net.WebException as we:
            # If 504 (Timeout), try the Standard OSM API as failover
            error_msg = str(we)
            if "504" in error_msg:
                # Standard API Format: min_lon,min_lat,max_lon,max_lat
                std_url = "https://www.openstreetmap.org/api/0.6/map?bbox={1},{0},{3},{2}".format(*bbox)
                
                # Retry download with standard API
                web_client.DownloadFile(std_url, temp_path)
                return temp_path
            else:
                # Re-raise for other types of errors (429, etc)
                raise we
        
    except System.Net.WebException as we:
        error_msg = str(we)
        if "504" in error_msg:
            description = "Server Timeout (504). The area might be too large or the server is busy."
        elif "429" in error_msg:
            description = "Too many requests (429). Please wait a moment."
        else:
            description = error_msg
        
        if update_callback: update_callback("Error: " + description)
        raise Exception(description)
        
    except Exception as e:
        if update_callback: update_callback("Error: " + str(e))
        raise e
    finally:
        web_client.Dispose()
