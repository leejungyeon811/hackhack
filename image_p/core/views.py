import cv2
import numpy as np
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def building(image):

    model = YOLO("./runs/detect/train/weights/best.pt")
    results = model(image)
    detections = results[0].boxes.data.cpu().numpy()
    mask = np.zeros(img.shape[:2], dtype=np.unit8)

    for *box, conf, cls in detections:
        if cls == 0:  # class 0은 building
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = 255
        elif cls == 1:  # class 1은 sign
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = 255

    inpainted_img = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    _, buffer = cv2.imencode('.jpg', inpainted_img)
    response_image = ContentFile(buffer.tobytes())

    return response_image

def text(image):
    return 0

def sign(image):
    return 0

@csrf_exempt
def process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        image_array = np.frombuffer(image_file_read(), np.uint8)
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        #front에서 building = check일 때
        img = building(img)

        #front에서 sign = check일 때
        #img = sign(img)

        #front에서 text = check일 때 
        #img = text(img)

        return HttpResponse(img, content_type='image/jpeg')
    return HttpResponse(status=400)