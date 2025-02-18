from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AgendamentoModel(BaseModel):
    grupo_id: int
    horario_disparo: datetime
    ativo: Optional[bool] = True
