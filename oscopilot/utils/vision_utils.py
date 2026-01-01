import os
from datetime import datetime
import base64

def screen_capture(save_dir) -> str:
    """ Return path of print screen """
    # Create a timestamped filename
    ob_name = "screenshot_{t}.jpg".format(t=datetime.now().strftime("%Y%m%d_%H%M%S"))
    img_path = os.path.join(save_dir, ob_name)

    # PowerShell command to take a screenshot
    os.system(f"""
        powershell.exe \"
            Add-Type -AssemblyName System.Windows.Forms
            [Windows.Forms.Sendkeys]::SendWait('+{{Prtsc}}')
            \$img = [Windows.Forms.Clipboard]::GetImage()
            \$img.Save('{img_path}', [Drawing.Imaging.ImageFormat]::Jpeg)\"
    """)
    print(f"Screenshot saved at {img_path}")
    return img_path

def encode_image(image_path) -> str:
    with open(image_path, 'rb') as image_file:
        
        # Read the file
        image_data = image_file.read()
        # Encode the image
        encoded_image = base64.b64encode(image_data)
        # Convert to a UTF-8 string
        encoded_string = encoded_image.decode('utf-8')
        return encoded_string
