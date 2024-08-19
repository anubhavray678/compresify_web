from django.http import HttpResponse
from django.shortcuts import render
from .utils.huffman import HuffmanCoding
import os
from django.conf import settings

def homepage(request):
    return render(request, "home.html")

# def compress_file(request):
#     if request.method == 'POST':
#         # Get the uploaded file
#         file = request.FILES['file']
#         original_file_path = os.path.join(settings.MEDIA_ROOT, file.name)

#         # Save the uploaded file temporarily
#         with open(original_file_path, 'wb+') as destination:
#             for chunk in file.chunks():
#                 destination.write(chunk)

#         # Compress the file using HuffmanCoding
#         h = HuffmanCoding(original_file_path)
#         compressed_file_path = h.compress()  # This stores the compressed file

#         # Decompress the file
#         decompressed_file_path = h.decompress(compressed_file_path)

#         # Prepare the decompressed file for download
#         with open(decompressed_file_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type='application/octet-stream')
#             response['Content-Disposition'] = f'attachment; filename="{os.path.basename(decompressed_file_path)}"'
        
#         # Clean up temporary files
#         os.remove(original_file_path)
#         os.remove(compressed_file_path)  # Remove the .bin file after decompression
#         os.remove(decompressed_file_path)
        
#         return response

#     return render(request, 'thankyou.html')



def compress_file(request):
    if request.method == 'POST':
        try:
            # Try to get the uploaded file
            file = request.FILES['file']
        except MultiValueDictKeyError:
            # Handle the case where 'file' is not found
            return HttpResponse("No file uploaded", status=400)
        
        # Ensure settings.MEDIA_ROOT is a string, not a list
        media_root = settings.MEDIA_ROOT
        if isinstance(media_root, list):
            media_root = media_root[0]  # Adjust this line depending on your setup

        original_file_path = os.path.join(media_root, file.name)

        # Save the uploaded file temporarily
        with open(original_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Compress the file using HuffmanCoding
        h = HuffmanCoding(original_file_path)
        compressed_file_path = h.compress()

        # Decompress the file
        decompressed_file_path = h.decompress(compressed_file_path)

        # Prepare the decompressed file for download
        with open(decompressed_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(decompressed_file_path)}"'
        
        # Clean up temporary files
        os.remove(original_file_path)
        os.remove(compressed_file_path)
        os.remove(decompressed_file_path)
        
        return response

    return render(request, 'thankyou.html')
