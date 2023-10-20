import obsws_python as obsws

class OBS:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def connect(self):
        self.ws = obsws.ReqClient(
            host = self.host,
            port = self.port,
            password = self.password
        )

    def get_capture(self, scene_name: str, srouce_name: str, filepath: str):
        self.connect()
        item_list = self.ws.get_scene_item_list(scene_name).scene_items
        for item in item_list:
            if item["sourceName"] == srouce_name:
                self.ws.save_source_screenshot(
                    name=item["sourceName"],
                    img_format="png",
                    file_path=filepath,
                    width=1280,
                    height=720,
                    quality=-1
                )
