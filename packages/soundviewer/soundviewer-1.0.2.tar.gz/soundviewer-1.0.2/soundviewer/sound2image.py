import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import argparse
import audio_metadata
import cv2


class Conf:
    
    def __init__(self,duration):

        self.sampling_rate = 44100
        self.duration = duration + 1 # sec
        self.hop_length = int(self.sampling_rate * self.duration / 1000)
        self.n_mels = 128
        self.n_fft = 2048
        self.samples = self.sampling_rate * duration


def get_audio_data(conf, pathname, trim_long_data):
    audio_data, sr = librosa.load(pathname)

    if len(audio_data):
        audio_data, _ = librosa.effects.trim(audio_data)

    if len(audio_data) > conf.samples:
        if trim_long_data:
            audio_data = audio_data[0:0+conf.samples]
    else:
        padding = conf.samples - len(audio_data)
        offset = padding // 2
        audio_data = np.pad(
            audio_data, (offset, conf.samples - len(audio_data) - offset), 'constant')

    return audio_data


def audio_to_melspectrogram(conf, audio):
    spectrogram = librosa.feature.melspectrogram(y=audio,
                                                 sr=conf.sampling_rate,
                                                 n_mels=conf.n_mels,
                                                 hop_length=conf.hop_length,
                                                 n_fft=conf.n_fft,
                                                 fmin=0.0,
                                                fmax=None
                                                 )
    return spectrogram


def read_as_melspectrogram(conf, pathname, trim_long_data):
    audio_data = get_audio_data(conf, pathname, trim_long_data)
    melspectrogram = audio_to_melspectrogram(conf, audio_data)
    return melspectrogram


def rename_file(img_name):
    img_name = img_name.split("/")[-1]
    img_name = img_name.split(".")[0]
    img_name += ".png"
    return img_name


def save_image_from_sound(sound_path,show_image=False,output=""):
    info = audio_metadata.load(sound_path)
    output = output.strip()
    if output:
        filename = output
    else:
        filename = rename_file(sound_path)
    wav_conf = Conf( int(info.streaminfo.duration))
    x = read_as_melspectrogram(
        wav_conf, sound_path, trim_long_data=False)

    if show_image:
        plt.figure(figsize=(12, 4))
        librosa.display.specshow(x, sr=wav_conf.sampling_rate,
                                 hop_length=wav_conf.hop_length, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()
        plt.show()


    cv2.imwrite(filename, x)
    return x

sound_to_image = save_image_from_sound

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="",  help="input sound file path")
    parser.add_argument("--show", action="store_true", default=False, help="show image")
    parser.add_argument("--output", type=str, default="",  help="output image file path")
    args = parser.parse_args()

    save_image_from_sound(args.input,show_image=args.show,output=args.output)

