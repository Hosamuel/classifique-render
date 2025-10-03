# Configuração da Chave Secreta

Este projeto utiliza uma chave secreta para segurança da aplicação Flask. Para executá-lo, você deve definir a variável de ambiente `SECRET_KEY`.

## Como Definir a Chave Secreta

### Desenvolvimento Local (.env)

Durante o desenvolvimento local, você pode criar um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
SECRET_KEY="sua_chave_secreta_aqui"
```

Substitua `"sua_chave_secreta_aqui"` por uma string longa e aleatória. Este arquivo será automaticamente carregado pelo `python-dotenv`.

**IMPORTANTE**: Nunca adicione o arquivo `.env` ao controle de versão (Git). Ele já está incluído no `.gitignore` para sua conveniência.

### Produção

Em ambientes de produção, defina a variável de ambiente `SECRET_KEY` diretamente no seu ambiente de hospedagem (e.g., Heroku, AWS, Docker). Consulte a documentação do seu provedor de hospedagem para obter instruções específicas.
