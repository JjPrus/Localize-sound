from scipy.io.wavfile import read
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave


def lag_finder(y1, y2, sr):
    """Zwraca różnicę w przybyciu sygnału do mikrofonów w sekundach
    y1 - sygnał z pierwszego mikrofonu
    y2 - sygnał z drugiego mikrofonu
    sr - ilość próbek"""

    n = len(y1)
    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)]
                                                           * signal.correlate(y2, y2, mode='same')[int(n/2)])

    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    return abs(delay) / 100


def get_audio(chunk, channels, rate, record_time):
    """Nagrywa dźwięk z mikrofonu
    chunk - na ile próbek dzielimy sygnał
    channels - liczba kanałów (stereo - 2)
    rate - próbkowanie w Hz
    record_time - czas nagrania"""

    format = pyaudio.paInt16
    wave_output_filename1 = "output1.wav"
    wave_output_filename2 = "output2.wav"
    p = pyaudio.PyAudio()

    stream1 = p.open(format=format,
                     channels=channels,
                     rate=rate,
                     input=True,
                     frames_per_buffer=chunk,
                     input_device_index=0)
    stream2 = p.open(format=format,
                     channels=channels,
                     rate=rate,
                     input=True,
                     frames_per_buffer=chunk,
                     input_device_index=1)

    frames1 = []
    frames2 = []

    for i in range(0, int(rate / chunk * record_time)):
        data1 = stream1.read(chunk)
        data2 = stream2.read(chunk)
        frames1.append(data1)
        frames2.append(data2)

    stream1.stop_stream()
    stream1.close()
    stream2.stop_stream()
    stream2.close()
    p.terminate()

    wf = wave.open(wave_output_filename1, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames1))
    wf.close()

    wf = wave.open(wave_output_filename2, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames2))
    wf.close()


for i in range(5):
    get_audio(1024, 2, 44100, 1)
    sample_rate1, data1 = read('output1.wav')
    sample_rate2, data2 = read('output2.wav')
    t = np.arange(0, data1.shape[0], 1)

    fig, axes = plt.subplots(2, 1, figsize=(20, 6))
    axes[0].plot(t, data1)
    axes[1].plot(t, data2)
    axes[0].set_ylabel("Sygnał 1", fontsize=14)
    axes[1].set_ylabel("Sygnał 2", fontsize=14)
    plt.show()
