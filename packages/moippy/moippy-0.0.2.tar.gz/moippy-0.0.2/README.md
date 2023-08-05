


# SDK Python3 para Integração com Moip/Wirecard - By PagSeguro

Esta SDK foi desenvolvida para abstrair aos desenvolvedores os principais detalhes da comunicação com API v2 da Moip tanto em [produção](https://moip.com.br/) quanto em ambiente [sandbox](hhttps://conta-sandbox.moip.com.br/).

Você pode acessar a documentação base da api aqui: [Docs Api Moip](https://docs.moip.com.br/).

![Licença](https://img.shields.io/github/license/robertons/moippy) ![image](https://img.shields.io/pypi/v/moippy) ![image](https://img.shields.io/pypi/status/moippy) ![image](https://img.shields.io/badge/python-v3.7-blue) ![image](https://img.shields.io/badge/build-passing-brightgreen) ![image](https://img.shields.io/badge/coverage-100%25-brightgreen) ![image](https://img.shields.io/github/last-commit/robertons/moippy)

# Instalação
Instalação utilizando Pip
```bash
pip install moippy
```
Git/Clone
```
git clone https://github.com/robertons/moippy
cd moippy
pip install -r requirements.txt
python setup.py install
```
# Objetos

Os objetos neste SDK podem ser criados em 3 (três) formas distintas a critério do utilizador.

## Criação

**Método 1 - Construção**
```python
objeto = Objeto(campo1 = 'valor', campo2 = 'valor 2', campo_datetime = datetime.now(), campo_float = 10.1)
```
**Método 2 - Construção com Dicionário**
```python
objeto = Objeto(**{'campo1':'valor', 'campo2':'valor 2', 'campo_datetime':datetime.now(), 'campo_float' = 10.1})
```
**Método 3 - Pós-Construção**
```python
objeto = Objeto()
objeto.campo1 = 'valor'
objeto.campo2 = 'valor 2'
objeto.campo_datetime = datetime.now()
objeto.campo_float = 10.1
```
##  Método toJSON

Método toJSON() retorna os dados do Objeto em formato *diciciontario* não codificados.

```python
objeto = Objeto(...)
print(objeto.toJSON())
```



## Suporte Oficial da Moip

Em caso de dúvidas, problemas ou sugestões:  [Central de Contato Moip](https://moip.com.br/contato/)

## Change log

Veja em  [CHANGELOG](CHANGELOG.md) para maiores informações sobre as mudanças recentes

## Contribuições

As contribuições  por meio de `Pull Requests` são bem-vindas e serão totalmente creditadas.

## Segurança

Se você descobrir qualquer problema relacionado à segurança, envie um e-mail para robertonsilva@gmail.com

## Créditos

- Autor [Roberto Neves](https://github.com/robertons)

## Licença
Veja em  [LICENÇA](LICENSE) para maiores informações sobre a licença de uso.
