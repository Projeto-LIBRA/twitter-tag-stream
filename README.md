# twitter-tag-stream

Este repositório contém o script responsável pela conexão com o grupo de endpoints `Filtered Stream` da API do Twitter, que envia eventos da plataforma em tempo real.

O código possui 3 funções principais
- `set_rules`: define as regras de filtragem para a API de streaming do Twitter. Para este caso de uso, os eventos são filtrados para que apenas marcações do perfil `@ProjetoLibra` sejam retornadas pelo endpoint `stream`. É necessário executar essa função apenas uma vez, já que as configurações são salvas pelo Twitter.
- `get_stream`: consulta o endpoint `stream` em loop, criando e enviando uma mensagem para uma fila no Amazon SQS
- `send_to_sqs_queue`: envia uma mensagem a uma fila no Amazon SQS, definida pela constante `queue_sqs_url`

Para execução do script, devem ser alterados os valores das constantes de autenticação no início do código.
