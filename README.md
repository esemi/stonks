# stonks


### Pre-requirements
- [redis server up and running](https://redis.io/docs/getting-started/installation/)
- [python 3.9+](https://www.python.org/downloads/)


### Local setup
```shell
$ git clone git@github.com:esemi/stonks.git
$ cd stonks
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install -U poetry pip setuptools
$ poetry install
```

Create env file to override default config
```bash
cat > .env << EOF
throttling_time=2.0
debug=true
EOF
```

### Local run tests
```shell
$ pytest --cov=app
```

### Local run background task
```
python -m app.rates_update_task
```

### Local run flake
```
poetry run flake8 app/
```
### Lokal run MyPy
```
poetry run mypy app/
```

TODO
---
- [x] mvp repo
- [x] linters + tests in CI

- [x] background live update cash rate (\[CZK|EUR|USD\].RUB)
- [x] background live update forex rate (\[CZK|EUR|USD\].RUB)
- [ ] save rates to redis
- [ ] deploy task to server in CI

- [ ] bot /help & /start
- [ ] bot /rates
- [ ] bot inline cmd
- [ ] deploy bot to server

- [ ] setup to tlg chanel
- [ ] readme update