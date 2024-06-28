import cv2
import numpy as np
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
import logging
import os
import pytesseract
from pytesseract import Output


def set_path():

    pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
    os.environ['TESSDATA_PREFIX'] = r'C:/Program Files/Tesseract-OCR/tessdata'
    return 0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def service_page(request):
    return render(request, 'myapp/service.html')

def main_page(request):
    return render(request, 'myapp/main.html')

def info_page(request):
    return render(request, 'myapp/more_info.html')

def building(image):
    logger.info("Building function started")
    model = YOLO("../core/static/runs/best.pt")
    results = model(image)
    detections = results[0].boxes.data.cpu().numpy()
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    for *box, conf, cls in detections:
        if cls == 0:  # class 0은 building
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = 255
        elif cls == 1:  # class 1은 sign
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = 255

    inpainted_img = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    logger.info("Building function completed")
    return inpainted_img

def text(image):
    set_path()
    detection = pytesseract.image_to_data(image, config="--psm 11 --oem 3", output_type=Output.DICT)

    n_boxes = len(detection['level'])

    for i in range(n_boxes):
        if detection['text'][i].isdigit():
            (x, y, w, h) = (detection['left'][i], detection['top'][i], detection['width'][i], detection['height'][i])

            surrounding_color = (
                    int(np.mean(image[y-10:y+h+10, x-10:x+10, 0])),
                    int(np.mean(image[y-10:y+h+10, x-10:x+10, 1])),
                    int(np.mean(image[y-10:y+h+10, x-10:x+10, 2]))
                )
            cv2.rectangle(image, (x, y), (x + w, y + h), surrounding_color, -1)

    return image




def sign(image):

    logger.info("sign function started")
    model = YOLO("../core/static/runs/best_sign.pt")
    results = model(image)
    detections = results[0].boxes.data.cpu().numpy()
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    for *box, conf, cls in detections:
        if cls == 0:  # class 0은 building
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = 255
        elif cls == 1:  # class 1은 sign
            x1, y1, x2, y2 = map(int, box)
            mask[y1:y2, x1:x2] = 255

    inpainted_img = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    logger.info("sign function completed")
    return inpainted_img

@require_POST
@csrf_exempt
def process_image(request):
    try:
        logger.info("Process image function started")
        if request.method in 'POST' and request.FILES['image']:
            image_file = request.FILES['image']
            image_array = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            logger.info("Image successfully decoded")

            process_sign = request.POST.get('check_btn1') == 'true'
            process_text = request.POST.get('check_btn2') == 'true'
            process_building = request.POST.get('check_btn3') == 'true'

            # 필요한 처리 수행
            if process_building:
                logger.info("Building processing started")
                img = building(img)

            if process_sign:
                logger.info("Sign processing started")
                img = sign(img)

            if process_text:
                logger.info("Text processing started")
                img = text(img)

            # 이미지 인코딩
            _, buffer = cv2.imencode('.jpg', img)
            logger.info("Image successfully encoded")
            return HttpResponse(buffer.tobytes(), content_type='image/jpeg')
        
        logger.error("Invalid request method or no image uploaded")
        return JsonResponse({'error': 'Invalid request method or no image uploaded'}, status=400)
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
