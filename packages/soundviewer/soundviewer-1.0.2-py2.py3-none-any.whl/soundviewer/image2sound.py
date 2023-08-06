import librosa
import cv2
from pendulum import duration
from soundviewer.sound2image import Conf
import numpy as np
import soundfile
import argparse


def rename_file(img_name):
    img_name = img_name.split("/")[-1]
    img_name = img_name.split(".")[0]
    img_name += ".wav"
    return img_name


def image_to_sound(image_path, output = ''):

        m=cv2.imread(image_path,0)
        duration = m.shape[-1]/250
        conf = Conf( duration=duration)
        img=m.astype(np.float32)
        output = output.strip()
        if output:
            filename = output
        else:
            filename = rename_file(image_path)

        sound=librosa.feature.inverse.mel_to_audio(img,
                                                sr=conf.sampling_rate,
                                                hop_length=conf.hop_length,
                                                n_fft=conf.n_fft,
                                                pad_mode='reflect',
                                                )
        samplerate = int(conf.sampling_rate/2)
        soundfile.write(filename,sound,samplerate=samplerate)
        return filename , sound



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="",  help="input sound file path")
    parser.add_argument("--output", type=str, default="",  help="output image file path")
    args = parser.parse_args()

    image_to_sound(args.input, args.output)
