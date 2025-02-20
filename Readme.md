# QR Code Generator with Logo

A Streamlit-based web application that generates customizable QR codes with embedded logos, custom colors, and border styles.

## Features

- Generate QR codes with custom URLs
- Embed company logos or images into QR codes
- Customize QR code colors
- Choose from multiple border styles (Solid, Dashed, Dotted)
- High error correction for reliable scanning
- Automatic logo sizing and positioning
- Download generated QR codes as PNG files
- Real-time preview
- Input validation and error handling
- Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/qr-code-generator
cd qr-code-generator
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter a URL and upload a logo:
   - Type or paste the destination URL
   - Upload your logo (supported formats: PNG, JPG, JPEG)
   - Choose a custom color for the QR code
   - Select a border style
   - Click "Generate QR Code"

4. Download the generated QR code using the "Download QR Code" button

## Technical Details

### QR Code Specifications
- Default QR Version: 5
- Error Correction Level: H (High)
- Box Size: 10
- Border Size: 4
- Logo Size: 25% of QR code size (max 150x150 pixels)

### Supported File Formats
- Logo Input: PNG, JPG, JPEG
- QR Code Output: PNG

### Dependencies
See requirements.txt for the complete list of dependencies.

## Error Handling

The application includes comprehensive error handling for:
- Invalid URLs
- Unsupported image formats
- Corrupt image files
- Invalid file types
- Processing errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **QR Code Not Scanning**
   - Ensure the URL is correctly entered
   - Try reducing logo size
   - Ensure sufficient contrast between QR code and background

2. **Logo Upload Issues**
   - Verify file format (PNG, JPG, JPEG only)
   - Check file size
   - Ensure image isn't corrupted

3. **Application Won't Start**
   - Verify all dependencies are installed
   - Check Python version (3.7+ required)
   - Ensure Streamlit is properly installed

### Getting Help

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the error message in the application
3. Create an issue in the GitHub repository

## Requirements

See requirements.txt for specific version requirements.