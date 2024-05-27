import re
import emoji
import string
from nltk.corpus import stopwords


def convert_emoticons(text):
    #text = re.escape(text)
    for emot in EMOTICONS_EMO:

        text = text.replace(emot, "_".join(EMOTICONS_EMO[emot].replace(",","").split()))
    return text
# Example
print('before Remove emoji')
print(df.iloc[1645,0])
print('After Remove emoji')
convert_emoticons(df.iloc[1645,0][1:-1])

def convert_emojis(text):
    for emot in UNICODE_EMOJI:
        text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()))
    return text
# Example
print('before Remove emoji')
print(df.iloc[387,0])
print('After Remove emoji')
convert_emojis(df.iloc[387,0][1:-1])

punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''' + string.punctuation
Otherpunc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

stop_words = stopwords.words('arabic')
arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)

def CleanData(text):

    # Remove usernames
    text = re.sub(r'@[^\s]+','',text)

    # Remove URL
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)

    # Remove None arabic
    text = re.sub(u"[^\u0621-\u063A\u0640-\u0652 ]", " ", text)
    text= re.sub(r'([@A-Za-z0-9_ـــــــــــــ]+)|[^\w\s]|#|http\S+', '', text)

    # Remove punctuations
    translator = str.maketrans('', '', punctuations)
    text = text.translate(translator)
    # translator2 = str.maketrans('', '', Otherpunc)
    # text = text.translate2(translator2)

    # Remove repeating character
    text = re.sub(r'(.)\1+', r'\1', text)


    # Remove tashkeel
    text = re.sub(arabic_diacritics, '', text)

    #Remove elongation
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)

    text= re.sub(r'هه+', 'face_with_tears_of_joy', text)
    text= convert_emojis(text)
    text= convert_emoticons(text)

    # Remove emojis
    text=  emoji.demojize(text)
    text= re.sub(r'(:[!_\-\w]+:)', ' ', text)

    # Remove numbers
    text = ''.join(i for i in text if not i.isdigit())

    # Remove repeated letters like "الللللللللللللللله" to "الله"
    text= text[0:2] + ''.join([text[i] for i in range(2, len(text)) if text[i]!=text[i-1] or text[i]!=text[i-2]])

    # Remove stop words
    text = ' '.join(word for word in text.split() if word not in stop_words)

    return text
