from escpos.printer import Usb
from PIL import Image
import os

VENDOR_ID = 0x0483
PRODUCT_ID = 0x5743
IN_ENDPOINT = 0x81
OUT_ENDPOINT = 0x03


class TicketPrinter:
    def __init__(self):
        self.p = Usb(VENDOR_ID, PRODUCT_ID)#, 0, IN_ENDPOINT, OUT_ENDPOINT)
        # Load the image
        try:
            image_path = os.path.join(os.path.dirname(__file__), "waltham_center.png")
            self.image = Image.open(image_path)
            max_width = 384
            if self.image.size[0] > max_width:
                ratio = max_width / float(self.image.size[0])
                new_height = int(self.image.size[1] * ratio)
                self.image = self.image.resize((max_width, new_height), Image.Resampling.NEAREST)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image = None

    def print_ticket(self, id):
        try:
            if self.image:
                self.p.image(self.image, impl="bitImageColumn")
            self.p.text("Scan this code: \n")
            self.p.qr(id, native=True, size=8)
            for i in range(5):
                self.p.text("\n")
            self.p.cut()
        except Exception as e:
            print(f"Error: {e}")

    def print_custom(self, text, qr_code=None, newlines=10):
        try:
            if self.image:
                self.p.image(self.image)
            if text:
                self.p.text(text)
                if not text.endswith("\n"):
                    self.p.text("\n")

            if qr_code:
                # Using same settings as print_ticket, adjustable if needed
                self.p.qr(qr_code, native=True, size=8)

            for i in range(newlines):
                self.p.text("\n")

            self.p.cut()
        except Exception as e:
            print(f"Error: {e}")
            raise e
