import soundfile as sf
from init import *
from scipy import signal as sg

####################            funções           ####################
def filtro(y, samplerate, cutoff_hz):
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = sg.kaiserord(ripple_db, width)
    taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = sg.lfilter(taps, 1.0, y)
    return yFiltrado


#######################################################################
signal_plot = mySignal()

#leitura do arquivo de audio - 1
signal_original = sf.read('audio.wav')[0]
taxa_amostragem = 44100
signal = signal_original[:,0]
duracao = np.linspace(0, 3, len(signal))
filtro = 4000

#filtragem - 2 
signal_filtrado = filtro(signal, taxa_amostragem, filtro)
duracao_filtrada = np.linspace(0, 3, len(signal_filtrado))

#Reproduza o sinal e verifique que continua audível - 3
sd.play(signal_filtrado, taxa_amostragem)
sd.wait()
sf.write('audio.wav', signal_filtrado, taxa_amostragem)

#Module esse sinal de áudio em AM com portadora de 14.000 Hz - 4
portadora = 14000
sinal_modulado = signal_filtrado*np.sin(2*np.pi*portadora*duracao_filtrada)

# Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), de modo que todos os pontos
# do sinal permaneçam dentro do intervalo[-1,1] - 5
sinal_modulado = sinal_modulado/abs(max(sinal_modulado))

#Reproduza o sinal modulado e verifique que continua audível - 6
sd.play(sinal_modulado, taxa_amostragem)
sd.wait()
sf.write('audio.wav', sinal_modulado, taxa_amostragem)

