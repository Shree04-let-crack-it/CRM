from googletrans import Translator

translator = Translator()

def translate_text(text, lang_code):
    if lang_code == "en":
        return text
    try:
        return translator.translate(text, dest=lang_code).text
    except:
        return text
