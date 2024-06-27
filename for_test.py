from googleapiclient.discovery import build
import requests
import os

# Google API 설정
api_key = "AIzaSyC8LGLso0eFC8jfgDCA3-QNws7jPQt21a8"
cse_id = "b36677029809947ea"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType='image', **kwargs).execute()
    return res['items']

def download_images(items, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    for i, item in enumerate(items):
        img_url = item['link']
        try:
            img_data = requests.get(img_url).content
            with open(os.path.join(folder_name, f'img_{i+1}.jpg'), 'wb') as handler:
                handler.write(img_data)
        except Exception as e:
            print(f"Could not download {img_url}: {e}")

# 검색어와 검색 결과 수 설정
search_terms = ["한국+교통안내표지판", "한국+도로명주소+표지판"]
num_images_per_batch = 10  # 한 번 요청할 때 다운로드할 이미지 수
total_images = 50  # 각 검색어별로 다운로드할 총 이미지 수
output_folder = 'source/sign_dataset_100'

for term in search_terms:
    for start_index in range(1, total_images, num_images_per_batch):
        try:
            items = google_search(term, api_key, cse_id, start=start_index, num=num_images_per_batch)
            download_images(items, os.path.join(output_folder, term.replace(" ", "_")))
        except Exception as e:
            print(f"Error occurred for term '{term}' starting at index {start_index}: {e}")
