[Stonks & Gents telegram bot](https://t.me/stonks_and_gents_bot)
---
[![tests](https://github.com/esemi/stonks/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/stonks/actions/workflows/tests.yml)

Simple telegram bot for display actual currency exchange rates from Forex (int) and offline point (Russia).

Support USD.RUB, CZK.RUB and EUR.RUB pairs.

Used for p2p exchange chats.


### Pre-requirements
- [redis server up and running](https://redis.io/docs/getting-started/installation/)
- [python 3.9+](https://www.python.org/downloads/)
- [telegram bot token](https://t.me/botfather)
- [unofficial yahoo finance token](https://www.yahoofinanceapi.com/dashboard)

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

### Links
- [production logs](http://stonks.esemi.ru/)
- [Stonks & Gents telegram bot](https://t.me/stonks_and_gents_bot)
- [Forex rates](https://exchangerate.host/)
- [Cash rates](https://blagodatka.ru/)
- [Bloomberg rates](https://www.bloomberg.com)
