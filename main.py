import json
import wave
import pymorphy2
import soundfile as sf

from vosk import Model, KaldiRecognizer, SetLogLevel
morph = pymorphy2.MorphAnalyzer()

# конвертер
data, samplerate = sf.read('terq.ogg')
sf.write('new_file.wav', data, 42000, 'PCM_16', 'FILE', format='WAV')

SetLogLevel(0)

# функция лемматизации
def lemmatize(text):
    words = text.split() # разбиваем текст на слова
    res = list()
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)

    return res

# def main() -> None:
# делаем слова из файла
wf = wave.open('new_file.wav', "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    exit(1)

model = Model("vosk-model22")
rec = KaldiRecognizer(model, wf.getframerate())
with open('voice_text.txt', 'w', encoding='utf-8') as file:
    while True:
        data = wf.readframes(16000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            rec_text = json.loads(rec.Result())
            # print(rec_text.get("text"))
            file.writelines(f'{rec_text.get("text")}\n')
        else:
            pass

# with open("voice_text.txt") as file:
    # text = file.readlines()

# print(lemmatize(rec_text.get("text")))

terr = lemmatize(rec_text.get("text"))
MyFile = open('result.txt', 'w', encoding='utf-8')
terr = map(lambda x: x + ' ', terr)
MyFile.writelines(terr)
MyFile.close()