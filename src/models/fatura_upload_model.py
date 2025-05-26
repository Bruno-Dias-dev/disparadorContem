from pydantic import BaseModel, Field

class FaturaUploadModel(BaseModel):
    codigo_da_fatura: str = Field(..., max_length=250)
    celular: str = Field(..., max_length=20)
    # 'enviado', 'created', 'modified' serão gerenciados pelo BD
