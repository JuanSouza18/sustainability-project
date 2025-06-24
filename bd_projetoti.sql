use bd_projetoti;
show tables;
select * from resultados_sustentabilidade;
select * from valores_sustentabilidade;
DELETE FROM resultados_sustentabilidade;
DELETE FROM valores_sustentabilidade;
-- Tabela principal com valores
CREATE TABLE valores_sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    valor_agua DECIMAL(9, 2),
    valor_energia DECIMAL(9, 2),
    valor_residuos DECIMAL(9, 2),
    valor_reciclaveis DECIMAL(9, 2),
    valor_transporte VARCHAR(170)
);

-- Tabela com classificações ligadas à tabela de valores
CREATE TABLE resultados_sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_valor INT,
    data date,
    consumo_agua VARCHAR(30),
    consumo_energia VARCHAR(30),
    geracao_residuos VARCHAR(30),
    uso_transporte VARCHAR(30),
    FOREIGN KEY (id_valor) REFERENCES valores_sustentabilidade(id)
);
