import io
import base64
import qrcode
import barcode
from barcode.writer import ImageWriter

def test():
    student_info = {'name': 'Test', 'roll': '123', 'gpa': '5.00'}
    qr = qrcode.QRCode(version=1, box_size=3, border=1)
    qr_data = f"Name: {student_info['name']} | Roll: {student_info['roll']} | GPA: {student_info['gpa']}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    print("QR Code generated successfully.")

    code128 = barcode.get_barcode_class('code128')
    barcode_img = code128('1234567890', writer=ImageWriter())
    
    bar_buffer = io.BytesIO()
    barcode_img.write(bar_buffer, options={"module_height": 8.0, "write_text": False, "quiet_zone": 2.0})
    print("Barcode generated successfully.")

try:
    test()
except Exception as e:
    import traceback
    traceback.print_exc()
