# Caching-Proxy-Server

```bash
# собрать python пакет
pip install -e .
```

```bash
# запустить прокси для https://dummyjson.com/ на localhost:3333 с TTL 30 сек в фоновом режиме  
caching-proxy run -o https://dummyjson.com/ -p 3333 --ttl 30 -d 
# посмотреть список ключей в кэше
caching-proxy keys
# очистить кэш полностью
caching-proxy clear
# остановить прокси
caching-proxy stop
```