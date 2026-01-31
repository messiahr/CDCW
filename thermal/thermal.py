
from escpos.printer import Usb

VENDOR_ID = 0x0483
PRODUCT_ID = 0x5743

class TicketPrinter:
    def print_ticket(self, id):
        try:
            # This configuration just works.
            # Tweak to work with your printer.
            p = Usb(VENDOR_ID, PRODUCT_ID, 0, 0x81, 0x03)
            p.text("Scan this code: \n")
            p.qr(id, native=True, size = 8)
            for i in range(5):
                p.text("\n")
            p.cut()
        except Exception as e:
            print(f"Error: {e}")
