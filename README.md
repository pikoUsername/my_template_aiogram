Bot Template
---------
Another Bot Template. <br>
based on [this](https://github.com/Forden/aiogram-bot-template) and [this](https://github.com/aiogram/bot).

For Start you need to do:
* rename app/data/_app.toml -> app/data/app.toml.
* psql -d <database> -U <user> -f schema.sql to cmd for create tables.
* and see [this](https://docs.aiogram.dev/en/latest/examples/i18n_example.html?highlight=i18n%20#i18n-example) intructions for i18n if you want.
* python -m pytest tests/ for run tests
