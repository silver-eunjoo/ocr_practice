from google.cloud import vision_v1p3beta1
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont
import os
# import translate_v3_translate_text

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\silver\\translate-ocr-408705-3a41838f941a.json'

# Cloud Vision API와 Translate API 클라이언트 생성
vision_client = vision_v1p3beta1.ImageAnnotatorClient()
translate_client = translate.Client()

# 원본 이미지 파일 로드
original_image_path = 'C:\silver\example5.png'
with open(original_image_path, 'rb') as original_image_file:
    original_content = original_image_file.read()

# Cloud Vision API를 사용하여 텍스트 감지
original_image = vision_v1p3beta1.Image(content=original_content)
response = vision_client.text_detection(image=original_image)

# 추출된 텍스트를 번역하고 번역된 텍스트만 담긴 빈 이미지 생성
if response.text_annotations:
    translations = []
    for text in response.text_annotations:
        extracted_text = text.description
        translation = translate_client.translate(extracted_text, target_language='en')
        translated_text = translation['translatedText']
        translations.append(translated_text)

    # 번역된 텍스트를 담은 빈 이미지 생성
    width, height =  (590, 868) # 빈 이미지의 크기 설정
    background_color = (255, 255, 255)  # 배경색 설정 (흰색)
    output_image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(output_image)
    font = ImageFont.load_default()

    # 번역된 텍스트를 빈 이미지에 추가
    y_position = 100  # 텍스트의 시작 위치 설정
    for translated_text in translations:
        draw.text((100, y_position), translated_text, fill=(0, 0, 0), font=font)
        y_position += 30  # 다음 텍스트의 세로 위치 설정

    # 결과 이미지를 저장
    output_image_path = 'C:\silver\\result10.png'
    output_image.save(output_image_path)

    # 결과 이미지를 표시하거나 필요한 작업을 수행
    output_image.show()

    # 결과 이미지를 저장한 경로를 반환
    print(f'번역된 텍스트를 담은 결과 이미지: {output_image_path}')