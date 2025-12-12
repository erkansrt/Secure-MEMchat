from PIL import Image

class LSBSteganography:
    def __init__(self):
        self.delimiter = "-----END-----"

    def text_to_bin(self, text):
        return ''.join(format(ord(i), '08b') for i in text)

    def hide_password(self, image_path, password, output_path):
        full_message = password + self.delimiter
        binary_msg = self.text_to_bin(full_message)
        msg_len = len(binary_msg)
        
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        data_index = 0
        for y in range(height):
            for x in range(width):
                if data_index < msg_len:
                    r, g, b = pixels[x, y]
                    new_r = (r & ~1) | int(binary_msg[data_index])
                    pixels[x, y] = (new_r, g, b)
                    data_index += 1
                else:
                    break
        img.save(output_path, "PNG")

    def extract_password(self, image_path):
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        binary_data = ""
        # Basitlik için ilk 4000 biti okuyalım (yeterince uzun)
        limit = 4000 
        count = 0
        
        for y in range(height):
            for x in range(width):
                if count >= limit: break
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                count += 1
            if count >= limit: break

        extracted_text = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) < 8: break
            char = chr(int(byte, 2))
            extracted_text += char
            if extracted_text.endswith(self.delimiter):
                return extracted_text.replace(self.delimiter, "")
        return None