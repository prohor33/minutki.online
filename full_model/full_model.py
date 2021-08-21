
from vosk import Model, KaldiRecognizer
import sys
import subprocess

import sys

sys.path.insert(0, 'neuro-comma/src')

from pathlib import Path
from neuro_comma.predict import RepunctPredictor



class FullModel():

    def __init__(self):
        print("Create vosk model...")
        self.vosk_model_create(path_to_model="models/vosk-model-ru-0.10")
        print("Create punctuation model...")
        self.punct_model_create()
        # create ner model

    def vosk_model_create(self, path_to_model):
        self.sample_rate=16000
        self.model = Model(path_to_model)
        self.rec = KaldiRecognizer(self.model, self.sample_rate)

    def vosk_model_run(self, path_to_file):
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                            path_to_file,
                            '-ar', str(self.sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                            stdout=subprocess.PIPE)

        results = []

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
                
            if self.rec.AcceptWaveform(data):
                results.append(self.rec.Result())
            else:
                results.append(self.rec.PartialResult())
        text = []
        for res in results:
            res = eval(res)
            if "text" in res:
                text.append(res["text"])
        return " ".join(text)


    def punct_model_create(self):
        self.punct_model = RepunctPredictor(model_name='repunct-model-new',
                             models_root=Path('models'),
                             model_weights='weights_ep6_9912.pt',
                             quantization=False,
                             device="cuda:1"
                            )

    def punct_model_run(self, text):
        return self.punct_model(text)

    def ner_model_create(self, ):
        pass

    def ner_model_run(self, ):
        pass