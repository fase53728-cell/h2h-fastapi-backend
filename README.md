# H2H Predictor Backend (FastAPI + CSV)

Backend **mínimo e funcional** em FastAPI para ler seus CSVs de ligas
(formato padrão Angers, 33 colunas, `;` como separador) e servir:

- Lista de ligas disponíveis (`/leagues`)
- Lista de times por liga (`/leagues/{league_id}/teams`)

A ideia é você subir seus CSVs na pasta `data/leagues` e conectar
esse backend ao seu painel H2H (Render, Replit, etc.).

---

## Estrutura do projeto

```text
h2h_fastapi_backend/
  ├── config.py
  ├── main.py
  ├── requirements.txt
  ├── README.md
  ├── data/
  │   └── leagues/
  │       └── .gitkeep
  ├── services/
  │   └── leagues_service.py
  └── utils/
      └── team_normalizer.py
```

- `data/leagues/`: coloque aqui seus CSVs de ligas (ex: `France Ligue 1.csv`).
- `config.py`: define a pasta dos dados.
- `services/leagues_service.py`: funções para listar ligas e times a partir dos CSVs.
- `utils/team_normalizer.py`: normaliza nomes de times.
- `main.py`: app FastAPI com as rotas.
- `requirements.txt`: dependências.

---

## Como rodar localmente (Replit ou PC)

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Coloque seus CSVs na pasta:

   ```text
   data/leagues/France Ligue 1.csv
   data/leagues/Spain La Liga.csv
   ...
   ```

   > Lembre-se: separador `;` (ponto e vírgula).

3. Rode o servidor:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Teste no navegador:

   - `http://localhost:8000/` → mensagem de status
   - `http://localhost:8000/leagues` → lista de ligas
   - `http://localhost:8000/leagues/france-ligue-1/teams` → times da liga

     (Aqui o `france-ligue-1` vem do nome do arquivo: `France Ligue 1.csv`).

---

## Como usar no Render (deploy rápido)

1. Crie um repositório no GitHub e faça upload de **todos** os arquivos deste projeto.
2. No Render:
   - Crie um novo serviço **Web Service**.
   - Conecte com seu repositório.
   - Runtime: **Python**.
   - Build command:

     ```bash
     pip install -r requirements.txt
     ```

   - Start command:

     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. Deploy e pronto: a URL pública terá as mesmas rotas (`/`, `/leagues`, etc.).

---

## Como o `league_id` é gerado

A função `_slugify` faz assim:

- `"France Ligue 1.csv"` → `"france-ligue-1"`
- `"Spain_La_Liga.csv"` → `"spain-la-liga"`

Então sua rota fica:

```text
/leagues/france-ligue-1/teams
```

---

## Ajustes futuros

Depois podemos:
- Adicionar rotas de H2H, probabilidades, Over/Under, etc.
- Integrar diretamente com SofaScore para atualizar os CSVs.
- Criar endpoints específicos para “Palpites do Dia”, “Múltiplas”, etc.

Por enquanto, esse backend é **mínimo** só pra você subir rápido,
apontar o painel pro `/leagues` e `/leagues/{league_id}/teams`
e começar a funcionar.
