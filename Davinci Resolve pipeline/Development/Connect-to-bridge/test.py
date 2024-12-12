from DisplayInBridge import BridgePreview

bp = BridgePreview()
bp.connect_to_bridge()


# url='localhost'
# port=33334
# web_socket_port=9724
# orchestration_name="enter_orchestration"
# data = {
#     "name": "default"
# }
# import requests
# # response = requests.get(f"http://{url}:{port}/{orchestration_name}")
# response = requests.post(f"http://{url}:{port}/{orchestration_name}", json=data)
# print (response.json)

# import requests
# response = requests.get("http://localhost:33334/bridge_version")
# print (response.text)

