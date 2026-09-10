# -*- coding: utf-8 -*-
"""
app_firma.py
Sistema de Governança de RH, KPIs e Avaliação — Firma Produções
(arquivo único, autocontido: login por papéis + persistência SQLite/Postgres)
"""

from __future__ import annotations



# ============================================================
# SEÇÃO 1/6 — DADOS (dados_firma.py)
# ============================================================
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# 1. ALÇADAS FINANCEIRAS E FRONTEIRAS CORPORATIVAS (consulta de bastidores)
# ---------------------------------------------------------------------------

ALCADAS = {
    "Auxiliares e Assistentes": {
        "limite_aprovacao": 0.0,
        "descricao": (
            "Alçada financeira igual a R$ 0,00. Não possuem autonomia para "
            "aprovar despesas ou prometer contratações/mudanças salariais."
        ),
    },
    "Técnicos e Supervisores": {
        "limite_aprovacao": 2000.0,
        "descricao": (
            "Podem aprovar despesas operacionais emergenciais de projetos até "
            "o limite de R$ 2.000,00, desde que a verba esteja prevista no "
            "orçamento do projeto. Valores acima disso, bem como contratações, "
            "demissões e alterações salariais, são de alçada exclusiva do CEO."
        ),
    },
}

FRONTEIRAS_CORPORATIVAS = [
    "1. Diretrizes da Liderança",
    "2. Políticas da Firma",
    "3. Processos Internos",
    "4. Responsabilidades de Outras Áreas",
    "5. Decisões Estratégicas da Empresa",
    "6. Escopo Contratado com o Cliente",
    "7. Segurança Física e da Informação (Risco de vida ou queima de "
    "patrimônio anula prazos operacionais)",
]

# ---------------------------------------------------------------------------
# 2. REGRAS DE ELEGIBILIDADE / JANELAS DE PROMOÇÃO
# ---------------------------------------------------------------------------

TEMPO_MINIMO_EMPRESA_MESES = 12       # 1 ano completo de vínculo
TEMPO_MINIMO_NIVEL_MESES = 6          # interstício mínimo entre subníveis
MESES_JANELA_PROMOCAO = (6, 12)       # Junho e Dezembro

# ---------------------------------------------------------------------------
# 3. GATILHO FINANCEIRO (régua 1.0 a 5.0)
# ---------------------------------------------------------------------------
# Ajuste este único valor para mudar o percentual de aproveitamento exigido
# para elegibilidade financeira. Ex.: 3.5 = 70%, 4.0 = 80%, 4.5 = 90%.

NOTA_MINIMA_ELEGIVEL = 4.0            # 80% de resultados positivos
NOTA_REGUA_MATURIDADE = 3.0           # meta padrão: consistência e estabilidade no nível atual
NOTA_MIN = 1.0
NOTA_MAX = 5.0

# ---------------------------------------------------------------------------
# 4. CAMADA 2 — MÓDULO PÓS-EVENTO (GABARITO DE CAMPO)
# ---------------------------------------------------------------------------
# Cada item tem duas variantes de pergunta, conforme a trilha do colaborador:
#   "auxiliar"            -> Auxiliar I/II/III
#   "assistente_tecnico"  -> Assistente/Técnico
# O ITEM 5 tem um único texto, aplicável a Auxiliar/Técnico conforme o
# documento oficial, e é reaproveitado para todos os perfis no sistema.

ITENS_CAMPO = {
    "item1": {
        "titulo": "SLA de Cronograma Corporativo (Tempo)",
        "auxiliar": (
            "O profissional realizou a movimentação de cases e a "
            "pré-separação de módulos/cabos de forma ágil, garantindo que o "
            "time iniciasse a montagem sem atrasar o cronograma do "
            "hotel/espaço?"
        ),
        "assistente_tecnico": (
            "Entregou o sistema ou a estação técnica sob sua responsabilidade "
            "100% pronta e testada antes do horário limite fixado para o "
            "ensaio técnico do cliente?"
        ),
    },
    "item2": {
        "titulo": "Qualidade e Estabilidade (Performance Geral)",
        "auxiliar": (
            "Executou o encaixe físico, travamento mecânico de estruturas ou "
            "passagens de cabos de forma firme, reta e perfeitamente alinhada "
            "ao padrão da Firma?"
        ),
        "assistente_tecnico": (
            "O sistema manteve 100% de estabilidade de sinal, áudio limpo, "
            "inteligibilidade e brilho/proporção corretos ao longo de toda a "
            "fita técnica ao vivo (zero piscadas, travamentos ou "
            "microfonias)?"
        ),
    },
    "item3": {
        "titulo": "Postura e Etiqueta Corporativa (O Olhar do Cliente)",
        "auxiliar": (
            "Demonstrou disciplina, uso completo de EPIs e uniforme da Firma, "
            "mantendo os materiais organizados e acondicionados corretamente "
            "nos cases?"
        ),
        "assistente_tecnico": (
            "Manteve postura altamente profissional e discreta na House, sem "
            "dispersão com celular pessoal e realizou o atendimento/"
            "microfonação de diretores corporativos com extrema cordialidade "
            "e respeito?"
        ),
    },
    "item4": {
        "titulo": "Gestão de Crise e Operação (Mudanças de Roteiro)",
        "auxiliar": (
            "Ao notar qualquer falha simples de cabo ou peça que não "
            "encaixava, atuou de forma calma, investigou objetivamente e "
            "acionou o responsável rápido sem improvisar?"
        ),
        "assistente_tecnico": (
            "Respondeu às mudanças urgentes de roteiro ou problemas de sinal "
            "de forma ágil e metódica por causa-efeito, aplicando caminhos "
            "lógicos/contingências com equilíbrio emocional sob pressão?"
        ),
    },
    "item5": {
        "titulo": "Eficiência de Desmonte e Logística (Zelo Patrimonial)",
        "auxiliar": (
            "Conduziu a retirada e a guarda de cabos limpos, enrolados por "
            "tamanho, cases organizados e lacrados, garantindo desmonte "
            "rápido para cumprir os prazos de devolução da sala do hotel, "
            "registrando avarias para a manutenção?"
        ),
        "assistente_tecnico": (
            "Conduziu a retirada e a guarda de cabos limpos, enrolados por "
            "tamanho, cases organizados e lacrados, garantindo desmonte "
            "rápido para cumprir os prazos de devolução da sala do hotel, "
            "registrando avarias para a manutenção?"
        ),
    },
}

NIVEIS_IMPACTO_CLIENTE = {
    "verde": {
        "label": "Nível Verde",
        "descricao": (
            "O trabalho elevou o nível de satisfação do cliente corporativo / "
            "agregou valor ao evento."
        ),
        "gera_alerta": False,
    },
    "amarelo": {
        "label": "Nível Amarelo",
        "descricao": (
            "O trabalho foi neutro. Cumpriu a obrigação sem gerar atritos ou "
            "impactos perceptíveis."
        ),
        "gera_alerta": False,
    },
    "laranja": {
        "label": "Nível Laranja",
        "descricao": (
            "Ocorreu um erro técnico ou de postura leve que gerou cobrança "
            "da agência/produção."
        ),
        "gera_alerta": False,
    },
    "vermelho": {
        "label": "Nível Vermelho (Crítico)",
        "descricao": (
            "O erro ou a postura gerou uma crise direta com o cliente final "
            "(atraso oficial, falha grave na fala do palestrante ou "
            "reclamação formal da diretoria do cliente)."
        ),
        "gera_alerta": True,
    },
}

# ---------------------------------------------------------------------------
# 5. CAMADA 3 — PARTE B: VALORES INSTITUCIONAIS (fixo para todos os cargos)
# ---------------------------------------------------------------------------

VALORES_CULTURA = {
    "Criatividade": (
        "Propôs soluções originais para resolver problemas de montagem ou "
        "melhorar os processos internos no mês?"
    ),
    "Excelência": (
        "Demonstrou alto padrão de capricho técnico, testes rigorosos e "
        "acabamentos impecáveis em campo?"
    ),
    "Honestidade": (
        "Assumiu falhas de forma transparente, jogou limpo com o time e "
        "comunicou perdas/avarias sem tentar omitir o erro?"
    ),
    "Colaboração": (
        "Apoiou voluntariamente as outras frentes técnicas do evento após "
        "concluir a sua tarefa individual?"
    ),
    "Fé": (
        "Manteve a postura positiva, foco na solução e energia alta mesmo em "
        "produções difíceis ou prazos estourados?"
    ),
    "Aprender Sempre": (
        "Demonstrou abertura para receber feedbacks, buscou aprender com "
        "seniores e expandir seu domínio técnico no mês?"
    ),
}

# ---------------------------------------------------------------------------
# 6. CAMADA 3 — PARTE A: CRITÉRIOS POR CARGO/NÍVEL (Capítulo 7 — Resumo por
#    Pilar). Estrutura: AREAS[area][cargo_label] = {pilar: texto, ...}
# ---------------------------------------------------------------------------

AREAS = {}

# ---- ÁREA: LED ----------------------------------------------------------
AREAS["LED"] = {
    "Auxiliar de LED I": {
        "Autonomia": "Executa tarefas conhecidas com menor acompanhamento e reconhece quando precisa de apoio.",
        "Criticidade": "Percebe falhas e situações que podem gerar dano, retrabalho, atraso ou impacto no evento.",
        "Comportamento": "Responsabilidade, atenção, organização, comunicação, cuidado e colaboração.",
        "Entrega": "Assume responsabilidade por etapas específicas e garante que sua parte da operação seja concluída corretamente.",
        "Complexidade": "Compreende e executa etapas técnicas conhecidas da montagem e operação.",
    },
    "Auxiliar de LED II": {
        "Autonomia": "Executa atividades conhecidas sem acompanhamento constante.",
        "Criticidade": "Começa a impactar diretamente ritmo, organização e retrabalho.",
        "Comportamento": "Iniciativa, responsabilidade, colaboração e comunicação.",
        "Entrega": "Atividade concluída com qualidade e preparação para a próxima etapa.",
        "Complexidade": "Lida com variações simples da rotina.",
    },
    "Auxiliar de LED III": {
        "Autonomia": "Executa com independência, antecipa necessidades e conhece os limites do próprio papel.",
        "Criticidade": "Impacta diretamente o andamento da equipe e a organização do trabalho.",
        "Comportamento": "Maturidade, equilíbrio sob pressão, postura de referência e disposição para ensinar.",
        "Entrega": "Execução consistente, antecipação de riscos e apoio ao desenvolvimento de outros profissionais.",
        "Complexidade": "Lida com mudanças de rotina, reorganizações e situações inesperadas simples.",
    },
}
_assistente_led = {
    "Autonomia": "Conduz etapas relevantes com elevada autonomia e sabe quando precisa acionar a liderança.",
    "Criticidade": "Atua diretamente na prevenção, antecipa riscos e compreende o impacto das falhas sobre a operação.",
    "Comportamento": "É referência de postura operacional, organização, comunicação, responsabilidade e apoio aos demais.",
    "Entrega": "Garante uma etapa pronta, testada, organizada, estável e confiável dentro do escopo.",
    "Complexidade": "Diagnostica, analisa ocorrências de forma estruturada e compreende as relações entre componentes do sistema.",
}
_tecnico_led = {
    "Autonomia": "Muito alta. Conduz soluções técnicas avançadas, investiga o que não é óbvio e toma decisões dentro de seu domínio.",
    "Criticidade": "Assume responsabilidade técnica pelos cenários mais críticos e complexos da operação, priorizando estabilidade e segurança.",
    "Comportamento": "Referência técnica máxima da área, mantém controle emocional estável sob crise, compartilha conhecimento e trabalha de forma colaborativa.",
    "Entrega": "Garante alta confiabilidade e consistência técnica, soluciona ocorrências complexas e atua para prevenir reincidências estruturais.",
    "Complexidade": "Analisa cenários fora do padrão, constrói e dimensiona soluções lógicas integradas (módulo → alimentação → cabeamento → sinal → processamento).",
}
for _n in ("I", "II", "III"):
    AREAS["LED"][f"Assistente de LED {_n}"] = dict(_assistente_led)
for _n in ("I", "II", "III"):
    AREAS["LED"][f"Técnico de LED {_n}"] = dict(_tecnico_led)

# ---- ÁREA: SOM ----------------------------------------------------------
_auxiliar_som = {
    "Autonomia": "Alta dentro das frentes básicas, organiza sua sequência e executa tarefas sem supervisão constante.",
    "Criticidade": "Identifica problemas simples, antecipa necessidades do escopo e comunica riscos de forma objetiva.",
    "Comportamento": "Maturidade, iniciativa, responsabilidade, colaboração e foco no desenvolvimento técnico contínuo.",
    "Entrega": "Entrega consistente, organizada, limpa e segura de cabeamentos e estruturas de palco.",
    "Complexidade": "Baixa/Moderada; domina rotinas básicas e reconhece o limite do próprio papel.",
}
_assistente_som = {
    "Autonomia": "Alta na condução de grandes frentes operacionais, operando com pouca ou nenhuma supervisão direta.",
    "Criticidade": "Atua sobre causas e recorrências, realiza testes estruturados e antecipa riscos no fluxo de sinal.",
    "Comportamento": "Iniciativa, segurança executiva, postura discreta e cordial no trato com palestrantes e orienta níveis anteriores.",
    "Entrega": "Entrega altamente consistente, de extrema qualidade, estabilidade e menor necessidade de acompanhamento.",
    "Complexidade": "Intermediário consolidado; gerencia patches, ganho, microfonação, in-ears e consoles digitais conhecidos.",
}
_tecnico_som = {
    "Autonomia": "Muito alta; define a engenharia de áudio e toma decisões técnicas complexas de forma independente.",
    "Criticidade": "Responde pela confiabilidade técnica global e inteligibilidade, eliminando microfonias e panes por ações de prevenção de raiz.",
    "Comportamento": "Referência técnica da área, mantém calma total sob pressão, forma novos técnicos e compartilha o raciocínio físico do áudio.",
    "Entrega": "Alta consistência técnica na House e transmissões, cria checklists e padrões corporativos para a empresa.",
    "Complexidade": "Avançado; soluciona intercorrências críticas integradas de RF, processamento, acústica e consoles avançados sem roteiro pronto.",
}
AREAS["SOM"] = {}
for _n in ("I", "II", "III"):
    AREAS["SOM"][f"Auxiliar de Som {_n}"] = dict(_auxiliar_som)
for _n in ("I", "II", "III"):
    AREAS["SOM"][f"Assistente de Som {_n}"] = dict(_assistente_som)
for _n in ("I", "II", "III"):
    AREAS["SOM"][f"Técnico de Som {_n}"] = dict(_tecnico_som)

# ---- ÁREA: ILUMINAÇÃO ---------------------------------------------------
_auxiliar_luz = {
    "Autonomia": "Alta nas atividades básicas de montagem, posicionamento e desmonte sem demandar supervisão constante.",
    "Criticidade": "Identifica ocorrências simples, antecipa falta de materiais e comunica riscos antes que virem problemas.",
    "Comportamento": "Maturidade, iniciativa, responsabilidade, cuidado com lentes e garras de fixação e apoio aos níveis iniciais.",
    "Entrega": "Execução consistente, cabeamento limpo e esteticamente alinhado, e desmonte organizado nos cases certos.",
    "Complexidade": "Baixa/Moderada; conhece os componentes de sinal/energia DMX e respeita os limites da alçada técnica.",
}
_assistente_luz = {
    "Autonomia": "Alta; conduz etapas estruturadas relevantes com pouca supervisão e sabe quando deve acionar a liderança técnica.",
    "Criticidade": "Assume maior responsabilidade pela qualidade, segurança elétrico-mecânica e prevenção ativa de problemas de dados na fita.",
    "Comportamento": "Referência de postura operacional, organização rigorosa na House, comunicação objetiva e compartilhamento de conhecimento.",
    "Entrega": "Garante uma entrega confiável, testada e pronta nos prazos do cronograma técnico para a gravação de cenas.",
    "Complexidade": "Lida com situações operacionais mais complexas, mudanças repentinas de layout e possui noções intermediárias de patches e universos.",
}
_tecnico_luz = {
    "Autonomia": "Muito alta; toma decisões técnicas de alto impacto e define arquiteturas integradas de luz com total independência.",
    "Criticidade": "É a referência de segurança e prevenção; diagnostica falhas sistêmicas de rede de dados e estabiliza operações críticas.",
    "Comportamento": "Referência técnica da área, mantém controle e racionalidade sob pressão, corrige sem centralizar e forma novos técnicos.",
    "Entrega": "Responde pela qualidade final das cenas e iluminação ideal para fotos, vídeos e streamings, criando padrões replicáveis na Firma.",
    "Complexidade": "Muito alta; resolve problemas complexos cruzando variáveis de carga de energia, dados de rede (ArtNet/DMX) e consoles de grande porte (GrandMA).",
}
AREAS["ILUMINACAO"] = {}
for _n in ("I", "II", "III"):
    AREAS["ILUMINACAO"][f"Auxiliar de Iluminação {_n}"] = dict(_auxiliar_luz)
for _n in ("I", "II", "III"):
    AREAS["ILUMINACAO"][f"Assistente de Iluminação {_n}"] = dict(_assistente_luz)
for _n in ("I", "II", "III"):
    AREAS["ILUMINACAO"][f"Técnico de Iluminação {_n}"] = dict(_tecnico_luz)

# ---- ÁREA: HOUSE / TECNOLOGIA -------------------------------------------
_auxiliar_house = {
    "Autonomia": "Conduz atividades conhecidas com pouca supervisão, organiza suas estações e antecipa necessidades simples de periféricos.",
    "Complexidade": "Lida com variações da rotina de informática, redes locais simples e realiza troubleshooting básico de sinal.",
    "Criticidade": "Atua preventivamente, realiza testes de vídeo prévios e entende o impacto de falhas de formato/resolução sobre o evento.",
    "Comportamento": "É referência de postura, organização, cuidado com notebooks caros, comunicação clara e disposição para ensinar.",
    "Entrega": "Garante que sua etapa esteja pronta, testada, limpa e disponível para a continuidade das apresentações corporativas.",
}
_assistente_house = {
    "Autonomia": "Conduz etapas importantes da preparação e montagem com elevada autonomia dentro de todo o escopo operacional da área.",
    "Criticidade": "Atua diretamente na prevenção de travamentos de slides e falhas na tela, resguardando a fita técnica do cliente.",
    "Comportamento": "Postura altamente profissional, discrição executiva na House (sem dispersão com celular) e cordialidade extrema com palestrantes.",
    "Entrega": "Garante notebooks de conteúdos, monitores de apoio de palco e pontos de sinal perfeitamente validados e estáveis no prazo.",
    "Complexidade": "Realiza diagnósticos rápidos e estruturados em falhas conhecidas, separando erros operacionais de decisões do Técnico. Domina redes básicas.",
}
_tecnico_house = {
    "Autonomia": "Muito alta; projeta soluções digitais integradas do zero e toma decisões técnicas críticas sem demandar scripts de suporte.",
    "Criticidade": "Protege a continuidade do ar de transmissões e playbacks críticos, estruturando redundâncias ativas e contingências.",
    "Comportamento": "Referência técnica sênior, mantém calma inabalável, distribui frentes por senioridade e atua na melhoria contínua da área.",
    "Entrega": "Responde pela engenharia e estabilidade dos servidores de mídia (Resolume/Watchout) e redes IP, criando checklists oficiais.",
    "Complexidade": "Avançado; resolve ocorrências avançadas cruzando variáveis de hardware, caminhos de cabos físicos, tráfego de dados e panes de software.",
}
AREAS["HOUSE_TECNOLOGIA"] = {}
for _n in ("I", "II", "III"):
    AREAS["HOUSE_TECNOLOGIA"][f"Auxiliar de House/Tecnologia {_n}"] = dict(_auxiliar_house)
for _n in ("I", "II", "III"):
    AREAS["HOUSE_TECNOLOGIA"][f"Assistente de House/Tecnologia {_n}"] = dict(_assistente_house)
for _n in ("I", "II", "III"):
    AREAS["HOUSE_TECNOLOGIA"][f"Técnico de House/Tecnologia {_n}"] = dict(_tecnico_house)

# ---- ÁREA: ELÉTRICA -----------------------------------------------------
AREAS["ELETRICA"] = {
    "Técnico II - Elétrica": {
        "Autonomia": "Alta. Conduz a operação elétrica com pouca supervisão em diferentes portes de projetos.",
        "Domínio Técnico": "Consolidado. Compreende infraestrutura, execução, testes elétricos avançados e diagnóstico por causa-efeito.",
        "Complexidade": "Atua em eventos de pequeno, médio e grande porte, gerenciando demandas elétricas simultâneas de Som, Luz e LED.",
        "Criticidade": "Identifica riscos de sobrecarga e oscilação e conduz ocorrências relevantes dentro do escopo com foco em proteger vidas e equipamentos.",
        "Segurança": "É referência de segurança durante a execução; recusa puxadinhos ou falta de aterramento mecânico.",
        "Entrega": "Responde pela qualidade da operação elétrica do início ao encerramento do desmonte.",
    },
    "Técnico III - Elétrica": {
        "Autonomia": "Muito alta. Define estratégias de distribuição complexas e toma decisões técnicas elétricas críticas de alto impacto.",
        "Domínio Técnico": "Aprofundado. Constrói soluções de engenharia elétrica novas e orienta tecnicamente toda a equipe.",
        "Complexidade": "Atua como referência máxima em operações de grande porte, lidando com paralelismo de geradores e restrições severas locais.",
        "Criticidade": "Toma decisões em cenários críticos, prioriza riscos e gerencia sistemas complexos de contingência de energia.",
        "Comportamento": "Líder estratégico, mantém equilíbrio emocional em panes, transmite segurança, ensina a equipe e cria a memória técnica da Firma.",
        "Melhoria Contínua": "Cria padrões corporativos, checklists de segurança elétrica oficiais, reduz reincidências e fortalece os processos da Firma.",
    },
}

# ---- ÁREA: ESTRUTURA ----------------------------------------------------
AREAS["ESTRUTURA"] = {
    "Auxiliar de Estrutura I": {
        "Autonomia": "Inicial; executa atividades simples de carregamento, descarga e movimentação com orientação e para antes de improvisar.",
        "Domínio Técnico": "Em construção; aprende materiais, ferramentas mecânicas e a sequência lógica das montagens estruturais.",
        "Criticidade": "Começa a compreender impactos e riscos; avisa sobre peças espanadas ou travamentos com folgas a tempo de corrigir.",
        "Entrega": "Executa corretamente o que foi orientado, mantendo o ambiente limpo e as ferramentas guardadas nas caixas certas.",
        "Comportamento": "Disponível, responsável, organizado, respeita as normas de segurança (EPI/NR-35) e é altamente colaborativo.",
    },
    "Auxiliar de Estrutura II": {
        "Autonomia": "Executa atividades conhecidas de montagem e desmonte de box truss e praticáveis com independência e menor supervisão direta.",
        "Criticidade": "Compreende impactos operacionais, identifica problemas simples e antecipa materiais que serão usados na sequência do grid.",
        "Entrega": "Mantém a qualidade, a conservação patrimonial das peças (sem riscar hotéis) e o ritmo/velocidade exigidos pela produção.",
        "Comportamento": "Iniciativa prática, responsabilidade, ajuda novos profissionais e colabora respeitando o espaço das outras áreas técnicas.",
    },
    "Técnico de Estrutura I": {
        "Autonomia": "Alta para atividades que domina; interpreta projetos de montagem estrutural e organiza seus próprios recursos técnicos.",
        "Criticidade": "Identifica erros de execução e condições inseguras de montagem de forma imediata, paralisando a fita se houver riscos de acidentes.",
        "Comportamento": "Responsável, altamente focado em precisão, comunica erros de forma respeitosa e apoia o desenvolvimento dos Auxiliares.",
        "Entrega": "Responde pela qualidade direta das frentes sob sua responsabilidade, eliminando retrabalhos causados por desorganização.",
        "Complexidade": "Consolidado nas principais rotinas de montagem e desmontagem mecânica, adaptando-se a variações conhecidas do local.",
    },
    "Técnico de Estrutura II": {
        "Autonomia": "Alta. Conduz etapas relevantes da operação estrutural global do evento com pouca supervisão e alta capacidade de decisão.",
        "Criticidade": "Identifica riscos, prioriza a segurança das estruturas aéreas e não aceita atalhos arriscados por pressões de prazos.",
        "Comportamento": "Líder operacional, distribui frentes conforme a capacidade do time, mantém o equilíbrio e é referência de organização em crises.",
        "Entrega": "Responde pela qualidade da estrutura do início ao desmonte, garantindo que o palco permita a ancoragem segura de LED, Som e Luz.",
        "Complexidade": "Gerencia frentes simultâneas com prazos reduzidos, interpreta plantas complexas e elimina conflitos de layout com outras áreas.",
    },
}

# Rótulos amigáveis para exibição em selects
NOMES_AREAS = {
    "LED": "LED",
    "SOM": "Som",
    "ILUMINACAO": "Iluminação",
    "HOUSE_TECNOLOGIA": "House / Tecnologia",
    "ELETRICA": "Elétrica",
    "ESTRUTURA": "Estrutura",
}


def cargo_e_auxiliar(cargo_label: str) -> bool:
    """Retorna True se o cargo pertencer à trilha 'Auxiliar' (para o
    gabarito de campo, que tem redação diferente por trilha)."""
    return cargo_label.strip().lower().startswith("auxiliar")


def extrair_nivel_numero(cargo_label: str) -> int:
    """Extrai o número romano de nível (I, II, III) do rótulo do cargo e
    devolve como inteiro. Usado para checar interstício de 6 meses."""
    mapa = {"III": 3, "II": 2, "I": 1}
    partes = cargo_label.strip().split()
    for token in reversed(partes):
        token_limpo = token.strip("-")
        if token_limpo in mapa:
            return mapa[token_limpo]
    return 1


# ============================================================
# SEÇÃO 2/6 — PERSISTÊNCIA (db.py) — SQLite local ou Postgres via DATABASE_URL
# ============================================================
# -*- coding: utf-8 -*-


import json
import os
import uuid
from contextlib import contextmanager
from datetime import date, datetime
from typing import Optional

DB_PATH = os.environ.get(
    "FIRMA_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "firma_rh.db"),
)


def _obter_database_url() -> Optional[str]:
    """Procura a connection string do Postgres em variável de ambiente e,
    como alternativa, em st.secrets (caso definida nos Secrets do Streamlit
    Cloud e não propagada automaticamente para o ambiente)."""
    valor = os.environ.get("DATABASE_URL")
    if valor:
        return valor
    try:
        import streamlit as st  # import tardio: db.py continua usável sem Streamlit
        return st.secrets.get("DATABASE_URL")
    except Exception:
        return None


DATABASE_URL = _obter_database_url()
USANDO_POSTGRES = bool(DATABASE_URL)

if USANDO_POSTGRES:
    import psycopg2
    import psycopg2.extras
else:
    import sqlite3


# ---------------------------------------------------------------------------
# Conexão e inicialização do schema (abstrai SQLite vs Postgres)
# ---------------------------------------------------------------------------

class _ConexaoUnificada:
    """Envolve a conexão real para uniformizar a assinatura de .execute()
    entre SQLite (placeholder '?') e Postgres (placeholder '%s'), permitindo
    reaproveitar as mesmas strings SQL em todo o resto do módulo."""

    def __init__(self, conn_real):
        self._conn = conn_real

    def execute(self, sql: str, params=()):
        if USANDO_POSTGRES:
            sql = sql.replace("?", "%s")
            cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cur = self._conn.cursor()
        cur.execute(sql, params)
        return cur

    def executescript(self, sql: str):
        if USANDO_POSTGRES:
            cur = self._conn.cursor()
            cur.execute(sql)
            cur.close()
        else:
            self._conn.executescript(sql)


@contextmanager
def get_conn():
    if USANDO_POSTGRES:
        conn_real = psycopg2.connect(DATABASE_URL)
    else:
        conn_real = sqlite3.connect(DB_PATH)
        conn_real.row_factory = sqlite3.Row
        conn_real.execute("PRAGMA foreign_keys = ON;")

    wrapper = _ConexaoUnificada(conn_real)
    try:
        yield wrapper
        conn_real.commit()
    finally:
        conn_real.close()


def _migrar_papel_produtor(conn):
    """
    Migração idempotente exclusiva do backend SQLite: bancos criados pela v2
    têm a tabela 'usuarios' com CHECK (papel IN ('RH','HEAD','COLABORADOR')),
    o que bloqueia o novo papel 'PRODUTOR'. Detecta esse caso pelo SQL de
    criação salvo no sqlite_master e recria a tabela sem CHECK (validação de
    papel passa a ser só na camada Python, em PAPEIS_VALIDOS),
    preservando todos os dados. Bancos Postgres novos já nascem sem esse
    CHECK, então esta função não faz nada nesse backend.
    """
    if USANDO_POSTGRES:
        return
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='usuarios'"
    ).fetchone()
    if row is None:
        return  # tabela ainda não existe, nada a migrar
    sql_atual = row[0] or ""
    if "PRODUTOR" in sql_atual or "CHECK" not in sql_atual:
        return  # já está no schema novo (sem CHECK) ou já suporta PRODUTOR

    conn.executescript(
        """
        ALTER TABLE usuarios RENAME TO usuarios_old_v2;

        CREATE TABLE usuarios (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            papel TEXT NOT NULL,
            area TEXT,
            colaborador_id TEXT,
            criado_em TEXT NOT NULL
        );

        INSERT INTO usuarios (id, nome, email, senha_hash, papel, area, colaborador_id, criado_em)
        SELECT id, nome, email, senha_hash, papel, area, colaborador_id, criado_em FROM usuarios_old_v2;

        DROP TABLE usuarios_old_v2;
        """
    )


def _migrar_coluna_ativo(conn):
    """Adiciona a coluna 'ativo' em bancos criados antes do recurso de
    arquivamento de colaboradores existir. Idempotente e segura tanto para
    SQLite quanto para Postgres."""
    if USANDO_POSTGRES:
        existe = conn.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'colaboradores' AND column_name = 'ativo'"
        ).fetchone()
    else:
        colunas = conn.execute("PRAGMA table_info(colaboradores)").fetchall()
        existe = any(c["name"] == "ativo" for c in colunas)
    if not existe:
        conn.execute("ALTER TABLE colaboradores ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1")


def _migrar_coluna_documentos(conn):
    """Adiciona a coluna 'documentos' em bancos criados antes desse recurso
    existir. Idempotente e segura tanto para SQLite quanto para Postgres."""
    if USANDO_POSTGRES:
        existe = conn.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'colaboradores' AND column_name = 'documentos'"
        ).fetchone()
    else:
        colunas = conn.execute("PRAGMA table_info(colaboradores)").fetchall()
        existe = any(c["name"] == "documentos" for c in colunas)
    if not existe:
        conn.execute("ALTER TABLE colaboradores ADD COLUMN documentos TEXT NOT NULL DEFAULT '[]'")



def init_db():
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                papel TEXT NOT NULL,
                area TEXT,
                colaborador_id TEXT,
                criado_em TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS colaboradores (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                area TEXT NOT NULL,
                cargo TEXT NOT NULL,
                data_admissao TEXT NOT NULL,
                data_inicio_nivel TEXT NOT NULL,
                gallup_top5 TEXT NOT NULL DEFAULT '[]',
                alertas TEXT NOT NULL DEFAULT '[]',
                ativo INTEGER NOT NULL DEFAULT 1,
                documentos TEXT NOT NULL DEFAULT '[]'
            );

            CREATE TABLE IF NOT EXISTS avaliacoes_campo (
                id TEXT PRIMARY KEY,
                colaborador_id TEXT NOT NULL REFERENCES colaboradores(id),
                projeto TEXT NOT NULL,
                data_evento TEXT NOT NULL,
                data_lancamento TEXT NOT NULL,
                itens TEXT NOT NULL,
                comentarios TEXT NOT NULL,
                textos TEXT NOT NULL,
                nivel_impacto TEXT NOT NULL,
                media REAL NOT NULL,
                lancado_por TEXT
            );

            CREATE TABLE IF NOT EXISTS avaliacoes_mensais (
                id TEXT PRIMARY KEY,
                colaborador_id TEXT NOT NULL REFERENCES colaboradores(id),
                periodo TEXT NOT NULL,
                data_lancamento TEXT NOT NULL,
                notas_parte_a TEXT NOT NULL,
                comentarios_parte_a TEXT NOT NULL,
                criterios_parte_a TEXT NOT NULL,
                notas_parte_b TEXT NOT NULL,
                comentarios_parte_b TEXT NOT NULL,
                criterios_parte_b TEXT NOT NULL,
                media_parte_a REAL NOT NULL,
                media_parte_b REAL NOT NULL,
                nota_final_mensal REAL NOT NULL,
                lancado_por TEXT,
                UNIQUE(colaborador_id, periodo)
            );
            """
        )
        _migrar_papel_produtor(conn)
        _migrar_coluna_ativo(conn)
        _migrar_coluna_documentos(conn)


# ---------------------------------------------------------------------------
# Helpers de (de)serialização
# ---------------------------------------------------------------------------

def _dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _loads(txt: str):
    return json.loads(txt) if txt else None


def _iso(d) -> str:
    if isinstance(d, (date, datetime)):
        return d.isoformat()
    return str(d)


def _from_iso_date(txt: str) -> date:
    return date.fromisoformat(txt) if hasattr(date, "fromisoformat") else txt  # pragma: no cover


# ---------------------------------------------------------------------------
# CRUD — colaboradores
# ---------------------------------------------------------------------------

LINK_GALLUP_PADRAO = "https://www.gallup.com/cliftonstrengths/en/252137/home.aspx"


def obter_configuracao(chave: str, padrao: Optional[str] = None) -> Optional[str]:
    with get_conn() as conn:
        row = conn.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,)).fetchone()
    return row["valor"] if row else padrao


def definir_configuracao(chave: str, valor: str):
    with get_conn() as conn:
        if USANDO_POSTGRES:
            conn.execute(
                """INSERT INTO configuracoes (chave, valor) VALUES (?, ?)
                   ON CONFLICT (chave) DO UPDATE SET valor = excluded.valor""",
                (chave, valor),
            )
        else:
            conn.execute(
                """INSERT INTO configuracoes (chave, valor) VALUES (?, ?)
                   ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor""",
                (chave, valor),
            )


def criar_colaborador(nome, area, cargo, data_admissao, data_inicio_nivel, gallup_top5=None) -> str:
    novo_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO colaboradores
               (id, nome, area, cargo, data_admissao, data_inicio_nivel, gallup_top5, alertas, ativo)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (
                novo_id, nome, area, cargo,
                _iso(data_admissao), _iso(data_inicio_nivel),
                _dumps(gallup_top5 or []), _dumps([]),
            ),
        )
    return novo_id


def listar_colaboradores(
    area: Optional[str] = None,
    apenas_id: Optional[str] = None,
    incluir_inativos: bool = False,
) -> list[dict]:
    with get_conn() as conn:
        if apenas_id:
            rows = conn.execute("SELECT * FROM colaboradores WHERE id = ?", (apenas_id,)).fetchall()
        elif area:
            if incluir_inativos:
                rows = conn.execute("SELECT * FROM colaboradores WHERE area = ? ORDER BY nome", (area,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM colaboradores WHERE area = ? AND ativo = 1 ORDER BY nome", (area,)).fetchall()
        else:
            if incluir_inativos:
                rows = conn.execute("SELECT * FROM colaboradores ORDER BY nome").fetchall()
            else:
                rows = conn.execute("SELECT * FROM colaboradores WHERE ativo = 1 ORDER BY nome").fetchall()
    return [_row_para_colaborador(r) for r in rows]


def listar_colaboradores_arquivados() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM colaboradores WHERE ativo = 0 ORDER BY nome").fetchall()
    return [_row_para_colaborador(r) for r in rows]


def arquivar_colaborador(colaborador_id: str):
    with get_conn() as conn:
        conn.execute("UPDATE colaboradores SET ativo = 0 WHERE id = ?", (colaborador_id,))


def reativar_colaborador(colaborador_id: str):
    with get_conn() as conn:
        conn.execute("UPDATE colaboradores SET ativo = 1 WHERE id = ?", (colaborador_id,))


def obter_colaborador(colaborador_id: str) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM colaboradores WHERE id = ?", (colaborador_id,)).fetchone()
    return _row_para_colaborador(row) if row else None


def atualizar_dados_basicos_colaborador(colaborador_id: str, nome: str, area: str, cargo: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE colaboradores SET nome = ?, area = ?, cargo = ? WHERE id = ?",
            (nome, area, cargo, colaborador_id),
        )


def atualizar_gallup(colaborador_id: str, gallup_top5: list):
    with get_conn() as conn:
        conn.execute(
            "UPDATE colaboradores SET gallup_top5 = ? WHERE id = ?",
            (_dumps(gallup_top5), colaborador_id),
        )


def atualizar_documentos(colaborador_id: str, documentos: list):
    """documentos: lista de dicts {'nome': str, 'link': str (opcional)}."""
    with get_conn() as conn:
        conn.execute(
            "UPDATE colaboradores SET documentos = ? WHERE id = ?",
            (_dumps(documentos), colaborador_id),
        )


def adicionar_alerta(colaborador_id: str, mensagem: str):
    with get_conn() as conn:
        row = conn.execute("SELECT alertas FROM colaboradores WHERE id = ?", (colaborador_id,)).fetchone()
        alertas = _loads(row["alertas"]) if row else []
        alertas.append(mensagem)
        conn.execute("UPDATE colaboradores SET alertas = ? WHERE id = ?", (_dumps(alertas), colaborador_id))


def _row_para_colaborador(row) -> dict:
    return {
        "id": row["id"],
        "nome": row["nome"],
        "area": row["area"],
        "cargo": row["cargo"],
        "data_admissao": date.fromisoformat(row["data_admissao"]),
        "data_inicio_nivel": date.fromisoformat(row["data_inicio_nivel"]),
        "gallup_top5": _loads(row["gallup_top5"]) or [],
        "alertas": _loads(row["alertas"]) or [],
        "ativo": bool(row["ativo"]) if row["ativo"] is not None else True,
        "documentos": _loads(row["documentos"]) if "documentos" in row.keys() and row["documentos"] is not None else [],
    }


# ---------------------------------------------------------------------------
# CRUD — avaliações pós-evento (Camada 2)
# ---------------------------------------------------------------------------

def criar_avaliacao_campo(colaborador_id, projeto, data_evento, itens, comentarios, textos,
                           nivel_impacto, media, lancado_por=None) -> str:
    novo_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO avaliacoes_campo
               (id, colaborador_id, projeto, data_evento, data_lancamento, itens,
                comentarios, textos, nivel_impacto, media, lancado_por)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                novo_id, colaborador_id, projeto, _iso(data_evento), _iso(datetime.now()),
                _dumps(itens), _dumps(comentarios), _dumps(textos), nivel_impacto, media, lancado_por,
            ),
        )
    return novo_id


def listar_avaliacoes_campo(colaborador_id: Optional[str] = None, periodo: Optional[str] = None) -> list[dict]:
    with get_conn() as conn:
        if colaborador_id:
            rows = conn.execute(
                "SELECT * FROM avaliacoes_campo WHERE colaborador_id = ? ORDER BY data_evento DESC",
                (colaborador_id,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM avaliacoes_campo ORDER BY data_evento DESC").fetchall()
    resultado = [_row_para_avaliacao_campo(r) for r in rows]
    if periodo:
        resultado = [a for a in resultado if a["data_evento"].strftime("%Y-%m") == periodo]
    return resultado


def _row_para_avaliacao_campo(row) -> dict:
    return {
        "id": row["id"],
        "colaborador_id": row["colaborador_id"],
        "projeto": row["projeto"],
        "data_evento": date.fromisoformat(row["data_evento"]),
        "data_lancamento": row["data_lancamento"],
        "itens": _loads(row["itens"]),
        "comentarios": _loads(row["comentarios"]),
        "textos": _loads(row["textos"]),
        "nivel_impacto": row["nivel_impacto"],
        "media": row["media"],
        "lancado_por": row["lancado_por"],
    }


# ---------------------------------------------------------------------------
# CRUD — avaliações mensais (Camada 3)
# ---------------------------------------------------------------------------

def salvar_avaliacao_mensal(colaborador_id, periodo, notas_parte_a, comentarios_parte_a,
                             criterios_parte_a, notas_parte_b, comentarios_parte_b,
                             criterios_parte_b, media_parte_a, media_parte_b,
                             nota_final_mensal, lancado_por=None) -> str:
    """Cria ou substitui (upsert) a ficha mensal de um colaborador/período."""
    novo_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO avaliacoes_mensais
               (id, colaborador_id, periodo, data_lancamento, notas_parte_a, comentarios_parte_a,
                criterios_parte_a, notas_parte_b, comentarios_parte_b, criterios_parte_b,
                media_parte_a, media_parte_b, nota_final_mensal, lancado_por)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(colaborador_id, periodo) DO UPDATE SET
                 data_lancamento=excluded.data_lancamento,
                 notas_parte_a=excluded.notas_parte_a,
                 comentarios_parte_a=excluded.comentarios_parte_a,
                 criterios_parte_a=excluded.criterios_parte_a,
                 notas_parte_b=excluded.notas_parte_b,
                 comentarios_parte_b=excluded.comentarios_parte_b,
                 criterios_parte_b=excluded.criterios_parte_b,
                 media_parte_a=excluded.media_parte_a,
                 media_parte_b=excluded.media_parte_b,
                 nota_final_mensal=excluded.nota_final_mensal,
                 lancado_por=excluded.lancado_por
            """,
            (
                novo_id, colaborador_id, periodo, _iso(datetime.now()),
                _dumps(notas_parte_a), _dumps(comentarios_parte_a), _dumps(criterios_parte_a),
                _dumps(notas_parte_b), _dumps(comentarios_parte_b), _dumps(criterios_parte_b),
                media_parte_a, media_parte_b, nota_final_mensal, lancado_por,
            ),
        )
    return novo_id


def listar_avaliacoes_mensais(colaborador_id: Optional[str] = None) -> list[dict]:
    with get_conn() as conn:
        if colaborador_id:
            rows = conn.execute(
                "SELECT * FROM avaliacoes_mensais WHERE colaborador_id = ? ORDER BY periodo DESC",
                (colaborador_id,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM avaliacoes_mensais ORDER BY periodo DESC").fetchall()
    return [_row_para_avaliacao_mensal(r) for r in rows]


def obter_avaliacao_mensal(colaborador_id: str, periodo: str) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM avaliacoes_mensais WHERE colaborador_id = ? AND periodo = ?",
            (colaborador_id, periodo),
        ).fetchone()
    return _row_para_avaliacao_mensal(row) if row else None


def _row_para_avaliacao_mensal(row) -> dict:
    return {
        "id": row["id"],
        "colaborador_id": row["colaborador_id"],
        "periodo": row["periodo"],
        "data_lancamento": row["data_lancamento"],
        "notas_parte_a": _loads(row["notas_parte_a"]),
        "comentarios_parte_a": _loads(row["comentarios_parte_a"]),
        "criterios_parte_a": _loads(row["criterios_parte_a"]),
        "notas_parte_b": _loads(row["notas_parte_b"]),
        "comentarios_parte_b": _loads(row["comentarios_parte_b"]),
        "criterios_parte_b": _loads(row["criterios_parte_b"]),
        "media_parte_a": row["media_parte_a"],
        "media_parte_b": row["media_parte_b"],
        "nota_final_mensal": row["nota_final_mensal"],
        "lancado_por": row["lancado_por"],
    }


# ============================================================
# SEÇÃO 3/6 — AUTENTICAÇÃO E PAPÉIS (auth.py)
# ============================================================
# -*- coding: utf-8 -*-


import os
import uuid
from datetime import datetime
from typing import Optional

import bcrypt


PAPEIS_VALIDOS = ("RH", "HEAD", "PRODUTOR", "COLABORADOR")


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except Exception:
        return False


def criar_usuario(nome: str, email: str, senha: str, papel: str,
                   area: Optional[str] = None, colaborador_id: Optional[str] = None) -> str:
    if papel not in PAPEIS_VALIDOS:
        raise ValueError(f"Papel inválido: {papel}")
    novo_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO usuarios (id, nome, email, senha_hash, papel, area, colaborador_id, criado_em)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                novo_id, nome.strip(), email.strip().lower(), hash_senha(senha),
                papel, area, colaborador_id, datetime.now().isoformat(),
            ),
        )
    return novo_id


def autenticar(email: str, senha: str) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email.strip().lower(),)
        ).fetchone()
    if not row:
        return None
    if not verificar_senha(senha, row["senha_hash"]):
        return None
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "papel": row["papel"],
        "area": row["area"],
        "colaborador_id": row["colaborador_id"],
    }


def listar_usuarios() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT id, nome, email, papel, area, colaborador_id, criado_em FROM usuarios ORDER BY criado_em").fetchall()
    return [dict(r) for r in rows]


def excluir_usuario(usuario_id: str):
    with get_conn() as conn:
        conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))


def existe_algum_usuario() -> bool:
    with get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()
    return row["total"] > 0


def seed_admin_padrao():
    """Cria um usuário RH padrão apenas se o banco ainda não tiver nenhum
    usuário. Credenciais padrão devem ser trocadas no primeiro acesso."""
    if existe_algum_usuario():
        return None
    email_padrao = os.environ.get("FIRMA_ADMIN_EMAIL", "admin@firmaproducoes.com")
    senha_padrao = os.environ.get("FIRMA_ADMIN_SENHA", "firma@admin123")
    criar_usuario("Administrador RH", email_padrao, senha_padrao, "RH")
    return {"email": email_padrao, "senha": senha_padrao}


# ============================================================
# SEÇÃO 4/6 — MOTOR DE CÁLCULO (motor_calculo.py)
# ============================================================
# -*- coding: utf-8 -*-


from dataclasses import dataclass, field
from datetime import date
from typing import Optional


# ---------------------------------------------------------------------------
# Utilitários de data
# ---------------------------------------------------------------------------

def meses_entre(data_inicio: date, data_fim: Optional[date] = None) -> int:
    """Quantidade de meses completos entre duas datas."""
    if data_fim is None:
        data_fim = date.today()
    if data_inicio is None:
        return 0
    meses = (data_fim.year - data_inicio.year) * 12 + (data_fim.month - data_inicio.month)
    if data_fim.day < data_inicio.day:
        meses -= 1
    return max(meses, 0)


# ---------------------------------------------------------------------------
# Camada 2 — Avaliação pós-evento (campo)
# ---------------------------------------------------------------------------

def media_avaliacao_campo(itens: dict) -> float:
    """Média simples das notas 1-5 dos 5 itens do gabarito de campo."""
    notas = [v for v in itens.values() if v is not None]
    if not notas:
        return 0.0
    return round(sum(notas) / len(notas), 2)


# ---------------------------------------------------------------------------
# Camada 3 — Avaliação mensal unificada (Parte A + Parte B)
# ---------------------------------------------------------------------------

def media_parte(notas: dict) -> float:
    """Média simples de um dicionário {critério: nota}."""
    valores = [v for v in notas.values() if v is not None]
    if not valores:
        return 0.0
    return round(sum(valores) / len(valores), 2)


def nota_mensal_unificada(notas_parte_a: dict, notas_parte_b: dict) -> dict:
    """Aplica o peso 50% Desempenho (Parte A) / 50% Cultura (Parte B) e
    devolve a nota final da Ficha Mensal Unificada."""
    media_a = media_parte(notas_parte_a)
    media_b = media_parte(notas_parte_b)
    nota_final = round((media_a * 0.5) + (media_b * 0.5), 2)
    return {
        "media_parte_a": media_a,
        "media_parte_b": media_b,
        "nota_final_mensal": nota_final,
    }


# ---------------------------------------------------------------------------
# Gatilho financeiro dos 70% (Nota Consolidada do Período)
# ---------------------------------------------------------------------------

def nota_consolidada_periodo(nota_mensal: Optional[float], notas_campo: list[float]) -> dict:
    """
    'O sistema junta os resultados da Ficha Mensal Unificada e das Notas de
    Campo daquele período.' Sem peso diferenciado explícito na governança,
    o sistema pondera igualmente a Ficha Mensal e a média das avaliações de
    campo (pós-evento) lançadas no mesmo período de apuração.

    Retorna a nota consolidada final e o status ELEGÍVEL / NÃO ELEGÍVEL.
    """
    componentes = []
    if nota_mensal is not None:
        componentes.append(nota_mensal)
    if notas_campo:
        componentes.append(round(sum(notas_campo) / len(notas_campo), 2))

    if not componentes:
        nota_final = 0.0
    else:
        nota_final = round(sum(componentes) / len(componentes), 2)

    elegivel = nota_final >= NOTA_MINIMA_ELEGIVEL
    return {
        "nota_final": nota_final,
        "percentual_equivalente": round((nota_final / 5.0) * 100, 1),
        "status": "ELEGÍVEL" if elegivel else "NÃO ELEGÍVEL",
        "elegivel": elegivel,
        "dispara_pdi": not elegivel,
    }


# ---------------------------------------------------------------------------
# Elegibilidade a promoção (tempo de empresa + interstício + janela)
# ---------------------------------------------------------------------------

@dataclass
class ElegibilidadePromocao:
    tempo_empresa_meses: int
    tempo_nivel_meses: int
    elegivel_tempo_empresa: bool
    elegivel_interstício: bool
    dentro_da_janela: bool
    proxima_janela: str
    elegivel_geral: bool
    motivos_bloqueio: list = field(default_factory=list)


def checar_elegibilidade_promocao(
    data_admissao: date,
    data_inicio_nivel: date,
    data_referencia: Optional[date] = None,
) -> ElegibilidadePromocao:
    if data_referencia is None:
        data_referencia = date.today()

    t_empresa = meses_entre(data_admissao, data_referencia)
    t_nivel = meses_entre(data_inicio_nivel, data_referencia)

    ok_empresa = t_empresa >= TEMPO_MINIMO_EMPRESA_MESES
    ok_nivel = t_nivel >= TEMPO_MINIMO_NIVEL_MESES

    mes_atual = data_referencia.month
    dentro_da_janela = mes_atual in MESES_JANELA_PROMOCAO

    # Calcula a próxima janela (Junho ou Dezembro) para exibição amigável.
    proximos_meses = sorted(MESES_JANELA_PROMOCAO)
    prox = next((m for m in proximos_meses if m >= mes_atual), None)
    if prox is None:
        prox_ano = data_referencia.year + 1
        prox_mes = proximos_meses[0]
    else:
        prox_ano = data_referencia.year
        prox_mes = prox
    nomes_mes = {6: "Junho", 12: "Dezembro"}
    proxima_janela = f"{nomes_mes.get(prox_mes, prox_mes)}/{prox_ano}"

    motivos = []
    if not ok_empresa:
        faltam = TEMPO_MINIMO_EMPRESA_MESES - t_empresa
        motivos.append(
            f"Faltam {faltam} mês(es) para completar 1 ano de empresa (mínimo "
            f"exigido para participar de qualquer ciclo de promoção)."
        )
    if not ok_nivel:
        faltam = TEMPO_MINIMO_NIVEL_MESES - t_nivel
        motivos.append(
            f"Faltam {faltam} mês(es) de interstício no nível atual (mínimo "
            f"de 6 meses exercendo o nível com consistência)."
        )
    if not dentro_da_janela:
        motivos.append(
            f"Fora da janela formal de movimentação. Próxima janela: {proxima_janela}."
        )

    elegivel_geral = ok_empresa and ok_nivel and dentro_da_janela

    return ElegibilidadePromocao(
        tempo_empresa_meses=t_empresa,
        tempo_nivel_meses=t_nivel,
        elegivel_tempo_empresa=ok_empresa,
        elegivel_interstício=ok_nivel,
        dentro_da_janela=dentro_da_janela,
        proxima_janela=proxima_janela,
        elegivel_geral=elegivel_geral,
        motivos_bloqueio=motivos,
    )


# ---------------------------------------------------------------------------
# Diagnóstico para o PDI: quais critérios tiraram nota 1 ou 2
# ---------------------------------------------------------------------------

def coletar_criterios_baixa_nota(
    notas_parte_a: dict,
    comentarios_parte_a: dict,
    criterios_texto_parte_a: dict,
    notas_parte_b: dict,
    comentarios_parte_b: dict,
    criterios_texto_parte_b: dict,
    itens_campo_lista: list,
) -> list:
    """
    Varre a Ficha Mensal (Parte A + Parte B) e as avaliações de campo do
    período, retornando uma lista de dicionários para cada critério que
    recebeu nota 1 ou 2, no formato exigido pelo gerador de PDI:
        {"pilar": ..., "nota": ..., "criterio_oficial": ..., "fato_gerador": ...}
    """
    achados = []

    for pilar, nota in (notas_parte_a or {}).items():
        if nota is not None and nota <= 2:
            achados.append({
                "origem": "Avaliação Mensal — Desempenho",
                "pilar": pilar,
                "nota": nota,
                "criterio_oficial": criterios_texto_parte_a.get(pilar, ""),
                "fato_gerador": (comentarios_parte_a or {}).get(pilar, "").strip()
                or "Sem comentário registrado pelo gestor no campo da nota.",
            })

    for valor, nota in (notas_parte_b or {}).items():
        if nota is not None and nota <= 2:
            achados.append({
                "origem": "Avaliação Mensal — Cultura",
                "pilar": valor,
                "nota": nota,
                "criterio_oficial": criterios_texto_parte_b.get(valor, ""),
                "fato_gerador": (comentarios_parte_b or {}).get(valor, "").strip()
                or "Sem comentário registrado pelo gestor no campo da nota.",
            })

    for avaliacao_campo in itens_campo_lista or []:
        itens = avaliacao_campo.get("itens", {})
        comentarios = avaliacao_campo.get("comentarios", {})
        textos = avaliacao_campo.get("textos", {})
        projeto = avaliacao_campo.get("projeto", "Projeto não identificado")
        for item_id, nota in itens.items():
            if nota is not None and nota <= 2:
                achados.append({
                    "origem": f"Avaliação Pós-Evento — {projeto}",
                    "pilar": textos.get(item_id, {}).get("titulo", item_id),
                    "nota": nota,
                    "criterio_oficial": textos.get(item_id, {}).get("pergunta", ""),
                    "fato_gerador": (comentarios or {}).get(item_id, "").strip()
                    or "Sem comentário registrado pelo gestor no campo da nota.",
                })

    return achados


# ============================================================
# SEÇÃO 5/6 — GERADOR DE PDI (gerador_pdi.py)
# ============================================================
# -*- coding: utf-8 -*-


import base64
import io
import os
from datetime import date
from typing import Optional

import requests

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

# Papel timbrado oficial da Firma Produções, embutido em base64 para manter
# o sistema como um único arquivo autocontido (sem depender de um asset
# externo que poderia se perder). Usado como fundo de todas as páginas do
# PDI gerado em PDF.
PAPEL_TIMBRADO_B64 = (
    "/9j/4AAQSkZJRgABAQEAyADIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAkjBnYDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3iiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFOVsdabRQBNnIzS1CrYNSg5FAhaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFKrYNJRQBMDkUtQqxB9qlByM0CFooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUqtg+1JRQBMDmlqJGwcHpUooEFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACpEbsajozg5oAnopqtkU6gQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACjNJS0AFFJRQAtFJS0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAqttNS5qGno2eKBElFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAB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isbm52I27yYmfHJ64FAHz9X1b8Cf+SZWn/XaX/0M18z/APCM6/8A9ATUv/AV/wDCvp74J2dzY/Dm1hu7eW3lEsuUlQqw+c9jQB6LRRRQMKKKKACuW+JH/JNfEX/XjJ/KuprmfiFDLcfDzX4YInlleykVERSzMcdAB1oA+La9l/Z1/wCRq1L/AK9l/ma8v/4RnX/+gJqX/gK/+FeufALSdR07xPqL3un3VsrW4AaaFkBOT6igR9D1i+K/ENt4W8OXmr3QZkgTKqoyWbsK2q8g+OupX0+ixeHtP029uXnZZpJIIGdVAPAJA60DPnTWdVudc1i61K7YtNcSF2yc4yeAPYdKveDtBbxL4r0/SRkLPKA5AJwvc1B/wjOvf9ATUv8AwFf/AAr3P4CeDrvTFvtc1C3eF5R5MUUsZV1weTg+tAj0KP4YeCkjVP8AhHLBioAy0Qyfenf8Ky8Ff9C1p/8A36FdXS0DOT/4Vl4K/wCha0//AL9CvPvi78MNOj8KrqHhvSLe2ls2Mk6wIAzpj9cda9tpkkayxtG6hlYYIPcUAfBVet/ATxImleKptMuLkRwXyYVW6GQdPoe1cp4v8IavaeMNYhtdGvmtheS+SY7dmXYWO3BAx0xWTb+H/EVrcxTx6LqavGwYEWsgPH4UCPt0UtUNDvpNT0KwvpoWhluLdJZImGCjFQSpHsav0DCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACpl+7UNSIeCKAH0UUUCCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRiiigBvlp/dX8qAig5CgfhTqKACiiigAooooAKQqCMEZFLRQA3y0/ur+VKFA6AD6UtFABR1oooAb5af3V/KgIoOQo/KnUUAFFFFABTSit1UH6inUUAN8tP7q/lShFXooH0FLRQAUhVW6gH6ilooAb5af3V/KlAAHAx9KWkoAWkryXwfaXfijxF4rS+1vVlSz1KWKFILooqru6YrW8XWWteD/AA7Pq+ia7cMlqPMniviZt698E9DQB6KKKradfQ6nptrf25JguYUmjJGCVYAj9DVmgANJjIwRXNfEK7uLDwFrN1aTPDPFbMySIcFTjqKy9C8JLqHh7TbyfXdcM1xaxSvi9YDcygn+dAHb7E/ur+VKEUHIAH0Fea69qeq+A/EegwxX017pGoy/Z5I7k75Ff1DHtzXplABTSqk8qD9RTq5zxx4il8L+F7jUbeDz7nIigj/vO3A+tAHQbEx91frilChRhQAPauD0nwnq2v6LDc+LtSvk1CQEvBZzGKNBngYHfGKp+JLTXfAdlFq+iahPeaVanffWt2/mN5Y6lWPP4UAek0tZ2ha1ZeIdGttU0+USW1wu5WHr3B9CDkVo0AITRXmXxVk1K71Tw1oNjqM1jHqV0YppIjzikvbjx94JmiYBvE2kKoDbI8XKgdTgfeNAHpuxTyVBP0o8tP7i/lWD4d8Z6N4mjC2V0qXgyJbOb5J4mHDBkPIwciugoAQAAYAwKWiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigApydabTk+9QBLRQKKBBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigApKWkoA8b8Cajqtj4n8Zrp2hy6i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P8O/9Ai2/wC+KPfD/Z/P8C9/bOm/8/1v/wB/BVuORJY1dGDIwyCOhFY3/CHeHf8AoEW3/fFbEFvFawRwQII4o1CIi9FA4AqlzdTOp7K3uX+ZJRRRVGYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUASx/dp1Nj+7TqBBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAoopCwVSzEADqT2oAWisiDxX4dublba317S5bh22rEl5GWZvQAHJNa2fagBaKTNLQAUUmaXNABRSZ4ozQAtFJmorq6hsrWS6uH2QxqWdj2FAE1FV7K8g1CygvLaQSQToJI3A6qRkGrFABRTJZUhieWQ4RAWY+gqOzu4b+ygvLZxJBPGskbjoysMg/kaAJ6KTNLQAUUUlAC0VC13bpcrbNPEtwy7liLjcR6gdcVNQAUVVsdRtdShkltJRIkcrwscYw6MVYfgQRVnNAC0VBFeW080sMNxFJLCQJERwWQ9RkDpx61NmgBaKKKACikozQAtFJmjNAC0Umaq6jqVppNjLe30oht4hl3I4AoAt0VHDMlxBHNE26ORQykdwRkGn5oAWikz7UvrQAUUmaM0ALRSZpaACiqNpq9jfX13ZW04kuLRgsyAH5CRkD8jV2gBaKM0maAFopqurZ2sDg4OCDilzQAtFJmloAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCWP7tOpqfdp1AgooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAVXvf8Ajxn/AOubY/KrFRXEZlt5I1IBZSAT7igDzS20nwVB4EgvtSitEcWgeV0I8wNjtjnOah0DxH4sfS9M0SKEPq11G1wk12OIrUMQhf1YgdOtd/omiRabo1nZzRQvNDEqO6rwSBz1rP1vQNTl8R2OuaPcQRzwxfZ5opgdssWScDA4OSaBlG01HxRpninTtL1m4s7u2vFkKXEEexsqASCvbrVHw5r3ifxHf6vKtxa29jpmpTWpjaHLTIjHGD24rdl0rWL/AMVabqlybaG0s0fESsTIWcAHPGMcetN8JeGrnQIdajuJYn+36hPdIY8/KrsSAc9+aBGXb3Pj3VLc6payaZBbSfvLa0dSWkjPK7mx8pxW54O1e81vw+LzUI0iuhdXELxp0Xy5nQD8lqpptl4s03R5LAyabO8e5LWcswAT+EOMdQMDjPSrvg/Rr3QfDy2WoXEVxdm4nmkliBCsZJWfoen3qAK+rQeKX1vGm6hYQ2hGUSaMlhwM5OPXNUb7V/EWo+IZtD0P7PA1jGn2y9nTcodlDAKvfgg/jXS3ovEuIJrSFJQu5ZFZtpx2IrFOi6xYeK7rWdPlt5La+RDdWshIbeqhQVPToBQBUtPFV9pCata+JVja5023F159uvyzxEkAgdjkEY9qxtYPjm88J3upyXOnR209u0n2Bo/nSMjIBf8AvYI/Gt6Xwldavc63caxPGDqFsLSKODP7qIc8k9Tkk0l3pfii48ITaGDYfajbmAXZY7CMYB24znHXtmgDD0jXdUj8NeFfD+gwxNqM+lQ3DzTfcijC4z7kkHitez1DxRpninTtK1mezura8WQpPBHsYlRkgjt17VFb+D9X0weH7rTru2+2afYx2V0kmdk0ajnaccHJNakuk6vqHivTdUufssNnZI+2JWJkLOMHPGMcetAGzq3/ACCLz/ri38q878ODx9H4K0e8tJtL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KKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiigdaAJl6UtIKWgQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKMUUUAJS0UUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBDcQC4j2F5EwQcxttPHvVfStKttHsjaWgcRmR5TvbcSzsWY5+pNXqKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAClUZakpydaAJBS0CigQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAp8Y6mmVKgwtADqKKKBBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAdamHSo0HzVLQIKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUAZIFAEiDAzT6QDAxS0CCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFOQZOabUyjAxQAtFFFAgooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFHtQA5Bk5qWmquBTqBBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACnIOc00DJqYDFAC0UUUCCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUU5Vyc9qAHIuBmn0UUCCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUAZOKAFUbjipQMcUiqAKdQIKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRR1OKACpVXAz3pFXbT6BBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKUAsaAExmpVXA96FUAU6gQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACjNHU4p6p60AIqk1IBilooEFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiigKT0oAKUIT9KeEAp4oEIAAKWiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRR1oAKAM9KcqZ61IFA6UAMCY61JRRQIKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFKFJPSpFQD60ARhC1SKoAp1FAgooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUdacEz1oAaMk4FSCP1pwGKWgQCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRShSelACUqoTUiqAPenUCGhQKdRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoooxmgAoAyeKeE9aeABQIaIxjmngYFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAopQpJ9qkCAUAMVSetPCAdKdiigQYooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUU8R+tADBk9BUgT1pwGKWgQAYooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUqqTQAlOCE9elPVAPenUCECgdKWiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRR3oAKApPSnhPWngYFADVjx1pwGKWigQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKUKT2qQKBQAwISfapAoHSjFLQIMUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKBz2p4j9aAGAEmpAmOtOAxS0CExS0UUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKVVLGgBKcEJ608IBTqBDQoHSnUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKMEnigAoCkmnqnrTwAKBDVQDrTwKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRShSfpUgUCgQwITUgAFLRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKOvFPEfrQAwAmpAg704DFLQIMUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBBRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKUKTQAnWnBM9eKeqhRTqBDQAOlOoooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUAZNABSqM04R+tPxigQ0IB15p9FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAo69KUISakCgUCGKhzzUgUClxRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKM0delSKnrQIYAT0qQIBTsUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiilCZPPFACU4JnrTwoFOoEIAB0paKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFAyelABSqpPSnqnrT8UCGKgFPoooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFHWnBCTTwoFADQnrTwAOlLRQIKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFKAT0p6pjrQAwKTUioBTsUUCCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRTghPWgBuM09Y+5pygDpTqBCAADiloooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUAE9KAClCk05UxyakoENCgU6iigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUdelOCE9akCgdKAGKnrTwAKWigQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAQUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooozQAUUAZ6VIqY60AMCk09UAp9FAgooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUU5UJ60ANAzwKesfrTgoFOoEIABS0UUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKACaAClClvpTwgHWnYoARVAp1FFAgooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUDk05UJ61IFA6UAMEfPNPxS0UCCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAgooooGFFFFABRRRQAUUUUAFFFFABRShSelPVAOvNADFUtUgUCnUUCCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCCiiigYUUUUAFFFFABRR16U5UPU0ANAz0p6x+tPAA6UtAhAKWiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAIKKKKBhRRSgE0AJSqpb2p6oB1p9AhoUCnUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRUMsxRsAUATUVW+0t6Cj7S3oKALNFVvtLego+0t6CgCzRVb7S3oKPtLegoAs0VW+0t6Cj7S3oKALNFVvtLego+0t6CgCzRVb7S3oKPtLegoAs0VW+0t6Cj7S3oKALNFVvtLego+0t6CgCzRVb7S3oKPtLegoAs0VW+0t6CnRTF3wRQBPRRRQAUUUUAFFFFABRRSMwUcnFAC0VC1wo6c037T6rQBYoqNZkbvT6AFooooAKKKKACiiigAooooAKKKhllMbADnigCaiqv2lvQUv2lvQUAWaKrfaW9BR9pb0FAFmiq32lvQUfaW9BQBZoqt9pb0FH2lvQUAWaKrfaW9BR9pb0FAFmiq32lvQUfaW9BQBZoqt9pb0FKLn1FAFiiohOh708MD0NADqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAzRmqcjMJG5PWm7m/vGgC9RmqO5v7xpQ7KQdxoAu0UyNw44P4U+gAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooqCWUAYU80AT0VR3N/eNG5v7xoAu0tUdzepqxbklTk96AJqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKSlqtO53BRxQBZpKpbm/vGk3N6mgC/RVeCTPymrFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBX7Uveq+l31rrGmW+o2M3m2lygkik2ldynocHBH41eCgUDGBB3p+KWigQUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAGqtx/rPwq0aqz/wCs/CgCKiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACpIP9b+FR1JB/rR9KALdFFFABRRRQAUUUUANZgoyaqO7Ock1JcHLAVDQAUUUUAFTQynO0moaKAL9FRxNujFSUAFFFFABRRRQAUUUUAFVrn74+lWarXP3x9KAIaKKKACiiigAooooAKKKKACiiigAooooAKMUUUAFKCVOQcUlFAEy3DA/N0qdWDDINUqAxVuDQBfoqKOUOcY5qWgAooooAKKKKACiiigAooooAKKKKACiiigClJ/rG+tNp0n+sb602gAooooAVWKHI61bjfeoPeqdKrFTkGgC9RUaSB1yOtSUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABSUtQTS4yo60ALLKVOFNVqKKACiiigAqzbfdb61Wqzbfdb60ATUUUUAFFFFABRRRQA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+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUABqrP/AKz8KtGqs/8ArPwoAiooooAKKKKACprf75+lQ1Nb/fNAFmiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigCnN/rTTKfN/rTTKACiiigAooooAs233D9amqG2+4frU1ABRRRQAUUUUAFFFFABVa5++PpVmq1z98fSgCGiiigAooooAKlg/wBaPpUVSQf60fSgC3RRRQAUUUUAFFFFABRRSZoAWq1wfmAqSWQIvB5qqSScmgAooooAKKKKAClTlwPekp8QzKtAFyiiigAooooAKKKKACiiigAooooApSf6xvrTadJ/rG+tNoAKKKKACiiigA7Zoqa3GdwNJLFtOQOKAIqKKKACiiigAooooAASpyDVuOQOOKqUqsUOVoAvUVHHIHHvUlABQaQ+tV5pedqnjvQAssucqPxNQUUUAFFFFABRRRQAUUUdTx1oAO9B4JBqzFFt5bk1Xk/1jfU0AJRRRQAUUUUAFWbb7rfWq1Wbb7rfWgCaiiigAooooAKKKKACiiigAooooAKKKKACiikJoAhuGwAvrVcU6Rt0hPbtTaACiiigAooooAKKO+KKACiiigAooooAKswNlMelVqdExWQH1oAu0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHKfDP/AJJn4d/68Y/5V1dcp8M/+SZ+Hf8Arxj/AJV1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAGqs/+s/CrRqrP/rPwoAiooooAKKKKACjOKKKADJ9aXJ9aSigBcn1oyfWkooAXJ9aMn1pKKAFyfWjJ9aSigBcn1pVJ3DnvTaVfvj60AXRS0lLQAUUUUAFFFFABRRRQAUUUUAU5v8AWmmU+b/WmmUAFFFFABRRRQBZtvuH61NUNt9w/WpqACiiigAooooAKKKKACq1z98fSrNVrn74+lAENFFFABRRRQAGnxMFkBNMooAteenvR56e9VaKALXnp70eenvVWigC156e9BnT3qrRQBY+0L6GmPOzDCjFRUUAHU5ooooAKKKKACiiigAqe3X+I1BgngdTV1BtUCgB1FFFABRRRQAUUUUAFFFFABRRRQBSk/1jfWm06T/WN9abQAUUUUAFFFFAE9t1ap8Z4NQW3VqsUAVJYihyOlR1eIB4NVZYipJA4oAjooooAKKKKACiiigAU7WBFW45RIPQ1UoBI6HFAE0s2cqv41DQKKACiiigAooooAKKKAMnA60AHXgVZii2cnrRFFt5PWpqAEqnJ/rG+pq7VKT/AFjfU0ANooooAKKKKACrNt91vrVarNt91vrQBNRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABUU7YTHrUlVZn3OR2FAEdFFFABRRRQAUUUUASwJubd2FJOu18+tWI12oPXHNNmTevuKAKtFFFABRRRQAUUUUAWoX3p9KlqpC4V8Hoat0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHKfDP/kmfh3/rxj/lXV1ynwz/AOSZ+Hf+vGP+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUABqrP8A6z8KtGqs/wDrPwoAiooooAKKKKACiiigAooooAKKKKACiiigAooooAKVfvj60lKv3x9aALtLSUtABRRRQAUUUUAFFFFABRRRQBTm/wBaaZT5v9aaZQAUUUUAFFFFAFm2+4frU1Q233D9amoAKKKKACiiigAooooAKrXP3x9Ks1Wufvj6UAQ0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUhpafFGXIP8NAEluh+8R9KsUgwOBS0AFFFFABRRRQAUUUUAFFFFABRRRQBSk/1jfWm06T/WN9abQAUUUUAFFFFAE9t1arFV7bq1WKACkIBGKWigCpLFsOV6VHV4jPFVpYivzKOKAIqKQUtABRRRQAUUUUAFFFFABRRRQAUUUAZOBQAAEnAqzFFtGSOaWKLYMnrUtABRRRQAVSk/1jfU1dqlJ/rG+poAbRRRQAUUUUAFWbb7rfWq1Wbb7rfWgCaiiigAooooAKKKKACiiigAooooAKKKKAGSPsUnvVPOeTUtwwLgDtUVABRRRQAUUUUAFSQpubnoKjq1ChVOepoAlHSiiigCnKpVz70yrU65TPcVVoAKKKKACiiigAq5G25Ae+Kp1NA+GKnv0oAs0UCigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDlPhn/wAkz8O/9eMf8q6uuU+Gf/JM/Dv/AF4x/wAq6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooADVWf/WfhVo1Vn/1n4UARUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFKv3x9aSlX7w+tAF2lpKWgAooooAKKKKACiiigAooooApy/wCtamU+X/Wt9aZQAUUUUAFFFFAFm2+4frU1Q233D9amoAKKKKACiiigAooooAKrXP3x9Ks1Wufvj6UAQ0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRQAWOAM1OkHd6AI44y554FWkUKMDpSgYFLQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBSk/1jfWm06T/AFjfWm0AFFFFABRRRQBPbdWqxVe26tVigAooooAKQjIxS0UAVJYihyoJFR1eIyKrSxbPmXpQBFRRRQAUUUUAFFFFABRRQAScCgAGTwOasxRBOT1oiiCYJ6mpqACiiigAooooAKpSf6xvqau1Sk/1jfU0ANooooAKKKKACrNt91vrVarNt91vrQBNRRRQAUUUUAFFFFABRRRQAUUUUAFNY4UmnVXnbotAEBOTmiiigAooooAKKKKAHRjMgHoau1Dbr8me9TUAFFFFACMMjHrVJ12ORV6oLheA1AFeiiigAooooAKAcMD6UUUAXlO5QaWoLduCtT0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAcp8M/wDkmfh3/rxj/lXV1ynwz/5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAGqs/+s/CrRqrP/rPwoAiooooAKKKKACnxIHbBplTW/wB8/SgB/wBnT3pfs6+pqWigCL7OvqaPs6+pqWigCL7OvqaPs6+pqWigCL7OvqaPs6+pqWigCH7OvvSiBQc1LRQAUUUUAFFFFABRRRQAUUUUAFFFFAFOX/Wt9aZT5f8AWt9aZQAUUUUAFFFFAFm2+4frU1Q233D9amoAKKKKACiiigAooooAKrXP3x9Ks1Wufvj6UAQ0UUUAFFFFABRRUkH+tFAEeaM1ewKMCgCjmjNXsCmSRh196AKlFBGCQaKACiiigAooooAfE5RvY1bHtVGp4JcfIaALFFIKWgAooooAKKKKACiiigAooooAKKKKACiiigClJ/rG+tNp0n+sb602gAooooAKKKKAJ7bq1WKr23VqsUAFFFFABRRRQAUhGRS0UAVJotnI6Go6vEVVliKfMOhoAjooooAKKKBknAoABknAq1FEEGe9EUWzk8k1LQAYooooAKKKKACiiigAqlJ/rG+pq7VKT/WN9TQA2iiigAooooAKs233W+tVqs233W+tAE1FFFABRRRQAUUUUAFFFFABRRRQAVRYlmJqxO2Fx61WoAKKKKACiiigApUXcwHY0lFAF0AKABTs1QooAv5ozVCigC/mmsAykGqVFAARhiKKKKACiiigAooooAVWKsCKuqcqD61RqzA+V29xQBNRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHKfDP/AJJn4d/68Y/5V1dcp8M/+SZ+Hf8Arxj/AJV1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAGqs/+s/CrRqrP/rPwoAiooooAKKKKACprf75+lQ1Nb/fP0oAs0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAU5f9a31plPl/1rfWmUAFFFFABRRRQBZtvuH61NUNt9w/WpqACiiigAooooAKKKKACq1z98fSrNVrn74+lAENFFFABRRRQAVLB/rR9KiqWD/Wj6UAWqKKKACkpaKAK88f8AEPxqvV881Vlj2HPY0AR0UUUAFFFFABR3oooAtRSbx796lqkjlGyPxq2rBlyKAHUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBSk/wBY31ptOk/1jfWm0AFFFFABRRRQBPbdWqxVe26tVigAooooAKKKKACiiigApMZ4NLRQBVli2ncOlRCrxGarSQkNlRkUARAZIAq1FFsHPJoiiCDnk1LQAUUUUAFFFFABRRRQAUUUUAFUpP8AWN9TV2qUn+sb6mgBtFFFABRRRQAVZtvut9arVZtvut9aAJqKKKACiiigAooooAKKKKACkJwM0tRzNtjI9RQBWlfe+ewptFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABT4mCyAnpTKDQBeFLUUDbk+nFS0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBynwz/AOSZ+Hf+vGP+VdXXKfDP/kmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAaqz/6z8KtGqs/+s/CgCKiiigAooooAKmt/vn6VDU1v98/SgCzRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBTl/1rfWmU6X/AFrfWm0AFFFFABRRRQBZtvuH61NUNt9w/WpqACiiigAooooAKKKKACq1z98fSrNVrn74+lAENFFFABRRRQAVLB/rR9KiqWD/AFo+lAFqiiigAooooAKa6BxginUUAUGUqxB7UValj3LkdRVWgAooooAKKKKAA1JDJtOCeKjooAvUtQwSbsqe1TUAFFFFABRRRQAUUUUAFFFFABRRRQBSk/1jfWm06T/WN9abQAUUUUAFFFFAE9t1arFV7bq1WKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAqlJ/rG+pq7VKT/WN9TQA2iiigAooooAKs233W+tVqs233W+tAE1FFFABRRRQAUUUUAFFFFABVSdt0mPSrEjbUJ71S75NAC0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEkLhXwehq1VHpVyNtyA0APooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAOU+Gf8AyTPw7/14x/yrq65T4Z/8kz8O/wDXjH/KuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAA1Vn/1n4VaNVZ/9Z+FAEVFFFABRRRQAVNb/AHz9Khqa3++fpQBZooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooApS/61vrTadL/rW+tNoAKKKKACiiigCzbfcP1qaobb7h+tTUAFFFFABRRRQAUUUUAFVrn74+lWarXP3x9KAIaKKKACiiigAqWD/Wj6VFUsH+tH0oAtUUUUAFFFFABRRRQAVVnjwdw6GrVIyhgQelAFGinSIUcjtTaACiiigAooooAUEqcjrVuN96g5571Tp8T7G9j1oAuUUgORmloAKKKKACiiigAooooAKKKKAKUn+sb602nSf6xvrTaACiiigAooooAnturVYqvbdWqxQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFUpP9Y31NXapSf6xvqaAG0UUUAFFFFABVm2+631qtVm2+631oAmooooAKKKKACiiigAoopGbaMnpQBXuGywX0qGgksxJooAKKKKACiiigAopyJvcDtU/wBnWgCtRVn7OnvR9nT3oArUVZ+zp70fZ096AK1FWfs6e9H2dPegCtRVn7OnvR9nT3oArUVZ+zp70fZ096AK1FWfs6e9QOuxytADaKKKACiiigAqW3Yh9vY1FSqSpBHagC9RTUbcoNOoAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAOU+Gf/ACTPw7/14x/yrq65T4Z/8kz8O/8AXjH/ACrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigANVZ/9Z+FWjVWf/WfhQBFRRRQAUUUUAFTW/3z9Khqa3++fpQBZooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooApS/wCtb602ny/61vrTKACiiigAooooAs233D9amqG2+4frU1ABRRRQAUUUUAFFFFABVa5++PpVmq1z98fSgCGiiigAooooAKlg/wBaPpUVSwf60fSgC1RRRQAUUUUAFFFFABRRRQBHKm9MDrVQgg4IxV+oJ48jcOooAr0UUUAFFFFABRRRQBNBJj5T+FWaoVbifevPWgCSiiigAooooAKKKKACiiigClJ/rG+tNp0n+sb602gAooooAKKKKAJ7bq1WKr23VqsUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABVKT/WN9TV2qUn+sb6mgBtFFFABRRRQAVZtvut9arVZtvut9aAJqKKKACiiigAooooAKguH42D8amPFU3bc5NADaKKKACiiigAoopVXcwX1oAnt14LEVPSKAq4HaloAKKKKACiiigAooooAKKKKACiiigAqvOmfmFWKay5UigClRQQVODRQAUUUUAFFFFAE9u/G2rFUVO1gR2q6DkUALRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBynwz/AOSZ+Hf+vGP+VdXXKfDP/kmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAaqz/6z8KtGqs/+s/CgCKiiigAooooAKmt/vn6VDU1v98/SgCzRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBTl/1rfWmU+X/AFrUygAooooAKKKKALNt9w/WpqhtvuH61NQAUUUUAFFFFABRRRQAVWufvj6VZqtc/fH0oAhooooAKKKKACpYP9aPpUVSwf60fSgC1RRRQAUUUUAFFFFABRRRQAUmKWigCnLH5Z9qZV11DqQapspVsHrQAlFFFABRRRQAU6N9jZptFAF1WDjIp1VIZNhwehq3QAUUUUAFFFFABRRRQBSk/wBY31ptOk/1jfWm0AFFFFABRRRQBPbdWqxVe26tVigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKpSf6xvqau1Sk/1jfU0ANooooAKKKKACrNt91vrVarNt91vrQBNRRRQAUUUUAFFFJQBHcNiPHrVWnStvc+gptABRRRQAUUUUAFTW68lqh61djG1APagBwooooAKKKKACiiigAooooAKKKKACiiigAooooArXC4Ib8Khq46h1IqnjBxQAUUUUAFFFFABVi3fK7fSq9OjfY4PbvQBdooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA5T4Z/8kz8O/wDXjH/KurrlPhn/AMkz8O/9eMf8q6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKq3H3x9KtUhVT1ANAFGiruxf7oo2L/AHRQBSoq7sX+6KNi/wB0UAUqlt/vn6VY2L/dFKFUdABQAtFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAFKX/WN9abV0op6qKNi/wB0UAUqKu7F/uijYv8AdFAFKiruxf7oo2L/AHRQBFb/AHT9anpAoXoAKWgAooooAKKKKACiiigAqtc/fH0qzSFVJyQDQBRoq7sX+6KNi/3RQBSoq7sX+6KNi/3RQBSqSD/WirOxP7opQqg5AAoAWiiigAooooAKKKKACiiigAooooAKhmi38jqKmooAodKKu+Wn90UbF/uigClRV3Yv90UbF/uigClRV3Yv90UbF/uigCjVmGXcNp61L5af3RShFByAM0AKKKKKACiiigAooooApSf61vrTaulFJztFGxf7ooApUVd2L/dFGxf7ooApUVd2L/dFGxf7ooAgtu9WaQKo6ACloAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACqMn+sb6mr1N2LnO0UAUqKu7F/uijYv8AdFAFKiruxf7oo2L/AHRQBSqxbfdb61LsT+6KUKF6DFAC0UUUAFFFFABUcr7FJ71JSEA9RmgCjRV3Yn90UbF/uigClRV3Yv8AdFGxf7ooApUVd2L/AHRRsX+6KAK8CZfPpVqkCgdBiloAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAEqrOm189jVukKg9QDQBRoq7sT+6KNi/3RQBSoq7sX+6KNi/3RQBSoq7sX+6KNi/3RQAyBsx/SpaQKB0GKWgAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDlPhn/yTPw7/ANeMf8q6uuU+Gf8AyTPw7/14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDlPhn/yTPw7/ANeMf8q6uuU+Gf8AyTPw7/14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooqvO7K4waALFFU/Ok9aPOk/vUAXKM1T85/71KJ3HfNAFuiq63GfvDH0qcMGHBzQAtFFFABRRRQAUUUUAFFFFABRRUczFUJHWgCSiqfnSf3qPOk/vUAXKM1T86T1o85/WgC5miqgncdcGpUnU8HigCaikBB6UtABRRRQAUUUUAFFFFABRRRQAUUUUAFFRvMq98moGnc+woAtZozVEsT3JpQzDuaAL2aKqLO4681OkqvxnmgCSiiigAooooAKKKKACiiigAooqKWTYMDrQBJmlqgWJ5JNPSZk46igC5RUaSK/Q8+lSUA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kz8O/wDXjH/KuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACopIRI2ckVLRQAyOPywRnNPoooAKKKKACiiigAooooAKKKKACiiigAooooAKa6b1xTqKAIUgCNnJqaiigAooooAKayhlwadRQBB9mH941MBgYpaKACiiigAooooAKKKKACiiigAooooAQqCORmoTbqeQcVPRQBVNu3bFAt27nirVFAEAt1HXJqYDHQUtFABRRRQAUUUUAFFFFABRRRQAU1lDDBHFOooArm29DT0hVeepqWigBKWiigAooooAKKKKACiiigAooooAjkiDnOSKSOIRnIJNS0UAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABSEgdTTGfsKYTnrQA8v6UUwUUAc38M/wDkmfh3/rxj/lXV1ynwz/5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRTS2BTC5PSgBzOBTCxJpKKACiiigYCigUUCOb+Gf8AyTPw7/14x/yrq65T4Z/8kz8O/wDXjH/KuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACikJxTTJ6UAOJwKjL5HFNJJ6migYUUUUAFFFFABRRRQACigUUCOb+Gf/JM/Dv8A14x/yrq65T4Z/wDJM/Dv/XjH/KuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoozTSwFADs0wuB0phYk0lACli3WkoooGFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/8AJM/Dv/XjH/KurrlPhn/yTPw7/wBeMf8AKuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKD0oAKQkDrTC/pTCSetADi+elNoooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/wAkz8O/9eMf8q6uuU+Gf/JM/Dv/AF4x/wAq6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACg00sBUbMWPtQA9nx0phYk80lFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/AOSZ+Hf+vGP+VdXXKfDP/kmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFITgc0wvxxQA8tgVGzk9Kb1ooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/8kz8O/8AXjH/ACrq65T4Z/8AJM/Dv/XjH/KuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACijNNZgKAFzTS4HSmFifpSUAKST1pKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/AMkz8O/9eMf8q6uuU+Gf/JM/Dv8A14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKQnFAC0hIHemM/PFMOT1NADmck8U3vRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/wCSZ+Hf+vGP+VdXXKfDP/kmfh3/AK8Y/wCVdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFIT60jMBUbMWoAeXA6daYST1pKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/wDJM/Dv/XjH/KurrlPhn/yTPw7/ANeMf8q6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACikJApjSZ6UAPLAdajZyeB0pvJ60UAFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBHN/DP/kmfh3/AK8Y/wCVdXXKfDP/AJJn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRTWcCgB2aYZOwphYn6UlAAST1NFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/+SZ+Hf8Arxj/AJV1dcp8M/8Akmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRSEgdTQAtIWAqNn7Cm5zQA5nJ6dKbRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/wDkmfh3/rxj/lXV1ynwz/5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFBoAKOlMLgUwsTQA5nx0phJPWiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/AMkz8O/9eMf8q6uuU+Gf/JM/Dv8A14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAopCQKYz54FADywAqMuT7U3r3oxQAUUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBHN/DP8A5Jn4d/68Y/5V1dcp8M/+SZ+Hf+vGP+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRTC4FAD6jZ/SmsSxpKAAkmiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/yTPw7/wBeMf8AKurrlPhn/wAkz8O/9eMf8q6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoopCQBQAtNLAU1nz0pmc0AOLk9OKbRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBHN/DP8A5Jn4d/68Y/5V1dcp8M/+SZ+Hf+vGP+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABSEgdaaz46UwsW60AOZx2pmSetFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/wCSZ+Hf+vGP+VdXXKfDP/kmfh3/AK8Y/wCVdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUhOKjMnpQA8uB3qMsT9KSigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/yTPw7/ANeMf8q6uuU+Gf8AyTPw7/14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoopjOB0oAcTimmT0phJNJQMCSetFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/yTPw7/wBeMf8AKurrlPhn/wAkz8O/9eMf8q6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiikLAdTQAtNLgUxnz0puaAFZi1JRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/wCSZ+Hf+vGP+VdXXKfDP/kmfh3/AK8Y/wCVdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFITgU1nA6HmmEk9TQA4v6Uwkk80UUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/5Jn4d/wCvGP8AlXV1ynwz/wCSZ+Hf+vGP+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRTSwFMZyelAD2cCoyxb6UlFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/AOSZ+Hf+vGP+VdXXKfDP/kmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFGaYzjtQA4nFMZ/SmEkmigAPJ5ooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAjm/hn/AMkz8O/9eMf8q6uuU+Gf/JM/Dv8A14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooppYKOaAHU1mAphfPTim0AKWJ+lJRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/8Akmfh3/rxj/lXV1ynwz/5Jn4d/wCvGP8AlXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUZxQAUhOKazjtUZYnrQA9pPSmE570UUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/+SZ+Hf+vGP+VdXXKfDP8A5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUU0sB1phcnp0oAeXA71GWJpKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/8kz8O/wDXjH/KurrlPhn/AMkz8O/9eMf8q6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACig0xnxwKAHEgUxn7Cmk560lAwOT1ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/5Jn4d/68Y/5V1dcp8M/wDkmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFNYgUALSFwKYXzTaAFLE0lFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/wDkmfh3/rxj/lXV1ynwz/5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUmaAFpCQBzTGk9KYST1oAez8cUyiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/8AJM/Dv/XjH/KurrlPhn/yTPw7/wBeMf8AKuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKQsB3qMuT3oAcXAphYmkooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/8AJM/Dv/XjH/KurrlPhn/yTPw7/wBeMf8AKuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACikyKYz44FADywHWmGTPSmEk9aKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/8AJM/Dv/XjH/KurrlPhn/yTPw7/wBeMf8AKuroAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoopCcDmgBaazAfWms+elMoAUsWpMUUUDCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/wDkmfh3/rxj/lXV1ynwz/5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUU1mAoACwAqNmLGk60UAFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/AOSZ+Hf+vGP+VdXXKfDP/kmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFMZ8cCgAZscCo+tFFABRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBHN/DP/kmfh3/AK8Y/wCVdXXKfDP/AJJn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFNZsUAIzYGAeajoPJzRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/+SZ+Hf8Arxj/AJV1dcp8M/8Akmfh3/rxj/lXV0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRQaAEY4FQkknNKzZNJQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBHN/DP/kmfh3/AK8Y/wCVdXXKfDP/AJJn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAVG7Z4FOY4FRdaACiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQACigUUCOb+Gf/JM/Dv/AF4x/wAq6uuU+Gf/ACTPw7/14x/yrq6ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACkpaY5xQAxjuNJRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/5Jn4d/wCvGP8AlXV1ynwz/wCSZ+Hf+vGP+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAVCx3GpHbAqKgAooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQI5v4Z/wDJM/Dv/XjH/KurrlPhn/yTPw7/ANeMf8q6ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiikY4FAETnLUlFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/wCSZ+Hf+vGP+VdXXKfDP/kmfh3/AK8Y/wCVdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABUch7VJULHLUAJRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/+SZ+Hf+vGP+VdXXKfDP8A5Jn4d/68Y/5V1dABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAITgGoakc4FR0AFFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAAUUCigRzfwz/5Jn4d/wCvGP8AlXV1ynwz/wCSZ+Hf+vGP+VdXQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAEUn3qbTnOWptAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEc38M/wDkmfh3/rxj/lXV1zvgnT7nRPBOj6ZfIEurW1SKVVYMAwHPI610AcHvQA6ijNFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABQelFIx+U0AQk5NFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEFFFFAwyRS7yKSigB4f1p+4HvUNFAifNFQhyKer568UAPooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKY5wtPpkn3aAI6KKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQIKKKKBhRRRQAUUUUAFFFFAACR0NSCT1qOigCYHNLUIJBp6uD1oEPoozRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFMk+7T6ZJ92gCOiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQACigUUCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFAChitSBwaio+lAE9FRByOvSpAwPSgQtFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFMk+7T6ZJ92gCOiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQACigUUCCiiigYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAPV/WnggioaUMR0oETUUxXB604GgBaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACmSfdp9NblTQBFRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBBRRRQMKKKKACiiigAoopKAFopKWgAoqjf6xp+lhDfXkNvu+75jgZrkdU+JlhbSmKwhe5I4LkYXPt61EqkY7s3o4WtW+CJ3lFeRSfE3WGbMcFuo9CCas2nxQvkYfarOOQd9hxWf1iB2PKcSlex6pRXK6d8QNBvYt012towxuW4+Xn2J610tvcQ3UKzQSLJG3RlOQa1jJS2OCpRqU3aa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TirFj4H1TS7q+urTxTcrNeyGWZ3tYXLE9slc4HQDsK7jbRigDifh5o+q6fot3Hql1MyyXl1iCWBUxmZzv4Gfmzu9OeKreDNIn8E6rqmjPHL/AGPJIbixm2/Igbkxk+oOa7/bRtFAHn81pc+L/H1ncT6dcW2maFIZIJpoyn2iX1XPVR6969BpNtLQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABSYpaKAEwK5jxH4K07XWluCnl3rJgSg98cZHeuopDyaUoqSszSlVnSlzQdmeB3vhDXbCZo5NPmlCkjzIULKw9axHUxyMjgqykgg9Qa+liBWRqPhbRdUJa70+B5D/y02AMPx61ySwvWLPbo529qsfuPn/0pUVpHCKCzE4AFexn4X+Gy+7ybn6faX/xrb03wroukOJLOwhSUDHm7QXI9261Kwsm9WdE87ope5F3PG7Hwlrl9PHGmnzxqxAMjoVUD1zXq3h/wTpmhSR3KK8t2q7fNcn8eOgrpgoFLXRToRgeTisyrV1y7LyEKjFRY9amHSo5BjmtjzhtFFFAwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAxRiiigAooooAKKKKACiiigAooooAMUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABQaKKACsnW/D2n69EiX0RcxnKMDgj8q1aKTSkrMqE5QkpQep4rrHgPWNLk/cwvexE/K8K5P4gVztxbzWkvlXMLxSDkq4wa+jKpX+j6dqkfl31nBcL2EiBsVyzwqesT2qOdTjZVFc+e/SivY5fht4clkL+ROmey3Dgflmrth4I8P6eVaLT43deQ83zsPxNZ/VZdWdbzqilonc8ftNC1W/VWttPuJEbo6odv516N4Y8AwWkUF3qaE3scnmKoc7VweM+td0qKihVAAHYClreGHjF3ep5mJzWrWXKtEGMDilpKWug8sKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooABRQKKBBRRRQMKKKKACiiigAooooAKKKKAEpaKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBMf5zS0UUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAKCRUiuD9aiooET0VCHIqRWDUAOooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACkxS0UAJijFLRQAmKMUtFACYoxS0UAFIRkUtFAEHQ4op8i96ZQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigApKWigAxRRRQAUUUUAJS0UUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAAKKBRQIKKKKBhRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFHTvRRQA5X9akDA9KhoyR0oET0VGsnY1JmgAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAEIzUTKQfapqa67hQBFRR3ooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAooFFAgooooGFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABSgkHikooAkDg0+oKUORQImopoYHvTqACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiikoAY69xTKmNRsuOR0oAbRRRQMKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAFFAooEZD+J9FikaN9StwynBBccU3/hK9C/6Cdt/32K8FUfKKXFcP1qXY+m/sOl/Mz3n/AISvQv8AoJ23/fYo/wCEr0L/AKCdt/32K8GxRij61LsH9iUv5me8/wDCV6F/0E7b/vsUf8JXoX/QTtv++xXg2KMUfWpdg/sSl/Mz3n/hK9C/6Cdt/wB9ij/hK9C/6Cdt/wB9ivBsUYo+tS7B/YlL+ZnvP/CV6F/0E7b/AL7FH/CV6F/0E7b/AL7FeDYoxR9al2D+xKX8zPef+Er0L/oJ23/fYo/4SvQv+gnbf99ivBsUYo+tS7B/YlL+ZnvP/CV6F/0E7b/vsUf8JXoX/QTtv++xXg2KMUfWpdg/sSl/Mz3n/hK9C/6Cdt/32KP+Er0L/oJ23/fYrwbFGKPrUuwf2JS/mZ7z/wAJXoX/AEE7b/vsUf8ACV6F/wBBO2/77FeDYoxR9al2D+xKX8zPef8AhK9C/wCgnbf99ij/AISvQv8AoJ23/fYrwbFGKPrUuwf2JS/mZ7z/AMJXoX/QTtv++xR/wlehf9BO2/77FeDYoxR9al2D+xKX8zPef+Er0L/oJ23/AH2KP+Er0L/oJ23/AH2K8GxRij61LsH9iUv5me8/8JXoX/QTtv8AvsUf8JXoX/QTtv8AvsV4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ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAuab/AMfLf7h/mKKNN/4+W/3D/MUVcdjmq/EUl+6KWkX7opag6QooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigC5pv/Hy3+4f5iijTf8Aj5b/AHD/ADFFXHY5qvxFJfuilpF+6KWoOkKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooo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"
)


def _obter_papel_timbrado_reader() -> Optional[ImageReader]:
    try:
        dados = base64.b64decode(PAPEL_TIMBRADO_B64)
        return ImageReader(io.BytesIO(dados))
    except Exception:
        return None


def _desenhar_papel_timbrado(canvas_obj, doc_obj):
    imagem = _obter_papel_timbrado_reader()
    if imagem is not None:
        largura, altura = A4
        canvas_obj.drawImage(imagem, 0, 0, width=largura, height=altura, preserveAspectRatio=False, mask="auto")


# ---------------------------------------------------------------------------
# Templates offline de plano de ação por pilar (fallback sem API)
# ---------------------------------------------------------------------------

_TEMPLATES_ACAO = {
    "Autonomia": (
        "Reduzir a dependência de acompanhamento direto",
        "Assumir integralmente, sem supervisão constante, uma etapa já conhecida da rotina, "
        "reportando apenas exceções e riscos ao líder direto.",
        "Nas próximas 2 produções, o líder não precisa reforçar orientações básicas já dadas "
        "sobre a etapa combinada.",
    ),
    "Criticidade": (
        "Antecipar riscos antes que virem problema",
        "Antes de iniciar a montagem/operação, identificar e comunicar por escrito (grupo do "
        "projeto) ao menos 1 risco potencial percebido no local ou no material.",
        "Registro de pelo menos 1 alerta preventivo por evento nos próximos 30 dias, sem "
        "ocorrências recorrentes do mesmo tipo de falha.",
    ),
    "Comportamento": (
        "Ajustar postura e comunicação em campo",
        "Seguir rigorosamente o uso de uniforme/EPI, manter tom cordial mesmo sob pressão e "
        "comunicar imprevistos ao líder de forma direta e respeitosa.",
        "Zero registros de reclamação de postura em avaliações pós-evento no próximo ciclo.",
    ),
    "Entrega": (
        "Fechar a etapa 100% testada antes do prazo",
        "Concluir e testar a própria etapa com antecedência mínima combinada com o líder antes "
        "do horário limite do cronograma do evento.",
        "Nenhuma entrega da etapa sob sua responsabilidade atrasada ou destestada nos próximos "
        "30 dias.",
    ),
    "Complexidade": (
        "Consolidar domínio técnico da rotina",
        "Revisar com o técnico de referência os passos da atividade em que houve dificuldade e "
        "repetir a execução supervisionada até atingir consistência.",
        "Executar a mesma atividade sem apontamentos negativos na próxima avaliação de campo.",
    ),
    "Domínio Técnico": (
        "Aprofundar domínio técnico específico",
        "Estudar e revisar, com apoio do técnico sênior da área, o procedimento técnico que "
        "gerou a ocorrência, documentando o passo a passo aprendido.",
        "Aplicar o procedimento revisado corretamente no próximo evento, sem reincidência.",
    ),
    "Segurança": (
        "Eliminar riscos de segurança na operação",
        "Seguir integralmente o checklist de segurança elétrica/estrutural da Firma antes de "
        "energizar ou liberar a estrutura, sem exceções por pressão de prazo.",
        "Checklist de segurança assinado e sem apontamentos em todos os eventos do próximo "
        "período.",
    ),
    "Melhoria Contínua": (
        "Formalizar aprendizado em padrão replicável",
        "Documentar a ocorrência e propor, junto ao líder, um ajuste no checklist ou processo "
        "interno para evitar reincidência.",
        "Checklist/processo atualizado e validado pela liderança dentro dos próximos 30 dias.",
    ),
    "Criatividade": (
        "Trazer ao menos uma sugestão de melhoria",
        "Levar para a próxima reunião de 1:1 uma sugestão concreta de melhoria de processo ou "
        "solução técnica observada em campo.",
        "Ao menos 1 sugestão registrada e discutida com o líder no período.",
    ),
    "Excelência": (
        "Elevar o padrão de acabamento técnico",
        "Revisar o próprio trabalho contra o checklist de padrão Firma antes de considerar a "
        "etapa concluída, corrigindo qualquer detalhe fora do padrão.",
        "Avaliação pós-evento sem apontamentos de acabamento/capricho técnico no próximo ciclo.",
    ),
    "Honestidade": (
        "Comunicar falhas e avarias sem omissão",
        "Reportar imediatamente ao líder qualquer erro, perda ou avaria assim que identificado, "
        "antes que seja percebido por terceiros.",
        "Nenhum caso de omissão identificado; feedback do líder confirmando transparência no "
        "próximo ciclo.",
    ),
    "Colaboração": (
        "Apoiar outras frentes após concluir a própria",
        "Ao finalizar a tarefa individual, procurar ativamente o líder ou colegas de outra "
        "frente para oferecer apoio antes de ser solicitado.",
        "Ao menos 1 registro de apoio espontâneo a outra frente por evento no próximo ciclo.",
    ),
    "Fé": (
        "Manter postura positiva sob pressão",
        "Em momentos de prazo apertado ou imprevisto, manter tom construtivo com o time e focar "
        "a comunicação em soluções, não em queixas.",
        "Feedback do líder e dos pares sobre postura mais estável em pelo menos 2 eventos "
        "seguidos.",
    ),
    "Aprender Sempre": (
        "Buscar ativamente feedback e capacitação",
        "Solicitar feedback estruturado ao líder após cada evento e aplicar ao menos um ponto "
        "de melhoria indicado no evento seguinte.",
        "Evolução visível (nota ≥ 3) no critério na próxima avaliação mensal.",
    ),
}

_TEMPLATE_PADRAO = (
    "Corrigir o desvio identificado no critério",
    "Revisar com o líder direto, na próxima reunião de 1:1, o que exatamente gerou a nota baixa "
    "e combinar um ajuste prático de comportamento/execução para o critério.",
    "Nota igual ou superior a 3.0 no mesmo critério na próxima avaliação.",
)


def _gerar_acao_offline(pilar: str, criterio_oficial: str, fato_gerador: str) -> dict:
    titulo, o_que_fazer, como_medir = _TEMPLATES_ACAO.get(pilar, _TEMPLATE_PADRAO)
    return {
        "titulo": titulo,
        "o_que_fazer": o_que_fazer,
        "como_medir": como_medir,
    }


def _gerar_acao_online(pilar: str, criterio_oficial: str, fato_gerador: str, api_key: str) -> Optional[dict]:
    """Chama a API da Anthropic para redigir uma ação mais personalizada.
    Retorna None em qualquer falha, para permitir fallback silencioso."""
    prompt = (
        "Você é um especialista em RH e desenvolvimento de pessoas em uma produtora de "
        "eventos corporativos. Um colaborador recebeu nota baixa (1 ou 2) no critério "
        f"'{pilar}'.\nCritério oficial avaliado: {criterio_oficial}\n"
        f"Comentário do gestor sobre o ocorrido: {fato_gerador}\n\n"
        "Gere APENAS um objeto JSON, sem nenhum texto antes ou depois, sem markdown, com "
        "exatamente estas 3 chaves:\n"
        '{"titulo": "título curto da ação focado no erro", '
        '"o_que_fazer": "instrução clara e prática de comportamento em campo", '
        '"como_medir": "métrica operacional objetiva para os próximos 30 dias"}'
    )
    try:
        resp = requests.post(
            ANTHROPIC_API_URL,
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": ANTHROPIC_MODEL,
                "max_tokens": 400,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        texto = "".join(
            bloco.get("text", "") for bloco in data.get("content", []) if bloco.get("type") == "text"
        ).strip()
        texto = texto.replace("```json", "").replace("```", "").strip()
        import json as _json
        parsed = _json.loads(texto)
        if all(k in parsed for k in ("titulo", "o_que_fazer", "como_medir")):
            return parsed
    except Exception:
        return None
    return None


def gerar_plano_de_acao(achado: dict) -> dict:
    """Decide entre modo online/offline e devolve a ação para um achado."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if api_key:
        resultado = _gerar_acao_online(
            achado["pilar"], achado["criterio_oficial"], achado["fato_gerador"], api_key
        )
        if resultado:
            return resultado
    return _gerar_acao_offline(achado["pilar"], achado["criterio_oficial"], achado["fato_gerador"])


# ---------------------------------------------------------------------------
# Renderização do PDF
# ---------------------------------------------------------------------------

def gerar_pdf_pdi(
    caminho_saida: str,
    colaborador_nome: str,
    cargo_nivel: str,
    nota_final: float,
    achados: list,
    cidade_uf: str = "Juazeiro do Norte - CE",
) -> str:
    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=A4,
        topMargin=3.4 * cm,
        bottomMargin=3.6 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "TituloPDI", parent=styles["Title"], fontSize=16, spaceAfter=4, textColor=colors.HexColor("#8B0000")
    )
    subtitulo_style = ParagraphStyle(
        "SubtituloPDI", parent=styles["Normal"], fontSize=10, textColor=colors.grey, spaceAfter=16
    )
    heading_style = ParagraphStyle(
        "HeadingPDI", parent=styles["Heading2"], fontSize=12, spaceBefore=14, spaceAfter=6,
        textColor=colors.HexColor("#1A1A1A"),
    )
    body_style = ParagraphStyle("BodyPDI", parent=styles["Normal"], fontSize=10, leading=14)
    bold_style = ParagraphStyle("BoldPDI", parent=styles["Normal"], fontSize=10, leading=14, fontName="Helvetica-Bold")

    story = []

    story.append(Paragraph("PLANO DE DESENVOLVIMENTO INDIVIDUAL (PDI)", titulo_style))
    story.append(Paragraph("Relatório de Melhoria Contínua Automatizado — Firma Produções", subtitulo_style))

    hoje = date.today().strftime("%d/%m/%Y")

    dados_cabecalho = [
        ["Data de Emissão:", hoje],
        ["Colaborador:", colaborador_nome],
        ["Cargo / Nível:", cargo_nivel],
        ["Aproveitamento do Período:", f"NÃO ELEGÍVEL ({nota_final:.1f} de 5.0)"],
    ]
    tabela_cabecalho = Table(dados_cabecalho, colWidths=[5 * cm, 10 * cm])
    tabela_cabecalho.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(tabela_cabecalho)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#CCCCCC")))

    # ---- Seção 1: Diagnóstico -----------------------------------------
    story.append(Paragraph("1. DIAGNÓSTICO: O QUE NÃO FOI ATINGIDO NO PERÍODO", heading_style))

    if not achados:
        story.append(Paragraph(
            "Nenhum critério individual com nota 1 ou 2 foi identificado, porém a nota "
            "consolidada do período ficou abaixo de 3.5. Recomenda-se revisão geral com o "
            "colaborador na próxima reunião de 1:1.",
            body_style,
        ))
    else:
        for i, achado in enumerate(achados, start=1):
            story.append(Paragraph(
                f"<b>{i}. {achado['pilar']}</b> — Nota: {achado['nota']:.1f} "
                f"<font size=8 color='grey'>({achado['origem']})</font>",
                bold_style,
            ))
            story.append(Paragraph(f"<i>Critério Oficial:</i> {achado['criterio_oficial']}", body_style))
            story.append(Paragraph(f"<i>Fato Gerador:</i> {achado['fato_gerador']}", body_style))
            story.append(Spacer(1, 8))

    # ---- Seção 2: Plano de ação -----------------------------------------
    story.append(Paragraph("2. PLANO DE AÇÃO: PONTOS DE MELHORIA PARA OS PRÓXIMOS 30 DIAS", heading_style))

    if not achados:
        story.append(Paragraph(
            "Definir com o colaborador, na próxima 1:1, ao menos uma meta objetiva de melhoria "
            "para o próximo ciclo, revisando a Ficha Mensal Unificada em conjunto.",
            body_style,
        ))
    else:
        for i, achado in enumerate(achados, start=1):
            acao = gerar_plano_de_acao(achado)
            story.append(Paragraph(f"<b>Ação Prática {i}: {acao['titulo']}</b>", bold_style))
            story.append(Paragraph(f"<i>O que fazer:</i> {acao['o_que_fazer']}", body_style))
            story.append(Paragraph(f"<i>Como medir o sucesso em 30 dias:</i> {acao['como_medir']}", body_style))
            story.append(Spacer(1, 8))

    # ---- Seção 3: Compromisso -----------------------------------------
    story.append(Paragraph("3. COMPROMISSO DE EVOLUÇÃO", heading_style))
    story.append(Paragraph(
        "O cumprimento destas metas de melhoria será reavaliado no próximo ciclo mensal de 1:1. "
        "O retorno à elegibilidade financeira depende diretamente da virada destas notas para o "
        "nível 3.0 ou superior.",
        body_style,
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"{cidade_uf}, {hoje}.", body_style))
    story.append(Spacer(1, 40))

    tabela_assinaturas = Table(
        [["_" * 40, "_" * 40], ["Assinatura do Colaborador", "Assinatura do Gestor / Head de Área"]],
        colWidths=[8 * cm, 8 * cm],
    )
    tabela_assinaturas.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTSIZE", (0, 1), (-1, 1), 9),
                ("TOPPADDING", (0, 1), (-1, 1), 4),
            ]
        )
    )
    story.append(tabela_assinaturas)

    doc.build(story, onFirstPage=_desenhar_papel_timbrado, onLaterPages=_desenhar_papel_timbrado)
    return caminho_saida


# ============================================================
# SEÇÃO 6/6 — APLICAÇÃO STREAMLIT (app_firma.py original)
# ============================================================
# -*- coding: utf-8 -*-


import os
import uuid
from datetime import date, datetime

import streamlit as st
import pandas as pd
from PIL import Image

# ---------------------------------------------------------------------------
# Identidade visual: logotipo e símbolo da marca, embutidos em base64 para
# manter o sistema como um único arquivo autocontido.
# ---------------------------------------------------------------------------

LOGO_SIDEBAR_B64 = (
    "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"
)

FAVICON_B64 = (
    "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"
)


def _obter_favicon():
    try:
        return Image.open(io.BytesIO(base64.b64decode(FAVICON_B64)))
    except Exception:
        return None


def _obter_logo_sidebar_bytes():
    try:
        return base64.b64decode(LOGO_SIDEBAR_B64)
    except Exception:
        return None




# ---------------------------------------------------------------------------
# Configuração da página e inicialização do banco
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Gestão de Performance Operacional",
    page_icon=_obter_favicon(),
    layout="wide",
)

st.markdown(
    """
    <style>
    /* A paleta de cores (fundo, texto, botões, inputs, popovers, alertas)
       agora vem do tema nativo do Streamlit, configurado em
       .streamlit/config.toml — isso garante contraste correto em TODO
       componente, inclusive os que o Streamlit renderiza fora da área
       principal da página (popovers, dropdowns de selectbox, calendário).
       Aqui só ficam ajustes puramente tipográficos/decorativos que o tema
       nativo não cobre. */

    h1, h2, h3, h4, h5,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        text-transform: uppercase;
        letter-spacing: -0.03em;
    }

    .stButton > button,
    .stDownloadButton > button,
    button[kind="formSubmit"],
    button[kind="secondaryFormSubmit"] {
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.03em;
    }

    .stTabs [data-baseweb="tab"] {
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    [data-testid="stMetricValue"] {
        color: #E12E2E !important;
    }
    </style>
    <div style="position: fixed; top: 0; left: 0; right: 0; height: 6px;
                background-color: #E12E2E; z-index: 999999;"></div>
    """,
    unsafe_allow_html=True,
)

PASTA_PDIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdis_gerados")
os.makedirs(PASTA_PDIS, exist_ok=True)

init_db()

if "credencial_seed_exibida" not in st.session_state:
    st.session_state.seed_info = seed_admin_padrao()
    st.session_state.credencial_seed_exibida = True


# ---------------------------------------------------------------------------
# Tela de login
# ---------------------------------------------------------------------------

def tela_login():
    _logo_bytes = _obter_logo_sidebar_bytes()
    if _logo_bytes:
        st.image(_logo_bytes, width=280)
    st.caption("Para toda boa ideia, uma boa solução.")
    st.title("Gestão de Performance Operacional")
    st.caption("Faça login para acessar o sistema.")

    if st.session_state.get("seed_info"):
        st.info(
            "Nenhum usuário existia no banco — foi criado um acesso administrativo padrão:\n\n"
            f"**E-mail:** {st.session_state.seed_info['email']}\n\n"
            f"**Senha:** {st.session_state.seed_info['senha']}\n\n"
            "Troque essa senha assim que possível criando um novo usuário RH na aba "
            "Administração e removendo este padrão."
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("form_login"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", type="primary")
            if entrar:
                usuario = autenticar(email, senha)
                if usuario:
                    st.session_state.usuario = usuario
                    st.rerun()
                else:
                    st.error("E-mail ou senha inválidos.")


def logout():
    for chave in ("usuario",):
        st.session_state.pop(chave, None)
    st.rerun()


# ---------------------------------------------------------------------------
# Ponto de entrada — exige login antes de qualquer coisa
# ---------------------------------------------------------------------------

if "usuario" not in st.session_state:
    tela_login()
    st.stop()

usuario = st.session_state.usuario
papel = usuario["papel"]



def colaboradores_visiveis() -> list[dict]:
    if papel in ("RH", "PRODUTOR"):
        # RH vê tudo; PRODUTOR também vê todas as áreas porque um evento
        # reúne equipes de LED, Som, Iluminação etc. ao mesmo tempo.
        return listar_colaboradores()
    if papel == "HEAD":
        return listar_colaboradores(area=usuario["area"])
    return listar_colaboradores(apenas_id=usuario["colaborador_id"])


def pode_cadastrar_colaborador() -> bool:
    return papel in ("RH", "HEAD")


def pode_arquivar_colaborador() -> bool:
    """Arquivar/reativar colaborador é ação administrativa sensível —
    restrita ao RH, mesmo que Heads possam cadastrar novos colaboradores."""
    return papel == "RH"


def pode_editar_gallup() -> bool:
    """O indicador Gallup é gerido única e exclusivamente pelo RH/CEO — Head
    de Área e Produtor de Eventos não cadastram nem editam esse dado."""
    return papel == "RH"


def pode_lancar_pos_evento() -> bool:
    """RH e Produtor de Eventos lançam a Avaliação Pós-Evento (Campo).
    Head de Área apenas visualiza (não lança mais)."""
    return papel in ("RH", "PRODUTOR")


def pode_lancar_mensal() -> bool:
    """RH e Head de Área lançam a Avaliação Mensal Unificada.
    Produtor de Eventos não enxerga nem edita essa camada."""
    return papel in ("RH", "HEAD")


def abas_visiveis_para_papel() -> list[str]:
    """Chaves das abas visíveis, na ordem em que devem aparecer."""
    if papel == "RH":
        return ["prontuario", "alcadas", "pos_evento", "mensal", "historico", "pdi", "admin"]
    if papel == "HEAD":
        return ["prontuario", "alcadas", "pos_evento", "mensal", "historico", "pdi"]
    if papel == "PRODUTOR":
        # Não enxerga nem edita Avaliação de Competências e Cultura, Painel
        # Consolidador ou PDI — todos derivados (direta ou indiretamente)
        # da nota mensal.
        return ["prontuario", "alcadas", "pos_evento"]
    if papel == "COLABORADOR":
        # Acesso de leitura protegido: apenas o próprio perfil, as próprias
        # diretrizes de cargo e o próprio painel consolidado (com download
        # do PDI embutido ali, sem aba separada).
        return ["prontuario", "alcadas", "historico"]
    return []


def exibir_tabela(df: pd.DataFrame):
    """st.dataframe usa um componente renderizado em canvas que, por uma
    limitação conhecida do Streamlit, costuma ignorar as cores do tema e
    aparecer sempre com fundo branco. st.table é HTML puro e respeita o
    tema corretamente, então é o que usamos em todo o sistema."""
    df = df.copy()
    df.index = [""] * len(df)
    st.table(df)


def lista_colaboradores_labels(colabs: list[dict]) -> dict:
    return {c["id"]: f"{c['nome']} — {c['cargo']}" for c in colabs}


# ---------------------------------------------------------------------------
# Cabeçalho + sidebar
# ---------------------------------------------------------------------------

st.title("Gestão de Performance Operacional")

with st.sidebar:
    _logo_bytes_sidebar = _obter_logo_sidebar_bytes()
    if _logo_bytes_sidebar:
        st.image(_logo_bytes_sidebar, width=180)
    rotulo_papel = {
        "RH": "RH / CEO (acesso total)",
        "HEAD": f"Head de Área — {NOMES_AREAS.get(usuario['area'], usuario['area'])}",
        "PRODUTOR": "Produtor de Eventos",
        "COLABORADOR": "Colaborador",
    }
    st.markdown(f"**{usuario['nome']}**")
    st.caption(rotulo_papel.get(papel, papel))
    if st.button("Sair"):
        logout()
    st.divider()
    modo_ia = "Online (ANTHROPIC_API_KEY detectada)" if os.environ.get("ANTHROPIC_API_KEY") else "Offline (templates internos)"
    st.caption(f"Gerador de PDI: {modo_ia}")
    st.caption(f"Banco de dados: `{os.path.basename(DB_PATH)}`")

    colaborador_foco_id = None
    if papel in ("RH", "HEAD", "PRODUTOR"):
        st.divider()
        st.markdown("**Colaborador em foco**")
        colabs_para_foco = colaboradores_visiveis()
        if colabs_para_foco:
            labels_foco = lista_colaboradores_labels(colabs_para_foco)
            colaborador_foco_id = st.selectbox(
                "Usado na aba Diretrizes e Escopo de Cargo",
                options=list(labels_foco.keys()),
                format_func=lambda i: labels_foco[i],
                key="colaborador_foco_id",
                label_visibility="collapsed",
            )
        else:
            st.caption("Nenhum colaborador disponível no seu escopo.")


# ===========================================================================
# VISÃO RH / HEAD — abas completas (escopo filtrado por área quando HEAD)
# ===========================================================================

TAB_SPECS = [
    ("prontuario", "Perfil do Profissional"),
    ("alcadas", "Diretrizes e Expectativas de Função"),
    ("pos_evento", "Avaliação de Entrega Técnica"),
    ("mensal", "Avaliação de Competências e Cultura"),
    ("historico", "Painel Consolidador e Elegibilidade"),
    ("pdi", "Plano de Desenvolvimento Individual (PDI)"),
    ("admin", "Administração do Sistema"),
]

chaves_visiveis = abas_visiveis_para_papel()
labels_visiveis = [label for chave, label in TAB_SPECS if chave in chaves_visiveis]
abas = st.tabs(labels_visiveis)
IDX = {chave: i for i, chave in enumerate(chaves_visiveis)}

# ===========================================================================
# ABA 1 — PRONTUÁRIO
# ===========================================================================
with abas[IDX["prontuario"]]:
    if papel == "COLABORADOR":
        colaborador_proprio = obter_colaborador(usuario["colaborador_id"]) if usuario.get("colaborador_id") else None
        if not colaborador_proprio:
            st.error("Sua conta não está vinculada a nenhum perfil. Fale com o RH.")
        else:
            st.subheader(f"Bem-vindo(a), {colaborador_proprio['nome']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Função / Nível", colaborador_proprio["cargo"])
            c2.metric("Setor", NOMES_AREAS.get(colaborador_proprio["area"], colaborador_proprio["area"]))
            c3.metric("Tempo de empresa", f"{meses_entre(colaborador_proprio['data_admissao'])} mês(es)")

            col_gallup, col_docs = st.columns(2)
            with col_gallup:
                st.markdown("**Perfil de Talentos Gallup**")
                link_teste_gallup = obter_configuracao("link_teste_gallup", LINK_GALLUP_PADRAO)
                st.markdown(f"[Clique aqui para realizar o seu teste de perfil Gallup]({link_teste_gallup})")
                if colaborador_proprio.get("gallup_top5"):
                    for talento in colaborador_proprio["gallup_top5"]:
                        st.write(f"- {talento}")
                else:
                    st.caption("Seus talentos ainda não foram validados pelo RH.")
            with col_docs:
                st.markdown("**Repositório de Documentos Oficiais**")
                if colaborador_proprio.get("documentos"):
                    for doc in colaborador_proprio["documentos"]:
                        if doc.get("link"):
                            st.markdown(f"- [{doc['nome']}]({doc['link']})")
                        else:
                            st.write(f"- {doc['nome']}")
                else:
                    st.caption("Nenhum documento cadastrado ainda.")

            for al in colaborador_proprio.get("alertas", []):
                st.error(al)
    else:
        st.subheader("Perfil do Profissional")
        st.caption("Cadastro e edição de dados ficam centralizados na aba Administração do Sistema (RH/CEO).")

        colabs = colaboradores_visiveis()
        if not colabs:
            st.info("Nenhum colaborador cadastrado nesta área ainda.")
        else:
            for c in colabs:
                with st.expander(f"{c['nome']} — {c['cargo']} ({NOMES_AREAS.get(c['area'], c['area'])})"):
                    st.write(f"**Admissão:** {c['data_admissao'].strftime('%d/%m/%Y')}")
                    st.write(f"**Início no nível atual:** {c['data_inicio_nivel'].strftime('%d/%m/%Y')}")
                    st.write(f"**Tempo de empresa:** {meses_entre(c['data_admissao'])} mês(es)")
                    st.write(f"**Tempo no nível:** {meses_entre(c['data_inicio_nivel'])} mês(es)")

                    col_gallup, col_docs = st.columns(2)
                    with col_gallup:
                        st.markdown("**Perfil de Talentos Gallup**")
                        if c.get("gallup_top5"):
                            for talento in c["gallup_top5"]:
                                st.write(f"- {talento}")
                        else:
                            st.caption("Teste Gallup ainda não registrado.")
                    with col_docs:
                        st.markdown("**Repositório de Documentos Oficiais**")
                        if c.get("documentos"):
                            for doc in c["documentos"]:
                                if doc.get("link"):
                                    st.markdown(f"- [{doc['nome']}]({doc['link']})")
                                else:
                                    st.write(f"- {doc['nome']}")
                        else:
                            st.caption("Nenhum documento cadastrado ainda.")

                    for al in c.get("alertas", []):
                        st.error(al)

                    if pode_arquivar_colaborador():
                        with st.popover("Arquivar colaborador"):
                            st.warning(
                                f"Isso remove **{c['nome']}** das listas de avaliação e do "
                                "prontuário ativo. O histórico de avaliações já lançadas "
                                "continua guardado e acessível na seção 'Colaboradores "
                                "arquivados', mais abaixo — nada é apagado de verdade."
                            )
                            confirmar = st.checkbox("Confirmo que quero arquivar este colaborador", key=f"confirma_arquivar_{c['id']}")
                            if st.button("Arquivar agora", key=f"arquivar_{c['id']}", disabled=not confirmar):
                                arquivar_colaborador(c["id"])
                                st.success(f"{c['nome']} foi arquivado.")
                                st.rerun()

        if pode_arquivar_colaborador():
            arquivados = listar_colaboradores_arquivados()
            with st.expander(f"Colaboradores arquivados ({len(arquivados)})"):
                if not arquivados:
                    st.caption("Nenhum colaborador arquivado no momento.")
                else:
                    for c in arquivados:
                        col_info, col_acao = st.columns([3, 1])
                        with col_info:
                            st.write(f"**{c['nome']}** — {c['cargo']} ({NOMES_AREAS.get(c['area'], c['area'])})")
                        with col_acao:
                            if st.button("Reativar", key=f"reativar_{c['id']}"):
                                reativar_colaborador(c["id"])
                                st.success(f"{c['nome']} foi reativado.")
                                st.rerun()

# ===========================================================================
# ABA 2 — DIRETRIZES E ESCOPO DE CARGO (Hub de Transparência e Expectativas)
# ===========================================================================
with abas[IDX["alcadas"]]:
    st.subheader("Diretrizes e Expectativas de Função")
    st.caption("Critérios de Avaliação e Alinhamento")

    if papel == "COLABORADOR":
        colaborador_diretrizes = obter_colaborador(usuario["colaborador_id"]) if usuario.get("colaborador_id") else None
    else:
        colaborador_diretrizes = obter_colaborador(colaborador_foco_id) if colaborador_foco_id else None

    if not colaborador_diretrizes:
        st.info("Selecione um colaborador na barra lateral para ver as diretrizes do cargo.")
    else:
        st.markdown(
            f"**Nome Completo:** {colaborador_diretrizes['nome']} &nbsp;|&nbsp; "
            f"**Setor/Área:** {NOMES_AREAS.get(colaborador_diretrizes['area'], colaborador_diretrizes['area'])} &nbsp;|&nbsp; "
            f"**Nível Atual:** {colaborador_diretrizes['cargo']}",
            unsafe_allow_html=True,
        )

        st.divider()
        st.markdown("#### Repositório de Documentos Oficiais")
        if colaborador_diretrizes.get("documentos"):
            for doc in colaborador_diretrizes["documentos"]:
                if doc.get("link"):
                    st.markdown(f"- [{doc['nome']}]({doc['link']})")
                else:
                    st.write(f"- {doc['nome']}")
        else:
            st.caption("Nenhum documento cadastrado ainda para este cargo.")

        st.divider()
        st.markdown(
            f"**Maturidade Profissional:** A Nota {NOTA_MINIMA_ELEGIVEL:.1f} estabelece o padrão de "
            "excelência corporativa da Firma Produções, demonstrando que o profissional entrega suas "
            "demandas com total consistência, estabilidade e autonomia exigidas para o nível atual."
        )
        st.markdown(
            f"**Resultados do Período:** O alcance de no mínimo {NOTA_MINIMA_ELEGIVEL/5*100:.0f}% de "
            "aproveitamento das frentes avaliadas (equivalente à Nota Consolidada Final igual ou maior "
            f"que {NOTA_MINIMA_ELEGIVEL:.1f}) assegura a concessão integral do incentivo de performance "
            "mensal daquela fita técnica. Desvios temporários abaixo desta meta suspendem o incentivo e "
            "ativam automaticamente o Plano de Desenvolvimento Individual (PDI) focado em aceleração e "
            "suporte."
        )

# ===========================================================================
# ABA 3 — AVALIAÇÃO PÓS-EVENTO (CAMADA 2)
# ===========================================================================
if "pos_evento" in IDX:
    with abas[IDX["pos_evento"]]:
        st.subheader("Avaliação de Entrega Técnica")

        if not pode_lancar_pos_evento():
            st.info("Seu papel só permite visualização desta camada. O lançamento é feito pelo RH ou pelo Produtor de Eventos.")
        else:
            colabs = colaboradores_visiveis()
            if not colabs:
                st.warning("Nenhum colaborador disponível para avaliação na sua área.")
            else:
                labels = lista_colaboradores_labels(colabs)
                colaborador_id = st.selectbox("Colaborador avaliado", options=list(labels.keys()), format_func=lambda i: labels[i], key="campo_colab")
                colaborador = obter_colaborador(colaborador_id)
                trilha_auxiliar = cargo_e_auxiliar(colaborador["cargo"])
                st.caption(f"Trilha detectada automaticamente pelo cargo: {'Auxiliar' if trilha_auxiliar else 'Assistente/Técnico'} (cargo: {colaborador['cargo']})")

                with st.form("form_avaliacao_campo"):
                    projeto = st.text_input("Nome / identificação do projeto ou evento")
                    data_evento = st.date_input("Data do evento", value=date.today(), format="DD/MM/YYYY")

                    notas_itens, comentarios_itens, textos_itens = {}, {}, {}
                    for item_id, item in ITENS_CAMPO.items():
                        pergunta = item["auxiliar"] if trilha_auxiliar else item["assistente_tecnico"]
                        st.markdown(f"**{item['titulo']}**")
                        st.write(pergunta)
                        notas_itens[item_id] = st.slider("Nota", 1, 5, 3, key=f"nota_{item_id}", label_visibility="collapsed")
                        comentarios_itens[item_id] = st.text_area("Comentário / evidência (obrigatório se nota 1 ou 2)", key=f"coment_{item_id}", height=60)
                        textos_itens[item_id] = {"titulo": item["titulo"], "pergunta": pergunta}
                        st.write("")

                    st.markdown("**Filtro de Impacto e Alertas do Cliente Corporativo**")
                    nivel_impacto = st.radio(
                        "Selecione o nível de impacto observado",
                        options=list(NIVEIS_IMPACTO_CLIENTE.keys()),
                        format_func=lambda k: f"{NIVEIS_IMPACTO_CLIENTE[k]['label']} — {NIVEIS_IMPACTO_CLIENTE[k]['descricao']}",
                    )
                    enviado_campo = st.form_submit_button("Registrar avaliação pós-evento")

                    if enviado_campo:
                        if not projeto.strip():
                            st.error("Informe o nome/identificação do projeto.")
                        else:
                            media = media_avaliacao_campo(notas_itens)
                            gera_alerta = NIVEIS_IMPACTO_CLIENTE[nivel_impacto]["gera_alerta"]
                            criar_avaliacao_campo(
                                colaborador_id, projeto.strip(), data_evento, notas_itens, comentarios_itens,
                                textos_itens, nivel_impacto, media, lancado_por=usuario["email"],
                            )
                            if gera_alerta:
                                adicionar_alerta(
                                    colaborador_id,
                                    f"Alerta crítico gerado em {data_evento.strftime('%d/%m/%Y')} no projeto '{projeto}' — Nível Vermelho.",
                                )
                            st.success(f"Avaliação registrada. Média do evento: {media:.2f} / 5.0")
                            if gera_alerta:
                                st.error("Alerta vermelho crítico registrado no perfil do colaborador.")
                            st.rerun()

        st.divider()
        st.markdown("##### Avaliações pós-evento já lançadas (no seu escopo)")
        ids_visiveis = {c["id"] for c in colaboradores_visiveis()}
        todas_campo = [a for a in listar_avaliacoes_campo() if a["colaborador_id"] in ids_visiveis]
        if todas_campo:
            mapa_nomes = {c["id"]: c["nome"] for c in colaboradores_visiveis()}
            exibir_tabela(
                pd.DataFrame([
                    {"Colaborador": mapa_nomes.get(a["colaborador_id"], "—"), "Projeto": a["projeto"],
                     "Data evento": a["data_evento"].strftime("%d/%m/%Y"), "Média": a["media"],
                     "Impacto": NIVEIS_IMPACTO_CLIENTE[a["nivel_impacto"]]["label"]}
                    for a in todas_campo
                ])
            )
        else:
            st.caption("Nenhuma avaliação pós-evento no seu escopo ainda.")

# ===========================================================================
# ABA 4 — AVALIAÇÃO MENSAL UNIFICADA (CAMADA 3)
# ===========================================================================
if "mensal" in IDX:
    with abas[IDX["mensal"]]:
        st.subheader("Avaliação de Competências e Cultura")
        st.caption("50% Desempenho e Governança (Parte A) + 50% Cultura e Valores (Parte B)")

        if not pode_lancar_mensal():
            st.info("Seu papel só permite visualização desta camada. O lançamento é feito pelo RH ou pelo Head de área.")
        else:
            colabs = colaboradores_visiveis()
            if not colabs:
                st.warning("Nenhum colaborador disponível na sua área.")
            else:
                labels = lista_colaboradores_labels(colabs)
                colaborador_id = st.selectbox("Colaborador avaliado", options=list(labels.keys()), format_func=lambda i: labels[i], key="mensal_colab")
                colaborador = obter_colaborador(colaborador_id)
                criterios_cargo = AREAS.get(colaborador["area"], {}).get(colaborador["cargo"])

                periodo = st.text_input("Período de referência (AAAA-MM)", value=date.today().strftime("%Y-%m"))

                if not criterios_cargo:
                    st.error(f"Não há critérios do Capítulo 7 cadastrados para o cargo '{colaborador['cargo']}'.")
                else:
                    existente = obter_avaliacao_mensal(colaborador_id, periodo.strip())
                    if existente:
                        st.warning("Já existe uma ficha lançada para este período — salvar novamente irá substituí-la (upsert).")

                    with st.form("form_avaliacao_mensal"):
                        st.markdown(f"#### PARTE A — Desempenho e Governança ({colaborador['cargo']})")
                        notas_parte_a, comentarios_parte_a = {}, {}
                        for pilar, texto in criterios_cargo.items():
                            st.markdown(f"**{pilar}**")
                            st.write(texto)
                            notas_parte_a[pilar] = st.slider("Nota", 1, 5, 3, key=f"pa_{pilar}", label_visibility="collapsed")
                            comentarios_parte_a[pilar] = st.text_area("Comentário / evidência (obrigatório se nota 1 ou 2)", key=f"pa_coment_{pilar}", height=60)
                            st.write("")

                        st.markdown("#### PARTE B — Cultura e Valores Institucionais (fixo para todos os cargos)")
                        notas_parte_b, comentarios_parte_b = {}, {}
                        for valor, pergunta in VALORES_CULTURA.items():
                            st.markdown(f"**{valor}**")
                            st.write(pergunta)
                            notas_parte_b[valor] = st.slider("Nota", 1, 5, 3, key=f"pb_{valor}", label_visibility="collapsed")
                            comentarios_parte_b[valor] = st.text_area("Comentário / evidência (obrigatório se nota 1 ou 2)", key=f"pb_coment_{valor}", height=60)
                            st.write("")

                        enviado_mensal = st.form_submit_button("Fechar Ficha Mensal Unificada")

                        if enviado_mensal:
                            resultado = nota_mensal_unificada(notas_parte_a, notas_parte_b)
                            salvar_avaliacao_mensal(
                                colaborador_id, periodo.strip(), notas_parte_a, comentarios_parte_a,
                                dict(criterios_cargo), notas_parte_b, comentarios_parte_b, dict(VALORES_CULTURA),
                                resultado["media_parte_a"], resultado["media_parte_b"], resultado["nota_final_mensal"],
                                lancado_por=usuario["email"],
                            )
                            st.success(
                                f"Ficha Mensal Unificada fechada. Nota Desempenho: {resultado['media_parte_a']:.2f} | "
                                f"Nota Cultura: {resultado['media_parte_b']:.2f} | Nota Final Mensal: {resultado['nota_final_mensal']:.2f}"
                            )
                            st.rerun()

        st.divider()
        st.markdown("##### Fichas mensais já lançadas (no seu escopo)")
        ids_visiveis = {c["id"] for c in colaboradores_visiveis()}
        todas_mensais = [m for m in listar_avaliacoes_mensais() if m["colaborador_id"] in ids_visiveis]
        if todas_mensais:
            mapa_nomes = {c["id"]: c["nome"] for c in colaboradores_visiveis()}
            exibir_tabela(
                pd.DataFrame([
                    {"Colaborador": mapa_nomes.get(m["colaborador_id"], "—"), "Período": m["periodo"],
                     "Nota Desempenho (A)": m["media_parte_a"], "Nota Cultura (B)": m["media_parte_b"],
                     "Nota Final Mensal": m["nota_final_mensal"]}
                    for m in todas_mensais
                ])
            )
        else:
            st.caption("Nenhuma ficha mensal no seu escopo ainda.")

# ===========================================================================
if "historico" in IDX:
    with abas[IDX["historico"]]:
        st.subheader("Painel Consolidador e Elegibilidade")

        if papel == "COLABORADOR":
            colaborador_proprio_hist = obter_colaborador(usuario["colaborador_id"]) if usuario.get("colaborador_id") else None
            colabs = [colaborador_proprio_hist] if colaborador_proprio_hist else []
        else:
            colabs = colaboradores_visiveis()

        if not colabs:
            st.warning("Nenhum colaborador disponível no seu escopo.")
        else:
            if papel == "COLABORADOR":
                colaborador_id = colabs[0]["id"]
                colaborador = colabs[0]
            else:
                labels = lista_colaboradores_labels(colabs)
                colaborador_id = st.selectbox("Colaborador", options=list(labels.keys()), format_func=lambda i: labels[i], key="hist_colab")
                colaborador = obter_colaborador(colaborador_id)

            historico_mensal = listar_avaliacoes_mensais(colaborador_id=colaborador_id)
            historico_campo = listar_avaliacoes_campo(colaborador_id=colaborador_id)
            periodos_disponiveis = sorted({m["periodo"] for m in historico_mensal}, reverse=True)

            if not periodos_disponiveis:
                st.info("Ainda não há Ficha Mensal Unificada fechada para calcular o status deste período.")
            else:
                periodo_sel = st.selectbox("Período de apuração", options=periodos_disponiveis, key="hist_periodo")
                ficha_mensal = next((m for m in historico_mensal if m["periodo"] == periodo_sel), None)
                campo_periodo = [a for a in historico_campo if a["data_evento"].strftime("%Y-%m") == periodo_sel]
                notas_campo = [a["media"] for a in campo_periodo]

                resultado = nota_consolidada_periodo(ficha_mensal["nota_final_mensal"] if ficha_mensal else None, notas_campo)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Nota Ficha Mensal", f"{ficha_mensal['nota_final_mensal']:.2f}" if ficha_mensal else "—")
                c2.metric("Média Notas de Campo", f"{(sum(notas_campo)/len(notas_campo)):.2f}" if notas_campo else "—")
                c3.metric("Nota Consolidada do Período", f"{resultado['nota_final']:.2f}")
                c4.metric("Equivalente %", f"{resultado['percentual_equivalente']}%")

                if resultado["elegivel"]:
                    st.success(f"Status: {resultado['status']} — nota ≥ {NOTA_MINIMA_ELEGIVEL} ({NOTA_MINIMA_ELEGIVEL/5*100:.0f}%). Elegível ao recebimento do valor mensal/bônus.")
                else:
                    st.error(f"Status: {resultado['status']} — nota < {NOTA_MINIMA_ELEGIVEL} ({NOTA_MINIMA_ELEGIVEL/5*100:.0f}%). Alerta automático de abertura de PDI disparado.")

                if papel == "COLABORADOR" and not resultado["elegivel"]:
                    st.divider()
                    st.markdown("#### Plano de Desenvolvimento Individual (PDI)")
                    achados_proprio = coletar_criterios_baixa_nota(
                        notas_parte_a=ficha_mensal["notas_parte_a"] if ficha_mensal else {},
                        comentarios_parte_a=ficha_mensal["comentarios_parte_a"] if ficha_mensal else {},
                        criterios_texto_parte_a=ficha_mensal["criterios_parte_a"] if ficha_mensal else {},
                        notas_parte_b=ficha_mensal["notas_parte_b"] if ficha_mensal else {},
                        comentarios_parte_b=ficha_mensal["comentarios_parte_b"] if ficha_mensal else {},
                        criterios_texto_parte_b=ficha_mensal["criterios_parte_b"] if ficha_mensal else {},
                        itens_campo_lista=campo_periodo,
                    )
                    if st.button("Gerar meu PDI em PDF"):
                        nome_arquivo_proprio = f"PDI_{colaborador['nome'].replace(' ', '_')}_{periodo_sel}.pdf"
                        caminho_proprio = os.path.join(PASTA_PDIS, nome_arquivo_proprio)
                        gerar_pdf_pdi(caminho_proprio, colaborador["nome"], colaborador["cargo"], resultado["nota_final"], achados_proprio)
                        with open(caminho_proprio, "rb") as f:
                            st.download_button("Baixar meu PDI", data=f.read(), file_name=nome_arquivo_proprio, mime="application/pdf")

            st.divider()
            st.markdown("##### Elegibilidade a Ciclo de Promoção")
            eleg = checar_elegibilidade_promocao(colaborador["data_admissao"], colaborador["data_inicio_nivel"])
            ce1, ce2, ce3 = st.columns(3)
            ce1.metric("Tempo de empresa", f"{eleg.tempo_empresa_meses} mês(es)")
            ce2.metric("Tempo no nível atual", f"{eleg.tempo_nivel_meses} mês(es)")
            ce3.metric("Próxima janela formal", eleg.proxima_janela)

            if eleg.elegivel_geral:
                st.success("Colaborador elegível a participar do próximo ciclo formal de promoção por mérito.")
            else:
                st.warning("Colaborador ainda não elegível ao ciclo de promoção. Motivos:")
                for motivo in eleg.motivos_bloqueio:
                    st.write(f"- {motivo}")

            st.divider()
            st.markdown("##### Histórico completo do colaborador")
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                st.markdown("**Fichas mensais**")
                if historico_mensal:
                    exibir_tabela(pd.DataFrame([
                        {"Período": m["periodo"], "Desempenho": m["media_parte_a"], "Cultura": m["media_parte_b"], "Final": m["nota_final_mensal"]}
                        for m in historico_mensal
                    ]))
                else:
                    st.caption("Sem lançamentos.")
            with col_h2:
                st.markdown("**Avaliações pós-evento**")
                if historico_campo:
                    exibir_tabela(pd.DataFrame([
                        {"Projeto": a["projeto"], "Data": a["data_evento"].strftime("%d/%m/%Y"), "Média": a["media"], "Impacto": NIVEIS_IMPACTO_CLIENTE[a["nivel_impacto"]]["label"]}
                        for a in historico_campo
                    ]))
                else:
                    st.caption("Sem lançamentos.")

# ===========================================================================
# ABA 6 — PDI AUTOMÁTICO
# ===========================================================================
if "pdi" in IDX:
    with abas[IDX["pdi"]]:
        st.subheader(f"Plano de Desenvolvimento Individual — Gatilho em Nota < {NOTA_MINIMA_ELEGIVEL}")
        st.caption(f"Disponível apenas para períodos em que a Nota Consolidada ficou abaixo do gatilho de {NOTA_MINIMA_ELEGIVEL} ({NOTA_MINIMA_ELEGIVEL/5*100:.0f}%).")

        colabs = colaboradores_visiveis()
        if not colabs:
            st.warning("Nenhum colaborador disponível no seu escopo.")
        else:
            labels = lista_colaboradores_labels(colabs)
            colaborador_id = st.selectbox("Colaborador", options=list(labels.keys()), format_func=lambda i: labels[i], key="pdi_colab")
            colaborador = obter_colaborador(colaborador_id)

            historico_mensal = listar_avaliacoes_mensais(colaborador_id=colaborador_id)
            historico_campo = listar_avaliacoes_campo(colaborador_id=colaborador_id)
            periodos_disponiveis = sorted({m["periodo"] for m in historico_mensal}, reverse=True)

            if not periodos_disponiveis:
                st.info("Este colaborador ainda não possui Ficha Mensal Unificada lançada.")
            else:
                periodo_sel = st.selectbox("Período de apuração", options=periodos_disponiveis, key="pdi_periodo")
                ficha_mensal = next((m for m in historico_mensal if m["periodo"] == periodo_sel), None)
                campo_periodo = [a for a in historico_campo if a["data_evento"].strftime("%Y-%m") == periodo_sel]
                notas_campo = [a["media"] for a in campo_periodo]

                resultado = nota_consolidada_periodo(ficha_mensal["nota_final_mensal"] if ficha_mensal else None, notas_campo)
                st.metric("Nota Consolidada do Período", f"{resultado['nota_final']:.2f}")

                if resultado["elegivel"]:
                    st.success("Colaborador ELEGÍVEL neste período — PDI automático não é disparado.")
                else:
                    st.error("Colaborador NÃO ELEGÍVEL — PDI automático disponível para geração.")

                    achados = coletar_criterios_baixa_nota(
                        notas_parte_a=ficha_mensal["notas_parte_a"] if ficha_mensal else {},
                        comentarios_parte_a=ficha_mensal["comentarios_parte_a"] if ficha_mensal else {},
                        criterios_texto_parte_a=ficha_mensal["criterios_parte_a"] if ficha_mensal else {},
                        notas_parte_b=ficha_mensal["notas_parte_b"] if ficha_mensal else {},
                        comentarios_parte_b=ficha_mensal["comentarios_parte_b"] if ficha_mensal else {},
                        criterios_texto_parte_b=ficha_mensal["criterios_parte_b"] if ficha_mensal else {},
                        itens_campo_lista=campo_periodo,
                    )

                    st.markdown(f"**Critérios com nota 1 ou 2 identificados: {len(achados)}**")
                    for a in achados:
                        st.write(f"- **{a['pilar']}** (nota {a['nota']}) — {a['origem']}")

                    if st.button("Gerar PDI em PDF", type="primary"):
                        nome_arquivo = f"PDI_{colaborador['nome'].replace(' ', '_')}_{periodo_sel}.pdf"
                        caminho = os.path.join(PASTA_PDIS, nome_arquivo)
                        with st.spinner("Gerando relatório de PDI..."):
                            gerar_pdf_pdi(caminho, colaborador["nome"], colaborador["cargo"], resultado["nota_final"], achados)
                        st.success("PDI gerado com sucesso.")
                        with open(caminho, "rb") as f:
                            st.download_button("Baixar PDI em PDF", data=f.read(), file_name=nome_arquivo, mime="application/pdf")

# ===========================================================================
# ABA 7 — ADMINISTRAÇÃO (somente RH)
# ===========================================================================
if papel == "RH":
    with abas[IDX["admin"]]:
        st.subheader("Dossiê do Colaborador")
        st.caption("Cadastro e edição centralizados — exclusivo do RH/CEO. O dossiê fica sempre editável depois de criado.")

        colabs_prontuario = listar_colaboradores(incluir_inativos=True)
        OPCAO_NOVO_PRONTUARIO = "+ Cadastrar novo colaborador"
        labels_prontuario = {OPCAO_NOVO_PRONTUARIO: OPCAO_NOVO_PRONTUARIO}
        for c in colabs_prontuario:
            sufixo = "" if c["ativo"] else " (arquivado)"
            labels_prontuario[c["id"]] = f"{c['nome']} — {c['cargo']}{sufixo}"

        selecao_prontuario = st.selectbox(
            "Colaborador",
            options=list(labels_prontuario.keys()),
            format_func=lambda i: labels_prontuario[i],
            key="admin_prontuario_sel",
        )
        modo_criacao_prontuario = selecao_prontuario == OPCAO_NOVO_PRONTUARIO
        dados_existentes_prontuario = None if modo_criacao_prontuario else obter_colaborador(selecao_prontuario)
        sufixo_key = "novo" if modo_criacao_prontuario else selecao_prontuario

        with st.form(f"form_prontuario_admin_{sufixo_key}"):
            st.markdown("##### Dados Básicos")
            nome_pront = st.text_input(
                "Nome Completo",
                value=dados_existentes_prontuario["nome"] if dados_existentes_prontuario else "",
                key=f"pront_nome_{sufixo_key}",
            )
            areas_disponiveis = list(AREAS.keys())
            area_default = dados_existentes_prontuario["area"] if dados_existentes_prontuario else areas_disponiveis[0]
            area_pront = st.selectbox(
                "Setor / Área", options=areas_disponiveis, format_func=lambda a: NOMES_AREAS.get(a, a),
                index=areas_disponiveis.index(area_default) if area_default in areas_disponiveis else 0,
                key=f"pront_area_{sufixo_key}",
            )
            cargos_disponiveis = list(AREAS[area_pront].keys())
            cargo_default = (
                dados_existentes_prontuario["cargo"]
                if dados_existentes_prontuario and dados_existentes_prontuario["cargo"] in cargos_disponiveis
                else cargos_disponiveis[0]
            )
            cargo_pront = st.selectbox(
                "Função / Nível", options=cargos_disponiveis,
                index=cargos_disponiveis.index(cargo_default),
                key=f"pront_cargo_{sufixo_key}",
            )

            if modo_criacao_prontuario:
                data_admissao_pront = st.date_input("Data de admissão", value=date.today(), max_value=date.today(), format="DD/MM/YYYY", key=f"pront_admissao_{sufixo_key}")
                data_inicio_nivel_pront = st.date_input("Data de início no nível atual", value=date.today(), max_value=date.today(), format="DD/MM/YYYY", key=f"pront_inicio_nivel_{sufixo_key}")

            st.divider()
            st.markdown("##### Bloco de Vínculo de Arquivos — até 5 documentos")
            st.caption("Ex.: Descrição de Cargo, Entregáveis da Função, Pilares da Função.")
            docs_existentes = dados_existentes_prontuario["documentos"] if dados_existentes_prontuario else []
            novos_docs_pront = []
            for i in range(5):
                nome_doc_atual = docs_existentes[i]["nome"] if i < len(docs_existentes) else ""
                link_doc_atual = docs_existentes[i].get("link", "") if i < len(docs_existentes) else ""
                col_doc_nome, col_doc_link = st.columns(2)
                with col_doc_nome:
                    nome_doc_pront = st.text_input(f"Nome do Documento #{i+1}", value=nome_doc_atual, key=f"pront_doc_nome_{sufixo_key}_{i}")
                with col_doc_link:
                    link_doc_pront = st.text_input("Link Opcional da Nuvem", value=link_doc_atual, key=f"pront_doc_link_{sufixo_key}_{i}")
                if nome_doc_pront.strip():
                    novos_docs_pront.append({"nome": nome_doc_pront.strip(), "link": link_doc_pront.strip()})

            rotulo_botao_pront = "Cadastrar colaborador" if modo_criacao_prontuario else "Salvar alterações"
            if st.form_submit_button(rotulo_botao_pront):
                if not nome_pront.strip():
                    st.error("Informe o nome do colaborador.")
                else:
                    if modo_criacao_prontuario:
                        alvo_id_pront = criar_colaborador(
                            nome_pront.strip(), area_pront, cargo_pront, data_admissao_pront, data_inicio_nivel_pront
                        )
                    else:
                        atualizar_dados_basicos_colaborador(selecao_prontuario, nome_pront.strip(), area_pront, cargo_pront)
                        alvo_id_pront = selecao_prontuario
                    atualizar_documentos(alvo_id_pront, novos_docs_pront)
                    st.success(f"Dossiê de {nome_pront.strip()} salvo com sucesso.")
                    st.rerun()

        if not modo_criacao_prontuario:
            st.divider()
            st.markdown("##### Bloco Gallup — Top 5 Talentos")
            st.caption("Independente do restante do dossiê: salvar aqui não altera nome, área, cargo ou documentos.")
            with st.form(f"form_gallup_admin_{sufixo_key}"):
                gallup_existente = dados_existentes_prontuario["gallup_top5"] if dados_existentes_prontuario else []
                novo_gallup_pront = []
                for i in range(5):
                    valor_atual = gallup_existente[i] if i < len(gallup_existente) else ""
                    novo_gallup_pront.append(st.text_input(f"Talento Gallup #{i+1}", value=valor_atual, key=f"pront_gallup_{sufixo_key}_{i}"))
                if st.form_submit_button("Salvar Talentos Gallup"):
                    atualizar_gallup(selecao_prontuario, [g.strip() for g in novo_gallup_pront if g.strip()])
                    st.success("Talentos Gallup atualizados.")
                    st.rerun()
        else:
            st.caption("Cadastre o colaborador primeiro — o Bloco Gallup fica disponível depois, ao selecioná-lo na lista acima.")

        st.divider()
        st.markdown("##### Link Institucional do Teste Gallup")
        link_atual_gallup = obter_configuracao("link_teste_gallup", LINK_GALLUP_PADRAO)
        novo_link_gallup = st.text_input("URL exibida ao colaborador para realizar o teste", value=link_atual_gallup)
        if st.button("Salvar link do teste Gallup"):
            definir_configuracao("link_teste_gallup", novo_link_gallup.strip() or LINK_GALLUP_PADRAO)
            st.success("Link do teste Gallup atualizado.")
            st.rerun()

        st.divider()
        st.subheader("Administração de Usuários")
        st.caption("Crie acessos para Heads de área e para os próprios colaboradores.")

        with st.form("form_novo_usuario", clear_on_submit=True):
            nome_u = st.text_input("Nome do usuário")
            email_u = st.text_input("E-mail de login")
            senha_u = st.text_input("Senha provisória", type="password")
            papel_u = st.selectbox("Papel", options=["RH", "HEAD", "PRODUTOR", "COLABORADOR"])

            area_u = None
            colaborador_u = None
            if papel_u == "HEAD":
                area_u = st.selectbox("Área sob responsabilidade", options=list(AREAS.keys()), format_func=lambda a: NOMES_AREAS.get(a, a))
                st.caption("Head de Área: visualiza sua equipe e lança apenas a Avaliação Mensal (5 Pilares + Cultura).")
            elif papel_u == "PRODUTOR":
                st.caption("Produtor de Eventos: visualiza colaboradores de todas as áreas e lança apenas a Avaliação Pós-Evento (Campo). Não enxerga Avaliações Mensais.")
            elif papel_u == "COLABORADOR":
                todos_colabs = listar_colaboradores()
                if todos_colabs:
                    mapa = {c["id"]: f"{c['nome']} — {c['cargo']}" for c in todos_colabs}
                    colaborador_u = st.selectbox("Vincular ao prontuário de", options=list(mapa.keys()), format_func=lambda i: mapa[i])
                else:
                    st.warning("Cadastre um colaborador no Dossiê do Colaborador (acima) antes de criar este tipo de acesso.")

            criar = st.form_submit_button("Criar usuário")
            if criar:
                if not (nome_u.strip() and email_u.strip() and senha_u):
                    st.error("Preencha nome, e-mail e senha.")
                elif papel_u == "COLABORADOR" and not colaborador_u:
                    st.error("Selecione o prontuário a vincular.")
                else:
                    try:
                        criar_usuario(nome_u, email_u, senha_u, papel_u, area=area_u, colaborador_id=colaborador_u)
                        st.success(f"Usuário '{nome_u}' criado com sucesso.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Não foi possível criar o usuário (e-mail já cadastrado?). Detalhe: {e}")

        st.divider()
        st.markdown("##### Usuários cadastrados")
        usuarios_existentes = listar_usuarios()
        mapa_colabs = {c["id"]: c["nome"] for c in listar_colaboradores()}
        linhas = []
        for u in usuarios_existentes:
            escopo = "—"
            if u["papel"] == "HEAD":
                escopo = NOMES_AREAS.get(u["area"], u["area"])
            elif u["papel"] == "PRODUTOR":
                escopo = "Todas as áreas (eventos)"
            elif u["papel"] == "COLABORADOR":
                escopo = mapa_colabs.get(u["colaborador_id"], "—")
            linhas.append({"Nome": u["nome"], "E-mail": u["email"], "Papel": u["papel"], "Escopo": escopo})
        exibir_tabela(pd.DataFrame(linhas))

        with st.expander("Remover usuário"):
            if usuarios_existentes:
                mapa_u = {u["id"]: f"{u['nome']} ({u['email']})" for u in usuarios_existentes if u["id"] != usuario["id"]}
                if mapa_u:
                    alvo = st.selectbox("Selecione o usuário a remover", options=list(mapa_u.keys()), format_func=lambda i: mapa_u[i])
                    if st.button("Remover acesso", type="secondary"):
                        excluir_usuario(alvo)
                        st.success("Usuário removido.")
                        st.rerun()
                else:
                    st.caption("Não há outros usuários para remover.")
