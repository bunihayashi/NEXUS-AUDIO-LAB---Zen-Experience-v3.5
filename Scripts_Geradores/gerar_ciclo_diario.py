import os
import numpy as np
from scipy.io.wavfile import write

# --- CONFIGURAÇÃO DE DIRETÓRIOS ---
ROOT_DIR = r"C:\Users\gabri\Desktop\Scripts\Sons Puros"
DIRS = {
    "Puras": os.path.join(ROOT_DIR, "Frequências Puras"),
    "Binaural": os.path.join(ROOT_DIR, "Binaural_Arsenal"),
    "Cores": os.path.join(ROOT_DIR, "Cores"),
    "Ciclo": os.path.join(ROOT_DIR, "Ciclo_Diario_Noturno")
}

SAMPLE_RATE = 96000
DURACAO_BASE = 300  
DURACAO_CICLO = 900 

SOLFEGGIO = {
    "FREQ_174Hz": 174, "FREQ_285Hz": 285, "FREQ_396Hz": 396,
    "FREQ_417Hz": 417, "FREQ_528Hz": 528, "FREQ_639Hz": 639,
    "FREQ_741Hz": 741, "FREQ_852Hz": 852, "FREQ_963Hz": 963
}

ARSENAL = {
    "BIN_DELTA_2Hz": 2.0, "BIN_THETA_6Hz": 6.0, "BIN_ALFA_10Hz": 10.0,
    "BIN_BETA_20Hz": 20.0, "BIN_GAMA_40Hz": 40.0
}

# --- FUNÇÕES DE PROTEÇÃO E GERAÇÃO ---
def aplicar_fade(audio, segundos=5):
    fade_len = int(segundos * SAMPLE_RATE)
    if len(audio) < fade_len * 2: return audio
    fade = np.linspace(0.0, 1.0, fade_len)
    if audio.ndim == 2: fade = fade.reshape(-1, 1)
    audio[:fade_len] *= fade
    audio[-fade_len:] *= fade[::-1]
    return audio

def salvar_blindado(audio, pasta, nome):
    if not os.path.exists(pasta): os.makedirs(pasta)
    caminho = os.path.join(pasta, nome + ".wav")
    
    # Proteção contra valores inválidos (NaN ou Inf)
    audio = np.nan_to_num(audio)
    
    # Limiter de segurança (Peak Clipping Protection)
    pico = np.max(np.abs(audio))
    if pico > 0.99:
        audio = audio / pico * 0.99
        
    data_int = np.int32(audio * 2147483647)
    write(caminho, SAMPLE_RATE, data_int)

# --- EXECUÇÃO MASTER ---
print("--- INICIANDO GÊNESE TOTAL NEXUS v2.1 (BLINDADA) ---")

# 1. GERAR PURAS
print("-> Gerando Solfeggio...")
t_base = np.linspace(0, DURACAO_BASE, int(SAMPLE_RATE * DURACAO_BASE), False)
for nome, hz in SOLFEGGIO.items():
    onda = 0.4 * np.sin(2 * np.pi * hz * t_base)
    salvar_blindado(aplicar_fade(onda), DIRS["Puras"], nome)

# 2. GERAR CORES
print("-> Gerando Ruídos Coloridos...")
amostras = int(SAMPLE_RATE * DURACAO_BASE)
# Branco
salvar_blindado(aplicar_fade(np.random.normal(0, 0.2, amostras)), DIRS["Cores"], "COR_Branco")
# Marrom (Com correção de deriva harmônica)
marrom = np.cumsum(np.random.normal(0, 0.1, amostras))
marrom = marrom - np.mean(marrom) # Centraliza a onda
salvar_blindado(aplicar_fade(marrom / np.max(np.abs(marrom)) * 0.3), DIRS["Cores"], "COR_Marrom")
# Rosa (Aproximação balanceada)
rosa = np.random.normal(0, 0.2, amostras)
salvar_blindado(aplicar_fade(rosa), DIRS["Cores"], "COR_Rosa")

# 3. GERAR BINAURAIS
print("-> Gerando Arsenal Binaural...")
portadora = 200
for nome, beat in ARSENAL.items():
    t = np.linspace(0, DURACAO_BASE, int(SAMPLE_RATE * DURACAO_BASE), False)
    l = 0.4 * np.sin(2 * np.pi * (portadora - beat/2) * t)
    r = 0.4 * np.sin(2 * np.pi * (portadora + beat/2) * t)
    salvar_blindado(aplicar_fade(np.column_stack((l, r))), DIRS["Binaural"], nome)

# 4. MIXAGEM DO CICLO NOTURNO
print("-> Mixando Ciclo Diário Noturno (Fases de 15 min)...")

def get_comp_mix(tipo, nome, vol):
    t = np.linspace(0, DURACAO_CICLO, int(SAMPLE_RATE * DURACAO_CICLO), False)
    if tipo == "pura":
        hz = SOLFEGGIO[nome]
        s = 0.4 * np.sin(2 * np.pi * hz * t)
        return np.column_stack((s, s)) * vol
    if tipo == "ruido":
        if "Marrom" in nome:
            r = np.cumsum(np.random.normal(0, 0.1, len(t)))
            r = (r - np.mean(r))
            r = (r / np.max(np.abs(r)) * 0.3)
        else: r = np.random.normal(0, 0.2, len(t))
        return np.column_stack((r, r)) * vol
    if tipo == "bin":
        beat = ARSENAL[nome]
        l = 0.4 * np.sin(2 * np.pi * (200 - beat/2) * t)
        r = 0.4 * np.sin(2 * np.pi * (200 + beat/2) * t)
        return np.column_stack((l, r)) * vol

# Fase 1: Purificação
salvar_blindado(aplicar_fade(get_comp_mix("pura", "FREQ_417Hz", 0.4) + get_comp_mix("ruido", "COR_Marrom", 0.6)), DIRS["Ciclo"], "01_FASE_PURIFICACAO_417Hz")

# Fase 2: Conexão
salvar_blindado(aplicar_fade(get_comp_mix("pura", "FREQ_741Hz", 0.5) + get_comp_mix("pura", "FREQ_852Hz", 0.5)), DIRS["Ciclo"], "02_FASE_CONEXAO_INTUICAO")

# Fase 3: Milagre
salvar_blindado(aplicar_fade(get_comp_mix("pura", "FREQ_528Hz", 0.3) + get_comp_mix("bin", "BIN_THETA_6Hz", 0.7)), DIRS["Ciclo"], "03_FASE_MILAGRE_REPARO")

# Fase 4: Sono
salvar_blindado(aplicar_fade(get_comp_mix("bin", "BIN_DELTA_2Hz", 0.4) + get_comp_mix("ruido", "COR_Marrom", 0.6)), DIRS["Ciclo"], "04_FASE_ENTREGA_SONO")

print("\n[NEXUS OPERATIONAL] Todas as bases e ciclos foram gerados com sucesso.")