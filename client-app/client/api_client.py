import requests
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.steganography import LSBSteganography

class APIClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.stego = LSBSteganography()

    def register(self, username, password, original_image_path):
        temp_image_path = "temp_register_image.png"
        try:
            self.stego.hide_password(original_image_path, password, temp_image_path)
            url = f"{self.server_url}/register"
            with open(temp_image_path, 'rb') as f:
                files = {'image': f}
                data = {'username': username}
                response = requests.post(url, files=files, data=data)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if os.path.exists(temp_image_path): os.remove(temp_image_path)