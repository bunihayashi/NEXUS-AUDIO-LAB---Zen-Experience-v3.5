import os
import numpy as np
from scipy.io.wavfile import read, write

# --- CONFIGURAÇÃO DE DIRETÓRIOS ---
BASE_DIR = r"C:\Users\gabri\Desktop\Scripts\Sons Puros"
DIR_CORES = os.path.join(BASE_DIR, "Cores")
DIR_BINEURAL = os.path.join(BASE_DIR, "Bineural")
DIR_PURAS = os.path.join(BASE_DIR, "Frequências Puras")
DIR_OUTPUT = os.path.join(BASE_DIR, "Mixagens_Nexus")

# --- RECEITAS DE MIXAGEM (PROTOCOLOS) ---
# Adicione ou remova combinações aqui. 
# O script vai procurar arquivos que CONTENHAM essas palavras no nome.
# --- PROTOCOLOS NEXUS (ARSENAL COMPLETO) ---
RECEITAS = [
    # --- CATEGORIA 1: FOCO E ALTA PERFORMANCE (TRABALHO/CODING) ---
    {
        "nome_saida": "01_NEXUS_DEEP_WORK_CODING.wav",
        "cor": "ROSA",            # O melhor para foco sustentado
        "binaural": "Beta",       # Foco ativo (14-30Hz)
        "pura": "40Hz",           # Gamma puro (Processamento cognitivo rápido)
        "vols": [0.5, 0.3, 0.1]   # Ruído domina, binaural guia, pura brilha
    },
    {
        "nome_saida": "02_NEXUS_HYPER_FOCUS_GAMMA.wav",
        "cor": "BRANCO",          # Isolamento total (abafa tudo)
        "binaural": "Gamma",      # Pico de performance (30Hz+)
        "pura": "741Hz",          # Clareza mental / Solução de problemas
        "vols": [0.4, 0.35, 0.05] 
    },

    # --- CATEGORIA 2: SONO E REGENERAÇÃO (NOITE) ---
    {
        "nome_saida": "03_NEXUS_SONO_PROFUNDO_REPAIR.wav",
        "cor": "MARROM",          # Conforto (som de útero/trovão)
        "binaural": "Delta",      # Sono sem sonhos (0.5-4Hz)
        "pura": "528Hz",          # Reparação celular (DNA)
        "vols": [0.6, 0.4, 0.1]   # Mais alto para abafar ruídos da rua
    },
    {
        "nome_saida": "04_NEXUS_ALIVIO_DOR_FISICA.wav",
        "cor": "MARROM",
        "binaural": "Delta",
        "pura": "174Hz",          # Frequência específica para dor e tensão
        "vols": [0.5, 0.4, 0.2]   # Pura um pouco mais presente aqui
    },

    # --- CATEGORIA 3: ANSIEDADE E MEDITAÇÃO (PAUSA) ---
    {
        "nome_saida": "05_NEXUS_ESCUDO_ANSIEDADE.wav",
        "cor": "ROSA",            # Suave e natural
        "binaural": "Alpha",      # Relaxamento alerta (8-14Hz)
        "pura": "396Hz",          # Libertação de Medo e Culpa
        "vols": [0.5, 0.3, 0.15]
    },
    {
        "nome_saida": "06_NEXUS_ATERRAMENTO_SCHUMANN.wav",
        "cor": "MARROM",
        "binaural": "Theta",      # Estado de transe leve
        "pura": "Schumann",       # Ressonância da Terra (Grounding),      
        "vols": [0.4, 0.3, 0.4]   # Schumann precisa de volume para vibrar o driver
    },
    {
        "nome_saida": "07_NEXUS_EXPANSAO_CRIATIVA.wav",
        "cor": "ROSA",
        "binaural": "Theta",      # Acesso ao subconsciente
        "pura": "741Hz",          # Despertar da intuição
        "vols": [0.4, 0.3, 0.1]
    },
    
    # --- CATEGORIA 4: HARMONIA UNIVERSAL ---
    {
        "nome_saida": "08_NEXUS_MATEMATICA_DIVINA_432.wav",
        "cor": "ROSA",
        "binaural": "Alpha",
        "pura": "432Hz",          # A frequência de Verdi
        "vols": [0.3, 0.3, 0.2]   # Equilíbrio total
    }
]

def encontrar_arquivo(diretorio, termo_busca):
    """Encontra o primeiro arquivo no diretório que contém o termo."""
    if not os.path.exists(diretorio):
        print(f"[ERRO] Diretório não encontrado: {diretorio}")
        return None
        
    for arquivo in os.listdir(diretorio):
        if termo_busca.lower() in arquivo.lower() and arquivo.endswith(".wav"):
            return os.path.join(diretorio, arquivo)
    
    print(f"[AVISO] Nenhum arquivo com '{termo_busca}' encontrado em {os.path.basename(diretorio)}")
    return None

def carregar_audio(caminho):
    """Carrega áudio e normaliza para float -1.0 a 1.0"""
    taxa, dados = read(caminho)
    
    # Se for stereo (2 canais), mantém. Se for mono, converte pra stereo duplicando.
    if len(dados.shape) == 1:
        dados = np.column_stack((dados, dados))
    
    # Normalização para float para evitar clipping na soma
    if dados.dtype == np.int16:
        dados = dados.astype(np.float32) / 32768.0
    elif dados.dtype == np.int32:
        dados = dados.astype(np.float32) / 2147483648.0
        
    return taxa, dados

def mixar_protocolos():
    if not os.path.exists(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)

    print(f"[NEXUS] Iniciando mixagem de {len(RECEITAS)} protocolos...\n")

    for receita in RECEITAS:
        print(f"--- Processando: {receita['nome_saida']} ---")
        
        # 1. Encontrar Arquivos
        arq_cor = encontrar_arquivo(DIR_CORES, receita["cor"])
        arq_bin = encontrar_arquivo(DIR_BINEURAL, receita["binaural"])
        arq_pur = encontrar_arquivo(DIR_PURAS, receita["pura"])
        
        if not (arq_cor and arq_bin and arq_pur):
            print("[PULANDO] Faltam arquivos para esta receita.\n")
            continue

        # 2. Carregar Dados
        rate_c, data_c = carregar_audio(arq_cor)
        rate_b, data_b = carregar_audio(arq_bin)
        rate_p, data_p = carregar_audio(arq_pur)

        # Verificar Compatibilidade de Sample Rate
        if not (rate_c == rate_b == rate_p):
            print(f"[ERRO] Taxas de amostragem diferentes detectadas ({rate_c}, {rate_b}, {rate_p}). O script exige 96kHz em todos.")
            continue
            
        # 3. Alinhar Tamanhos (Corta pelo menor para não dar erro)
        min_len = min(len(data_c), len(data_b), len(data_p))
        data_c = data_c[:min_len]
        data_b = data_b[:min_len]
        data_p = data_p[:min_len]

        # 4. Mixagem Ponderada (Matemática Vetorial)
        vol_c, vol_b, vol_p = receita["vols"]
        
        mix_final = (data_c * vol_c) + (data_b * vol_b) + (data_p * vol_p)

        # 5. Proteção de Clipping (Limiter)
        pico_max = np.max(np.abs(mix_final))
        if pico_max > 1.0:
            print(f"  > Normalizando pico de {pico_max:.2f} para 1.0 (evitando distorção)")
            mix_final /= pico_max
            
        # 6. Salvar (Convertendo para PCM 32-bit Integer para máxima qualidade)
        caminho_final = os.path.join(DIR_OUTPUT, receita['nome_saida'])
        dados_finais_int = np.int32(mix_final * 2147483647)
        
        write(caminho_final, rate_c, dados_finais_int)
        print(f"  > [SUCESSO] Arquivo salvo em: Mixagens_Nexus\\{receita['nome_saida']}\n")

if __name__ == "__main__":
    mixar_protocolos()