import os
import numpy as np
from scipy.io.wavfile import write

# --- CONFIGURAÇÃO DO NEXUS ---
CAMINHO_DESTINO = os.getcwd() 
DURACAO_SEGUNDOS = 600  # 10 Minutos
SAMPLE_RATE = 96000     # 44.1kHz é suficiente para binaural, mas pode usar 96000
VOLUME = 0.5

# Frequência Base (Portadora)
# É o tom que você vai ouvir "carregando" o binaural.
# 200Hz a 400Hz são tons agradáveis para o ouvido.
FREQ_PORTADORA = 200.0 

# --- PROTOCOLOS BINAURAIS ---
# A chave é o nome, o valor é a diferença em Hz (o Beat)
protocolos = {
    "01_Delta_2.5Hz_Sono_Profundo_Cura": 2.5,
    "02_Theta_5.5Hz_Intuicao_Criatividade": 5.5,
    "03_Alpha_10Hz_Super_Learning_Foco": 10.0,
    "04_Beta_20Hz_Foco_Ativo_Trabalho": 20.0,
    "05_Gamma_40Hz_Alta_Performance_Cognitiva": 40.0
}

def aplicar_fade(audio, sample_rate, duracao_fade=2.0):
    amostras_fade = int(duracao_fade * sample_rate)
    fade_in = np.linspace(0.0, 1.0, amostras_fade).reshape(-1, 1)
    fade_out = np.linspace(1.0, 0.0, amostras_fade).reshape(-1, 1)
    
    # Aplica fade nos dois canais
    audio[:amostras_fade] *= fade_in
    audio[-amostras_fade:] *= fade_out
    return audio

def gerar_binaurais():
    print(f"[NEXUS] Iniciando geração de Protocolos Binaurais (Stereo)...")
    
    t = np.linspace(0, DURACAO_SEGUNDOS, int(SAMPLE_RATE * DURACAO_SEGUNDOS), endpoint=False)
    
    for nome, beat_freq in protocolos.items():
        nome_arquivo = f"BINAURAL_{nome}.wav"
        print(f"  > Gerando: {beat_freq}Hz (Beat) na portadora {FREQ_PORTADORA}Hz -> {nome_arquivo}")
        
        # Canal Esquerdo (L): Frequência Base
        freq_L = FREQ_PORTADORA
        
        # Canal Direito (R): Frequência Base + Beat Desejado
        freq_R = FREQ_PORTADORA + beat_freq
        
        # Gerar ondas
        onda_L = VOLUME * np.sin(2 * np.pi * freq_L * t)
        onda_R = VOLUME * np.sin(2 * np.pi * freq_R * t)
        
        # Combinar em Stereo (Numpy Array com 2 colunas)
        audio_stereo = np.column_stack((onda_L, onda_R))
        
        # Aplicar Fade
        audio_stereo = aplicar_fade(audio_stereo, SAMPLE_RATE)
        
        # Converter para 16-bit PCM (Padrão WAV Stereo)
        audio_int = np.int16(audio_stereo * 32767)
        
        write(nome_arquivo, SAMPLE_RATE, audio_int)
        
    print("\n[NEXUS] Geração Binaural Concluída.")

if __name__ == "__main__":
    gerar_binaurais()