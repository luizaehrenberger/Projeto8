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

def filtro_meu(signal):
    #MatLab
    # w = 2500
    # s = tf('s')
    # G = (w^2/(s^2+2*w*s + w^2))
    # G_d = c2d(G,1/44100) --> 0.001547s+0.00149/z^2-1.89z+0.8928

    #Leganda nos slides
    a = 0.001547
    b = 0.00149
    d = -1.89
    e = 0.8928

    sinal_filtrado = [signal[0],signal[1]]
    for k in range(2, len(signal)):
        P = -d * sinal_filtrado[k - 1] - e*sinal_filtrado[k - 2] + a*signal[k - 1] + b*signal[k - 2]
        sinal_filtrado.append(P)

    return sinal_filtrado


#######################################################################
signal_plot = mySignal()

#leitura do arquivo de audio - 1
signal_original, samplerate = sf.read('Miranha.wav')
taxa_amostragem = 44100
signal = signal_original[:,0]
t = len(signal_original)/taxa_amostragem
duracao = np.linspace(0, 4, len(signal_original))

print("original")
sd.play(signal)
sd.wait()

#filtragem - 2 
# signal_filtrado = filtro(signal, taxa_amostragem, 4000)
signal_filtrado = filtro_meu(signal)
duracao_filtrada = np.linspace(0, 4, len(signal_filtrado))

#Reproduza o sinal e verifique que continua audível - 3
print("filtrado")
sd.play(signal_filtrado)
sd.wait()
sf.write('audio.wav', signal_filtrado, taxa_amostragem)

#Module esse sinal de áudio em AM com portadora de 14.000 Hz - 4
freq_portadora = 14000
portadora = np.sin(2*np.pi*freq_portadora*duracao_filtrada)
sinal_modulado = signal_filtrado*portadora

# Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), de modo que todos os pontos
# do sinal permaneçam dentro do intervalo[-1,1] - 5
sinal_normalizado = sinal_modulado/np.abs(np.max(sinal_modulado))

#Reproduza o sinal modulado e verifique que continua audível - 6
print("modulado e normalizado")
sd.play(sinal_normalizado, taxa_amostragem)
sd.wait()
sf.write('audio.wav', sinal_modulado, taxa_amostragem)


# signal_plot.plotFFT(sinal_modulado, taxa_amostragem)
# plt.title("Sinal de áudio modulado na frequencia")

#graficos
#Gráfico 1: Sinal de áudio original normalizado – domínio do tempo.
plt.figure(" Grafico 1 normalizado no tempo")
plt.plot(duracao, sinal_normalizado)
plt.title("Grafico 1 normalizado no tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.show()

#Gráfico 2: Sinal de áudio filtrado – domínio do tempo. (repare que não se nota diferença). 
plt.figure("Grafico 2 filtrado no tempo")
plt.plot(duracao_filtrada, signal_filtrado)
plt.title("Grafico 2 filtrado no tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.show()

#Gráfico 3: Sinal de áudio filtrado – domínio da frequência (Fourier). ERRADO
signal_plot.plotFFT(signal_filtrado, taxa_amostragem)
plt.title("Grafico 3 Sinal de áudio filtrado na frequencia")
# plt.figure("filtrado_fourier")
# plt.plot(taxa_amostragem, signal_filtrado)
# plt.title("Sinal de áudio filtrado")
# plt.xlabel("frequencia (Hz)")
# plt.ylabel("Amplitude")
# plt.show()

#Gráfico 4: Sinal de áudio modulado – domínio do tempo.
plt.figure("modulado")
plt.plot(duracao_filtrada, sinal_modulado)
plt.title("Grafico 4 Sinal de áudio modulado no tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.show()

#Gráfico 5: Sinal de áudio modulado – domínio da frequência (Fourier).
signal_plot.plotFFT(sinal_modulado, taxa_amostragem)
plt.title("Grafico 5 - Sinal de áudio modulado na frequencia")
plt.show()