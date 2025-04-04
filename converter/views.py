from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import os

# Ensure temp directory exists
TEMP_DIR = os.path.join(settings.BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def home(request):
    return render(request, "converter/home.html")

def convert_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]  # Get the uploaded file
        temp_image_path = os.path.join(TEMP_DIR, image_file.name)

        # Save the uploaded file
        with open(temp_image_path, "wb") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Open the image using PIL (Pillow)
        try:
            image = Image.open(temp_image_path)
        except Exception as e:
            return render(request, "converter/home.html", {"error": f"Error opening image: {e}"})

        # Define output path
        output_path = temp_image_path.rsplit(".", 1)[0] + ".png"

        # Convert and save the image
        image.save(output_path, "PNG")

        # Read the converted file
        with open(output_path, "rb") as f:
            converted_image = f.read()

        # Clean up temp files
        os.remove(temp_image_path)
        os.remove(output_path)

        # Send file to user
        from django.http import HttpResponse
        response = HttpResponse(converted_image, content_type="image/png")
        response["Content-Disposition"] = "attachment; filename=converted.png"
        return response

    return render(request, "converter/home.html", {"error": "No file uploaded."})
