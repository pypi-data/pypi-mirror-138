# UToken - Tokens seguros.
![BADGE](https://img.shields.io/static/v1?label=status&message=em%20desenvolvimento&color=green)
![BADGE](https://img.shields.io/static/v1?label=language&message=python&color=blue)

UToken (ou Unhandleable Token) é uma bilioteca criada para ser
utilizada na geração de tokens seguros e íntegros, ou seja, não
podem ser alterados. Veja o que você pode fazer com o UToken:

- Criar tokens seguros
- Inserir um conteúdo no token
- Definir tempo de expiração para o token


## Atalhos

- [Como usar](#Como-usar)
  - [Criando um token](#Criando-um-token)
  - [Decodificando um token](#Decodificando-um-token)
- [Licença](#Licença)

# Como usar

Aqui vai um breve tutorial sobre como utilizar o UToken de forma simples.

## Criando um token

Vamos começar criando um token, veja o código abaixo:

```python
from utoken import encode

# definindo nossa chave
KEY = 'secret-key'

# codificando
my_token = encode({'message': 'Firlast'}, KEY)
print(my_token)

# > eyJtZXNzYWdlIjogIkZpcmxhc3QifQ.5c99ae8e7ce3a000d5b0c35cb53e9e8f
```

Primeiro passamos como parâmetro para utoken.encode() o conteúdo do token, que pode ser um dicionário ou lista, depois,
passamos a chave que vai ser utilizada para codificar. Após isso, temos o nosso token.

Também podemos adicionar o tempo de expiração do token,veja:


```python
from utoken import encode
from datetime import datetime, timedelta

max_time = datetime.now() + timedelta(minutes=5)

# codificando
my_token = encode({'message': 'Firlast', 'max-time': max_time}, 'KEY')
```

Após o tempo máximo ser atingido, a exceção ```ExpiredTokenError``` será lançada.

## Decodificando um token

Agora, vamos decodificar um token. Veja o código abaixo:

```python
from utoken import decode

# definindo nossa chave
KEY = 'secret-key'
token = 'eyJtZXNz...'

# decodificando
my_decode_token = decode(token, KEY)
print(my_decode_token)

# > {'message': 'Firlast'}
```

Pronto! Nosso token foi decodificado. Em ```utoken.decode()``` passamos como parâmetro o token e a chave utilizada na codificação, simples.

Se você definiu um tempo de expiração no token, receberá uma exceção ao tentar decodificar o token se o token estiver expirado, para isso,
faça um tratamento de exceção:

```python
from utoken import decode
from utoken import ExpiredTokenError

# definindo nossa chave
KEY = 'secret-key'
token = 'eyJtZXNz...'

# decodificando
try:
    my_decode_token = decode(token, KEY)
except ExpiredTokenError:
    print('O token expirou')
else:
    print(my_decode_token)
```

# Licença

Esse projeto utiliza a licença GNU GPL v3.0.

```made with python by Firlast.```
