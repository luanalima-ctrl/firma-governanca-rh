# Gestão de Performance Operacional — Portal Corporativo Firma Prod.

Protótipo em **Python + Streamlit**, com persistência real (SQLite local ou
Postgres via `DATABASE_URL`), login por papel e identidade visual da marca.
Todo o sistema vive num único arquivo autocontido: `app_firma.py`.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app_firma.py
```

## Identidade visual

O tema visual agora é aplicado pelo **sistema de tema nativo do Streamlit**
(arquivo `.streamlit/config.toml`), não por CSS manual. Isso é importante:
tentativas anteriores de forçar cor via CSS não alcançavam os menus de
seleção, calendários e popovers, porque o Streamlit renderiza esses
elementos fora da área principal da página — resultando em texto branco
sobre fundo branco em alguns cantos. O tema nativo resolve isso de vez,
porque calcula automaticamente cores de texto legíveis para **todo**
componente, incluindo esses.

- Fundo: `#111111` · Texto: `#FFFFFF` · Cor primária/links: `#E12E2E`
- Tipografia: Montserrat (carregada via Google Fonts pelo próprio tema)
- Um CSS bem mais enxuto continua no `app_firma.py`, só para detalhes que
  o tema nativo não cobre (títulos e abas em caixa alta, botões em negrito).

**Por isso agora são dois arquivos no repositório:**
```
app_firma.py
.streamlit/
└── config.toml
```
Sem o `config.toml` na pasta `.streamlit/`, o app roda normalmente mas
volta a usar o tema claro padrão do Streamlit — não vai dar erro, mas
perde a identidade visual da marca. Confira que a estrutura de pastas no
GitHub ficou exatamente assim (a pasta `.streamlit` com o ponto na frente
é obrigatória, é o nome que o Streamlit procura).

- Logotipo oficial ("FIRMA PROD.", versão branca) no topo da barra lateral
  e da tela de login; símbolo da marca (o "F" com o ponto vermelho) como
  favicon da aba do navegador.
- PDI em PDF sai no **papel timbrado oficial** da Firma (logo, marca d'água
  e rodapé de contato em todas as páginas).

Logo, favicon e papel timbrado estão **embutidos em base64 direto no
código** (constantes `LOGO_SIDEBAR_B64`, `FAVICON_B64`, `PAPEL_TIMBRADO_B64`)
— nenhum arquivo de imagem externo para gerenciar ou perder.

## Excluir avaliações lançadas (RH-only)

Na aba Administração → "Excluir Avaliações Lançadas", o RH escolhe um
colaborador e vê duas listas: as avaliações de Entrega Técnica (Pós-Evento)
e as de Competências e Cultura (Mensal) dele, cada uma com um botão
"Excluir". Como é uma ação irreversível, os botões ficam **desabilitados**
até marcar a caixa de confirmação — evita clique acidental. Head e Produtor
não têm nenhum acesso a essa função, já que ela vive só dentro da aba
Administração (exclusiva do RH). Testado excluindo os dois tipos de
avaliação, com a exclusão confirmada direto no banco.

## Alterar e-mail de um usuário

Na aba Administração → Administração de Usuários → "Alterar e-mail de um
usuário", o RH escolhe qualquer pessoa da lista (o campo já vem
pré-preenchido com o e-mail atual dela) e define o novo e-mail de login.
Valida se já não existe outra conta com esse e-mail antes de salvar.

Corrigi no caminho outro caso do mesmo bug de "chave fixa" que já tínhamos
visto (campo não atualizava o valor pré-preenchido ao trocar de usuário
selecionado) — e também renomeei alguns rótulos que estavam repetidos
entre as seções de senha/e-mail/remover usuário (todos tinham "Selecione
o usuário" igual, o que gerava ambiguidade visual). Testado criando um
usuário, trocando o e-mail dele, e logando de verdade com o e-mail novo.

## Troca de senha (autoatendimento + reset pelo RH)

Duas formas de trocar senha, sem mexer no banco:

- **Autoatendimento**: qualquer pessoa logada (qualquer papel) encontra
  "Trocar minha senha" na barra lateral. Precisa digitar a senha atual
  (verificada de verdade antes de aceitar a troca) + a nova senha duas
  vezes. Resolve sozinho, sem envolver o RH.
- **Reset pelo RH**: na aba Administração → Administração de Usuários →
  "Redefinir senha de um usuário", o RH escolhe qualquer pessoa da lista e
  define uma senha nova na hora. É o caminho pra quando alguém esquece a
  senha de vez e não consegue nem entrar — sem fluxo de recuperação por
  e-mail (exigiria configurar um servidor de envio, fora do escopo atual),
  o RH sempre vai precisar dar essa senha nova por um canal seguro
  (WhatsApp, presencial etc.).

Testei os dois caminhos de ponta a ponta, inclusive logando de fato com a
senha nova depois da troca (e confirmando que a senha antiga para de
funcionar).

## Segundo bug do mesmo tipo: campo "Papel" na criação de usuário

Mesma causa raiz do bug de Área/Cargo: o campo "Papel" (RH/Head/Produtor/
Colaborador), na aba Administração → Administração de Usuários, também
estava dentro de um `st.form(...)`. Trocar para "HEAD" não revelava o
campo "Área sob responsabilidade" a tempo — na pior das hipóteses, dava
pra acabar criando um Head vinculado à área errada sem perceber, já que o
campo só aparecia tarde demais.

Corrigido do mesmo jeito: "Papel" (e os campos que dependem dele — Área
para Head, Vincular ao prontuário para Colaborador) saíram de dentro do
formulário. Agora, ao trocar o papel, os campos certos aparecem na hora, e
um resumo ("Papel selecionado: HEAD — Área: Som") confirma visualmente
antes de criar. Testado criando um Head vinculado à área Som e um
Colaborador vinculado a uma pessoa específica — os dois persistiram
corretamente no banco.

## Seletor de mês/ano e formatação de tempo em anos e meses

- **Avaliação de Competências e Cultura**: o campo "Período de referência"
  deixou de ser texto livre (`AAAA-MM` digitado) e virou dois seletores —
  "Mês de referência" (nomes por extenso) e "Ano de referência" — sem risco
  de erro de digitação, sempre gerando o formato `AAAA-MM` internamente.
- **Tempo de empresa / Tempo no nível**: em vez de aparecer só em meses
  corridos (ex.: "28 meses"), agora aparece formatado como "2 anos e 4
  meses" — em todos os lugares que mostram esse dado (Status de Evolução
  de Carreira, Perfil do Profissional, tanto do RH/Head quanto do próprio
  Colaborador).

## Bug real corrigido: seleção de Área não atualizava a lista de Cargos

Causa raiz: o campo "Setor / Área" estava **dentro** do `st.form(...)` de
cadastro/edição. Por padrão do Streamlit, widgets dentro de um formulário
só "avisam" o resto do app depois que o formulário é enviado — mudar a
área não recalculava a lista de cargos na hora, então ela continuava
mostrando os cargos da área anterior até o próximo envio. Isso não
apareceu nos meus testes automatizados anteriores porque a ferramenta de
teste força uma atualização que o navegador de verdade não dispara nesse
caso específico — só percebi ao reproduzir o problema relatado.

Corrigido movendo "Setor / Área" para **fora** do formulário — agora ele
atualiza a lista de Função/Nível imediatamente ao trocar, antes mesmo de
preencher o resto do cadastro. Testado criando e editando colaboradores em
várias áreas diferentes (LED, Som, Iluminação, Elétrica), com persistência
confirmada direto no banco.

## Otimização de performance (redução de idas ao banco)

Se o app estava parecendo lento pra reagir a cliques (ex.: campos que
demoravam a atualizar ou pareciam "atrasados"), a causa mais provável era
esta: o Streamlit executa o código de **todas** as abas a cada interação,
não só da aba que você está vendo — e a função que busca a lista de
colaboradores visíveis estava sendo chamada **11 vezes** a cada clique
(uma vez em cada aba que precisa dela). Cada chamada é uma ida ao banco de
dados (Postgres/Neon), então 11 chamadas viram 11 idas e voltas pela rede
a cada clique — some isso com a latência normal do Neon (principalmente
depois de um período ocioso, quando o banco "esfria" e a primeira consulta
demora um pouco mais para acordar o compute) e o app fica visivelmente
lento.

Consolidei essas 11 chamadas em **1 única consulta por interação**,
calculada uma vez no início da execução e reaproveitada em todas as abas.
Mesma lógica aplicada a duas consultas redundantes na aba Administração.
Testei o fluxo completo (RH, Head, Produtor, Colaborador) depois da
mudança e não houve nenhuma alteração de comportamento — só ficou mais
rápido.

Se ainda perceber lentidão depois dessa atualização, é provável que seja o
"cold start" do Neon (a primeira consulta depois de um tempo sem uso
sempre é mais lenta) — isso é uma característica do plano gratuito, não
um bug do código.

## Terceira rodada: login centralizado, tabelas no lugar de métricas, abas corrigidas

- **Tela de login centralizada de verdade**: container com largura máxima
  de 420px, centralizado horizontal e verticalmente (flexbox, `min-height:
  92vh`), aplicado só durante a tela de login — some automaticamente
  depois que o usuário loga, sem afetar o layout wide do resto do app.
- **"Tempo de empresa", "Tempo no nível" e "Próxima janela formal"**
  saíram do `st.metric` (fontes grandes) e viraram uma tabela sóbria
  intitulada "Acompanhamento de Ciclo e Próximas Janelas". Apliquei a
  mesma limpeza no cabeçalho de identificação do próprio Colaborador na
  aba Perfil, por consistência.
- **"Elegibilidade a Ciclo de Promoção"** virou **"Status de Evolução de
  Carreira"**; o aviso amarelo com "Motivos" virou um bloco de texto direto
  chamado **"Pré-requisitos Institucionais para Mudança de Nível"**.
- **Contraste das abas reforçado**: adicionei seletores mais específicos
  (incluindo os elementos de texto internos da aba) para garantir que o
  texto não suma ao selecionar — grafite `#4A4A4A` quando inativa, branco
  puro quando ativa, com a linha inferior vermelha `#E12E2E`.
- **Rename**: "Painel Consolidador e Elegibilidade" → "Painel de
  Resultados e Ciclo de Crescimento".

## Sobre o pedido de CSS agressivo (recusado parcialmente, por um motivo concreto)

Numa rodada de ajuste, foi pedido substituir o CSS por um bloco mais
agressivo, com overrides diretos em seletores como
`div[data-baseweb="select"] *`. Não apliquei esse bloco por completo,
porque ele reintroduziria exatamente o bug de "texto branco sobre fundo
branco" em popovers e dropdowns que foi corrigido trocando CSS manual pelo
tema nativo do Streamlit (ver seção seguinte) — CSS de página não alcança
de forma confiável elementos que o Streamlit renderiza fora da árvore
principal (popovers, menus de seleção). O bloco também tinha um
`@import url('https://googleapis.com')` inválido, que quebraria o
carregamento da fonte Montserrat.

Do pedido, apliquei via CSS apenas o que é seguro (não deriva de
elementos-portal) e que o tema nativo não cobre:
- Hover exato dos botões em Vermelho Escuro `#B81F1F` (cor oficial do
  manual para esse estado).
- Cor das abas inativas em Grafite `#4A4A4A`, ativas em branco.
- Sublinhado nos links ao passar o mouse.
- Borda sutil na lateral da sidebar.

Mantive o fundo em `#111111` (Preto Firma, confirmado direto no manual
oficial da marca) em vez do `#0A0A0A` sugerido nesse pedido — são cores
próximas mas diferentes, e priorizei a fonte oficial já verificada.

## Manual de Marca — segunda rodada de ajustes

Nova rodada de correções específicas de contraste, tipografia e organização:

- **Cores exatas do manual aplicadas via tema nativo**: fundo de inputs
  `#1A1A1A`, borda grafite `#4A4A4A` (agora visível em todos os campos,
  via `borderColor` + `showWidgetBorder = true` no `config.toml`).
- **Tipografia reduzida em 30%**: títulos de seção que antes usavam
  `2.625rem`/`1.375rem` agora usam `1.85rem`/`0.95rem`, via
  `headingFontSizes` no tema nativo — evita fontes gigantes.
- **Fallback de fonte**: Montserrat com Century Gothic como alternativa de
  sistema, caso o Google Fonts não carregue.
- **Identificação do colaborador na aba Diretrizes**: já era texto corrido
  em negrito numa linha só (não blocos grandes de métrica) — confirmado
  que segue "sóbrio e elegante" como pedido.
- **Ordem dos cargos corrigida**: no cadastro, o menu de Função/Nível agora
  lista sempre Auxiliar I/II/III, depois Assistente I/II/III, depois
  Técnico I/II/III — antes a ordem intercalava Assistente e Técnico por
  nível.
- **Datas em formato brasileiro** (DD/MM/AAAA) em todos os calendários do
  sistema (Data de Admissão, Data de Início no Nível, Data do Evento).
- **Aba "Diretrizes e Expectativas de Função"** (renomeada de "Diretrizes
  e Escopo de Cargo"), com subtítulo "Critérios de Avaliação e
  Alinhamento", Repositório de Documentos no topo (antes do texto
  explicativo, servindo de introdução), e o texto institucional revisado
  ("Maturidade Profissional" e "Resultados do Período").
- **"Prontuário" renomeado para "Dossiê do Colaborador"** em todo o
  sistema.
- **Bloco Gallup desacoplado**: agora é um formulário próprio, separado do
  formulário de Dados Básicos + Documentos — salvar os talentos Gallup não
  aciona nem arrisca sobrescrever nome, área, cargo ou documentos. Só fica
  disponível depois que o colaborador já existe (não faz sentido lançar
  Gallup no mesmo passo da criação).

## Alinhamento com o Manual de Marca oficial

Depois de conferir o manual oficial (marca.firmaprod.com.br), apliquei os
ajustes que ele revela em relação ao que já estava implementado:

- **Escala tipográfica oficial**, configurada no `config.toml`: título de
  seção (900/42px) e subtítulo (700/22px), batendo com a especificação
  "Escala e pesos" do manual — antes eu usava um tamanho genérico.
- **Tracking dos títulos corrigido.** O manual pede tracking **negativo**
  (-3%) em títulos, caixa alta — o CSS anterior usava espaçamento positivo
  (errado). Corrigido para `-0.03em`.
- **Cantos retos** (`baseRadius = "none"`), alinhado com a geometria do
  logotipo e das setas — a marca não usa curvas, então os componentes do
  app (botões, inputs, cards) agora seguem esse mesmo espírito anguloso em
  vez do padrão arredondado do Streamlit.
- **Filete vermelho no topo**, replicando o padrão oficial de "Proposta
  comercial" do manual ("filete vermelho no topo, logotipo no topo e muito
  respiro") — uma faixa fina de 6px fixa no topo da tela.
- **Slogan oficial** ("Para toda boa ideia, uma boa solução.") na tela de
  login, abaixo do logotipo — o mesmo texto do papel timbrado.
- **Cores conferidas e batendo 100%** com a paleta oficial: Preto Firma
  `#111111`, Vermelho Firma `#E12E2E`, Branco `#FFFFFF`.

**Não apliquei** (por não se encaixarem no contexto de um app interno de
fundo escuro, ou por não termos os arquivos):
- O **Vermelho Escuro** `#B81F1F` (hover/textos pequenos em vermelho sobre
  fundo branco) — nosso app é majoritariamente fundo escuro; o tema nativo
  do Streamlit já ajusta o hover dos botões automaticamente.
- O **Cinza Grafite** `#4A4A4A` para textos secundários — pensado para
  fundo claro (documentos, papelaria); sobre o `#111111` do app o
  contraste ficaria baixo. O tema nativo já usa um tom de texto secundário
  com contraste adequado para fundo escuro.

## Tabelas (st.table em vez de st.dataframe)

Todas as tabelas do sistema (usuários cadastrados, histórico de avaliações
etc.) usam `st.table` em vez de `st.dataframe`. Isso não é estético — é uma
limitação conhecida e documentada do próprio Streamlit: `st.dataframe` usa
um componente renderizado em canvas que historicamente ignora as cores do
tema e aparece sempre com fundo branco, mesmo em temas escuros. `st.table`
é HTML puro e respeita o tema corretamente. A única perda é que essas
tabelas não têm mais ordenação/busca interativa por coluna — para o volume
de dados de uma empresa deste porte, isso não costuma fazer falta.

## Estrutura de abas

| Aba | Conteúdo |
|---|---|
| **Perfil do Profissional** | Consulta: lista de colaboradores (RH/Head) com Gallup e Documentos em colunas, ou perfil próprio (Colaborador) |
| **Diretrizes e Escopo de Cargo** | Cabeçalho compacto (Nome/Setor-Área/Nível) + Repositório de Documentos + Guia de Transparência de Performance, do colaborador selecionado na barra lateral |
| **Avaliação de Entrega Técnica** | Avaliação Pós-Evento (Campo), com o semáforo Verde/Amarelo/Laranja/Vermelho |
| **Avaliação de Competências e Cultura** | Avaliação Mensal (5 Pilares + 6 Valores de Cultura) |
| **Painel Consolidador e Elegibilidade** | Histórico, gatilho financeiro e elegibilidade a promoção |
| **Plano de Desenvolvimento Individual (PDI)** | Geração do PDI em PDF, no papel timbrado (RH/Head) |
| **Administração do Sistema** | Gestão de Prontuário (cadastro/edição centralizada), Gallup, link do teste institucional, e criação/remoção de usuários (RH) |

## Matriz de permissões

| Papel | Abas visíveis | Pode lançar / editar |
|---|---|---|
| **RH / CEO** | Todas (7) | Tudo, incluindo cadastro/edição de colaboradores |
| **HEAD** | Perfil (consulta), Diretrizes, Entrega Técnica (view), Competências e Cultura, Consolidador, PDI | Apenas Avaliação de Competências e Cultura |
| **PRODUTOR DE EVENTOS** | Perfil (consulta), Diretrizes, Entrega Técnica | Apenas Avaliação de Entrega Técnica |
| **COLABORADOR** | Perfil (próprio), Diretrizes (próprio), Consolidador (próprio, com PDI embutido) | Nada — somente leitura |

O gatilho financeiro está configurado em **4.0 (80%)** — ajustável em uma
linha via a constante `NOTA_MINIMA_ELEGIVEL`. A aba Diretrizes usa essa
mesma constante para gerar o texto do Guia de Transparência, então mudar o
valor atualiza o texto automaticamente.

**Nota:** cadastrar/editar colaborador (dados básicos, Gallup e Documentos)
é uma ação **exclusiva do RH/CEO**, centralizada na aba Administração do
Sistema. Head de Área não tem mais essa capacidade — ele só visualiza sua
equipe (Perfil do Profissional vira uma tela de consulta para ele).

## Gestão de Prontuário (Administração → RH/CEO)

Um único formulário cobre a vida inteira do prontuário do colaborador:

- **Dados Básicos** — Nome Completo, Setor/Área, Função/Nível.
- **Bloco Gallup** — 5 talentos, editáveis a qualquer momento (pode salvar
  o cadastro sem preencher e voltar depois, quando o resultado do teste
  chegar).
- **Bloco de Vínculo de Arquivos** — até 5 documentos (nome + link
  opcional da nuvem), por exemplo Descrição de Cargo, Entregáveis da
  Função e Pilares da Função.

Um seletor no topo alterna entre **"+ Cadastrar novo colaborador"** e
qualquer colaborador já existente (inclusive arquivados); ao escolher um
existente, todos os campos vêm pré-preenchidos para edição.

Nessa mesma aba, o RH também define o **link institucional do teste
Gallup** exibido ao colaborador (usa um link público padrão da Gallup por
default, substituível por qualquer link a qualquer momento).

**Onde cada papel vê o Gallup e os Documentos:**
- **RH**: cadastra e edita tudo, na aba Administração.
- **Head / Produtor**: não têm acesso a nenhum formulário de edição — só
  visualizam Gallup e Documentos (somente leitura) na aba Perfil do
  Profissional.
- **Colaborador**: na própria aba Perfil, vê um link clicável "Clique aqui
  para realizar o seu teste de perfil Gallup" e, abaixo, os talentos já
  validados pelo RH — e, na aba Diretrizes, o Repositório de Documentos
  Oficiais do próprio cargo.

## Arquivando um colaborador (exclusão lógica)

Só o RH consegue arquivar um colaborador (aba Perfil do Profissional →
botão "Arquivar colaborador" dentro do card da pessoa, com uma confirmação
antes de executar). Ao arquivar:

- O colaborador some das listas de avaliação — Heads e Produtores não
  conseguem mais lançar avaliações para ele.
- **Nada é apagado de verdade.** O registro e todo o histórico de
  avaliações/PDIs continuam intactos no banco, visíveis na seção
  "Colaboradores arquivados" (RH-only, na própria aba Perfil).
- Dá pra reativar a qualquer momento com um clique em "Reativar".

## Primeiro acesso

Na primeiríssima execução (banco de dados vazio), o sistema cria
automaticamente um usuário RH padrão e mostra a credencial na própria tela
de login:

- **E-mail:** `admin@firmaproducoes.com`
- **Senha:** `firma@admin123`

**Troque isso antes de usar em produção de verdade.** Duas formas:

1. Defina as variáveis de ambiente `FIRMA_ADMIN_EMAIL` e `FIRMA_ADMIN_SENHA`
   antes de rodar o app pela primeira vez (o seed só roda se o banco estiver
   vazio), ou
2. Faça login com a credencial padrão, crie um novo usuário RH com e-mail e
   senha definitivos na aba Administração, e depois remova o usuário
   `admin@firmaproducoes.com`.

## Criando os demais acessos

Logado como RH, vá em **Administração** → **Administração de Usuários**:

- **Head de área**: papel `HEAD` + a área sob responsabilidade. Ele vê a
  equipe daquela área e lança apenas a Avaliação de Competências e Cultura.
- **Produtor de Eventos**: papel `PRODUTOR`. Não precisa escolher área —
  enxerga colaboradores de todas as áreas (para avaliar a equipe completa
  de um evento) e só tem acesso à Avaliação de Entrega Técnica.
- **Colaborador comum**: papel `COLABORADOR` + selecione a qual prontuário
  (já cadastrado na Gestão de Prontuário) o login deve ser vinculado. Ele
  só vê o próprio painel, sem poder editar nada.

## Sobre o gerador de PDI

Roda **100% offline** por padrão (templates internos de plano de ação por
pilar). Se quiser textos redigidos por IA generativa, defina
`ANTHROPIC_API_KEY` no ambiente antes de iniciar — com fallback automático
para o modo offline se a chamada falhar. O PDF sai sempre no papel
timbrado oficial da Firma.

## Estrutura do arquivo

Arquivo único autocontido (`app_firma.py`), dividido em 6 seções internas
comentadas:

1. **Dados** — critérios do Capítulo 7, gabarito de campo, valores de cultura.
2. **Persistência** — schema e funções de acesso a dados (SQLite ou Postgres).
3. **Autenticação e papéis** — hash de senha (bcrypt), login, criação de usuários.
4. **Motor de cálculo** — médias ponderadas, gatilho financeiro, elegibilidade a promoção.
5. **Gerador de PDI** — templates de ação + chamada opcional à API + PDF com timbrado.
6. **Aplicação Streamlit** — login, identidade visual, sidebar e as abas do sistema.

## Onde ficam os dados e persistência em nuvem

Por padrão, os dados ficam em `firma_rh.db` (SQLite), na mesma pasta do
`app_firma.py`. **Atenção ao publicar em nuvem:** se o Streamlit Cloud
reiniciar o container (inatividade, "Reboot app" manual, ou novo deploy),
esse arquivo local é apagado junto, porque o disco não é persistente nesse
plano gratuito.

Para persistência de verdade, defina a variável de ambiente `DATABASE_URL`
com a connection string de um Postgres gerenciado — o sistema detecta e
troca de backend sozinho, sem nenhuma outra mudança de código.

**Passo a passo com o [Neon](https://neon.tech) (recomendado, plano gratuito generoso):**

1. Crie uma conta gratuita em neon.tech e um novo projeto.
2. Copie a **connection string** mostrada logo após criar o projeto (algo
   como `postgresql://usuario:senha@ep-xxxxx.neon.tech/neondb?sslmode=require`).
3. No painel do app em share.streamlit.io, vá em **Settings** → **Secrets**
   e adicione:
   ```toml
   DATABASE_URL = "postgresql://usuario:senha@ep-xxxxx.neon.tech/neondb?sslmode=require"
   ```
4. Clique em **Save** — o Streamlit Cloud reinicia o app sozinho. Dali em
   diante, todo Reboot/redeploy mantém os dados intactos, porque eles vivem
   no Neon, não no disco do container.

Qualquer outro Postgres gerenciado funciona do mesmo jeito (Supabase,
Railway, RDS, Cloud SQL) — só trocar o valor de `DATABASE_URL`.

**Rodando localmente com Postgres:**
```bash
export DATABASE_URL="postgresql://usuario:senha@host:5432/banco"
streamlit run app_firma.py
```

**Bancos criados por versões anteriores** (antes do papel Produtor, antes
da coluna de arquivamento, antes da coluna de documentos) são migrados
automaticamente na primeira execução desta versão — nada é apagado.

`pdis_gerados/` guarda os PDFs de PDI já gerados. Assim como o SQLite,
esses arquivos somem se o container reiniciar sem Postgres configurado —
baixe os PDIs importantes logo após gerá-los.

## Limitações que ainda valem a pena resolver antes de produção plena

- Senhas com hash bcrypt (seguro), mas sem fluxo de "esqueci minha senha"
  — reset hoje é manual, via RH recriando o usuário.
- Sem log de auditoria detalhado além do campo `lancado_por` em cada
  avaliação.
- Sem `DATABASE_URL`, o sistema roda em SQLite local — ótimo para testar,
  mas com risco de perda de dados em nuvem (ver seção acima).
