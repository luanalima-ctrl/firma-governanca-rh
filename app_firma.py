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
"""
dados_firma.py
Banco de dados estático (constantes de negócio) da Firma Produções.

Este módulo NÃO contém lógica de cálculo nem interface. Ele apenas guarda,
em estruturas Python, o texto oficial do Capítulo 7 (critérios por cargo/nível),
o gabarito de campo pós-evento, os valores institucionais e as regras de
alçada financeira, exatamente como especificado no documento de governança.
"""

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
        "label": "🟢 Nível Verde",
        "descricao": (
            "O trabalho elevou o nível de satisfação do cliente corporativo / "
            "agregou valor ao evento."
        ),
        "gera_alerta": False,
    },
    "amarelo": {
        "label": "🟡 Nível Amarelo",
        "descricao": (
            "O trabalho foi neutro. Cumpriu a obrigação sem gerar atritos ou "
            "impactos perceptíveis."
        ),
        "gera_alerta": False,
    },
    "laranja": {
        "label": "🟠 Nível Laranja",
        "descricao": (
            "Ocorreu um erro técnico ou de postura leve que gerou cobrança "
            "da agência/produção."
        ),
        "gera_alerta": False,
    },
    "vermelho": {
        "label": "🔴 Nível Vermelho (Crítico)",
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

# ---- 🟥 ÁREA: LED ----------------------------------------------------------
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
    AREAS["LED"][f"Técnico de LED {_n}"] = dict(_tecnico_led)

# ---- 🔊 ÁREA: SOM ----------------------------------------------------------
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
    AREAS["SOM"][f"Assistente de Som {_n}"] = dict(_assistente_som)
    AREAS["SOM"][f"Técnico de Som {_n}"] = dict(_tecnico_som)

# ---- 💡 ÁREA: ILUMINAÇÃO ---------------------------------------------------
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
    AREAS["ILUMINACAO"][f"Assistente de Iluminação {_n}"] = dict(_assistente_luz)
    AREAS["ILUMINACAO"][f"Técnico de Iluminação {_n}"] = dict(_tecnico_luz)

# ---- 💻 ÁREA: HOUSE / TECNOLOGIA -------------------------------------------
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
    AREAS["HOUSE_TECNOLOGIA"][f"Assistente de House/Tecnologia {_n}"] = dict(_assistente_house)
    AREAS["HOUSE_TECNOLOGIA"][f"Técnico de House/Tecnologia {_n}"] = dict(_tecnico_house)

# ---- 🔌 ÁREA: ELÉTRICA -----------------------------------------------------
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

# ---- 🏗️ ÁREA: ESTRUTURA ----------------------------------------------------
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
    "LED": "🟥 LED",
    "SOM": "🔊 Som",
    "ILUMINACAO": "💡 Iluminação",
    "HOUSE_TECNOLOGIA": "💻 House / Tecnologia",
    "ELETRICA": "🔌 Elétrica",
    "ESTRUTURA": "🏗️ Estrutura",
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
"""
db.py
Camada de persistência do sistema de governança da Firma Produções.

Suporta dois backends, escolhidos automaticamente por variável de ambiente:

  • SQLite local (padrão) — arquivo firma_rh.db na mesma pasta do app.
    Ótimo para rodar localmente, mas em plataformas de hospedagem com disco
    efêmero (ex.: Streamlit Community Cloud) os dados somem a cada reinício
    do container.

  • Postgres remoto — ativado automaticamente se a variável de ambiente
    DATABASE_URL estiver definida (ex.: connection string do Neon, Supabase,
    Railway, RDS etc.). Os dados passam a persistir de verdade, independente
    de reinícios do app.

Todas as funções públicas deste módulo (criar_colaborador, listar_*,
salvar_avaliacao_mensal etc.) têm exatamente o mesmo comportamento nos dois
backends — o resto do sistema (app_firma.py) não precisa saber qual está em
uso. As mesmas strings SQL (escritas com placeholder '?') funcionam nos dois
bancos: no Postgres, o wrapper de conexão troca '?' por '%s' automaticamente
antes de executar.

Datas são guardadas em formato ISO (YYYY-MM-DD) e listas/dicts são
serializados em JSON dentro de colunas TEXT.
"""


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

            CREATE TABLE IF NOT EXISTS colaboradores (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                area TEXT NOT NULL,
                cargo TEXT NOT NULL,
                data_admissao TEXT NOT NULL,
                data_inicio_nivel TEXT NOT NULL,
                gallup_top5 TEXT NOT NULL DEFAULT '[]',
                alertas TEXT NOT NULL DEFAULT '[]'
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

def criar_colaborador(nome, area, cargo, data_admissao, data_inicio_nivel, gallup_top5=None) -> str:
    novo_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO colaboradores
               (id, nome, area, cargo, data_admissao, data_inicio_nivel, gallup_top5, alertas)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                novo_id, nome, area, cargo,
                _iso(data_admissao), _iso(data_inicio_nivel),
                _dumps(gallup_top5 or []), _dumps([]),
            ),
        )
    return novo_id


def listar_colaboradores(area: Optional[str] = None, apenas_id: Optional[str] = None) -> list[dict]:
    with get_conn() as conn:
        if apenas_id:
            rows = conn.execute("SELECT * FROM colaboradores WHERE id = ?", (apenas_id,)).fetchall()
        elif area:
            rows = conn.execute("SELECT * FROM colaboradores WHERE area = ? ORDER BY nome", (area,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM colaboradores ORDER BY nome").fetchall()
    return [_row_para_colaborador(r) for r in rows]


def obter_colaborador(colaborador_id: str) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM colaboradores WHERE id = ?", (colaborador_id,)).fetchone()
    return _row_para_colaborador(row) if row else None


def atualizar_gallup(colaborador_id: str, gallup_top5: list):
    with get_conn() as conn:
        conn.execute(
            "UPDATE colaboradores SET gallup_top5 = ? WHERE id = ?",
            (_dumps(gallup_top5), colaborador_id),
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
"""
auth.py
Autenticação e controle de acesso por papel (RH, HEAD, PRODUTOR, COLABORADOR).

Papéis:
  RH           -> acesso total: todas as áreas, cadastro de colaboradores,
                  todas as avaliações, visão unificada de relatórios e
                  consolidações financeiras, aba de Administração de usuários.
  HEAD         -> escopo travado na própria área: visualiza sua equipe e
                  lança exclusivamente a Avaliação Mensal (5 Pilares +
                  Cultura). NÃO lança Avaliação Pós-Evento (só visualiza).
  PRODUTOR     -> "Produtor de Eventos": visualiza os colaboradores (todas
                  as áreas, pois um evento reúne equipes de áreas diferentes)
                  e lança exclusivamente a Avaliação Pós-Evento (Campo).
                  NÃO enxerga nem edita Avaliações Mensais, Histórico
                  consolidado ou PDI (que derivam da nota mensal).
  COLABORADOR  -> somente leitura do próprio prontuário/histórico/PDI;
                  não lança avaliações nem edita nada.

Senhas são armazenadas como hash bcrypt — nunca em texto puro.
"""


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
"""
motor_calculo.py
Regras matemáticas e de elegibilidade do sistema de governança da Firma
Produções. Mantido isolado da interface (Streamlit) para poder ser testado
de forma independente.
"""


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
"""
gerador_pdi.py
Gera o Plano de Desenvolvimento Individual (PDI) automático quando a Nota
Consolidada do Período é MENOR que 3.5.

Duas engrenagens de geração de texto para o Plano de Ação:

1. Modo ONLINE (opcional): se a variável de ambiente ANTHROPIC_API_KEY
   estiver definida, o sistema chama a API da Anthropic para redigir ações
   cirúrgicas e a métrica de sucesso a partir do critério oficial e do fato
   gerador (comentário do gestor).
2. Modo OFFLINE (padrão, sem dependências externas): usa um banco de
   templates por pilar/valor para montar uma ação prática coerente com o
   critério que falhou, garantindo que o sistema funcione mesmo sem chave de
   API configurada.

O relatório final é sempre renderizado em PDF com reportlab, seguindo
exatamente as seções do template oficial fornecido pela governança de RH.
"""


import os
from datetime import date
from typing import Optional

import requests

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
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
        topMargin=2 * cm,
        bottomMargin=2 * cm,
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

    story.append(Paragraph("📝 PLANO DE DESENVOLVIMENTO INDIVIDUAL (PDI)", titulo_style))
    story.append(Paragraph("Relatório de Melhoria Contínua Automatizado — Firma Produções", subtitulo_style))

    hoje = date.today().strftime("%d/%m/%Y")

    dados_cabecalho = [
        ["Data de Emissão:", hoje],
        ["Colaborador:", colaborador_nome],
        ["Cargo / Nível:", cargo_nivel],
        ["Aproveitamento do Período:", f"🔴 NÃO ELEGÍVEL ({nota_final:.1f} de 5.0)"],
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
    story.append(Paragraph("🔍 1. DIAGNÓSTICO: O QUE NÃO FOI ATINGIDO NO PERÍODO", heading_style))

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
    story.append(Paragraph("🎯 2. PLANO DE AÇÃO: PONTOS DE MELHORIA PARA OS PRÓXIMOS 30 DIAS", heading_style))

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
    story.append(Paragraph("📝 3. COMPROMISSO DE EVOLUÇÃO", heading_style))
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

    doc.build(story)
    return caminho_saida


# ============================================================
# SEÇÃO 6/6 — APLICAÇÃO STREAMLIT (app_firma.py original)
# ============================================================
# -*- coding: utf-8 -*-
"""
app_firma.py — v2 (com login e banco de dados persistente)
Sistema de Governança de RH, KPIs e Avaliação — Firma Produções

Diferenças em relação ao protótipo v1 (em memória):
  • Dados agora persistem em SQLite (arquivo firma_rh.db) via módulo db.py
  • Login obrigatório com 3 papéis via módulo auth.py:
      - RH: acesso total a todas as áreas e à Administração de usuários
      - HEAD: acesso travado à própria área (Head de área/Supervisor)
      - COLABORADOR: acesso somente-leitura ao próprio prontuário/histórico

Execução local:
    pip install -r requirements.txt
    streamlit run app_firma.py

Na primeira execução, se não houver nenhum usuário cadastrado, o sistema
cria automaticamente um usuário RH padrão e mostra a credencial na tela de
login (troque a senha assim que possível criando um novo usuário RH e
removendo o padrão, ou defina as variáveis de ambiente FIRMA_ADMIN_EMAIL /
FIRMA_ADMIN_SENHA antes de rodar pela primeira vez).
"""


import os
import uuid
from datetime import date, datetime

import streamlit as st
import pandas as pd


# ---------------------------------------------------------------------------
# Configuração da página e inicialização do banco
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Firma Produções | Governança de RH",
    page_icon="🎛️",
    layout="wide",
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
    st.title("🎛️ Firma Produções — Governança de RH")
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
        # Não enxerga nem edita Avaliação Mensal, Histórico consolidado ou
        # PDI — todos derivados (direta ou indiretamente) da nota mensal.
        return ["prontuario", "alcadas", "pos_evento"]
    return []  # COLABORADOR usa o painel próprio, tratado antes deste ponto


def lista_colaboradores_labels(colabs: list[dict]) -> dict:
    return {c["id"]: f"{c['nome']} — {c['cargo']}" for c in colabs}


# ---------------------------------------------------------------------------
# Cabeçalho + sidebar
# ---------------------------------------------------------------------------

st.title("🎛️ Firma Produções — Governança de RH, KPIs e Avaliação")

with st.sidebar:
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
    modo_ia = "🟢 Online (ANTHROPIC_API_KEY detectada)" if os.environ.get("ANTHROPIC_API_KEY") else "⚪ Offline (templates internos)"
    st.caption(f"Gerador de PDI: {modo_ia}")
    st.caption(f"Banco de dados: `{os.path.basename(DB_PATH)}`")

# ===========================================================================
# VISÃO DO COLABORADOR — painel próprio, somente leitura
# ===========================================================================
if papel == "COLABORADOR":
    if not usuario.get("colaborador_id"):
        st.error("Sua conta de colaborador não está vinculada a nenhum prontuário. Fale com o RH.")
        st.stop()

    colaborador = obter_colaborador(usuario["colaborador_id"])
    if not colaborador:
        st.error("Prontuário vinculado não encontrado. Fale com o RH.")
        st.stop()

    st.subheader(f"👋 Bem-vindo(a), {colaborador['nome']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Cargo / Nível", colaborador["cargo"])
    c2.metric("Área", NOMES_AREAS.get(colaborador["area"], colaborador["area"]))
    c3.metric("Tempo de empresa", f"{meses_entre(colaborador['data_admissao'])} mês(es)")

    if colaborador.get("gallup_top5"):
        st.markdown("**Seu Top 5 Gallup:** " + " · ".join(f"`{g}`" for g in colaborador["gallup_top5"]))

    if colaborador.get("alertas"):
        for al in colaborador["alertas"]:
            st.error(al)

    st.divider()
    st.markdown("#### 📜 Seu histórico de avaliações")

    historico_mensal = listar_avaliacoes_mensais(colaborador_id=colaborador["id"])
    historico_campo = listar_avaliacoes_campo(colaborador_id=colaborador["id"])

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.markdown("**Fichas mensais**")
        if historico_mensal:
            st.dataframe(
                pd.DataFrame([
                    {"Período": m["periodo"], "Desempenho": m["media_parte_a"],
                     "Cultura": m["media_parte_b"], "Final": m["nota_final_mensal"]}
                    for m in historico_mensal
                ]), width='stretch', hide_index=True,
            )
        else:
            st.caption("Sem lançamentos ainda.")
    with col_h2:
        st.markdown("**Avaliações pós-evento**")
        if historico_campo:
            st.dataframe(
                pd.DataFrame([
                    {"Projeto": a["projeto"], "Data": a["data_evento"].strftime("%d/%m/%Y"),
                     "Média": a["media"], "Impacto": NIVEIS_IMPACTO_CLIENTE[a["nivel_impacto"]]["label"]}
                    for a in historico_campo
                ]), width='stretch', hide_index=True,
            )
        else:
            st.caption("Sem lançamentos ainda.")

    st.divider()
    st.markdown("#### 🎯 Gatilho financeiro e PDI")
    periodos = sorted({m["periodo"] for m in historico_mensal}, reverse=True)
    if not periodos:
        st.info("Ainda não há Ficha Mensal Unificada fechada para calcular seu status.")
        st.stop()

    periodo_sel = st.selectbox("Período", options=periodos)
    ficha_mensal = next((m for m in historico_mensal if m["periodo"] == periodo_sel), None)
    campo_periodo = [a for a in historico_campo if a["data_evento"].strftime("%Y-%m") == periodo_sel]
    notas_campo = [a["media"] for a in campo_periodo]
    resultado = nota_consolidada_periodo(ficha_mensal["nota_final_mensal"] if ficha_mensal else None, notas_campo)

    c1, c2 = st.columns(2)
    c1.metric("Nota Consolidada do Período", f"{resultado['nota_final']:.2f}")
    c2.metric("Equivalente %", f"{resultado['percentual_equivalente']}%")

    if resultado["elegivel"]:
        st.success(f"✅ Status: {resultado['status']} — parabéns pelo desempenho no período!")
    else:
        st.error(f"🔴 Status: {resultado['status']} — abaixo do gatilho de {NOTA_MINIMA_ELEGIVEL} ({NOTA_MINIMA_ELEGIVEL/5*100:.0f}%).")
        achados = coletar_criterios_baixa_nota(
            notas_parte_a=ficha_mensal["notas_parte_a"] if ficha_mensal else {},
            comentarios_parte_a=ficha_mensal["comentarios_parte_a"] if ficha_mensal else {},
            criterios_texto_parte_a=ficha_mensal["criterios_parte_a"] if ficha_mensal else {},
            notas_parte_b=ficha_mensal["notas_parte_b"] if ficha_mensal else {},
            comentarios_parte_b=ficha_mensal["comentarios_parte_b"] if ficha_mensal else {},
            criterios_texto_parte_b=ficha_mensal["criterios_parte_b"] if ficha_mensal else {},
            itens_campo_lista=[{**a, "textos": a["textos"]} for a in campo_periodo],
        )
        if st.button("📄 Gerar meu PDI em PDF"):
            nome_arquivo = f"PDI_{colaborador['nome'].replace(' ', '_')}_{periodo_sel}.pdf"
            caminho = os.path.join(PASTA_PDIS, nome_arquivo)
            gerar_pdf_pdi(caminho, colaborador["nome"], colaborador["cargo"], resultado["nota_final"], achados)
            with open(caminho, "rb") as f:
                st.download_button("⬇️ Baixar meu PDI", data=f.read(), file_name=nome_arquivo, mime="application/pdf")

    st.stop()


# ===========================================================================
# VISÃO RH / HEAD — abas completas (escopo filtrado por área quando HEAD)
# ===========================================================================

TAB_SPECS = [
    ("prontuario", "📋 Prontuário"),
    ("alcadas", "🔐 Alçadas & Fronteiras"),
    ("pos_evento", "🏗️ Avaliação Pós-Evento"),
    ("mensal", "📊 Avaliação Mensal"),
    ("historico", "📈 Histórico & Elegibilidade"),
    ("pdi", "🤖 PDI Automático"),
    ("admin", "⚙️ Administração"),
]

chaves_visiveis = abas_visiveis_para_papel()
labels_visiveis = [label for chave, label in TAB_SPECS if chave in chaves_visiveis]
abas = st.tabs(labels_visiveis)
IDX = {chave: i for i, chave in enumerate(chaves_visiveis)}

# ===========================================================================
# ABA 1 — PRONTUÁRIO
# ===========================================================================
with abas[IDX["prontuario"]]:
    st.subheader("Prontuário do Colaborador")

    col_form, col_lista = st.columns([1, 1.3])

    with col_form:
        if pode_cadastrar_colaborador():
            st.markdown("##### ➕ Novo colaborador")
            with st.form("form_novo_colaborador", clear_on_submit=True):
                nome = st.text_input("Nome completo")
                if papel == "RH":
                    area_sel = st.selectbox("Área", options=list(AREAS.keys()), format_func=lambda a: NOMES_AREAS.get(a, a))
                else:
                    area_sel = usuario["area"]
                    st.text_input("Área", value=NOMES_AREAS.get(area_sel, area_sel), disabled=True)
                cargo_sel = st.selectbox("Cargo / Nível", options=list(AREAS[area_sel].keys()))
                data_admissao = st.date_input("Data de admissão", value=date.today(), max_value=date.today())
                data_inicio_nivel = st.date_input("Data de início no nível atual", value=date.today(), max_value=date.today())
                st.markdown("**Teste de Perfil Gallup — Top 5 Forças/Talentos**")
                gallup = []
                gcols = st.columns(5)
                for i in range(5):
                    with gcols[i]:
                        gallup.append(st.text_input(f"Força #{i+1}", key=f"gallup_novo_{i}"))
                enviado = st.form_submit_button("Salvar colaborador")

                if enviado:
                    if not nome.strip():
                        st.error("Informe o nome do colaborador.")
                    else:
                        novo_id = criar_colaborador(
                            nome.strip(), area_sel, cargo_sel, data_admissao, data_inicio_nivel,
                            [g.strip() for g in gallup if g.strip()],
                        )
                        st.success(f"Colaborador '{nome}' cadastrado com sucesso.")
                        st.rerun()
        else:
            st.info("Seu papel não permite cadastrar novos colaboradores.")

    with col_lista:
        st.markdown("##### 👥 Colaboradores visíveis para você")
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
                    if c.get("gallup_top5"):
                        st.write("**Top 5 Gallup:**")
                        st.write(" · ".join(f"`{g}`" for g in c["gallup_top5"]))
                    else:
                        st.caption("Teste Gallup ainda não registrado.")
                    for al in c.get("alertas", []):
                        st.error(al)

                    if pode_cadastrar_colaborador():
                        with st.popover("✏️ Editar Top 5 Gallup"):
                            novo_gallup = []
                            for i in range(5):
                                valor_atual = c["gallup_top5"][i] if i < len(c["gallup_top5"]) else ""
                                novo_gallup.append(st.text_input(f"Força #{i+1}", value=valor_atual, key=f"edit_gallup_{c['id']}_{i}"))
                            if st.button("Salvar Gallup", key=f"salvar_gallup_{c['id']}"):
                                atualizar_gallup(c["id"], [g.strip() for g in novo_gallup if g.strip()])
                                st.success("Perfil Gallup atualizado.")
                                st.rerun()

# ===========================================================================
# ABA 2 — ALÇADAS & FRONTEIRAS (somente leitura para todos os papéis)
# ===========================================================================
with abas[IDX["alcadas"]]:
    st.subheader("🔐 Limites de Autonomia e Alçadas (consulta de bastidores)")
    st.caption("Referência fixa de governança — não editável pela operação.")

    for grupo, info in ALCADAS.items():
        st.markdown(f"**{grupo}** — limite de aprovação: R$ {info['limite_aprovacao']:,.2f}")
        st.write(info["descricao"])
        st.divider()

    st.subheader("🧭 Fronteiras Corporativas (ordem obrigatória de decisão)")
    for linha in FRONTEIRAS_CORPORATIVAS:
        st.write(f"- {linha}")

    st.info(
        "Risco de vida ou queima de patrimônio (item 7) anula prazos operacionais e prevalece "
        "sobre qualquer outra diretriz da lista."
    )

# ===========================================================================
# ABA 3 — AVALIAÇÃO PÓS-EVENTO (CAMADA 2)
# ===========================================================================
with abas[IDX["pos_evento"]]:
    st.subheader("🏗️ Módulo Pós-Evento Corporativo (preencher em até 48h após o desmonte)")

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
                data_evento = st.date_input("Data do evento", value=date.today())

                notas_itens, comentarios_itens, textos_itens = {}, {}, {}
                for item_id, item in ITENS_CAMPO.items():
                    pergunta = item["auxiliar"] if trilha_auxiliar else item["assistente_tecnico"]
                    st.markdown(f"**{item['titulo']}**")
                    st.write(pergunta)
                    notas_itens[item_id] = st.slider("Nota", 1, 5, 3, key=f"nota_{item_id}", label_visibility="collapsed")
                    comentarios_itens[item_id] = st.text_area("Comentário / evidência (obrigatório se nota 1 ou 2)", key=f"coment_{item_id}", height=60)
                    textos_itens[item_id] = {"titulo": item["titulo"], "pergunta": pergunta}
                    st.write("")

                st.markdown("**⚠️ Filtro de Impacto e Alertas do Cliente Corporativo**")
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
                                f"🔴 Alerta crítico gerado em {data_evento.strftime('%d/%m/%Y')} no projeto '{projeto}' — Nível Vermelho.",
                            )
                        st.success(f"Avaliação registrada. Média do evento: {media:.2f} / 5.0")
                        if gera_alerta:
                            st.error("Alerta vermelho crítico registrado no perfil do colaborador.")
                        st.rerun()

    st.divider()
    st.markdown("##### 🗂️ Avaliações pós-evento já lançadas (no seu escopo)")
    ids_visiveis = {c["id"] for c in colaboradores_visiveis()}
    todas_campo = [a for a in listar_avaliacoes_campo() if a["colaborador_id"] in ids_visiveis]
    if todas_campo:
        mapa_nomes = {c["id"]: c["nome"] for c in colaboradores_visiveis()}
        st.dataframe(
            pd.DataFrame([
                {"Colaborador": mapa_nomes.get(a["colaborador_id"], "—"), "Projeto": a["projeto"],
                 "Data evento": a["data_evento"].strftime("%d/%m/%Y"), "Média": a["media"],
                 "Impacto": NIVEIS_IMPACTO_CLIENTE[a["nivel_impacto"]]["label"]}
                for a in todas_campo
            ]), width='stretch', hide_index=True,
        )
    else:
        st.caption("Nenhuma avaliação pós-evento no seu escopo ainda.")

# ===========================================================================
# ABA 4 — AVALIAÇÃO MENSAL UNIFICADA (CAMADA 3)
# ===========================================================================
if "mensal" in IDX:
    with abas[IDX["mensal"]]:
        st.subheader("📊 Avaliação Mensal Unificada (Reunião de 1:1)")
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
        st.markdown("##### 🗂️ Fichas mensais já lançadas (no seu escopo)")
        ids_visiveis = {c["id"] for c in colaboradores_visiveis()}
        todas_mensais = [m for m in listar_avaliacoes_mensais() if m["colaborador_id"] in ids_visiveis]
        if todas_mensais:
            mapa_nomes = {c["id"]: c["nome"] for c in colaboradores_visiveis()}
            st.dataframe(
                pd.DataFrame([
                    {"Colaborador": mapa_nomes.get(m["colaborador_id"], "—"), "Período": m["periodo"],
                     "Nota Desempenho (A)": m["media_parte_a"], "Nota Cultura (B)": m["media_parte_b"],
                     "Nota Final Mensal": m["nota_final_mensal"]}
                    for m in todas_mensais
                ]), width='stretch', hide_index=True,
            )
        else:
            st.caption("Nenhuma ficha mensal no seu escopo ainda.")

# ===========================================================================
# ABA 5 — HISTÓRICO & ELEGIBILIDADE
# ===========================================================================
if "historico" in IDX:
    with abas[IDX["historico"]]:
        st.subheader("📈 Histórico Consolidado, Gatilho Financeiro e Elegibilidade a Promoção")

        colabs = colaboradores_visiveis()
        if not colabs:
            st.warning("Nenhum colaborador disponível no seu escopo.")
        else:
            labels = lista_colaboradores_labels(colabs)
            colaborador_id = st.selectbox("Colaborador", options=list(labels.keys()), format_func=lambda i: labels[i], key="hist_colab")
            colaborador = obter_colaborador(colaborador_id)

            historico_mensal = listar_avaliacoes_mensais(colaborador_id=colaborador_id)
            historico_campo = listar_avaliacoes_campo(colaborador_id=colaborador_id)
            periodos_disponiveis = sorted({m["periodo"] for m in historico_mensal}, reverse=True)

            if not periodos_disponiveis:
                st.info("Este colaborador ainda não possui Ficha Mensal Unificada lançada.")
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
                    st.success(f"✅ Status: {resultado['status']} — nota ≥ {NOTA_MINIMA_ELEGIVEL} ({NOTA_MINIMA_ELEGIVEL/5*100:.0f}%). Elegível ao recebimento do valor mensal/bônus.")
                else:
                    st.error(f"🔴 Status: {resultado['status']} — nota < {NOTA_MINIMA_ELEGIVEL} ({NOTA_MINIMA_ELEGIVEL/5*100:.0f}%). Alerta automático de abertura de PDI disparado.")

            st.divider()
            st.markdown("##### 🪜 Elegibilidade a Ciclo de Promoção")
            eleg = checar_elegibilidade_promocao(colaborador["data_admissao"], colaborador["data_inicio_nivel"])
            ce1, ce2, ce3 = st.columns(3)
            ce1.metric("Tempo de empresa", f"{eleg.tempo_empresa_meses} mês(es)")
            ce2.metric("Tempo no nível atual", f"{eleg.tempo_nivel_meses} mês(es)")
            ce3.metric("Próxima janela formal", eleg.proxima_janela)

            if eleg.elegivel_geral:
                st.success("✅ Colaborador elegível a participar do próximo ciclo formal de promoção por mérito.")
            else:
                st.warning("⏳ Colaborador ainda não elegível ao ciclo de promoção. Motivos:")
                for motivo in eleg.motivos_bloqueio:
                    st.write(f"- {motivo}")

            st.divider()
            st.markdown("##### 📜 Histórico completo do colaborador")
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                st.markdown("**Fichas mensais**")
                if historico_mensal:
                    st.dataframe(pd.DataFrame([
                        {"Período": m["periodo"], "Desempenho": m["media_parte_a"], "Cultura": m["media_parte_b"], "Final": m["nota_final_mensal"]}
                        for m in historico_mensal
                    ]), width='stretch', hide_index=True)
                else:
                    st.caption("Sem lançamentos.")
            with col_h2:
                st.markdown("**Avaliações pós-evento**")
                if historico_campo:
                    st.dataframe(pd.DataFrame([
                        {"Projeto": a["projeto"], "Data": a["data_evento"].strftime("%d/%m/%Y"), "Média": a["media"], "Impacto": NIVEIS_IMPACTO_CLIENTE[a["nivel_impacto"]]["label"]}
                        for a in historico_campo
                    ]), width='stretch', hide_index=True)
                else:
                    st.caption("Sem lançamentos.")

# ===========================================================================
# ABA 6 — PDI AUTOMÁTICO
# ===========================================================================
if "pdi" in IDX:
    with abas[IDX["pdi"]]:
        st.subheader(f"🤖 Gerador Automático de PDI (Nota Consolidada < {NOTA_MINIMA_ELEGIVEL})")
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
                    st.success("✅ Colaborador ELEGÍVEL neste período — PDI automático não é disparado.")
                else:
                    st.error("🔴 Colaborador NÃO ELEGÍVEL — PDI automático disponível para geração.")

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

                    if st.button("📄 Gerar PDI em PDF", type="primary"):
                        nome_arquivo = f"PDI_{colaborador['nome'].replace(' ', '_')}_{periodo_sel}.pdf"
                        caminho = os.path.join(PASTA_PDIS, nome_arquivo)
                        with st.spinner("Gerando relatório de PDI..."):
                            gerar_pdf_pdi(caminho, colaborador["nome"], colaborador["cargo"], resultado["nota_final"], achados)
                        st.success("PDI gerado com sucesso.")
                        with open(caminho, "rb") as f:
                            st.download_button("⬇️ Baixar PDI em PDF", data=f.read(), file_name=nome_arquivo, mime="application/pdf")

# ===========================================================================
# ABA 7 — ADMINISTRAÇÃO (somente RH)
# ===========================================================================
if papel == "RH":
    with abas[IDX["admin"]]:
        st.subheader("⚙️ Administração de Usuários")
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
                    st.warning("Cadastre um colaborador na aba Prontuário antes de criar este tipo de acesso.")

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
        st.markdown("##### 👥 Usuários cadastrados")
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
        st.dataframe(pd.DataFrame(linhas), width='stretch', hide_index=True)

        with st.expander("🗑️ Remover usuário"):
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
