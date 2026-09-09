# Firma Produções — Sistema de Governança de RH, KPIs e Avaliação

Protótipo em **Python + Streamlit**, com banco de dados simulado em memória
(`st.session_state`), implementando as regras de negócio descritas no
documento de governança:

- Prontuário do colaborador com **Top 5 Gallup** fixo
- **Alçadas financeiras** e fronteiras corporativas (consulta de bastidores)
- **Camada 2** — Avaliação Pós-Evento (gabarito de campo, texto muda pela trilha Auxiliar x Assistente/Técnico)
- **Camada 3** — Avaliação Mensal Unificada (50% Desempenho por cargo/nível + 50% Cultura, fixo)
- **Gatilho financeiro** → nota consolidada ≥ 4.0 (80%) = ELEGÍVEL; abaixo disso, dispara alerta de PDI
  (ajustável em 1 linha — veja `NOTA_MINIMA_ELEGIVEL` na Seção 1 do código)
- **Elegibilidade a promoção**: 1 ano de empresa + 6 meses de interstício no nível + janelas de Junho/Dezembro
- **Gerador automático de PDI em PDF**, com plano de ação por critério que tirou nota 1 ou 2

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app_firma.py
```

O app abre em `http://localhost:8501`.

## Sobre o gerador de PDI

Por padrão o sistema roda **100% offline**, usando templates internos de
plano de ação por pilar/valor (não depende de nenhuma API externa).

Se você quiser que o texto do plano de ação seja redigido por um modelo de
IA generativa (mais personalizado ao comentário do gestor), defina a
variável de ambiente `ANTHROPIC_API_KEY` antes de iniciar o app:

```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"
streamlit run app_firma.py
```

Se a chave não estiver definida, ou se a chamada à API falhar por qualquer
motivo, o sistema cai automaticamente de volta para o modo offline — o app
nunca quebra por falta de chave.

## Estrutura do arquivo

Este é um **arquivo único autocontido** (`app_firma.py`), dividido em 4
seções internas comentadas, para facilitar leitura e manutenção:

1. **Dados** — banco de critérios do Capítulo 7 (por área/cargo/nível),
   alçadas, gabarito de campo e valores institucionais.
2. **Motor de cálculo** — médias ponderadas, gatilho de elegibilidade (4.0 = 80%), elegibilidade
   a promoção.
3. **Gerador de PDI** — templates de ação + chamada opcional à API +
   exportação em PDF (reportlab).
4. **Aplicação Streamlit** — interface com as 6 abas do sistema.

## Limitações do protótipo (a evoluir antes de produção)

- Os dados são **perdidos ao reiniciar a sessão** (não há banco persistente).
  Para produção, trocar `st.session_state` por um banco real (Postgres,
  SQLite, etc.) mantendo as mesmas funções do motor de cálculo.
- Não há controle de usuários/login — qualquer pessoa com acesso ao app
  pode lançar avaliações. Adicionar autenticação antes de publicar.
- A "Nota Consolidada do Período" pondera igualmente a Ficha Mensal e a
  média das avaliações de campo do mês, pois o documento de governança não
  especificou um peso diferente entre as duas fontes — ajustar a função
  `nota_consolidada_periodo()` se a regra oficial for outra.
