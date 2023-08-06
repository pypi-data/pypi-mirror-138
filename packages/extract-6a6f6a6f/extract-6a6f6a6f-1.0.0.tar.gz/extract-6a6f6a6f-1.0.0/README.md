# Lazy Android App Extraction

Um jeito preguiçoso e que funciona, para fazer o *pull* de uma aplicação Android qualquer.

- **Sem problemas** quando tiver mais de um *device* listável via `adb`;
- **Funciona em qualquer OS**, desde que você tenha o `adb` em seu `$PATH`;
- Você **não precisa saber ou digitar todo o *package name***, basta alguma coisa; e
- Via `pip`, **sem dor de cabeça com depêndencias**, é somente um *wrapper* do `adb`.

<img src="https://raw.githubusercontent.com/zone016/lazy-android-app-extraction/main/gifs/from_cli.gif" title="`extract` functionando" alt="`extract` functionando" data-align="center">

No jeito mais simples, basta instalar via `pip` e já sair utilizando:

```sh
$ pip3 install extract-6a6f6a6f
```
