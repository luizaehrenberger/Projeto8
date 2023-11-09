import soundfile as sf
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as sg

#Define a função de filtro
def filtro(y, samplerate, cutoff_hz):
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = sg.kaiserord(ripple_db, width)
    taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = sg.lfilter(taps, 1.0, y)
    return yFiltrado

#Define a classe do sinal
class signalMeu:
    def __init__(self):
        self.init = 0

    def __init__(self):
        self.init = 0
 
    def calcFFT(self, signal, fs):
        N  = len(signal)
        W = sg.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs, titulo):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier {}'.format(titulo))
#Inicia a classe do sinal
signal = signalMeu()

#################################Variáveis###################################
freq_leitura = 44100
freq_portadora = 14000
##############################################################################
# # Abre o arquivo de áudio modulado
# sd.default.samplerate = freq_leitura  #taxa de amostragem
# sd.default.channels = 1 
# tGravacao = 5 #tempo de gravação
# numAmostras = int(sd.default.samplerate * tGravacao)

# # Grava o áudio modulado
# print('Gravando...')
# audio_modulado = sd.rec(int(numAmostras), freq_leitura, channels=1)
# sd.wait()
# print('Audio Gravado')

# # Toca o áudio modulado
# print('Audio Modulado...')
# sd.play(audio_modulado, freq_leitura)
# sd.wait()
# print('Fim do Audio Modulado')

#################################MODULADO####################################
audio_modulado, freq_leitura = sf.read('audio.wav')
signal.plotFFT(audio_modulado, freq_leitura, 'modulado')

audio_samples = len(audio_modulado)
duracao = audio_samples/freq_leitura
vetor_tempo = np.linspace(0, 4, audio_samples)

#definindo a portadora
senoide_portadora = 1 * np.sin(2*np.pi*freq_portadora*vetor_tempo)

##################################DEMODULAÇÃO#################################
#Definindo audio demodulado
audio_demodulado = senoide_portadora * audio_modulado
print('Audio Demodulado...')
sd.play(audio_demodulado, freq_leitura)
sd.wait()
print('Fim do Audio Demodulado')


#Plotando o grafico do sinal demodulado pelo tempo
plt.figure("Sinal recebido no tempo")
plt.plot(vetor_tempo[::500], audio_demodulado[::500])
plt.title("Sinal demodulado no tempo")
plt.show()
#Plot do fourier
signal.plotFFT(audio_demodulado, freq_leitura, 'demodulado')
plt.title("Sinal demodulado na frequencia")

########################################FILTRO##################################
#Filtrando o sinal
filtrado = filtro(audio_demodulado, freq_leitura, 4000)

# # #Plotando o grafico do sinal filtrado pelo tempo
# plt.plot(vetor_tempo[::500], filtrado[::500])
# plt.title("Sinal recebido filtrado")
# plt.show()
#Plot do fourier
signal.plotFFT(filtrado, freq_leitura, 'filtrado')
plt.title("Sinal demodulado e filtrado na frequencia")
plt.show()

# #Tocando o som filtrado
sd.play(filtrado, freq_leitura)
sd.wait()
#salvando audio filtrado
sf.write('somFiltradoDemodulado.wav', filtrado, freq_leitura)
