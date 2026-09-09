# Gestão de Performance Operacional — Portal Corporativo Firma Prod.

Protótipo em **Python + Streamlit**, com persistência real (SQLite local ou
Postgres via `DATABASE_URL`) e login por papel.

## Identidade visual

Tema escuro minimalista aplicado via CSS injetado no próprio `app_firma.py`
(não depende de arquivo de configuração externo):

- Fundo: `#111111`
- Texto: `#FFFFFF`
- Botões e detalhes de ação: `#E12E2E`
- Tipografia: Montserrat (importada via Google Fonts), títulos em caixa alta
- Sem emojis em nenhuma tela

## Estrutura de abas (nomenclatura corporativa)

| Aba | Conteúdo |
|---|---|
| **Perfil do Profissional** | Cadastro/listagem de colaboradores (RH/Head) ou perfil próprio (Colaborador) |
| **Diretrizes e Escopo de Cargo** | Hub de transparência: Missão/Requisitos, Entregáveis Esperados e Matriz de Governança de Alçadas do colaborador selecionado na barra lateral |
| **Avaliação de Entrega Técnica** | Antiga avaliação Pós-Evento (Campo) |
| **Avaliação de Competências e Cultura** | Antiga avaliação Mensal (5 Pilares + Cultura) |
| **Painel Consolidador e Elegibilidade** | Histórico, gatilho financeiro e elegibilidade a promoção |
| **Plano de Desenvolvimento Individual (PDI)** | Geração do PDI em PDF (RH/Head) |
| **Administração do Sistema** | Criação/remoção de usuários (RH) |

> **Nota sobre a aba "Diretrizes e Escopo de Cargo":** os blocos de Missão,
> Requisitos e Entregáveis Esperados são **derivados automaticamente** dos
> textos já oficiais do Capítulo 7 (Autonomia, Criticidade, Comportamento,
> Entrega, Complexidade etc.) — não são um texto novo inventado. Se a Firma
> tiver um manual de cargos formal com "Missão da Função" redigida à parte,
> vale substituir essa derivação automática pelo texto oficial.
>
> Esta aba **não exibe mais** nenhuma informação de alçada financeira,
> orçamento ou limite de gasto — isso foi removido de propósito de todas as
> telas do sistema. A terceira seção da aba ("Transparência de Performance")
> agora explica em texto fixo a régua de maturidade (Nota 3.0 = meta padrão
> de consistência) e o gatilho financeiro (Nota ≥ 4.0 = 80% dos resultados
> esperados).

## Matriz de permissões

| Papel | Abas visíveis | Pode lançar |
|---|---|---|
| **RH / CEO** | Todas (7) | Tudo |
| **HEAD** | Perfil, Diretrizes, Entrega Técnica (view), Competências e Cultura, Consolidador, PDI | Apenas Competências e Cultura |
| **PRODUTOR DE EVENTOS** | Perfil, Diretrizes, Entrega Técnica | Apenas Entrega Técnica |
| **COLABORADOR** | Perfil (próprio), Diretrizes (próprio), Consolidador (próprio, com PDI embutido) | Nada — somente leitura |

O gatilho financeiro está configurado em **4.0 (80%)** — ajustável em uma
linha via a constante `NOTA_MINIMA_ELEGIVEL`.

## Gestão de Talentos Gallup (exclusiva do RH)

A partir desta versão, o cadastro e a edição do Top 5 Gallup **saíram do
Perfil do Profissional e do formulário de novo colaborador** e vivem
única e exclusivamente na aba **Administração do Sistema**, visível apenas
para o RH/CEO. Head de Área e Produtor de Eventos não têm nenhum acesso —
nem para ver o formulário, nem para editar.

Nessa mesma seção da Administração, o RH também define o **link
institucional do teste Gallup** (usa um link público padrão da Gallup por
default, mas pode ser trocado por qualquer link — inclusive um link interno
da Firma — a qualquer momento).

**Onde cada papel vê o quê agora:**

- **RH**: cadastra/edita os 5 talentos e o link do teste, tudo na aba
  Administração.
- **Head / Produtor**: não veem nenhuma opção de Gallup em lugar nenhum.
- **Colaborador**: na aba Perfil do Profissional, vê um link clicável
  "Clique aqui para realizar o seu teste de perfil Gallup" e, logo abaixo,
  a lista somente-leitura dos talentos já validados pelo RH.

## Perfil do Profissional em duas colunas

O card de cada colaborador (visão de RH/Head) e o perfil do próprio
Colaborador agora mostram, lado a lado:

- **Coluna esquerda** — Perfil de Talentos Gallup (somente leitura aqui;
  edição fica na Administração).
- **Coluna direita** — Repositório de Documentos Oficiais, com o nome de
  cada documento como link clicável (quando tiver link cadastrado).

O botão "Editar Documentos" (RH/Head) continua na aba Perfil do
Profissional, dentro do card de cada colaborador — só o Gallup que mudou de
lugar.

## Diretrizes e Escopo de Cargo (simplificada)

Esta aba não exibe mais os blocos derivados de Missão/Requisitos/
Entregáveis (nem qualquer menção a alçada financeira, orçamento ou
compliance). Ficou reduzida a:

1. Cabeçalho: Nome, Setor/Área, Função/Nível.
2. Transparência de Performance (texto fixo): a Régua de Maturidade
   (Nota 3.0 = meta padrão de consistência) e o Gatilho dos 80%
   (Nota ≥ 4.0 para elegibilidade financeira).

## Identidade visual: logo e favicon

O logotipo oficial ("FIRMA PROD.", versão branca/mono) aparece no topo da
barra lateral e na tela de login. O símbolo da marca (o "F" com o ponto
vermelho, versão colorida oficial) é usado como favicon (ícone da aba do
navegador).

Assim como o papel timbrado do PDI, essas imagens estão **embutidas em
base64 direto no `app_firma.py`** — nenhum arquivo externo pra gerenciar.
Para trocar o logo ou o favicon no futuro, basta gerar uma nova imagem PNG
com fundo transparente e substituir o valor das constantes
`LOGO_SIDEBAR_B64` (logotipo) ou `FAVICON_B64` (símbolo) no código.

## Papel timbrado no PDI

O PDI gerado em PDF agora sai automaticamente **no papel timbrado oficial
da Firma Produções** — logo, tagline, marca d'água central e rodapé com
contato, em todas as páginas do documento (não só a primeira).

A imagem do timbrado está **embutida no próprio `app_firma.py`** (em
base64), então não existe um arquivo de imagem separado para gerenciar ou
perder — o sistema continua sendo um único arquivo autocontido. Se um dia
a Firma trocar a identidade visual do papel timbrado, basta gerar uma nova
imagem A4 (recomendado: 200 DPI, formato JPEG ou PNG) e substituir o valor
da constante `PAPEL_TIMBRADO_B64` no código.

## Documentos do colaborador

Na aba **Perfil do Profissional**, RH e Head conseguem cadastrar até 5
documentos por colaborador (nome + link opcional, ex.: Google Drive) através
do botão "Editar Documentos" no card de cada pessoa. Esses documentos
aparecem:

- Para RH/Head, dentro do próprio card do colaborador na lista.
- Para o Colaborador, no seu próprio Perfil do Profissional, como links
  clicáveis (quando tiver link) ou apenas texto (quando for só o nome).

Se você já tinha colaboradores cadastrados antes dessa versão, não precisa
fazer nada — o sistema adiciona a coluna necessária automaticamente na
primeira execução.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app_firma.py
```

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
   senha definitivos na aba **Administração**, e depois remova o usuário
   `admin@firmaproducoes.com`.

## Arquivando um colaborador (exclusão lógica)

Só o RH consegue arquivar um colaborador (aba Prontuário → botão "🗑️
Arquivar colaborador" dentro do card da pessoa, com uma confirmação antes de
executar). Ao arquivar:

- O colaborador some das listas de avaliação e do prontuário ativo — Heads e
  Produtores não conseguem mais lançar avaliações para ele.
- **Nada é apagado de verdade.** O registro e todo o histórico de
  avaliações/PDIs continuam intactos no banco, visíveis na seção "🗄️
  Colaboradores arquivados" (RH-only, na própria aba Prontuário).
- Dá pra reativar a qualquer momento com um clique em "↩️ Reativar" — o
  colaborador volta a aparecer normalmente, com todo o histórico anterior.

Se você já tinha colaboradores cadastrados antes dessa versão, não precisa
fazer nada: o sistema adiciona a coluna necessária automaticamente na
primeira execução, sem apagar nada.

## Criando os demais acessos

Logado como RH, vá em **Administração** → **Criar usuário**:

- **Head de área**: papel `HEAD` + a área sob responsabilidade. Ele vê a
  equipe daquela área e lança apenas a Avaliação Mensal.
- **Produtor de Eventos**: papel `PRODUTOR`. Não precisa escolher área — ele
  enxerga colaboradores de todas as áreas (para avaliar a equipe completa de
  um evento) e só tem acesso à aba de Avaliação Pós-Evento.
- **Colaborador comum**: papel `COLABORADOR` + selecione a qual prontuário
  (já cadastrado na aba Prontuário) o login deve ser vinculado. Ele só vê o
  próprio painel, sem poder editar nada.

## Se você já tinha um `firma_rh.db` da v2 (antes do papel Produtor)

Sem problema — o `app_firma.py` detecta automaticamente bancos criados pela
versão anterior (que só aceitavam RH/HEAD/COLABORADOR) e migra o schema na
primeira execução, preservando todos os usuários, colaboradores e avaliações
já cadastrados. Não é preciso apagar nem recriar o banco.

## Sobre o gerador de PDI

Mesmo comportamento da v1: roda **100% offline** por padrão (templates
internos de plano de ação por pilar). Se quiser textos redigidos por IA
generativa, defina `ANTHROPIC_API_KEY` no ambiente antes de iniciar — com
fallback automático para o modo offline se a chamada falhar.

## Estrutura do arquivo

Arquivo único autocontido (`app_firma.py`), dividido em 6 seções internas
comentadas:

1. **Dados** — critérios do Capítulo 7, alçadas, gabarito de campo, valores.
2. **Persistência (SQLite)** — schema e funções de acesso a dados.
3. **Autenticação e papéis** — hash de senha (bcrypt), login, criação de
   usuários RH/HEAD/COLABORADOR.
4. **Motor de cálculo** — médias ponderadas, gatilho financeiro,
   elegibilidade a promoção.
5. **Gerador de PDI** — templates de ação + chamada opcional à API + PDF.
6. **Aplicação Streamlit** — login, sidebar e as abas do sistema.

## Onde ficam os dados

Por padrão, os dados ficam em `firma_rh.db` (SQLite), na mesma pasta do
`app_firma.py`.

**Atenção ao publicar em nuvem:** se o Streamlit Cloud reiniciar o
container (por inatividade, por um "Reboot app" manual, ou por um novo
deploy), o arquivo `firma_rh.db` local **é apagado junto**, porque o disco
não é persistente entre reinícios nesse plano gratuito. Para não perder
dados de verdade, use um banco Postgres externo — veja a seção abaixo.

## Persistência de verdade: conectando um Postgres gratuito

O sistema detecta sozinho se deve usar Postgres em vez de SQLite: basta
definir a variável de ambiente `DATABASE_URL` com a connection string do seu
banco. Sem essa variável, ele continua usando SQLite local normalmente (bom
para testar na sua máquina).

**Passo a passo com o [Neon](https://neon.tech) (recomendado, tem plano gratuito generoso):**

1. Crie uma conta gratuita em neon.tech e crie um novo projeto.
2. Copie a **connection string** que o Neon mostra logo após criar o
   projeto (algo como `postgresql://usuario:senha@ep-xxxxx.neon.tech/neondb?sslmode=require`).
3. No painel do seu app em share.streamlit.io, vá em **Settings** → **Secrets**
   e adicione:
   ```toml
   DATABASE_URL = "postgresql://usuario:senha@ep-xxxxx.neon.tech/neondb?sslmode=require"
   ```
4. Clique em **Save** — o Streamlit Cloud reinicia o app sozinho. A partir
   daí, todo Reboot/redeploy mantém os dados intactos, porque eles vivem no
   Neon, não no disco do container.

Qualquer outro Postgres gerenciado funciona do mesmo jeito (Supabase,
Railway, RDS, Cloud SQL) — só trocar o valor de `DATABASE_URL` pela
connection string correspondente.

**Rodando localmente com Postgres:** defina a variável de ambiente antes de
rodar o Streamlit:
```bash
export DATABASE_URL="postgresql://usuario:senha@host:5432/banco"
streamlit run app_firma.py
```

**Migrando dados que já existem no SQLite:** se você já tem um `firma_rh.db`
local com colaboradores/avaliações e quer levá-los para o Postgres, isso
exige um script simples de cópia tabela a tabela (não incluído aqui, pois
depende do estado atual do seu banco) — posso gerar um se for necessário.

- `pdis_gerados/` — PDFs de PDI já gerados, salvos localmente pelo app (em
  ambos os backends). Assim como o SQLite, esses arquivos também somem se o
  container reiniciar; se isso for um problema, baixe os PDIs importantes
  logo após gerá-los.

## Limitações que ainda valem a pena resolver antes de produção plena

- Senhas são armazenadas com hash bcrypt (seguro), mas não há fluxo de
  "esqueci minha senha" — reset hoje é manual, via RH recriando o usuário.
- Não há log de auditoria detalhado (quem editou o quê e quando) além do
  campo `lancado_por` guardado em cada avaliação.
- Sem `DATABASE_URL` configurada, o sistema roda em SQLite local — ótimo
  para testar, mas com o risco de perda de dados em nuvem já explicado
  acima. Configurar o Postgres é o passo que resolve isso de vez.
