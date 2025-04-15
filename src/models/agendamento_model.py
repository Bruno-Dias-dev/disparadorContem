from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List, Optional

class AgendamentoModel(BaseModel):
    grupo_id: int
    horario_disparo: datetime
    ativo: Optional[bool] = True
    mensagem_ids: Optional[List[int]] = None
    conexao_id: str
    departamento_id: str