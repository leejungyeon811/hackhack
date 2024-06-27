import os
import cv2
import pytesseract
from PIL import Image
import konlpy
from konlpy.tag import Okt
from pytesseract import Output
import numpy as np

# Tesseract 경로 설정 (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
# 환경 변수 설정
os.environ['TESSDATA_PREFIX'] = r'C:/Program Files/Tesseract-OCR/tessdata'

# 텍스트 인식 (OCR)
# 이미지 열기
image_path = "870x531-pb100.jpg"
img = cv2.imread(image_path)

# # 이미지 전처리 (선택 사항)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

# img_thresh = cv2.adaptiveThreshold(
#     img_blurred, 
#     maxValue=255.0, 
#     adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#     thresholdType=cv2.THRESH_BINARY_INV, 
#     blockSize=19, 
#     C=9
# )

# OCR 수행
custom_config = r'--oem 3 --psm 6 outputbase digits'
details = pytesseract.image_to_string(img, output_type=pytesseract.Output.DICT, config=custom_config, lang='kor+eng')  # 한글 표지판의 경우 'kor' 사용
digit=pytesseract.image_to_string(img, lang='digits', config="--psm 11 --oem 3") 
detection = pytesseract.image_to_data(img, config="--psm 11 --oem 3", output_type=Output.DICT)

n_boxes = len(detection['level'])
for i in range(n_boxes):
    if detection['text'][i].isdigit():
        (x, y, w, h) = (detection['left'][i], detection['top'][i], detection['width'][i], detection['height'][i])
 
        # 주변 색을 계산 (여기서는 상하좌우 픽셀을 평균하여 주변 색을 결정)
        surrounding_color = (
                int(np.mean(img[y-10:y+h+10, x-10:x+10, 0])),
                int(np.mean(img[y-10:y+h+10, x-10:x+10, 1])),
                int(np.mean(img[y-10:y+h+10, x-10:x+10, 2]))
            )
        cv2.rectangle(img, (x, y), (x + w, y + h), surrounding_color, -1)

# 결과 이미지를 저장하거나 출력합니다
base_name = os.path.basename(image_path)
name, ext = os.path.splitext(base_name)
output_image_path = f'{name}_converted{ext}'
cv2.imwrite(output_image_path, img)
