# Firma Produções — Sistema de Governança de RH, KPIs e Avaliação (v2)

Protótipo em **Python + Streamlit**, agora com:

- **Persistência real em SQLite** (arquivo `firma_rh.db`, criado automaticamente
  na primeira execução, na mesma pasta do `app_firma.py`) — os dados não são
  mais perdidos ao reiniciar o app.
- **Login obrigatório com 4 papéis:**
  - **RH / CEO** — acesso total: todas as áreas, cadastro de colaboradores, todas
    as avaliações, visão unificada dos relatórios e da consolidação financeira
    dos 80%, e a aba **Administração** para criar/remover usuários.
  - **HEAD** (Head de área) — visualiza sua própria equipe e lança
    **exclusivamente a Avaliação Mensal** (5 Pilares + Cultura). Não lança
    mais a Avaliação Pós-Evento (só visualiza o que já foi lançado).
  - **PRODUTOR DE EVENTOS** — visualiza os colaboradores de **todas as áreas**
    (um evento reúne LED, Som, Iluminação etc. ao mesmo tempo) e lança
    **exclusivamente a Avaliação Pós-Evento** (Campo). Não enxerga nem edita
    Avaliação Mensal, Histórico consolidado ou PDI — essas telas nem aparecem
    para ele, porque derivam da nota mensal.
  - **COLABORADOR** — acesso somente-leitura ao próprio prontuário, histórico
    e PDI; não lança nem edita nada.

Todas as regras de negócio (pesos 50/50, gatilho financeiro, elegibilidade a
promoção, gerador de PDI) continuam exatamente as mesmas da v1 — só a camada
de dados e de acesso mudou.

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

- `firma_rh.db` — banco SQLite com colaboradores, avaliações e usuários.
  Pode ser copiado/versionado como backup simples (é um único arquivo).
  Para trocar o caminho, defina a variável de ambiente `FIRMA_DB_PATH`.
- `pdis_gerados/` — PDFs de PDI já gerados, salvos localmente pelo app.

**Atenção ao publicar em nuvem:** se o Streamlit Cloud reiniciar o
container (por inatividade, por exemplo), o arquivo `firma_rh.db` local
some junto, porque o disco não é persistente entre reinícios nesse plano
gratuito. Para produção de verdade, o próximo passo é apontar `FIRMA_DB_PATH`
para um volume persistente ou migrar as mesmas funções de `db.py`/seções
2-3 do arquivo para um Postgres gerenciado (Supabase, Neon, RDS etc.).

## Limitações que ainda valem a pena resolver antes de produção plena

- Senhas são armazenadas com hash bcrypt (seguro), mas não há fluxo de
  "esqueci minha senha" — reset hoje é manual, via RH recriando o usuário.
- Não há log de auditoria detalhado (quem editou o quê e quando) além do
  campo `lancado_por` guardado em cada avaliação.
- SQLite é ótimo até dezenas de milhares de linhas; se a Firma crescer
  muito além de ~100 funcionários, vale migrar para Postgres.
