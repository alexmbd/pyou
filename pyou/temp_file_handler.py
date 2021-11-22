import tempfile
import requests
from io import BytesIO


class TempFileHandler(tempfile.TemporaryDirectory):
    def __init__(self) -> None:
        super().__init__()

    def add_file(self, url: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".jpg", mode="w+b", dir=self.name, delete=False) as tf:
            temp = requests.get(url)
            temp_bytes = BytesIO(temp.content).read()
            tf.write(temp_bytes)
            return tf.name
