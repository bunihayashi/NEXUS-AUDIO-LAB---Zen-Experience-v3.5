import os
import numpy as np
from scipy.io.wavfile import write, read

# --- CONFIGURAÇÃO NEXUS ---
ROOT_DIR = r"C:\Users\gabri\Desktop\Scripts\Sons Puros"
DIRS = {
    "Cores": os.path.join(ROOT_DIR, "Cores"),
    "Arsenal": os.path.join(ROOT_DIR, "Binaural_Arsenal"),
    "Puras": os.path.join(ROOT_DIR, "Frequências Puras"),
    "Mixes": os.path.join(ROOT_DIR, "Mixagens_Nexus")
}

SAMPLE_RATE = 96000

# --- RECEITAS DOS MIXES ---
# Formato: "Nome": (Arquivo_Cor, Vol_C, Arquivo_Bin, Vol_B, Arquivo_Pura, Vol_P)
RECEITAS_ALFA = {
    "NEXUS_MIX_ALFA_ZEN_FLOW": ("COR_Verde.wav", 0.5, "04_ALFA_8Hz_Relaxamento_Leve.wav", 0.4, "FREQ_432Hz.wav", 0.1),
    "NEXUS_MIX_ALFA_ESTUDO_DEEP": ("COR_Rosa.wav", 0.6, "05_ALFA_10Hz_Foco_Aprendizado.wav", 0.4, None, 0.0),
    "NEXUS_MIX_ALFA_INSIGHT_CREATIVO": ("COR_Marrom.wav", 0.4, "05_ALFA_10Hz_Foco_Aprendizado.wav", 0.4, "FREQ_741Hz.wav", 0.2),
    "NEXUS_MIX_ALFA_ALERTA_CALMO": ("COR_Branco.wav", 0.5, "06_ALFA_12Hz_Presença_Alerta.wav", 0.5, None, 0.0)
}

def carregar_audio(pasta, nome):
    if nome is None: return None
    caminho = os.path.join(pasta, nome)
    if not os.path.exists(caminho): return None
    rate, data = read(caminho)
    # Converter para float
    if data.dtype == np.int16: data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32: data = data.astype(np.float32) / 2147483648.0
    return data

def criar_mix(nome, c_info, b_info, p_info):
    print(f"-> Mixando: {nome}...")
    
    # Carregar áudios
    aud_c = carregar_audio(DIRS["Cores"], c_info[0])
    aud_b = carregar_audio(DIRS["Arsenal"], b_info[0])
    aud_p = carregar_audio(DIRS["Puras"], p_info[0])
    
    # Filtrar apenas o que carregou
    ativos = []
    if aud_c is not None: ativos.append(aud_c * c_info[1])
    if aud_b is not None: ativos.append(aud_b * b_info[1])
    if aud_p is not None: ativos.append(aud_p * p_info[1])
    
    # Alinhamento
    min_len = min(len(a) for a in ativos)
    mix = sum(a[:min_len] for a in ativos)
    
    # Limiter / Normalização
    pico = np.max(np.abs(mix))
    if pico > 1.0: mix /= pico
    
    # Salvar 32-bit
    dados_int = np.int32(mix * 2147483647)
    write(os.path.join(DIRS["Mixes"], f"{nome}.wav"), SAMPLE_RATE, dados_int)

if __name__ == "__main__":
    print("\n--- INICIANDO ALQUIMIA ALFA NEXUS ---")
    for nome, r in RECEITAS_ALFA.items():
        criar_mix(nome, (r[0], r[1]), (r[2], r[3]), (r[4], r[5]))
    print("\n[SUCESSO] Todos os mixes Alfa foram integrados ao Cofre.")