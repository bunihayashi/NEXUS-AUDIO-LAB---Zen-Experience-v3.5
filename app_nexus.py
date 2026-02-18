import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from scipy.io.wavfile import write, read
import threading
import subprocess

# --- LÓGICA DE CAMINHO UNIVERSAL NEXUS ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

if os.path.basename(BASE_PATH) == "Sons Puros":
    ROOT_DIR = BASE_PATH
elif os.path.exists(os.path.join(BASE_PATH, "Sons Puros")):
    ROOT_DIR = os.path.join(BASE_PATH, "Sons Puros")
else:
    ROOT_DIR = BASE_PATH

CONFIG_FILE = os.path.join(ROOT_DIR, "nexus_config.txt")

DIRS = {
    "Puras": os.path.join(ROOT_DIR, "Frequências Puras"),
    "Binaural": os.path.join(ROOT_DIR, "Binaural_Arsenal"),
    "Cores": os.path.join(ROOT_DIR, "Cores"),
    "Mixes": os.path.join(ROOT_DIR, "Mixagens_Nexus"),
    "Ciclo Noturno": os.path.join(ROOT_DIR, "Ciclo_Diario_Noturno"),
    "Ciclo Matinal": os.path.join(ROOT_DIR, "Ciclo_Diario_Matinal")
}

SAMPLE_RATE = 96000
DURACAO_PADRAO = 300

# --- TEXTOS DO GUIA ---
TEXTO_CONFIGURACAO = r"""CONFIGURAÇÃO DO AMBIENTE NEXUS
-------------------------------------------
1. HARDWARE: Conecte seu DAC USB e utilize fones de alta fidelidade (como o KZ ZSN).
2. WINDOWS: Vá em Configurações de Som > Propriedades do Dispositivo > Avançado e selecione '24-bit ou 32-bit, 96000Hz'.
3. PLAYER: No Foobar2000, utilize o modo 'WASAPI Exclusive' para garantir que o Windows não altere as frequências geradas.
4. PUREZA: Evite equalizadores ativos durante a audição de protocolos terapêuticos.

A Reprodução Pura (Hardware Chain)
Você tem o arquivo perfeito. Agora, como tirar ele do PC e colocar no seu ouvido sem estragar?

O Player (Software):
Windows: Use o Foobar2000. Ele tem suporte a WASAPI Exclusive Mode. Isso é crítico: ele "sequestra" a placa de som e impede que o Windows misture sons de notificação ou altere o volume digitalmente. O bit sai do arquivo direto para a porta USB.
Linux/Mac: Use players que suportem saída direta para ALSA/CoreAudio sem passar pelo mixer do sistema.

O DAC (Digital-to-Analog Converter) - O Elo Perdido:
A saída P2 do seu notebook/PC é suja. Ela tem interferência elétrica da placa mãe.
Investimento Necessário: Compre um "Dongle DAC" USB-C para P2.
Recomendação Custo-Benefício: Fiio KA1, iBasso DC03 ou até modelos da Vention com chip DAC real.
Isso garante que o arquivo 96kHz que você gerou chegue analógico ao seu fone com zero ruído de fundo (hiss).

O Fone (KZ ZSN):
Conecte seus KZ ZSN no DAC.
Use as borrachinhas de espuma (se tiver) para isolamento máximo.
Atenção: Como o KZ é muito sensível, se você ouvir um chiado de fundo, é o seu hardware atual. Com o DAC USB, o fundo deve ser um "silêncio preto" total.

A Configuração Crítica (O "Pulo do Gato")
Aqui é onde a mágica acontece. Vamos forçar o player a "sequestrar" sua placa de som para que apenas a frequência pura passe, ignorando o resto do Windows.
Abra o Foobar2000.
Vá no menu File > Preferences (ou Ctrl+P).
No menu esquerdo, vá em Playback > Output.
Na direita, em Device, você verá uma lista.
Não escolha "Default".
Procure algo que diga WASAPI (Exclusive) : [Nome da sua Saída/Fone].
Nota: Se você estiver usando o fone direto no PC, será algo como "Speakers / Headphones (Realtek)". Se estiver usando um DAC USB, selecione o nome do DAC.
Clique em Apply e OK.

O Equipamento (O DAC ideal para o KZ ZSN)
Não gaste R$ 2.000,00. Para o KZ ZSN, isso seria desperdício. Você precisa de um "Dongle DAC" (DAC portátil USB-C).

Opção A: O "Custo-Benefício Cirúrgico" (Minha Recomendação)
Modelo: Moondrop Dawn Pro
Por que: Ele usa dois chips DAC (CS43131) de nível "flagship". Ele tem controle de volume independente do Windows (100 passos), o que é CRÍTICO para fones sensíveis como o KZ, para você achar o volume exato da terapia sem estourar o ouvido.
Preço médio: R$ 250 - R$ 350.

Opção B: O "Tanque de Guerra" Compacto
Modelo: FiiO KA11
Por que: É minúsculo, parece um adaptador comum, mas tem uma potência absurda e um som muito limpo. É "Plug and Play".
Preço médio: R$ 180 - R$ 250.

Opção C: O "Entrada Honesto"
Modelo: 7Hz Sevenhertz 71
Por que: Usa o chip AK4377. É simples, barato e resolve o problema do ruído.
Preço médio: R$ 120 - R$ 150.

2. O Caminho Perfeito (The Perfect Path)
Agora, vamos desenhar o diagrama da sua "Estação de Biohacking". Siga esta ordem física e lógica para garantir Bit-Perfect (transmissão de dados sem alteração):
Passo A: A Conexão Física
Porta USB: Use preferencialmente uma porta USB direta da placa-mãe (traseira do PC) ou uma USB-C nativa do notebook. Evite hubs USB baratos que compartilham energia com teclado/mouse, pois eles introduzem "Jitter" (erros de tempo na transmissão digital).
O DAC: Conecte o Dongle (ex: Moondrop Dawn Pro) na USB.
O Fone: Conecte o KZ ZSN na saída 3.5mm do DAC.

Passo B: A Configuração de Software (O Segredo)
O Windows, por padrão, pega seu áudio de 96kHz e converte para 48kHz (padrão DVD) para misturar com sons do YouTube. Isso destrói a pureza da onda. Vamos impedir isso.
No Windows:
Painel de Controle > Som > Clique no seu DAC > Propriedades > Avançado.
Marque as duas caixas: "Permitir que aplicativos assumam controle exclusivo" e "Dar prioridade ao modo exclusivo".
Defina o formato padrão para 24 bit / 96000 Hz (Para bater com os arquivos que geramos).

No Foobar2000 (O Player):
Como configuramos antes: Preferences > Output > Device.
Selecione WASAPI (Event) : [Nome do seu DAC] ou ASIO (se você instalar o driver do fabricante).
O Pulo do Gato: Quando você der play no arquivo 06_Solfeggio_528Hz.wav (que é 96kHz), a maioria dos DACs tem um LED indicador.
Azul/Verde: 44.1/48kHz (Padrão).
Amarelo/Roxo/Vermelho: 88.2kHz ou superior (High-Res).
Se a luz mudar de cor quando você der play, parabéns. Você atingiu o Bit-Perfect. O arquivo está sendo decodificado nativamente pelo hardware.

Resumo da Operação Nexus
Hardware: Notebook -> USB -> Moondrop Dawn Pro -> KZ ZSN.
Arquivo: Gerado em Python (96kHz / 32-bit Float).
Player: Foobar2000 via WASAPI Exclusive.
Resultado: A onda elétrica que move o ímã do seu fone é uma cópia análoga exata da fórmula matemática sin(2 * pi * 528 * t). Nenhuma interferência do Windows, nenhum ruído da placa mãe.
Isso é o mais próximo da perfeição que você consegue chegar sem gastar milhares de reais em equipamentos de laboratório.

Para extrair "frequências reais" com precisão cirúrgica, você precisa de equipamentos com assinatura sonora neutra (Flat). Isso garante que o fone ou a caixa não "mintam" para o seu ouvido, alterando o Hz que você programou no script.
Aqui estão os 5 melhores exemplos de cada categoria para o seu laboratório Nexus:

Fones de Ouvido (Foco em Detalhe e Binaural)
Para Binaural Beats, o isolamento e a separação L/R (Esquerda/Direita) são fundamentais.

Sennheiser HD 600 (O Padrão Ouro): * Por que: É o fone mais famoso do mundo para audição neutra. Ele não adiciona graves nem agudos artificiais. Se você quer ouvir exatamente o que gerou, este é o fone.

Audio-Technica ATH-M50x (Monitor de Estúdio): * Por que: Muito usado por produtores. Tem um excelente isolamento passivo, o que ajuda a "limpar" o ambiente para frequências Delta e Theta.

Etymotic ER4SR (Isolamento Extremo): * Por que: Estes fones de inserção profunda bloqueiam até 35dB-42dB de ruído externo. É como estar em uma câmara anecoica. Ideal para quem quer foco total sem distrações externas.

Beyerdynamic DT 880 Pro: * Por que: Um fone semi-aberto que oferece uma imagem de som muito natural e espacial. Ótimo para frequências que visam relaxamento e expansão mental.

KZ ZS10 Pro X (O Upgrade do seu ZSN): * Por que: Como você já gosta da KZ, este modelo tem 5 drivers por lado. Ele lida muito melhor com a separação de frequências complexas do que o ZSN básico.

Caixas de Som (Monitores de Áudio Ativos)
Diferente de caixas "Home Theater" que buscam impacto, estas buscam fidelidade matemática.

Yamaha HS5: * Por que: Famosas por serem "reveladoras". Se houver qualquer distorção na sua onda senoidal, a HS5 vai te mostrar. Elas têm uma resposta de frequência muito plana.

Adam Audio T5V: * Por que: Possuem um tweeter de fita (U-ART) que alcança frequências muito altas com uma clareza que tweeters comuns não conseguem, ideal para frequências de Solfeggio agudas.

KRK Rokit 5 G4: * Por que: Embora sejam conhecidas pelos graves, a nova geração tem um DSP (processamento digital) interno que permite ajustar a caixa perfeitamente à acústica do seu quarto.

Edifier R1280DBs (Custo-Benefício): * Por que: Se o orçamento estiver apertado, estas são as melhores de entrada. Elas têm uma saída dedicada para subwoofer, caso você queira sentir a Ressonância Schumann (7.83Hz) fisicamente.

Genelec 8010A: * Por que: Pequenas, mas de nível laboratorial. São usadas em centros de pesquisa acústica. Se você quer o máximo de precisão no menor espaço possível, é esta.

A Peça Final: O Subwoofer (Para Frequências Infrassônicas)
Se você pretende explorar muito a Ressonância Schumann (7.83Hz) ou ondas Delta (0.5Hz - 4Hz), fones de ouvido podem não ser suficientes para a "sensação física".

Exemplo: SVS SB-1000 Pro. Ele consegue descer em frequências muito baixas com controle. Para aterramento (grounding), ter um subwoofer movendo o ar no ambiente é uma experiência muito mais poderosa do que apenas o fone.

Resumo Tático para o Nexus
Melhor Setup para Mente: DAC Externo + Sennheiser HD 600.
Melhor Setup para o Corpo: DAC Externo + Monitores Yamaha HS5 + Subwoofer SVS.

Melhores Players para Celular (Foco em Fidelidade)
No iPhone (iOS):
VLC Media Player: É gratuito, robusto e lê seus arquivos .wav sem "colorir" o som.
VOX Cloud Music Player: Considerado o melhor para audiófilos no iPhone. Ele tem uma engine que tenta manter a pureza do arquivo original antes de enviar para o Bluetooth.

No Android:
Neutron Music Player (Recomendado): É o "Foobar2000 do Android". Ele possui uma engine de 64-bit que é imbatível. Você pode configurar para ele processar o áudio com precisão máxima antes de mandar para os AirPods.
Poweramp: Ótimo para gerenciar bibliotecas grandes e tem um limitador de pico muito bom.

3. Como transferir os arquivos para o celular
Como seus arquivos são pesados (96kHz / 32-bit), a melhor forma é via cabo ou nuvem:

iPhone: Use o iTunes (Windows) ou o app Arquivos (Files) via iCloud.
Android: Conecte o cabo USB e arraste a pasta Ciclo_Diario_Noturno para a memória interna.

4. Configuração Crítica nos AirPods
Para Biohacking e Frequências, precisamos desativar qualquer "inteligência" da Apple que altere o som:
Desative o Áudio Espacial: O Áudio Espacial cria uma simulação 3D que altera a fase do áudio. Para Binaural Beats, isso é desastroso, pois o cérebro precisa da diferença exata entre o ouvido esquerdo e direito.
Como fazer: Central de Controle > Segure o volume > Desative o "Áudio Espacial".
Desative o EQ do sistema: Vá em Ajustes > Música > EQ > Desativado.
Cancelamento de Ruído (ANC): Pode deixar ativado se estiver em ambiente barulhento, mas para meditação profunda, o modo "Desativado" (nem ANC, nem Transparência) é o que entrega a resposta mais plana.

5. Otimização para Binaural no Bluetooth
Como o Bluetooth pode causar pequenos atrasos entre os lados, os Binaurais muito rápidos (Gama) podem perder um pouco da eficácia.
Dica do Estrategista: Para o Ciclo Noturno (Delta/Theta), os AirPods funcionam muito bem, pois as ondas são lentas e o cérebro as processa com facilidade mesmo via Bluetooth.

Conclusão do Setup:
Caminho: Arquivo .wav (96kHz) -> App Neutron/VOX -> AirPods (Volume em 50-60%).

Lembrete: Quando tiver tempo e quiser a experiência de "Cura Profunda", volte para o KZ ZSN + DAC, pois ali você terá 100% da informação matemática que o seu script gerou."""

TEXTO_RECEITAS = r"""LIVRO DE PROTOCOLOS E RECEITAS
-------------------------------------------
PADRÃO DE NOMENCLATURA SUGERIDO:
- Puras: FREQ_[Hz]_[Finalidade]
- Binaurais: BIN_[Estado]_[Hz]
- Mixes: MIX_[Objetivo]

EXEMPLOS DE MIXAGEM (2 SONS):
- FOCO: Rosa (60%) + Beta 20Hz (40%) + Pura (0%)
- CALMA: Marrom (70%) + Alpha 10Hz (30%) + Pura (0%)

EXEMPLO DE MIXAGEM (3 SONS):
- REGENERAÇÃO: Marrom (50%) + Delta 2.5Hz (30%) + 528Hz (20%)

Protocolo Nexus: Ciclo Noturno de Purificação
Este protocolo totaliza 60 minutos. Você pode programar o Foobar2000 para tocar os arquivos em sequência e usar o "Sleep Timer" do Windows para desligar o PC após 1 hora.

1. Fase de Purificação (00:00 - 00:15)
Frequência: FREQ_417Hz (Transmutação) + COR_Marrom (Ruído Marrom)
Objetivo: Limpeza energética. O 417Hz "desfaz" situações negativas do dia e limpa traumas, enquanto o Ruído Marrom acalma o sistema nervoso central imediatamente.
Volumes Sugeridos: 417Hz (40%) | Ruído Marrom (60%).

2. Fase de Conexão e Intuição (00:15 - 00:30)
Frequência: FREQ_741Hz (Intuição) + FREQ_852Hz (Despertar)
Objetivo: Desintoxicação mental e retorno à ordem espiritual. O 741Hz limpa as células e o 852Hz abre a percepção para o Eu Superior. É o momento de soltar preocupações lógicas.
Volumes Sugeridos: 741Hz (50%) | 852Hz (50%).

3. Fase de Milagre e Regeneração (00:30 - 00:45)
Frequência: FREQ_528Hz (Amor/DNA) + BIN_THETA_6Hz (Arsenal)
Objetivo: Reparo profundo. O 528Hz atua na vibração do amor e cura, enquanto a onda Theta (6Hz) induz o estado de meditação profunda, preparando o cérebro para o desligamento.
Volumes Sugeridos: 528Hz (30%) | Theta 6Hz (70%).

4. Fase de Entrega ao Vácuo (00:45 - 01:00)
Frequência: BIN_DELTA_2Hz (Sono Profundo) + COR_Marrom ou COR_Rosa
Objetivo: Sono reparador. Os 2Hz Delta forçam o cérebro a entrar no estágio 3 e 4 do sono (ondas lentas), onde ocorre a liberação de GH (hormônio do crescimento) e a limpeza de toxinas cerebrais.
Volumes Sugeridos: Delta 2Hz (40%) | Ruído (60%).

Instrução de Biohacking para o Estrategista:
Se você sentir que sua mente está muito barulhenta antes de começar a playlist, adicione a Ressonância Schumann (7.83Hz) nos primeiros 5 minutos. Ela vai atuar como uma "âncora" na Terra, facilitando todo o resto do processo de purificação.
Dica de Ouro: Não use volumes altos. No estado noturno, o ouvido fica mais sensível. O volume deve ser baixo o suficiente para que, na fase 4, você mal perceba que o som parou.

No Foobar2000:
Vá em File > Preferences > Media Library.
Adicione o caminho C:\Users\gabri\Desktop\Scripts\Sons Puros\Ciclo_Diario_Noturno.
Clique em Library > Rescan All.
Agora basta criar uma playlist chamada "NEXUS NIGHT" e arrastar os 4 arquivos em ordem.

Modo de Uso Sugerido:
Ao deitar, inicie a playlist. 
Cada fase tem 15 minutos e termina com um "fade out" (volume diminuindo suavemente) de 10 segundos, sinalizando a transição para a próxima etapa sem dar sustos no seu cérebro. 
No final da Fase 4, você já estará em estado de sono Delta profundo.

🟢 FREQUÊNCIAS SOLFEGGIO (CURA ANTIGA)
174 Hz — Frequência de Alívio
Valor: 174 Hz
Para que serve: Conhecida como frequência de alívio da dor, ajuda a reduzir dores físicas e tensões, trazendo sensação de segurança e relaxamento. Muitas pessoas relatam um efeito analgésico suave e conforto ao ouvi-la.
Tempo recomendado: ~10 a 15 minutos, ou conforme necessário para aliviar desconfortos.

285 Hz — Frequência de Regeneração
Valor: 285 Hz
Para que serve: Auxilia na cura física, promovendo regeneração de tecidos e células lesionadas. Pode acelerar a cicatrização de feridas e reduzir inflamações, ajudando na recuperação do corpo.
Tempo recomendado: 15 a 30 minutos em sessões relaxantes, focando nas áreas que precisam de cura.

396 Hz — Frequência Libertadora
Valor: 396 Hz
Para que serve: Associada à liberação do medo e da culpa, transformando emoções negativas em positivas. Ajuda a aliviar sentimentos de culpa e ansiedade, promovendo alegria e segurança.
Tempo recomendado: Cerca de 15 minutos de meditação, visando alívio emocional e fortalecimento da autoestima.

417 Hz — Frequência da Transmutação
Valor: 417 Hz
Para que serve: Ajuda a “desfazer” situações negativas e facilitar mudanças positivas. Está ligada à limpeza de energia negativa de ambientes e da mente, auxiliando no desprendimento de traumas e no recomeço.
Tempo recomendado: ~15 minutos, especialmente no início do dia ou durante períodos de transição.
528 Hz — Frequência do Amor (Milagres)

Valor: 528 Hz
Para que serve: Chamada de “frequência dos milagres”, está associada à transformação e cura profunda – alguns a relacionam à reparação do DNA e ao estímulo do amor próprio. Pode aumentar sentimentos de positividade, amor e paz interior.
Tempo recomendado: 15 a 30 minutos em sessões de relaxamento ou meditação.

639 Hz — Frequência da Harmonia
Valor: 639 Hz
Para que serve: Ligada ao chakra do coração, promove harmonia nos relacionamentos, comunicação amorosa e equilíbrio emocional. Indicada para melhorar conexões interpessoais e estimular compreensão e perdão.
Tempo recomendado: 15 a 30 minutos, ouvindo em um momento calmo.

741 Hz — Frequência da Intuição
Valor: 741 Hz
Para que serve: Auxilia na solução de problemas e na expressão da verdade interior, despertando a intuição. Ajuda a “desintoxicar” células de energias negativas ou radiação eletromagnética, trazendo clareza mental.
Tempo recomendado: ~15 minutos durante práticas contemplativas (ioga ou journaling).

852 Hz — Frequência do Despertar Espiritual
Valor: 852 Hz
Para que serve: Associada ao retorno à ordem espiritual, eleva a consciência e expande a percepção espiritual. Estimula a intuição profunda e a conexão com o Eu superior.
Tempo recomendado: 15 a 20 minutos em meditação silenciosa.

963 Hz — Frequência da Consciência Divina
Valor: 963 Hz
Para que serve: Chamada de “frequência de Deus” ou do chakra da coroa. Está ligada à expansão da consciência, ativação da glândula pineal e conexão com a luz do universo. Auxilia no sentimento de unidade.
Tempo recomendado: 20 minutos (ou mais) em meditação profunda.

🔵 OUTRAS FREQUÊNCIAS NATURAIS E POPULARES
7,83 Hz — Ressonância Schumann
Valor: ~7,83 Hz
Propósito: Frequência fundamental da Terra ("batimento cardíaco"). Usada para grounding (aterramento) e equilíbrio, sincronizando a mente com a natureza. Reduz estresse e induz calma criativa.
Tempo: 10 a 30 minutos em ambiente tranquilo.

111 Hz — Frequência Divina
Valor: 111 Hz
Propósito: Frequência sagrada para induzir transe meditativo. Estimula endorfinas, reduz dores e eleva o humor. Favorece a regeneração celular e meditação profunda.
Tempo: 10 a 20 minutos.

136,1 Hz — Frequência OM
Valor: ~136,1 Hz (Nota C# natural)
Propósito: Associada ao “Om” primordial e ao chakra do coração. Transmite tranquilidade, equilíbrio e paz interior, ajudando no foco no presente.
Tempo: 5 a 15 minutos.

432 Hz — Frequência Natural do Universo
Valor: 432 Hz
Propósito: Afinação natural que cria sensação de bem-estar. Reduz estresse, ansiedade e melhora a concentração. Proporciona um sono de melhor qualidade.
Tempo: 15 minutos ou mais durante estudos, ioga ou antes de dormir.

440 Hz — Afinação Padrão (Referência)
Observação: Padrão global da música contemporânea. Mencionada para contexto; não possui uso terapêutico específico em biohacking sonoro comparada à 432 Hz.
777 Hz — Frequência Dourada (Angélica)
Propósito: Promove relaxamento, clareza mental e equilíbrio espiritual. Atua nos níveis físico e emocional simultaneamente, auxiliando na manifestação de intenções positivas.
Tempo: Até 20 minutos ou sessões longas de 1 hora.

888 Hz — Frequência da Abundância
Propósito: Ligada à prosperidade e equilíbrio. Gera forte relaxamento, limpa negatividades e reforça a positividade interna, fortalecendo o sistema imune via redução de estresse.
Tempo: 15 a 30 minutos antes de dormir.

🧠 ONDAS CEREBRAIS (BINAURAIS)
Ondas Delta (0,5–4 Hz)
Estado: Sono profundo e reparador.
Uso: Cura física e regeneração do corpo. Ideal para insônia.
Dica: 2 Hz (sono profundo) ou 3,5 Hz (sono REM). Usar temporizador para desligar após 1 hora.

Ondas Theta (4–8 Hz)
Estado: Relaxamento profundo, meditação leve e criatividade.
Uso: Melhorar intuição, memória e induzir sonhos lúcidos.
Dica: 6 Hz binaural ajuda a gerar sensação de serenidade.

Ondas Alfa (8–12 Hz)
Estado: Mente calma porém alerta (presença).
Uso: Reduzir ansiedade e melhorar o foco suave. Excelente para iniciar meditações.
Dica: 10 Hz para foco calmo sem induzir sono.

Ondas Beta (13–30 Hz)
Estado: Alerta, foco ativo e pensamento analítico.
Uso: Aumentar concentração e desempenho cognitivo. Ajuda em tarefas lógicas.
Dica: 15 Hz para estudos intensos. Usar moderadamente para evitar cansaço mental.

Ondas Gama (30–100 Hz)
Estado: Atividade mental ampliada e aprendizagem acelerada.
Uso: Processamento cognitivo intenso e experiências de insight.
Dica: 40 Hz para pico de foco. Sessões curtas de 5 a 15 minutos.

🌈 RUÍDOS COLORIDOS (MÁSCARAS SONORAS)
Ruído Branco (White Noise)
Som: Estática constante (todas as frequências).
Efeito: Mascara ruídos externos (trânsito, conversas). Ajuda a adormecer abafando sons repentinos.

Ruído Rosa (Pink Noise)
Som: Chuva constante ou vento suave (ênfase em graves).
Efeito: Mais "macio". Prolonga o sono profundo e pode melhorar a memória.

Ruído Marrom (Brown Noise)
Som: Cachoeira ou rugido profundo (graves potentes).
Efeito: Muito relaxante. Extremamente eficaz para mentes aceleradas (TDAH) e concentração intensa.

Ruído Verde (Green Noise)
Som: Ambiente natural (floresta ao longe).
Efeito: Transporta a mente para a natureza. Auxilia no relaxamento e alívio de ansiedade.

🧪 COMBINAÇÕES (MIXES PRINCIPAIS)
Mix 432 Hz + 528 Hz — Cura e Alinhamento
Une a ressonância natural com o reparo profundo. Induz relaxamento intenso e vibração positiva.

Mix 396 Hz + 639 Hz + 963 Hz — Libertação e Elevação
Trabalha o emocional (liberação), relacional (amor) e espiritual (conexão) simultaneamente.

Mix 741 Hz + 852 Hz — Intuição e Despertar
Limpeza interior e clareza mental para fortalecer o autoconhecimento e insights.

Mix 7 Chakras (Sequência 396–963 Hz)
Protocolo completo de alinhamento energético. Dedique de 4 a 5 minutos para cada tom, da base ao topo da cabeça.

Mix Frequências de Abundância
Combina frequências angélicas (ex: 777 + 888) para criar um ambiente de alta vibração, gratidão e manifestação.

Tipo de Alfa,Portadora (Hz),Beat Alvo (Hz),Nome Sugerido,Objetivo
Alfa Baixo,200,8,BIN_ALFA_8Hz_Relax,"Relaxamento profundo, quase meditação."
Alfa Médio,200,10,BIN_ALFA_10Hz_Foco,O melhor para Estudo. Foco sem ansiedade.
Alfa Alto,200,12,BIN_ALFA_12Hz_Alerta,"Mente clara, pronta para ação rápida."

Nome do Mix,Base (Ruído),Mente (Binaural),Corpo (Solfeggio),Utilidade Biohacking
ALFA_ZEN_FLOW,Verde (50%),Alfa 8Hz (40%),432 Hz (10%),"Relaxamento Ativo. Ótimo para ler, meditar ou descompressão pós-trabalho."
ALFA_ESTUDO_DEEP,Rosa (60%),Alfa 10Hz (40%),0% (Desativado),Hiper-Foco. O ruído rosa mascara distrações e os 10Hz mantêm o cérebro em modo de absorção.
ALFA_INSIGHT_CREATIVO,Marrom (40%),Alfa 10Hz (40%),741 Hz (20%),Resolução de Problemas. 741Hz desperta a intuição enquanto Alfa estabiliza a mente.
ALFA_ALERTA_CALMO,Branco (50%),Alfa 12Hz (50%),0% (Desativado),Presença Total. Ideal para reuniões ou tarefas que exigem rapidez sem o nervosismo do café.
ALFA_REPARO_MENTAL,Rosa (50%),Alfa 8Hz (30%),528 Hz (20%),Recuperação de Burnout. Foco no relaxamento (8Hz) com a frequência de reparação (528Hz)."""

# --- PERSISTÊNCIA DE CONFIGURAÇÃO ---
def carregar_player_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return ""

def salvar_player_config(path):
    with open(CONFIG_FILE, "w") as f:
        f.write(path)

# --- ENGINE DE ÁUDIO (Backend) ---
def garantir_diretorios():
    for path in DIRS.values():
        if not os.path.exists(path):
            os.makedirs(path)

def aplicar_fade_save(audio, caminho):
    fade_len = int(2.0 * SAMPLE_RATE)
    fade_in = np.linspace(0.0, 1.0, fade_len)
    fade_out = np.linspace(1.0, 0.0, fade_len)
    if len(audio.shape) == 2: # Stereo
        fade_in = fade_in.reshape(-1, 1); fade_out = fade_out.reshape(-1, 1)
    audio[:fade_len] *= fade_in
    audio[-fade_len:] *= fade_out
    # Salvar em 32-bit para máxima precisão matemática
    audio_int = np.int32(audio * 2147483647)
    write(caminho, SAMPLE_RATE, audio_int)

def gerar_onda_pura(freq, nome_arq):
    t = np.linspace(0, DURACAO_PADRAO, int(SAMPLE_RATE * DURACAO_PADRAO), endpoint=False)
    onda = 0.5 * np.sin(2 * np.pi * float(freq) * t)
    aplicar_fade_save(onda, os.path.join(DIRS["Puras"], nome_arq + ".wav"))

def gerar_binaural(portadora, beat, nome_arq):
    t = np.linspace(0, DURACAO_PADRAO, int(SAMPLE_RATE * DURACAO_PADRAO), endpoint=False)
    freq_L = float(portadora)
    freq_R = float(portadora) + float(beat)
    onda_L = 0.5 * np.sin(2 * np.pi * freq_L * t)
    onda_R = 0.5 * np.sin(2 * np.pi * freq_R * t)
    stereo = np.column_stack((onda_L, onda_R))
    aplicar_fade_save(stereo, os.path.join(DIRS["Binaural"], nome_arq + ".wav"))

def gerar_ruido(cor, nome_arq):
    amostras = int(SAMPLE_RATE * DURACAO_PADRAO)
    if cor == "Branco":
        ruido = np.random.normal(0, 0.5, amostras)
    elif cor == "Rosa":
        # Aproximação para ruído rosa
        ruido = np.random.normal(0, 0.5, amostras)
    elif cor == "Marrom":
        ruido = np.cumsum(np.random.normal(0, 0.5, amostras))
        ruido = ruido / np.max(np.abs(ruido)) * 0.5
    aplicar_fade_save(ruido, os.path.join(DIRS["Cores"], nome_arq + ".wav"))

def mixar_arquivos(file_cor, file_bin, file_pura, vol_c, vol_b, vol_p, nome_saida):
    try:
        componentes = []
        # Só processa arquivos se o volume for maior que zero
        if vol_c > 0 and file_cor: componentes.append((file_cor, vol_c))
        if vol_b > 0 and file_bin: componentes.append((file_bin, vol_b))
        if vol_p > 0 and file_pura: componentes.append((file_pura, vol_p))

        if not componentes: return False, "Nenhum som selecionado com volume."

        audios_list = []
        for path, vol in componentes:
            r, d = converter_para_float(path)
            audios_list.append(d * vol)

        # Alinhamento pelo menor arquivo
        min_len = min(len(a) for a in audios_list)
        mix = sum(a[:min_len] for a in audios_list)

        # Normalização de segurança
        pico = np.max(np.abs(mix))
        if pico > 1.0: mix /= pico

        dados_int = np.int32(mix * 2147483647)
        write(os.path.join(DIRS["Mixes"], nome_saida + ".wav"), SAMPLE_RATE, dados_int)
        return True, "Sucesso"
    except Exception as e:
        return False, str(e)

def converter_para_float(caminho):
    rate, dados = read(caminho)
    if len(dados.shape) == 1: dados = np.column_stack((dados, dados))
    if dados.dtype == np.int16: dados = dados.astype(np.float32) / 32768.0
    elif dados.dtype == np.int32: dados = dados.astype(np.float32) / 2147483648.0
    return rate, dados

# --- INTERFACE GRÁFICA ---
class NexusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS AUDIO LAB - Zen Experience v3.5")
        self.root.geometry("950x750")
        
        self.bg_color = "#f4f7f6"
        self.panel_color = "#ffffff"
        self.accent_color = "#4a90e2"
        self.text_color = "#2c3e50"
        self.sub_text = "#7f8c8d"
        
        self.root.configure(bg=self.bg_color)
        self.player_path = carregar_player_config()
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#d1d8d7", foreground=self.text_color, padding=[20, 10], font=("Segoe UI", 10))
        self.style.map("TNotebook.Tab", background=[("selected", self.panel_color)], foreground=[("selected", self.accent_color)])
        
        self.style.configure("TFrame", background=self.panel_color)
        self.style.configure("TLabel", background=self.panel_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.accent_color)
        
        self.style.configure("TButton", background="#e8eceb", foreground=self.text_color, borderwidth=0, font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[("active", self.accent_color)], foreground=[("active", "#ffffff")])
        
        self.style.configure("Horizontal.TScale", background=self.panel_color, troughcolor="#e8eceb")

        garantir_diretorios()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.tab_guia = ttk.Frame(self.notebook)
        self.tab_gen = ttk.Frame(self.notebook)
        self.tab_mix = ttk.Frame(self.notebook)
        self.tab_lib = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_guia, text="📖 Guia & Protocolos")
        self.notebook.add(self.tab_gen, text="✨ Gerador de Ondas")
        self.notebook.add(self.tab_mix, text="🎚️ Mesa de Mixagem")
        self.notebook.add(self.tab_lib, text="📂 Biblioteca")
        
        self.setup_guia()
        self.setup_generator()
        self.setup_mixer()
        self.setup_library()

    def setup_guia(self):
        main_frame = ttk.Frame(self.tab_guia)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ttk.Label(main_frame, text="Manual do Usuário Nexus", style="Header.TLabel").pack(pady=(0, 20))
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="Guia de Configuração", command=lambda: self.exibir_guia(TEXTO_CONFIGURACAO)).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(btn_frame, text="Livro de Receitas", command=lambda: self.exibir_guia(TEXTO_RECEITAS)).pack(side="left", expand=True, fill="x", padx=5)
        
        self.txt_guia = tk.Text(main_frame, wrap="word", font=("Segoe UI", 11), bg="#fdfdfd", fg=self.text_color, padx=20, pady=20, relief="flat", highlightthickness=1, highlightbackground="#e8eceb")
        self.txt_guia.pack(fill="both", expand=True, pady=10)
        self.txt_guia.insert("1.0", "Selecione um guia acima para ver os protocolos...")
        self.txt_guia.config(state="disabled")

    def exibir_guia(self, texto):
        self.txt_guia.config(state="normal")
        self.txt_guia.delete("1.0", tk.END)
        self.txt_guia.insert("1.0", texto)
        self.txt_guia.config(state="disabled")

    def setup_generator(self):
        frame = ttk.Frame(self.tab_gen)
        frame.pack(pady=40, padx=40, fill="x")
        
        ttk.Label(frame, text="Sintetizador de Alta Precisão", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")
        
        ttk.Label(frame, text="Tipo de Onda:").grid(row=1, column=0, sticky="w", pady=10)
        self.combo_tipo = ttk.Combobox(frame, values=["Frequência Pura", "Binaural Beat", "Ruído Colorido"], state="readonly", font=("Segoe UI", 10))
        self.combo_tipo.grid(row=1, column=1, sticky="ew", pady=10)
        self.combo_tipo.current(0)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.update_gen_inputs)
        
        self.lbl_p1 = ttk.Label(frame, text="Frequência (Hz):")
        self.lbl_p1.grid(row=2, column=0, sticky="w", pady=10)
        self.ent_p1 = ttk.Entry(frame, font=("Segoe UI", 10))
        self.ent_p1.grid(row=2, column=1, sticky="ew", pady=10)
        
        self.lbl_p2 = ttk.Label(frame, text="Beat (Diferença Hz):")
        self.lbl_p2.grid(row=3, column=0, sticky="w", pady=10)
        self.ent_p2 = ttk.Entry(frame, font=("Segoe UI", 10))
        self.ent_p2.grid(row=3, column=1, sticky="ew", pady=10)
        
        ttk.Label(frame, text="Nome do Arquivo:").grid(row=4, column=0, sticky="w", pady=10)
        self.ent_nome = ttk.Entry(frame, font=("Segoe UI", 10))
        self.ent_nome.grid(row=4, column=1, sticky="ew", pady=10)
        
        ttk.Button(frame, text="GERAR ÁUDIO", command=self.run_generator).grid(row=5, column=0, columnspan=2, pady=30, ipady=5, sticky="ew")
        self.log_gen = ttk.Label(frame, text="Aguardando parâmetros...", foreground=self.sub_text)
        self.log_gen.grid(row=6, column=0, columnspan=2)
        
        frame.columnconfigure(1, weight=1)
        self.update_gen_inputs(None)

    def update_gen_inputs(self, event):
        tipo = self.combo_tipo.get()
        self.ent_p1.config(state="normal"); self.ent_p2.config(state="normal")
        if tipo == "Frequência Pura":
            self.lbl_p1.config(text="Frequência (Hz):"); self.lbl_p2.config(text="---", state="disabled"); self.ent_p2.config(state="disabled")
        elif tipo == "Binaural Beat":
            self.lbl_p1.config(text="Portadora (Hz):"); self.lbl_p2.config(text="Beat Alvo (Hz):")
        elif tipo == "Ruído Colorido":
            self.lbl_p1.config(text="Cor (Branco/Rosa/Marrom):"); self.lbl_p2.config(text="---", state="disabled"); self.ent_p2.config(state="disabled")

    def run_generator(self):
        tipo, nome = self.combo_tipo.get(), self.ent_nome.get()
        if not nome: messagebox.showwarning("Aviso", "Por favor, nomeie seu som."); return
        self.log_gen.config(text="Sintetizando...", foreground=self.accent_color); self.root.update()
        def task():
            try:
                if tipo == "Frequência Pura": gerar_onda_pura(float(self.ent_p1.get()), nome)
                elif tipo == "Binaural Beat": gerar_binaural(float(self.ent_p1.get()), float(self.ent_p2.get()), nome)
                elif tipo == "Ruído Colorido": gerar_ruido(self.ent_p1.get().capitalize(), nome)
                self.log_gen.config(text=f"Pronto: {nome}.wav gerado.", foreground="#27ae60")
                self.refresh_library(); self.refresh_mixer_lists()
            except Exception as e: self.log_gen.config(text=f"Erro: {str(e)}", foreground="#c0392b")
        threading.Thread(target=task).start()

    def setup_mixer(self):
        frame = ttk.Frame(self.tab_mix)
        frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        ttk.Label(frame, text="Mesa de Mixagem Flexível", style="Header.TLabel").grid(row=0, column=0, columnspan=4, pady=(0, 30), sticky="w")
        
        def criar_slider(row, label_text, default_val):
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w", pady=15)
            cb = ttk.Combobox(frame, state="readonly", width=30, font=("Segoe UI", 9))
            cb.grid(row=row, column=1, padx=10, pady=15)
            lbl_pct = ttk.Label(frame, text=f"{int(default_val*100)}%", width=5, font=("Segoe UI", 9, "bold"))
            lbl_pct.grid(row=row, column=3, padx=5)
            scale = ttk.Scale(frame, from_=0.0, to=1.0, value=default_val, orient="horizontal", command=lambda v: lbl_pct.config(text=f"{int(float(v)*100)}%"))
            scale.grid(row=row, column=2, padx=10, sticky="ew")
            return cb, scale

        self.cb_cor, self.vol_cor = criar_slider(1, "Camada 1 (Cores):", 0.5)
        self.cb_bin, self.vol_bin = criar_slider(2, "Camada 2 (Binaural):", 0.3)
        self.cb_pur, self.vol_pur = criar_slider(3, "Camada 3 (Pura):", 0.0) 
        
        ttk.Label(frame, text="Nome da Mixagem:").grid(row=4, column=0, pady=30, sticky="w")
        self.ent_mix_nome = ttk.Entry(frame, font=("Segoe UI", 10))
        self.ent_mix_nome.grid(row=4, column=1, columnspan=2, sticky="ew", pady=30, padx=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=4, sticky="ew")
        ttk.Button(btn_frame, text="↻ ATUALIZAR LISTAS", command=self.refresh_mixer_lists).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(btn_frame, text="❃ CRIAR MIXAGEM", command=self.run_mixer).pack(side="left", expand=True, fill="x", padx=5)

        self.lbl_status_mix = ttk.Label(frame, text="Dica: Deixe o volume em 0% para mixar apenas 1 ou 2 sons.", font=("Segoe UI", 9, "italic"))
        self.lbl_status_mix.grid(row=6, column=0, columnspan=4, pady=10)
        frame.columnconfigure(2, weight=1)

    def refresh_mixer_lists(self):
        def scan_recursive(path):
            files = []
            if os.path.exists(path):
                for root, d, f in os.walk(path):
                    for file in f:
                        if file.endswith(".wav"): files.append(file)
            return files

        self.cb_cor['values'] = scan_recursive(DIRS["Cores"])
        self.cb_bin['values'] = scan_recursive(DIRS["Binaural"])
        self.cb_pur['values'] = scan_recursive(DIRS["Puras"])
        
        # Auto-seleciona o primeiro se existir
        for cb in [self.cb_cor, self.cb_bin, self.cb_pur]:
            if cb['values']: cb.current(0)

    def run_mixer(self):
        f_cor, f_bin, f_pur, nome = self.cb_cor.get(), self.cb_bin.get(), self.cb_pur.get(), self.ent_mix_nome.get()
        if not nome: messagebox.showwarning("Aviso", "Dê um nome à sua mixagem."); return
        
        self.lbl_status_mix.config(text="Mixagem em curso...", foreground=self.accent_color); self.root.update()
        
        def task():
            path_c = os.path.join(DIRS["Cores"], f_cor) if f_cor else None
            path_b = os.path.join(DIRS["Binaural"], f_bin) if f_bin else None
            path_p = os.path.join(DIRS["Puras"], f_pur) if f_pur else None
            
            ok, msg = mixar_arquivos(path_c, path_b, path_p, self.vol_cor.get(), self.vol_bin.get(), self.vol_pur.get(), nome)
            if ok: self.lbl_status_mix.config(text=f"Sucesso: {nome} salvo.", foreground="#27ae60"); self.refresh_library()
            else: self.lbl_status_mix.config(text=f"Erro: {msg}", foreground="#c0392b")
        threading.Thread(target=task).start()

    def setup_library(self):
        frame = ttk.Frame(self.tab_lib)
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        cfg_frame = tk.Frame(frame, bg="#f9f9f9", padx=15, pady=15, highlightthickness=1, highlightbackground="#e8eceb")
        cfg_frame.pack(fill="x", pady=(0, 20))
        self.lbl_player = ttk.Label(cfg_frame, text=f"Player: {os.path.basename(self.player_path) if self.player_path else 'Sistema'}", background="#f9f9f9", font=("Segoe UI", 9, "italic"))
        self.lbl_player.pack(side="left")
        ttk.Button(cfg_frame, text="Selecionar Player Externo", command=self.selecionar_player).pack(side="right")
        
        columns = ("nome", "tipo", "tamanho")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("nome", text="Arquivo"); self.tree.heading("tipo", text="Categoria"); self.tree.heading("tamanho", text="Tamanho")
        self.tree.column("nome", width=400); self.tree.column("tamanho", width=100, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y"); self.tree.configure(yscrollcommand=scroll.set)
        
        btn_frame = ttk.Frame(self.tab_lib)
        btn_frame.pack(fill="x", padx=30, pady=(0, 30))
        ttk.Button(btn_frame, text="↻ ATUALIZAR BIBLIOTECA", command=self.refresh_library).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="▶ REPRODUZIR", command=self.play_file).pack(side="right", padx=5, ipadx=20)
        self.refresh_library()

    def selecionar_player(self):
        path = filedialog.askopenfilename(title="Selecionar Foobar2000", filetypes=[("Executáveis", "*.exe")])
        if path: self.player_path = path; salvar_player_config(path); self.lbl_player.config(text=f"Player: {os.path.basename(path)}")

    def refresh_library(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for cat_nome, cat_path in DIRS.items():
            if os.path.exists(cat_path):
                for root, dirs, files in os.walk(cat_path):
                    for f in files:
                        if f.endswith(".wav"):
                            full_p = os.path.join(root, f)
                            size_mb = f"{os.path.getsize(full_p)/(1024*1024):.1f} MB"
                            self.tree.insert("", "end", values=(f, cat_nome, size_mb), tags=(full_p,))

    def play_file(self):
        selected = self.tree.selection()
        if not selected: return
        full_path = self.tree.item(selected[0])['tags'][0]
        try:
            if self.player_path and os.path.exists(self.player_path): subprocess.Popen([self.player_path, full_path])
            else: os.startfile(full_path)
        except Exception as e: messagebox.showerror("Erro", f"Falha ao reproduzir: {e}")

if __name__ == "__main__":
    root = tk.Tk(); app = NexusApp(root); root.mainloop()