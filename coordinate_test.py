from google.cloud import vision_v1p3beta1
from google.cloud import translate_v2 as translate
from PIL import Image, ImageDraw, ImageFont
import os
# import translate_v3_translate_text

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\silver\\translate-ocr-408705-3a41838f941a.json'

# Cloud Vision API와 Translate API 클라이언트 생성
vision_client = vision_v1p3beta1.ImageAnnotatorClient()
translate_client = translate.Client()

# 이미지 파일 로드
image_path = 'C:\silver\example5.png'
with open(image_path, 'rb') as image_file:
    content = image_file.read()

# Cloud Vision API를 사용하여 텍스트 감지
image = vision_v1p3beta1.Image(content=content)
response = vision_client.text_detection(image=image)

# 추출된 텍스트를 번역하고 좌표에 다시 출력
if response.text_annotations:
    image = Image.open(image_path)
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for text in response.text_annotations:
        bounding_box = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        extracted_text = text.description
        translation = translate_client.translate(extracted_text, target_language='en')
        translated_text = translation['translatedText']

        # 번역된 텍스트를 원래 좌표에 출력
        draw.text(bounding_box[0], translated_text, fill=(0, 0, 0), font=font)


    image.save('output_image.jpg')