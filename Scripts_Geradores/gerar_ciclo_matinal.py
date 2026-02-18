import os
import numpy as np
from scipy.io.wavfile import write

# --- CONFIGURAÇÃO NEXUS ---
ROOT_DIR = r"C:\Users\gabri\Desktop\Scripts\Sons Puros"
DIRS = {
    "Matinal": os.path.join(ROOT_DIR, "Ciclo_Diario_Matinal")
}

SAMPLE_RATE = 96000
DURACAO_FASE = 600 # 10 minutos por fase

def aplicar_fade(audio, seg=5):
    fade_len = int(seg * SAMPLE_RATE)
    fade = np.linspace(0.0, 1.0, fade_len)
    if audio.ndim == 2: fade = fade.reshape(-1, 1)
    audio[:fade_len] *= fade
    audio[-fade_len:] *= fade[::-1]
    return audio

def gerar_onda(hz, dur):
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    s = 0.4 * np.sin(2 * np.pi * hz * t)
    return np.column_stack((s, s))

def gerar_binaural(beat, dur):
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    portadora = 200
    l = 0.4 * np.sin(2 * np.pi * (portadora - beat/2) * t)
    r = 0.4 * np.sin(2 * np.pi * (portadora + beat/2) * t)
    return np.column_stack((l, r))

# --- GERAÇÃO DO PROTOCOLO ---
print("--- INICIANDO PROTOCOLO MATINAL NEXUS ---")
if not os.path.exists(DIRS["Matinal"]): os.makedirs(DIRS["Matinal"])

# FASE 1: DESPERTAR CELULAR (528Hz + Alfa 10Hz)
# Objetivo: Transição suave do sono para o estado de alerta relaxado.
print("-> Gerando Fase 1: Despertar Celular...")
f1 = aplicar_fade(gerar_onda(528, DURACAO_FASE) * 0.4 + gerar_binaural(10, DURACAO_FASE) * 0.6)
write(os.path.join(DIRS["Matinal"], "01_FASE_IGNICAO_528Hz_ALFA.wav"), SAMPLE_RATE, np.int32(f1 * 2147483647))

# FASE 2: FOCO E CLAREZA (741Hz + Beta 20Hz)
# Objetivo: Ativação do raciocínio e limpeza mental para o dia.
print("-> Gerando Fase 2: Foco e Clareza...")
f2 = aplicar_fade(gerar_onda(741, DURACAO_FASE) * 0.3 + gerar_binaural(20, DURACAO_FASE) * 0.7)
write(os.path.join(DIRS["Matinal"], "02_FASE_FOCO_BETA.wav"), SAMPLE_RATE, np.int32(f2 * 2147483647))

# FASE 3: SUPER COGNIÇÃO (GAMA 40Hz + 963Hz)
# Objetivo: Pico de performance, insights e conexão divina para agir.
print("-> Gerando Fase 3: Super Cognição...")
f3 = aplicar_fade(gerar_onda(963, DURACAO_FASE) * 0.3 + gerar_binaural(40, DURACAO_FASE) * 0.7)
write(os.path.join(DIRS["Matinal"], "03_FASE_PICO_GAMA.wav"), SAMPLE_RATE, np.int32(f3 * 2147483647))

print(f"\n[SUCESSO] Ciclo Matinal pronto em: {DIRS['Matinal']}")