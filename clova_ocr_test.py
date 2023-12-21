from google.cloud import vision_v1p3beta1
from google.cloud import translate_v2 as translate
import io
import os
# import translate_v3_translate_text

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\silver\\translate-ocr-408705-3a41838f941a.json'

# Cloud Vision API와 Translate API 클라이언트 생성
vision_client = vision_v1p3beta1.ImageAnnotatorClient()
translate_client = translate.Client()

# 이미지 파일 로드
with open('C:\silver\example5.png', 'rb') as image_file:
    content = image_file.read()

# Cloud Vision API를 사용하여 텍스트 감지
image = vision_v1p3beta1.Image(content=content)
response = vision_client.text_detection(image=image)
texts = response.text_annotations

# 추출된 텍스트를 번역하고 출력
if texts:
    extracted_text = texts[0].description
    extracted_text = extracted_text.replace('\n', ' ')  # 줄 바꿈 문자 제거
    sentences = extracted_text.split('. ')  # 문장 분리 (예: 마침표 뒤에 공백을 사용하여)

    translated_text = []
    for sentence in sentences:
        translation = translate_client.translate(sentence, target_language='en')
        translated_text.append(translation['translatedText'])

    translated_text = '. '.join(translated_text)  # 번역된 문장을 다시 합침
    print(translated_text)