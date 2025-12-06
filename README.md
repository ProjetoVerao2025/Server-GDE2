# server-GDE2
(backend para o app que nao eh o gde)


## Estrutura do projeto
```
Server
├── Cargo.lock
├── Cargo.toml # Arquivo que descreve o projeto e contem as dependencias
├── migrations # Nesta pasta ficam os scripts SQL responsaveis por quaisquer modificações no banco de dados
└── src        # Aqui fica o código fonte do servidor em si.
    ├── config.rs
    ├── db.rs
    ├── handlers.rs # Aqui temos as funções que são executadas para cada um dos endpoints da api.
    ├── main.rs   # Ponto de entrada do programa.
    ├── models.rs # Define a representação de coisas como alunos, turmas, frequência etc.
    └── routes.rs # Define as rotas ou endpoints da nossa API.
```
