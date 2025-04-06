from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import os
import zipfile
from io import BytesIO

# Ensure temp directory exists
TEMP_DIR = os.path.join(settings.BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def home(request):
    return render(request, "converter/home.html")

def convert_image(request):
    if request.method == "POST":
        files = request.FILES.getlist("images")
        if not files:
            return HttpResponse("No files were uploaded.")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in files:
                if file.name.endswith(".jpg") or file.name.endswith(".jpeg"):
                    img = Image.open(file)
                    file_name = os.path.splitext(file.name)[0] + ".png"

                    img_io = BytesIO()
                    img.save(img_io, format="PNG")
                    zip_file.writestr(file_name, img_io.getvalue())

        zip_buffer.seek(0)
        return FileResponse(zip_buffer, as_attachment=True, filename="converted_images.zip")

    return HttpResponse("Invalid request.")
