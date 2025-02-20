
# This app generates a QR code with a logo in the center and directs users to a specified URL upon scanning.

import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import io

async def main():
    st.title("QR Code Generator with Logo", "Create QR codes with a personal touch")

    url = st.text_input("URL", placeholder="e.g., https://www.google.com", key="url")
    logo_file = st.file_uploader("Logo", type=["png", "jpg", "jpeg"], key="logo")

    color = st.color_picker("QR Code Color", value="#000000", key="color")
    border_style = st.selectbox("Border Style", ["Solid", "Dashed", "Dotted"], key="border_style")

    submitted = st.button("Generate QR code")

    if submitted:
        if not url or not logo_file:
            st.error("Please enter both the URL and logo.")
        else:
            # Create a QR code
            qr = qrcode.QRCode(
                version=5,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create an image from the QR code instance
            img = qr.make_image(fill_color=color, back_color="white")

            # Add the logo to the QR code
            logo = Image.open(logo_file)
            logo = logo.resize((100, 100))  # Resize the logo to fit in the QR code
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos)

            # Add border to the QR code
            if border_style == "Dashed":
                draw = ImageDraw.Draw(img)
                for i in range(0, img.size[0], 10):
                    draw.line([(i, 0), (i, 10)], fill=color, width=2)
                for i in range(0, img.size[1], 10):
                    draw.line([(0, i), (10, i)], fill=color, width=2)
            elif border_style == "Dotted":
                draw = ImageDraw.Draw(img)
                for i in range(0, img.size[0], 10):
                    draw.ellipse([(i, 0), (i+2, 2)], fill=color)
                for i in range(0, img.size[1], 10):
                    draw.ellipse([(0, i), (2, i+2)], fill=color)

            # Display the generated QR code
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            st.image(img_bytes.getvalue())

            # Allow users to download the QR code
            st.download_button("Download QR code", img_bytes.getvalue(), "qrcode.png", "image/png")
