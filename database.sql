
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);


CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    concluida BOOLEAN DEFAULT FALSE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(id_usuario) 
	    REFERENCES usuarios(id)
	    ON DELETE CASCADE 
);


CREATE INDEX idx_tarefas_usuario ON tarefas(id_usuario);
