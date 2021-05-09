<div>
    <p align="center">
    <img src='https://raw.githubusercontent.com/Projeto-ECOmposteira/documentacao/main/assets/img/logo/logo.png' alt="Projeto Kokama" width="25%"/>
    </p> 
    <h1 align="center">
    Projeto ECOmposteira
    </h1>
</div>

## Microsserviço da Composteira

O presente microsserviço disponibiliza informações das composteira. Portanto, fornece a possibilidade recuperar, cadastrar, modificar e deletar informações pertinentes a composteira como, por exemplo, dados das composteiras, medidas de propriedades físico-químicas dos sensores embarcados, dados sobre materiais que podem (ou não) serem colocados na composteira e comunicação com o sistema embarcado.

## Rode o Backend com Docker

### Dependências

Inicialmente, instale localmente as seguintes dependências:

1. Instale o [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/);
2. Instale o [Docker Compose](https://docs.docker.com/compose/install/).

### Arquivo de Configuração

1. Crie um arquivo `.env` e preencha as variáveis de ambiente de acordo com os exemplos localizados nos arquivos `.env.example`.

### Inicialização do Projeto

1. Na pasta principal do projeto, construa e inicialize a aplicação com o comando:

```bash
sudo make
```

2. O microsserviço de notificação estará disponível em: `http://localhost:8002/`.
