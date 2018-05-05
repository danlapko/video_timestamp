# 2b811a3cdb09ca9b525bc073e91af4f3
import pytesseract
from pytesseract import Output
import textract
import cv2
from difflib import SequenceMatcher
import editdistance


def get_slide_texts(path):
    text = textract.process(path).decode('utf-8')
    slides = text.split("\u000c")
    return slides


def filter_text(text):
    res = filter(lambda x: "а" <= x <= "я" or "А" <= x <= "Я" or
                           "a" <= x <= "z" or "A" <= x <= "Z", text)
    # res = text
    return "".join(res)


def get_image_text(img, lang="rus+eng"):
    d = pytesseract.image_to_boxes(img, lang=lang, output_type=Output.DICT)
    return "".join(d['char'])


def strings_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()


def best_slide(img_text, slide_texts, len_text_tresh):
    best_ratio = float('inf')
    best_i = -1
    for i, slide in enumerate(slide_texts):
        if len(slide) == 0 or len(img_text) / len(slide) <= len_text_tresh:
            continue
        ratio = (editdistance.eval(img_text, slide) - (len(slide) - len(img_text))) / len(img_text)
        # dist = strings_similarity(img_text, slide)
        if ratio < best_ratio:
            best_i = i
            best_ratio = ratio
    return best_i, best_ratio


if __name__ == "__main__":
    pdf_path = "data/cpp_lec6.pdf"
    path = "data/recognized.png"

    slides = get_slide_texts(pdf_path)

    for i, slide in enumerate(slides):
        slides[i] = filter_text(slide)

    img = cv2.imread(path)
    img_text = get_image_text(img)
    img_text = filter_text(img_text)

    best_slide_i, ratio = best_slide(img_text, slides, 0.1)
    print("======== best_slide=", best_slide_i, "ratio=", ratio, "=======")
    print(slides[best_slide_i])
    print(img_text)
