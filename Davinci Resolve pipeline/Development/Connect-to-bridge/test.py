import os
import time
from DisplayInBridge import BridgePreview, Playlist

bp = BridgePreview()
bp.connect_to_bridge()

pl = Playlist("Preview", False)
# pl.add_quilt_item(f"{os.getcwd()}/../Test images/GreenBuddha/GreenBuddha_qs7x5a0.5625.jpg", 5, 7, 0.5625, 7 * 5)
# pl.add_quilt_item("https://s3.amazonaws.com/lkg-blocks/u/9aa4b54a7346471d/steampunk_qs8x13.jpg", 13, 8, 0.75, 13*8)
# pl.add_quilt_item("D:/Projects/- Looking Glass holograms/- Holograms Go -/themba_qs4x11a0.5625.png", 11, 4, 0.5625, 4*11)
# pl.add_quilt_item("D:/Projects/- Looking Glass holograms/- Holograms Go -/Labradorite_qs11x6a0.5602_C.png", 6, 11, 0.5625, 6*11)
pl.add_quilt_item("D:/Projects/- Looking Glass holograms/- Quilt projects -/Max Headroom/Render/Max Headroom/Max Headroom_qs59x5a0.5625.jpg", 5, 59, 0.5625, 5*59)

bp.bridge.try_play_playlist(pl)
time.sleep(5)
bp.bridge.try_show_window(False)