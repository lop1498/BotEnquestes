
# BotEnquestes

L’objectiu general de la pràctica consisteix en desenvolupar un chatbot que permeti recollir les dades d’enquestes definides mitjançant un compilador a través de telegram i consultar gràfiques simples i informes sobre les dades recollides.

## Comencem

Aquestes instruccions et serviran per obtenir una copia del projecte i per poder-lo executar amb objectius de desenvolupament o testeig. Vegi l'apartat deployment per saber com fer deploy del projecte en un sistema real.

### Prerequisits

En cas que es vulgui modificar i executar el compilador que reconeix el llenguatge demanat, cal instal·lar la llibreria ANTLR4:

```
pip install antlr4-python3-runtime
```

Per tal de que l'script generi el graf amb les preguntes i les respostes donades, cal instal·lar la llibreria de python NetworkX amb la següent comanda:

```
pip install networkx
```

Per poder executar el bot d'enquestes, cal descarregar i instal·lar la llibreria Python-telegram-bot, que s'ha usat per desenvolupar-lo:
```
pip install python-telegram-bot --upgrade
```

Per configurar el bot cal enviar el missatge /newbot al BotFather de telegram, que us demanarà un nom i un usuari, i generarà una clau d'autorització pel vostre nou bot. Aquesta clau s'ha de guardar en un fitxer token.txt dins de la carpeta on estarà el bot.

## Executant els tests

Amb la comanda
```
antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g
```
compilarem la gramàtica i generarem la plantilla del visitor (ExprVisitor.py), tot i que s'ignorarà ja que el visitor ja està definit. A continuació, farem servir l'script script.py per veure si la gramàtica és correcte, reconeix l'input donat i generara el graf demanat mitjançant la llibreria NetworkX.

```
python3 script.py input.txt
```

A continuació executarem el Bot i ja el podrem fer servir dins del Telegram:

```
python3 BotEnquestes.py
```


## Authors

* **Pol Garcia Recasens** - [lop1498](https://github.com/lop1498)

