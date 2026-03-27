SISTEMA DE GERENCIAMENTO DE VIAGENS

DESCRIÇÃO
Este projeto é um software desenvolvido em Python para gerenciar agências de viagens. O sistema permite o cadastro, controle e relacionamento de viagens, clientes, pagamentos, transportes e roteiros turísticos.

ARQUITETURA
O sistema segue o padrão de arquitetura MVC (Model-View-Controller), garantindo a separação de responsabilidades:
 * Model (Entidade): Classes que representam os dados (Pessoa, Viagem, etc.).
 * View (Limite): Classes da interface gráfica com o usuário.
 * Controller (Controle): Regras de negócio e orquestração do sistema.
 * DAO: Camada de persistência de dados.

FUNCIONALIDADES
O sistema realiza operações de cadastro, leitura, atualização e exclusão (CRUD) para:
 * Viagens (pacotes, datas, passageiros)
 * Pessoas (clientes)
 * Locais (cidades e países)
 * Transportes e Empresas
 * Trechos de viagem
 * Passeios Turísticos
 * Pagamentos (PIX, Dinheiro, Cartão)
Além disso, gera relatórios gerenciais como destinos mais visitados e controle financeiro.

TECNOLOGIAS
 * Linguagem: Python 3
 * Interface Gráfica: FreeSimpleGUI
 * Persistência: Pickle (arquivos binários)

ESTRUTURA DE PASTAS
/entidade - Classes de dados
