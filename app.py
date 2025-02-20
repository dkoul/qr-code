import streamlit as st
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageEnhance
import io
from typing import Optional, Tuple
import validators

class QRCodeGenerator:
    def __init__(self):
        self.DEFAULT_QR_VERSION = 5
        self.DEFAULT_BOX_SIZE = 10
        self.DEFAULT_BORDER = 4
        self.LOGO_SIZE_RATIO = 0.25  # Logo will take up 25% of QR code
        self.MAX_LOGO_SIZE = (150, 150)
        self.SUPPORTED_FORMATS = ["png", "jpg", "jpeg"]

    def validate_url(self, url: str) -> bool:
        """Validate if the provided URL is well-formed."""
        return validators.url(url)

    def validate_logo(self, logo_file) -> Tuple[bool, str]:
        """Validate the uploaded logo file."""
        if not logo_file:
            return False, "No logo file provided"
        
        try:
            img = Image.open(logo_file)
            format_lower = img.format.lower()
            if format_lower not in self.SUPPORTED_FORMATS:
                return False, f"Unsupported image format. Please use {', '.join(self.SUPPORTED_FORMATS)}"
            return True, ""
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"

    def process_logo(self, logo: Image.Image, qr_size: Tuple[int, int]) -> Image.Image:
        """Process and resize logo to fit properly in QR code."""
        # Calculate logo size based on QR code size
        logo_size = int(min(qr_size) * self.LOGO_SIZE_RATIO)
        logo_size = min(logo_size, min(self.MAX_LOGO_SIZE))
        
        # Resize logo while maintaining aspect ratio
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Add white background to logo
        if logo.mode in ('RGBA', 'LA'):
            background = Image.new('RGBA', logo.size, 'WHITE')
            background.paste(logo, mask=logo.split()[-1])
            logo = background

        # Enhance logo contrast
        enhancer = ImageEnhance.Contrast(logo)
        logo = enhancer.enhance(1.5)
        
        return logo

    def add_border(self, img: Image.Image, style: str, color: str) -> Image.Image:
        """Add styled border to the QR code."""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        border_width = 2

        if style == "Solid":
            # Draw solid border
            draw.rectangle([(0, 0), (width-1, height-1)], outline=color, width=border_width)
        
        elif style == "Dashed":
            # Draw dashed border
            dash_length = 10
            for i in range(0, width, dash_length*2):
                draw.line([(i, 0), (min(i+dash_length, width), 0)], fill=color, width=border_width)
                draw.line([(i, height-1), (min(i+dash_length, width), height-1)], fill=color, width=border_width)
            for i in range(0, height, dash_length*2):
                draw.line([(0, i), (0, min(i+dash_length, height))], fill=color, width=border_width)
                draw.line([(width-1, i), (width-1, min(i+dash_length, height))], fill=color, width=border_width)
        
        elif style == "Dotted":
            # Draw dotted border
            dot_spacing = 10
            dot_size = 3
            for i in range(0, width, dot_spacing):
                draw.ellipse([(i, 0), (i+dot_size, dot_size)], fill=color)
                draw.ellipse([(i, height-dot_size), (i+dot_size, height)], fill=color)
            for i in range(0, height, dot_spacing):
                draw.ellipse([(0, i), (dot_size, i+dot_size)], fill=color)
                draw.ellipse([(width-dot_size, i), (width, i+dot_size)], fill=color)

        return img

    def generate_qr_code(self, url: str, logo_file, color: str, border_style: str) -> Optional[bytes]:
        """Generate QR code with logo and styling."""
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=self.DEFAULT_QR_VERSION,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for logo
                box_size=self.DEFAULT_BOX_SIZE,
                border=self.DEFAULT_BORDER,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create QR code image
            img = qr.make_image(fill_color=color, back_color="white")
            img = img.convert('RGBA')

            # Process and add logo
            logo = Image.open(logo_file)
            logo = self.process_logo(logo, img.size)
            
            # Calculate position to center logo
            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            
            # Create mask for smooth logo integration
            mask = Image.new('L', logo.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse([(0, 0), logo.size], fill=255)
            
            # Paste logo with mask
            img.paste(logo, pos, mask)

            # Add border
            img = self.add_border(img, border_style, color)

            # Convert to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG", optimize=True)
            return img_bytes.getvalue()

        except Exception as e:
            st.error(f"Error generating QR code: {str(e)}")
            return None

def main():
    st.set_page_config(page_title="QR Code Generator with Logo", layout="wide")
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-top: 1rem;
        }
        .stDownloadButton>button {
            width: 100%;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("QR Code Generator with Logo")
    st.subheader("Create professional QR codes with your logo")

    # Initialize QR code generator
    generator = QRCodeGenerator()

    # Create two columns for input and preview
    col1, col2 = st.columns([1, 1])

    with col1:
        url = st.text_input("Enter URL", placeholder="https://www.example.com")
        logo_file = st.file_uploader("Upload Logo", type=generator.SUPPORTED_FORMATS)
        color = st.color_picker("QR Code Color", value="#000000")
        border_style = st.selectbox("Border Style", ["Solid", "Dashed", "Dotted"])

        if st.button("Generate QR Code"):
            # Validate inputs
            if not url:
                st.error("Please enter a URL")
            elif not generator.validate_url(url):
                st.error("Please enter a valid URL")
            else:
                logo_valid, logo_error = generator.validate_logo(logo_file)
                if not logo_valid:
                    st.error(logo_error)
                else:
                    # Generate QR code
                    qr_bytes = generator.generate_qr_code(url, logo_file, color, border_style)
                    if qr_bytes:
                        # Store in session state for download
                        st.session_state.qr_bytes = qr_bytes
                        st.session_state.show_download = True

    with col2:
        if 'show_download' in st.session_state and st.session_state.show_download:
            st.image(st.session_state.qr_bytes, caption="Generated QR Code", use_column_width=True)
            filename = f"qr_code_{Path(url).stem}.png"
            st.download_button(
                "Download QR Code",
                st.session_state.qr_bytes,
                filename,
                "image/png",
                use_container_width=True
            )

if __name__ == "__main__":
    main()