import os
import numpy as np
from scipy.io.wavfile import write

# --- CONFIGURAÇÃO NEXUS ---
CAMINHO_DESTINO = os.getcwd()
DURACAO_SEGUNDOS = 300  # 5 Minutos
SAMPLE_RATE = 96000     # 44.1kHz é padrão para ruído
VOLUME = 0.8            # Ruídos precisam de mais volume que senoides puras para serem percebidos igual

def gerar_ruido_colorido(cor, amostras):
    """
    Gera ruído colorido usando filtragem no domínio da frequência (FFT).
    Algoritmo: 1/f^alpha
    """
    # 1. Gerar Ruído Branco (Gaussiano Puro)
    ruido_branco = np.random.standard_normal(amostras)
    
    # 2. Transformar para o Domínio da Frequência (FFT)
    espectro = np.fft.rfft(ruido_branco)
    
    # 3. Criar o filtro espectral
    # White: alpha = 0 | Pink: alpha = 1 | Brown: alpha = 2 | Blue: alpha = -1
    if cor == "branco":
        alpha = 0.0
    elif cor == "rosa":
        alpha = 1.0
    elif cor == "marrom":
        alpha = 2.0
    elif cor == "azul":
        alpha = -1.0
    elif cor == "violeta":
        alpha = -2.0
    else:
        alpha = 0.0

    # Evitar divisão por zero na frequência 0 (DC component)
    frequencias = np.fft.rfftfreq(amostras)
    frequencias[0] = 1  # Truque matemático seguro, pois a amplitude DC será zerada ou mantida
    
    # O filtro é 1 / f^(alpha/2)
    filtro = 1 / (frequencias ** (alpha / 2.0))
    
    # Manter a fase original, alterar apenas a magnitude
    espectro_filtrado = espectro * filtro
    
    # 4. Voltar para o Domínio do Tempo (Inverse FFT)
    ruido_colorido = np.fft.irfft(espectro_filtrado)
    
    # 5. Normalizar o volume (essencial, pois o filtro altera drasticamente a amplitude)
    max_amp = np.max(np.abs(ruido_colorido))
    if max_amp > 0:
        ruido_colorido /= max_amp
        
    return ruido_colorido

def aplicar_fade(audio, sample_rate, duracao_fade=2.0):
    amostras_fade = int(duracao_fade * sample_rate)
    fade_in = np.linspace(0.0, 1.0, amostras_fade)
    fade_out = np.linspace(1.0, 0.0, amostras_fade)
    audio[:amostras_fade] *= fade_in
    audio[-amostras_fade:] *= fade_out
    return audio

def main():
    print(f"[NEXUS] Iniciando geração de Cores Sonoras (Espectro Matemático)...")
    
    cores_alvo = ["branco", "rosa", "marrom", "azul"]
    total_amostras = int(SAMPLE_RATE * DURACAO_SEGUNDOS)
    
    for cor in cores_alvo:
        nome_arquivo = f"RUIDO_COR_{cor.upper()}.wav"
        print(f"  > Sintetizando Espectro: {cor.upper()} -> {nome_arquivo}")
        
        # Gerar
        onda = gerar_ruido_colorido(cor, total_amostras)
        
        # Volume e Fade
        onda = onda * VOLUME
        onda = aplicar_fade(onda, SAMPLE_RATE)
        
        # Converter para 16-bit PCM
        onda_int = np.int16(onda * 32767)
        
        write(nome_arquivo, SAMPLE_RATE, onda_int)
        
    print("\n[NEXUS] Cores geradas com sucesso.")

if __name__ == "__main__":
    main()