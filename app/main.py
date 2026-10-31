"""API de tarefas com armazenamento em memoria por processo."""
from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictBool


class TarefaIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    titulo: str = Field(min_length=1)


class TarefaUpdate(TarefaIn):
    concluida: StrictBool


class TarefaOut(BaseModel):
    id: int
    titulo: str
    concluida: bool


def create_app() -> FastAPI:
    api = FastAPI(title="API de tarefas", version="1.0.0")
    tarefas: dict[int, TarefaOut] = {}
    ids = count(1)
    lock = Lock()

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.post("/tarefas", status_code=201, response_model=TarefaOut)
    def criar(tarefa: TarefaIn) -> TarefaOut:
        with lock:
            nova = TarefaOut(id=next(ids), titulo=tarefa.titulo, concluida=False)
            tarefas[nova.id] = nova
            return nova

    @api.get("/tarefas", response_model=list[TarefaOut])
    def listar() -> list[TarefaOut]:
        with lock:
            return list(tarefas.values())

    @api.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
    def consultar(tarefa_id: int) -> TarefaOut:
        with lock:
            if tarefa_id not in tarefas:
                raise HTTPException(status_code=404, detail="Tarefa nao encontrada")
            return tarefas[tarefa_id]

    @api.put("/tarefas/{tarefa_id}", response_model=TarefaOut)
    def atualizar(tarefa_id: int, tarefa: TarefaUpdate) -> TarefaOut:
        with lock:
            if tarefa_id not in tarefas:
                raise HTTPException(status_code=404, detail="Tarefa nao encontrada")
            atualizada = TarefaOut(id=tarefa_id, **tarefa.model_dump())
            tarefas[tarefa_id] = atualizada
            return atualizada

    return api


app = create_app()

