CREATE TABLE grupo_mensagens (
    id SERIAL PRIMARY KEY, 
    nome VARCHAR(250) NOT NULL,   
    convenios JSONB,  
    estipulantes JSONB,  
    status_contratos JSONB,  
    alertas_contratos JSONB,  
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

/*TRIGGER MODIFIED*/
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_modified
BEFORE UPDATE ON grupo_mensagens
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();


CREATE INDEX idx_contrato ON relatorio_contratos(id_contrato);
