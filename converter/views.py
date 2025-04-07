from django.shortcuts import render
from django.http import FileResponse
from PIL import Image
import os
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO

def home(request):
    return render(request, 'converter/home.html')

def convert_image(request):
    if request.method == 'POST' and request.FILES:
        images = request.FILES.getlist('images')
        conversion_type = request.POST.get('conversion_type')
        
        output_zip = BytesIO()
        with ZipFile(output_zip, 'w') as zipf:
            for img in images:
                with Image.open(img) as im:
                    filename = os.path.splitext(img.name)[0]
                    
                    # Convert based on user selection
                    if conversion_type == 'jpg_to_png':
                        output_filename = f"{filename}.png"
                        img_format = 'PNG'
                    elif conversion_type == 'png_to_jpg':
                        output_filename = f"{filename}.jpg"
                        img_format = 'JPEG'
                        if im.mode in ("RGBA", "P"):  # PNG with transparency
                            im = im.convert("RGB")
                    else:
                        continue
                    
                    # Save to zip
                    buffer = BytesIO()
                    im.save(buffer, format=img_format)
                    buffer.seek(0)
                    zipf.writestr(output_filename, buffer.read())

        output_zip.seek(0)
        return FileResponse(output_zip, as_attachment=True, filename='converted_images.zip')

    return render(request, 'home.html')
