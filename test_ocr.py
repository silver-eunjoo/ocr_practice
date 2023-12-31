"""Detects text in the file."""
from google.cloud import vision, translate
import openai
from openai import OpenAI
import io
import os
# import translate_v3_translate_text



# def detect_document(path) :
#     """Detects document features in an image."""
#     from google.cloud import vision
#
#     client = vision.ImageAnnotatorClient()
#
#     # [START vision_python_migration_document_text_detection]
#     with open(path, "rb") as image_file:
#         content = image_file.read()
#
#     image = vision.Image(content=content)
#
#     response = client.document_text_detection(image=image)
#
#     for page in response.full_text_annotation.pages:
#         for block in page.blocks:
#             print(f"\nBlock confidence: {block.confidence}\n")
#
#             for paragraph in block.paragraphs:
#                 print("Paragraph confidence: {}".format(paragraph.confidence))
#
#                 for word in paragraph.words:
#                     word_text = "".join([symbol.text for symbol in word.symbols])
#                     print(
#                         "Word text: {} (confidence: {})".format(
#                             word_text, word.confidence
#                         )
#                     )
#                     # word : word
#                     # symbol : letter
#                     for symbol in word.symbols:
#                         print(
#                             "\tSymbol: {} (confidence: {})".format(
#                                 symbol.text, symbol.confidence
#                             )
#                         )
#
#     if response.error.message:
#         raise Exception(
#             "{}\nFor more info on error messages, check: "
#             "https://cloud.google.com/apis/design/errors".format(response.error.message)
#         )
#     # [END vision_python_migration_document_text_detection]
def detect_text() :
    client = vision.ImageAnnotatorClient()
    path = 'C:\silver\example6.png'

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    price_candidate = []
    card_number_candidate = []
    date_candidate = []

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    # texts 는 각 단어들의 좌표값이랑 단어들의 배열임. (단어를 추출할 때는 .description)

    #이어서 텍스트로 쭉 추출하려면?
    # resource = ""
    # resource = texts[0].description
    resource = texts[0].description.replace('\n', ' ')
    # num = 1
    # print(texts[1].bounding_poly.vertices[0].x, texts[1].bounding_poly[0].vertices[0])


    for text in texts:
        content = text.description
        # print(text.bounding_poly.vertices[0])
        # print(num, end =":")
        # num+=1
        # print(content)
        # content = content.replace('\n',' ')
        # print('{}'.format(content))
        # print(content, end="")
        # resource+=content3
    return resource

# def translate_text(target: str, text: str) -> dict:
#     """Translates text into the target language.
#
#     Target must be an ISO 639-1 language code.
#     See https://g.co/cloud/translate/v2/translate-reference#supported_languages
#     """
#     from google.cloud import translate_v2 as translate
#
#     translate_client = translate.Client()
#
#     if isinstance(text, bytes):
#         text = text.decode("utf-8")
#
#     # Text can also be a sequence of strings, in which case this method
#     # will return a sequence of results for each text.
#     result = translate_client.translate(text, target_language=target)
#
#     print("Text: {}".format(result["input"]))
#     print("Translation: {}".format(result["translatedText"]))
#     print("Detected source language: {}".format(result["detectedSourceLanguage"]))
#
#     return result

# Initialize Translation client
def translate_text(
    text: str = "YOUR_TEXT_TO_TRANSLATE", project_id: str = "YOUR_PROJECT_ID"
) -> translate.TranslationServiceClient:
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    # glossary = client.glossary_path(parent_id, location, 'loco_translator_glossary')
    # 특정 뜻으로 번역할 용어집 (glossary)'를 적용하기 위한 code
    # 나중에 DB에 있는 단어들을 바꿔줘야할 때 쓰면 될 것 같음.

    # glossary_config = translate.TranslationServiceClient(glossary=glossary)

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French ex) en_US -> fr, zh-CN, ru
    # 지금은 한국어 -> 영어로 바꿔보겠음.
    # 참고 사이트 : https://blog.naver.com/ansrl23/223084035195
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "ko",
            "target_language_code": "en",
            #glossary_config" : glossary_config 마찬가지로 특수 용어들을 특정 의미로 바꿀 때 써주면 될 것 같음.
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print("Translated text:", end="")
        translated = translation.translated_text
        print(translation.translated_text)
        # print("origianl text : ", text)
        # print(f"Translated text: {translation.translated_text}")

    return translated


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def restructuring(text):
    texts=[{"role" : "user", "content" : ""},]
    client = OpenAI()
    question = "다음의 내용을 있는 문자 그대로 형식만 알아보기 쉽게 줄 띄움 좀 해줘. 번역할 필요는 없어. 내용은 다음과 같아. " + text
    texts.append({"role" : "user", "content" : question},)

    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=texts
    )
    reply = chat.choices[0].message.content
    texts.append({"role" : "assistant", "content" : reply})
    print("Restructured : ", reply)

    return reply

def matching(original, translated) :
    texts=[{"role" : "user", "content" : ""},]
    client = OpenAI()
    question = "1번 내용이 원본이고 2번 내용이 번역본이야. 한 문장씩 매칭해서 두 텍스트를 비교해서 보여줘. 예를 들어 안녕하세요 띄우고 Hello처럼 말이야. 번역본과 원본을 비교하면서 보기 쉽게 출력해줬으면 좋겠어. 1번 내용 : " + original + " 2번 내용 : " + translated + "출력할 때는 원본 : ~ 줄 띄우고 번역본 : ~ 이렇게 해줘!"
    texts.append({"role" : "user", "content" : question})

    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=texts
    )

    reply = chat.choices[0].message.content
    texts.append({"role" : "assistant", "content" : reply})
    print("Matching : ", reply)


if __name__ == "__main__":
    resource = detect_text()
    print()
    print("content : ", resource)
    response = translate_text(resource, "translate-ocr-408705")
    print()
    restructred = restructuring(response)
    matching(resource, restructred)