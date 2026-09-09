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

Tema escuro minimalista aplicado via CSS injetado no próprio `app_firma.py`
(não depende de arquivo de configuração externo):

- Fundo: `#111111` · Texto: `#FFFFFF` · Botões e links: `#E12E2E`
- Tipografia: Montserrat (Google Fonts), títulos em caixa alta, sem emojis
- Todo campo de texto, seleção (`selectbox`/`multiselect`) e dropdown força
  fundo escuro (`#1E1E1E`) com texto branco — inclusive nos menus que o
  Streamlit renderiza fora da área principal do app (BaseWeb popovers),
  eliminando cenários de texto invisível (branco sobre branco).
- Logotipo oficial ("FIRMA PROD.", versão branca) no topo da barra lateral
  e da tela de login; símbolo da marca (o "F" com o ponto vermelho) como
  favicon da aba do navegador.
- PDI em PDF sai no **papel timbrado oficial** da Firma (logo, marca d'água
  e rodapé de contato em todas as páginas).

Logo, favicon e papel timbrado estão **embutidos em base64 direto no
código** (constantes `LOGO_SIDEBAR_B64`, `FAVICON_B64`, `PAPEL_TIMBRADO_B64`)
— nenhum arquivo de imagem externo para gerenciar ou perder.

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
