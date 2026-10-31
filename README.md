# API REST de tarefas — exercício 4.1

Autor: Kin Modesto Sugai. Implementação com apoio do Codex.

API local com FastAPI e armazenamento em memória. Cada reinício apaga as tarefas e reinicia os identificadores em 1.

## Executar

~~~sh
python -m venv .venv
# Git Bash: source .venv/Scripts/activate
# PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
~~~

## Contrato

| Método | Rota | Resultado |
|---|---|---|
| GET | /health | status ok |
| POST | /tarefas | Cria tarefa com titulo; retorna 201, id e concluida=false |
| GET | /tarefas | Lista todas as tarefas |
| GET | /tarefas/{id} | Consulta uma tarefa; 404 se ausente |
| PUT | /tarefas/{id} | Substitui titulo e concluida; 404 se ausente |

Título vazio e dados inválidos retornam 422. Os identificadores são sequenciais; PUT não cria um recurso inexistente. A documentação interativa fica em http://localhost:8000/docs.

## Verificar e entregar

~~~sh
python -m unittest discover -s tests -v
# Reinicie a API antes de avaliar: o primeiro POST deve receber id=1.
autograde validar 4.1
~~~

O MCP do exercício 4.2 consome esta API. Execute um único processo, pois o armazenamento é local à memória do processo.

Referência: [tutorial oficial](https://github.com/alexlopespereira/idp_governodigital/blob/main/exercicios/tutorial_4.1.md).

