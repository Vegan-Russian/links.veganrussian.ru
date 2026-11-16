# links.veganrussian.ru

Страница со ссылками Vegan Russian (замена taplink).

## Как добавить / изменить ссылку

Отредактируйте [`links.yaml`](links.yaml) и закоммитьте в `main` — GitHub Actions соберёт и задеплоит сайт сам.

```yaml
- section: Название секции
  links:
    - title: Заголовок
      description: Подпись (необязательно)
      url: https://example.com
```

## Локальная сборка

```sh
pip install pyyaml
python3 build.py   # → _site/index.html
```
