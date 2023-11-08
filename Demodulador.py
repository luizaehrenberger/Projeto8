import wave

# Abre o arquivo de áudio modulado
audio_modulado = wave.open("audio_modulado.wav", "rb")

# Obtém os parâmetros do arquivo de áudio
nchannels = audio_modulado.getnchannels()
sample_width = audio_modulado.getsampwidth()
framerate = audio_modulado.getframerate()
nframes = audio_modulado.getnframes()

# Lê os dados do arquivo de áudio e armazena em uma lista
audio_data = []
for i in range(nframes):
    frame = audio_modulado.readframes(1)
    data = int.from_bytes(frame, byteorder="little", signed=True)
    audio_data.append(data)

# Fecha o arquivo de áudio modulado
audio_modulado.close()

vetor_tempo = np.linspace(0, 3, len(sample_width))
