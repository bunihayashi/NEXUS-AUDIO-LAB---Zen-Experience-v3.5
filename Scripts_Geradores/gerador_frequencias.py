import os
import numpy as np
from scipy.io.wavfile import write

# --- CONFIGURAÇÃO DO SISTEMA NEXUS ---
CAMINHO_DESTINO = r"C:\Users\gabri\Desktop\Scripts\Sons Puros"
DURACAO_SEGUNDOS = 300  # 5 Minutos por arquivo (ajuste conforme necessário)
SAMPLE_RATE = 96000     # Qualidade de Estúdio (High-Res Audio)
VOLUME = 0.5            # 50% de amplitude (Senoidais puras são MUITO altas, não use 1.0)

# --- BIBLIOTECA DE FREQUÊNCIAS (DATABASE) ---
# Formato: Frequência (Hz) : "Nome do Arquivo - Propósito"
frequencias_alvo = {
    # --- Ressonância Schumann (Terra) ---
    7.83: "01_Schumann_Ressonancia_Terra_Grounding",
    
    # --- Escala Solfeggio (Completa) ---
    174.0: "02_Solfeggio_174Hz_Alivio_Dor_Tensao",
    285.0: "03_Solfeggio_285Hz_Regeneracao_Tecidos",
    396.0: "04_Solfeggio_396Hz_Liberacao_Medo_Culpa",
    417.0: "05_Solfeggio_417Hz_Transmutacao_Situacoes",
    528.0: "06_Solfeggio_528Hz_Reparacao_DNA_Milagre",
    639.0: "07_Solfeggio_639Hz_Conexoes_Relacionamentos",
    741.0: "08_Solfeggio_741Hz_Despertar_Intuicao",
    852.0: "09_Solfeggio_852Hz_Ordem_Espiritual",
    963.0: "10_Solfeggio_963Hz_Conexao_Divina",
    
    # --- Frequências Clássicas / Rife ---
    432.0: "11_Verdi_A_432Hz_Matematica_Universal_Calma",
    40.0:  "12_Gamma_40Hz_Foco_Cognitivo_Memoria"
}

def garantir_diretorio(caminho):
    if not os.path.exists(caminho):
        print(f"[NEXUS] Criando diretório: {caminho}")
        os.makedirs(caminho)
    else:
        print(f"[NEXUS] Diretório encontrado: {caminho}")

def aplicar_fade(audio, sample_rate, duracao_fade=2.0):
    """Aplica fade-in e fade-out para evitar 'pop' nos fones."""
    amostras_fade = int(duracao_fade * sample_rate)
    
    # Fade In
    fade_in = np.linspace(0.0, 1.0, amostras_fade)
    audio[:amostras_fade] *= fade_in
    
    # Fade Out
    fade_out = np.linspace(1.0, 0.0, amostras_fade)
    audio[-amostras_fade:] *= fade_out
    
    return audio

def gerar_biblioteca():
    garantir_diretorio(CAMINHO_DESTINO)
    
    print(f"[NEXUS] Iniciando geração de {len(frequencias_alvo)} arquivos de alta fidelidade...")
    
    # Eixo do tempo (comum a todas)
    t = np.linspace(0, DURACAO_SEGUNDOS, int(SAMPLE_RATE * DURACAO_SEGUNDOS), endpoint=False)
    
    for freq, nome in frequencias_alvo.items():
        nome_arquivo = f"{nome}.wav"
        caminho_completo = os.path.join(CAMINHO_DESTINO, nome_arquivo)
        
        print(f"  > Gerando: {freq}Hz -> {nome_arquivo} ...")
        
        # Geração da Onda
        onda = VOLUME * np.sin(2 * np.pi * freq * t)
        
        # Aplica Fade In/Out
        onda = aplicar_fade(onda, SAMPLE_RATE)
        
        # Conversão para 32-bit Integer (Compatibilidade Maxima com Amplitude)
        # Multiplicamos pelo range máximo de um inteiro de 32 bits
        onda_int = np.int32(onda * 2147483647)
        
        write(caminho_completo, SAMPLE_RATE, onda_int)
    
    print("\n[NEXUS] Processo concluído com sucesso.")
    print(f"[NEXUS] Arquivos disponíveis em: {CAMINHO_DESTINO}")

if __name__ == "__main__":
    gerar_biblioteca()