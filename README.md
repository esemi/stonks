Stonks telegram bot
---
[![tests](https://github.com/esemi/stonks/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/stonks/actions/workflows/tests.yml)


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
$ poetry config virtualenvs.create false --local
$ poetry install
```

Create env file to override default config
```bash
cat > .env << EOF
throttling_time=2.0
debug=true
EOF
```

### Run tests
```shell
$ pytest --cov=app
```

### Run background task
```
python -m app.rates_update_task
```

### Run linters
```
$ poetry run mypy app/
$ poetry run flake8 app/
```

TODO
---
- [x] mvp repo
- [x] linters + tests in CI

- [x] background live update cash rate (\[CZK|EUR|USD\].RUB)
- [x] background live update forex rate (\[CZK|EUR|USD\].RUB)
- [x] save rates to redis
- [x] deploy task to server in CI

- [ ] bot /help & /start
- [ ] bot /rates
- [ ] bot inline cmd
- [ ] deploy bot to server

- [ ] setup to tlg chanel
- [ ] readme update