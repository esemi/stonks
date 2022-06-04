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


TODO
---
- [x] mvp repo
- [ ] linters + tests in CI

- [ ] background live update ligovka rate (\[CZK|EUR|USD\].RUB)
- [ ] background live update forex rate (\[CZK|EUR|USD\].RUB)
- [ ] deploy task to server in CI

- [ ] bot /help & /start
- [ ] bot /rates
- [ ] bot inline cmd
- [ ] deploy bot to server

- [ ] setup to tmg chanel
- [ ] readme update