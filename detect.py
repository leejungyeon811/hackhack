import pytesseract
from PIL import Image
import konlpy
from konlpy.tag import Okt
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Tesseract 경로 설정 (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# 텍스트 인식 (OCR)
# 이미지 열기
img = Image.open("14659928_1.jpg")

# OCR 수행
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img, config=custom_config, lang='kor+eng')  # 한글 표지판의 경우 'kor' 사용
print(text)

#자연어 처리 (NLP)
okt = Okt()
doc = okt.pos(text)

# # 품사 태깅 및 명명된 개체 인식
# for token in doc:
#     print(token.text, token.pos_, token.ent_type_)

# # 예시: 특정 정보 추출 (예: 지명, 도로명 등)
# for ent in doc.ents:
#     print(ent.text, ent.label_)