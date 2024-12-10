# Структура проекта

# Генерация ключей
## Генерация приватного RSA ключа, размер 2048

```shell
openssl genrsa -out jwt-private.pem 2048
```

## Генерация открытого RSA ключа, на основании приватного

```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -ot  jwt-public.pem
```


