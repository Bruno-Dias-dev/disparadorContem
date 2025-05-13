CREATE TABLE grupo_mensagens (
    id SERIAL PRIMARY KEY, 
    nome VARCHAR(250) NOT NULL,   
    convenios JSONB,  
    estipulantes JSONB,  
    status_contratos JSONB,  
    alertas_contratos JSONB,  
    ativo BOOLEAN DEFAULT TRUE,
    pdf BOOLEAN DEFAULT FALSE,
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

CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    grupo_id INTEGER NOT NULL REFERENCES grupo_mensagens(id) ON DELETE CASCADE,
    horario_disparo TIMESTAMP NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

ALTER TABLE grupo_mensagens ADD COLUMN texto TEXT;

CREATE TABLE mensagens (
	id serial primary key not null,
	mensagem text,
	created timestamp,
	modified timestamp
);
alter table mensagens add column ativo bool;
alter table mensagens add column title varchar(250);
alter table agendamentos add column mensagem_ids integer[];
ALTER TABLE agendamentos ADD COLUMN conexao_id UUID;
ALTER TABLE agendamentos ADD COLUMN departamento_id UUID;

CREATE TABLE usuarios(
    id serial primary key not null,
    nome varchar(250),
    email varchar(250),
    senha varchar(250),
    ativo bool,
    created timestamp,
    modified timestamp
);

alter table grupo_mensagens add column fase varchar(20);
CREATE TABLE logs_envio (
    id SERIAL PRIMARY KEY,
    
    agendamento_id INTEGER NOT NULL,
    FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id),
    
    inicio_envio TIMESTAMP NOT NULL,
    final_envio TIMESTAMP,

    qtd_enviados INTEGER DEFAULT 0,
    qtd_falha INTEGER DEFAULT 0
);


