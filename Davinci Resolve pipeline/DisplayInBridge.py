import requests
import json
from threading import Thread

class PlaylistItem:
    def __init__(self, id, URI, rows, cols, aspect, viewCount, tag="", durationMS=20000,
                 depthiness=0, depth_cutoff=0, focus=0, depth_loc=0, cam_dist=0, fov=0, zoom=1,
                 crop_pos_x=0, crop_pos_y=0, quilt_size_x=4096, quilt_size_y=4096,
                 doDepthInversion=False, chromaDepth=False, isRGBD=0):
        self.id = id
        self.URI = URI.replace("\\", "\\\\")  # Adjust for JSON
        self.rows = rows
        self.cols = cols
        self.aspect = aspect
        self.viewCount = viewCount
        self.tag = tag
        self.durationMS = durationMS
        self.isRGBD = isRGBD
        self.depthiness = depthiness
        self.depth_cutoff = depth_cutoff
        self.focus = focus
        self.depth_loc = depth_loc
        self.cam_dist = cam_dist
        self.fov = fov
        self.zoom = zoom
        self.crop_pos_x = crop_pos_x
        self.crop_pos_y = crop_pos_y
        self.quilt_size_x = quilt_size_x
        self.quilt_size_y = quilt_size_y
        self.depth_inversion = 1 if doDepthInversion else 0
        self.chroma_depth = 1 if chromaDepth else 0

    def to_json(self, session, playlist_name):
        return json.dumps({
            "orchestration": session["Token"],
            "name": playlist_name,  # Use the playlist name directly
            "index": self.id,
            "uri": self.URI,
            "rows": self.rows,
            "cols": self.cols,
            "aspect": self.aspect,
            "view_count": self.viewCount,
            "durationMS": self.durationMS,
            "isRGBD": self.isRGBD,
            "depth_inversion": self.depth_inversion,
            "chroma_depth": self.chroma_depth,
            "crop_pos_x": self.crop_pos_x,
            "crop_pos_y": self.crop_pos_y,
            "quilt_size_x": self.quilt_size_x,
            "quilt_size_y": self.quilt_size_y,
            "depthiness": self.depthiness,
            "depth_cutoff": self.depth_cutoff,
            "depth_loc": self.depth_loc,
            "focus": self.focus,
            "cam_dist": self.cam_dist,
            "fov": self.fov,
            "zoom": self.zoom,
            "tag": self.tag
        })


class Playlist:
    def __init__(self, name, loop=True):
        self.name = name
        self.loop = loop
        self.items = []

    def add_quilt_item(self, URI, rows, cols, aspect, viewCount, tag="whatever whatever", durationMS=20000):
        item = PlaylistItem(id=len(self.items), URI=URI, rows=rows, cols=cols,
                            aspect=aspect, viewCount=viewCount, tag=tag, durationMS=durationMS)
        self.items.append(item)

    def add_rgbd_item(self, URI, rows, cols, aspect, depthiness, depth_cutoff, focus, depth_loc,
                      cam_dist, fov, tag="whatever whatever", zoom=1, crop_pos_x=0, crop_pos_y=0,
                      quilt_size_x=4096, quilt_size_y=4096, doDepthInversion=False, chromaDepth=False,
                      durationMS=20000):
        item = PlaylistItem(id=len(self.items), URI=URI, rows=rows, cols=cols, aspect=aspect,
                            depthiness=depthiness, depth_cutoff=depth_cutoff, focus=focus, depth_loc=depth_loc,
                            cam_dist=cam_dist, fov=fov, tag=tag, zoom=zoom, crop_pos_x=crop_pos_x,
                            crop_pos_y=crop_pos_y,
                            quilt_size_x=quilt_size_x, quilt_size_y=quilt_size_y, doDepthInversion=doDepthInversion,
                            chromaDepth=chromaDepth, durationMS=durationMS, isRGBD=1, viewCount=1)
        self.items.append(item)

    def remove_item(self, id):
        del self.items[id]
        for i, item in enumerate(self.items):
            item.id = i

    def get_instance_json(self, session):
        return json.dumps({
            "orchestration": session["Token"],
            "name": self.name,
            "loop": str(self.loop).lower()
        })

    def get_playlist_items_as_json(self, session):
        return [item.to_json(session, self.name) for item in self.items]

    def get_play_playlist_json(self, session, head):
        return json.dumps({
            "orchestration": session["Token"],
            "name": self.name,
            "head_index": head
        })

    # Additional method to convert individual playlist items to JSON
    def to_json(self, session):
        return json.dumps({item.id: item.__dict__ for item in self.items})


class BridgeConnectionHTTP:
    def __init__(self, url='localhost', port=33334, web_socket_port=9724):
        self.url = url
        self.port = port
        self.web_socket_port = web_socket_port
        self.all_displays = {}
        self.lkg_displays = {}
        self.event_listeners = {}
        self.connection_state_listeners = set()
        self.last_connection_state = False
        self.session = None
        self.current_playlist_name = ""
        self.client = None
        self.web_socket_thread = None
        self.web_socket = None

    def close_web_socket(self):
        if self.web_socket_thread and self.web_socket:
            self.web_socket.close()
            self.web_socket_thread.join()  # Wait for the WebSocket thread to terminate
            print("WebSocket connection closed.")

    def _web_socket_listener(self):
        def on_message(ws, message):
            json_message = json.loads(message)
            payload = json_message.get('payload', {}).get('value')
            if payload:
                event_name = payload['event']['value']
                for listener in self.event_listeners.get(event_name, []):
                    listener(json.dumps(payload))
                for listener in self.event_listeners.get('', []):
                    listener(json.dumps(payload))

        def on_error(ws, error):
            print(error)

        def on_close(ws, close_status_code, close_msg):
            print("### websocket closed ###")
            self.update_connection_state(False)

        def on_open(ws):
            self.update_connection_state(True)

    def update_connection_state(self, state):
        self.last_connection_state = state
        for callback in self.connection_state_listeners:
            callback(self.last_connection_state)
        return self.last_connection_state

    def connect(self, timeout_seconds=300):
        # Initialize the requests.Session here before setting timeout
        self.client = requests.Session()
        self.client.timeout = timeout_seconds
        self.web_socket_thread = Thread(target=self._web_socket_listener)
        self.web_socket_thread.start()
        # Assuming immediate connection success; in practice, you might need to wait/check for actual connection success
        return self.update_connection_state(True)

    def try_send_message(self, endpoint, content):
        try:
            response = self.client.put(f"http://{self.url}:{self.port}/{endpoint}", data=content)
            self.update_connection_state(True)
            return response.text
        except requests.RequestException as e:
            print(e)
            self.update_connection_state(False)
            return None

    def __del__(self):
        if self.web_socket:
            self.web_socket.close()
        if self.client:
            self.client.close()

    def try_enter_orchestration(self, name="default"):
        message = json.dumps({"name": name})
        resp = self.try_send_message("enter_orchestration", message)
        if resp:
            resp_json = json.loads(resp)
            if "payload" in resp_json and "value" in resp_json["payload"]:
                self.session = {"Token": resp_json["payload"]["value"]}
                return True
        return False

    def try_exit_orchestration(self):
        if not self.session:
            return False
        message = json.dumps({"orchestration": self.session["Token"]})
        resp = self.try_send_message("exit_orchestration", message)
        print(resp)
        if resp:
            self.session = None
            return True
        return False

    def try_show_window(self, show_window, head=-1):
        if not self.session:
            return False
        message = json.dumps({
            "orchestration": self.session["Token"],
            "show_window": show_window,
            "head_index": head
        })
        resp = self.try_send_message("show_window", message)
        print(resp)
        return resp is not None

    def try_play_playlist(self, playlist, head=-1):
        if not self.session:
            print("Session not established.")
            return False

        # Remove current playlist
        delete_message = playlist.get_instance_json(self.session)
        print("Sending delete playlist message:", delete_message)
        resp = self.try_send_message("delete_playlist", delete_message)
        print("Received response:", resp)

        print("Attempting to show window.")
        self.try_show_window(True, head)

        message = playlist.get_instance_json(self.session)
        print("Sending instance playlist message:", message)
        resp = self.try_send_message("instance_playlist", message)
        print("Received response:", resp)

        playlist_items = playlist.get_playlist_items_as_json(self.session)
        for index, p_message in enumerate(playlist_items):
            print(f"Sending playlist item {index} message:", p_message)
            resp = self.try_send_message("insert_playlist_entry", p_message)
            print("Received response:", resp)

        self.current_playlist_name = playlist.name

        play_message = playlist.get_play_playlist_json(self.session, head)
        print("Sending play playlist message:", play_message)
        resp = self.try_send_message("play_playlist", play_message)
        print("Received response:", resp)

        return True


class BridgePreview:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_image": ("IMAGE",),
                "depthiness": ("FLOAT", {"default": 2.0, "min": 0, "max": 3.0}),
                "focus": ("FLOAT", {"default": 0, "min": -1.0, "max": 1.0, "step": 0.001}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "process_image"
    CATEGORY = "Null Nodes"

    def __init__(self, url='localhost', port=33334, web_socket_port=9724, orchestration_name="default"):
        self.url = url
        self.port = port
        self.web_socket_port = web_socket_port
        self.orchestration_name = orchestration_name
        self.counter = 0

    def connect_to_bridge(self):
        self.bridge = BridgeConnectionHTTP(self.url, self.port, self.web_socket_port)
        print("Attempting to connect to bridge...")
        if self.bridge.connect():
            print("Connected to bridge successfully.")
            if self.bridge.try_enter_orchestration(self.orchestration_name):
                print(f"Entered orchestration '{self.orchestration_name}'.")
                return True
            else:
                print(f"Failed to enter orchestration '{self.orchestration_name}'.")
        else:
            print("Failed to connect to bridge.")
        return False

    def cleanup(self):
        if self.bridge:
            self.bridge.try_exit_orchestration()
            print("Exited orchestration and cleaned up the bridge connection.")

    def __del__(self):
        self.cleanup()