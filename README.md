[Stonks & Gents telegram bot](t.me/stonks_and_gents_bot)
---
[![tests](https://github.com/esemi/stonks/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/stonks/actions/workflows/tests.yml)




### Pre-requirements
- [redis server up and running](https://redis.io/docs/getting-started/installation/)
- [python 3.9+](https://www.python.org/downloads/)
- [telegram bot token](https://t.me/botfather)


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
telegram_token=U_TELEGRAM_TOKEN
EOF
```

### Run tests
```shell
$ pytest --cov=app
```

### Run linters
```
$ poetry run mypy app/
$ poetry run flake8 app/
```

### Run background task
```
python -m app.rates_update_task
```

### Run telegram bot
```
python -m app.bot_app
```


TODO
---
- [x] mvp repo
- [x] linters + tests in CI

- [x] background live update cash rate (\[CZK|EUR|USD\].RUB)
- [x] background live update forex rate (\[CZK|EUR|USD\].RUB)
- [x] save rates to redis
- [x] deploy task to server in CI

- [x] bot /help cmd
- [x] bot /stonks cmd
- [x] deploy bot to server

- [x] fill bot description
- [x] fill bot settings (group add needed)
- [ ] add bot to semrush.CZK group
- [ ] readme update