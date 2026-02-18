import os
import numpy as np
from scipy.io.wavfile import write

# --- CONFIGURAÇÃO NEXUS ---
ROOT_DIR = r"C:\Users\gabri\Desktop\Scripts\Sons Puros"
FOLDER_NAME = "Binaural_Arsenal"
OUTPUT_PATH = os.path.join(ROOT_DIR, FOLDER_NAME)

SAMPLE_RATE = 96000
DURACAO = 600  # 10 minutos cada para dar tempo de sincronizar o cérebro
PORTADORA_BASE = 200 # Hz (Tom macio e confortável para os fones KZ)

# --- DEFINIÇÃO DO ARSENAL (Frequências Alvo) ---
ARSENAL = {
    "01_DELTA_2Hz_Sono_Profundo": 2.0,
    "02_DELTA_3.5Hz_REPARO_FISICO": 3.5,
    "03_THETA_6Hz_Criatividade_Insight": 6.0,
    "04_ALFA_8Hz_Relaxamento_Leve": 8.0,
    "05_ALFA_10Hz_Foco_Aprendizado": 10.0,
    "06_ALFA_12Hz_Presença_Alerta": 12.0,
    "07_BETA_15Hz_Raciocinio_Logico": 15.0,
    "08_BETA_20Hz_Foco_Ativo": 20.0,
    "09_GAMA_40Hz_Alta_Performance": 40.0
}

def gerar_binaural_full(nome, beat_alvo):
    print(f"-> Sintetizando: {nome} ({beat_alvo}Hz)...")
    
    t = np.linspace(0, DURACAO, int(SAMPLE_RATE * DURACAO), endpoint=False)
    
    # Cálculo das frequências para cada ouvido
    f_l = PORTADORA_BASE - (beat_alvo / 2)
    f_r = PORTADORA_BASE + (beat_alvo / 2)
    
    onda_l = 0.5 * np.sin(2 * np.pi * f_l * t)
    onda_r = 0.5 * np.sin(2 * np.pi * f_r * t)
    
    # Aplicação de Fade in/out de 5 segundos para evitar estalos
    fade_len = int(5.0 * SAMPLE_RATE)
    fade = np.linspace(0.0, 1.0, fade_len)
    
    onda_l[:fade_len] *= fade
    onda_l[-fade_len:] *= fade[::-1]
    onda_r[:fade_len] *= fade
    onda_r[-fade_len:] *= fade[::-1]
    
    # Stack Stereo
    stereo = np.column_stack((onda_l, onda_r))
    
    # Conversão para 32-bit PCM para máxima pureza
    dados_int = np.int32(stereo * 2147483647)
    
    arquivo_final = os.path.join(OUTPUT_PATH, f"{nome}.wav")
    write(arquivo_final, SAMPLE_RATE, dados_int)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        print(f"[NEXUS] Pasta {FOLDER_NAME} criada.")

    print("\n--- INICIANDO GERAÇÃO DO ARSENAL CEREBRAL ---")
    for nome, hz in ARSENAL.items():
        gerar_binaural_full(nome, hz)
    
    print("\n[SUCESSO] Arsenal completo gerado em 96kHz.")
    print(f"Local: {OUTPUT_PATH}")