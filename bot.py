import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import sys
import networkx as nx
from networkx import *
import tkinter
import matplotlib.pyplot as plt
import numpy as np

from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from antlr4.InputStream import InputStream
from EnquestesVisitor_o import EnquestesVisitor_o

preguntes = []
respostes = [[]]


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Soc un Bot que fa enquestes!")

def help(bot, update):
    text = """L’objectiu general del bot consisteix en recollir les dades d’enquestes definides mitjançant un compilador i consultar gràfiques simples i informes sobre les dades recollides. \n
Les comandes que inclou el bot són les següents:\n
    author: El nom de l'autor i el seu correu de la Facultat d'Informàtica de Barcelona\n
    start: Inicia la conversa amb el bot\n
    help: Informació i comandes\n
    quiz: Inicia un intèrpret\n
    bar: Mostra un diagrama de barres de les respostes a la pregunta donada\n
    pie: Mostra una gràfica de formtges amb el percentatge de les respostes a la pregunta donada\n
    report: Retorna una taula amb el nombre de respostes obtingudes per cada valor de cada pregunta"""
    bot.send_message(chat_id=update.message.chat_id, text=text)

def author(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="""Pol Garcia Recasens
pol.garcia.recasens@est.fib.upc.edu""")

def pie(bot,update,args):

    n = args[0]
    G = nx.read_gpickle("test.gpickle")
    valors = G._node[n]['valors']

    veins = [o for o in G.neighbors(n)]

    for i in veins:
        if (i[0] == 'R'):
            l = [k for k in G._node[i]['respostes']]
    l = l[1:]

    if l[0] == 'zero':
        for i in range(len(l)):
            if not i in valors:
                valors[i] = 0

    else:
        for i in range(1,len(l)):
            if not i in valors:
                valors[i] = 0

    tams = list(valors.keys())
    labels = list(valors.values())

    explode = [0.075 for x in range(len(tams))]
    explode[0] = 0.15

    plt.pie(tams, labels=labels,autopct='%1.1f%%', shadow=True, startangle=140, explode = explode)
    plt.axis('equal')
    plt.savefig('prova.png')
    bot.send_photo(chat_id=update.message.chat_id, photo=open('prova.png', 'rb'))


def bar(bot,update,args):

    n = args[0]
    G = nx.read_gpickle("test.gpickle")
    valors = G._node[n]['valors']

    veins = [o for o in G.neighbors(n)]

    for i in veins:
        if (i[0] == 'R'):
            l = [k for k in G._node[i]['respostes']]
    l = l[1:]

    if l[0] == 'zero':
        for i in range(len(l)):
            if not i in valors:
                valors[i] = 0

    else:
        for i in range(1,len(l)):
            if not i in valors:
                valors[i] = 0

    tams = list(valors.keys())
    labels = list(valors.values())

    y_pos = np.arange(len(tams))

    plt.bar(y_pos, tams)
    plt.xticks(y_pos, labels)
    plt.savefig('prova1.png')
    bot.send_photo(chat_id=update.message.chat_id, photo=open('prova1.png', 'rb'))

def report(bot,update):

    G = nx.read_gpickle("test.gpickle")
    nodes = sorted(list(G.nodes()))

    llista = """"""

    for i in nodes:
        if (i[0] == 'P'):
            valors = G._node[i]['valors']
            for k in valors:
                llista = llista + i + " " + str(k) + " " + str(valors[k]) + "\n"

    bot.send_message(chat_id=update.message.chat_id, text = "pregunta valor respostes\n" + llista)    

def quiz(bot,update,args,user_data):

    try:
        n = args[0]
        if (n == 'E'):

            G = nx.read_gpickle("test.gpickle")
            nodes = sorted(list(G.nodes()))
            l = [x for x in nodes if x[0] == 'P']
            x = l[0]
            user_data['counter'] = 0
    

            t = n + '> ' + G._node[x]['pregunta'] + '\n' 
            veins = [n for n in G.neighbors(x)]

            for i in veins:
                if (i[0] == 'R'):
                    l = [k for k in G._node[i]['respostes']]
                    if (l[1] == 'zero'): cont = 0
                    else: cont = 1
                    for x in l[1:]:
                        t = t + str(cont) + ': ' + x + '\n'
                        cont += 1

            user_data['counter'] += 1
            bot.send_message(chat_id=update.message.chat_id, text = t)


    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='Error')

def msg(bot, update,user_data):
    
    try:

        #resposta a la pregunta counter-1 de la llista ordenada de preguntes
        text = update.message.text
        if (not text.isnumeric()): 
            bot.send_message(chat_id=update.message.chat_id, text='Error! Introdueix un número')
            raise TypeError("Introdueix un número!")

        G = nx.read_gpickle("test.gpickle")

        nodes = sorted(list(G.nodes()))
        l = [x for x in nodes if x[0] == 'P']
        node = [n for n in G.neighbors(l[user_data['counter'] - 1]) if n[0] == 'R']

        #actualitzem respostes

        val = G._node[l[user_data['counter'] - 1]]['valors']
        if int(text) in val:
            val[int(text)] += 1
        else:
            val[int(text)] = 0
        
        if (int(text) > (len(G._node[node[0]]['respostes'])-1)): 
            bot.send_message(chat_id=update.message.chat_id, text='Error! Introdueix un número dins del rang de preguntes')
            raise Exception("Error! Introdueix un número dins del rang de preguntes!")


        val = G._node[l[user_data['counter'] - 1]]['valors'] = val
        nx.write_gpickle(G,"test.gpickle")        

        if (user_data['counter'] < len(l)):

            x = l[user_data['counter']]
                
            t = 'E' + '> ' + G._node[x]['pregunta'] + '\n' 
            veins = [n for n in G.neighbors(x)]

            for i in veins:
                if (i[0] == 'R'):
                    l = [k for k in G._node[i]['respostes']]
                    if (l[1] == 'zero'): cont = 0
                    else: cont = 1
                    for x in l[1:]:
                        t = t + str(cont) + ': ' + x + '\n'
                        cont += 1

            bot.send_message(chat_id=update.message.chat_id, text = t)
            user_data['counter'] += 1

        else: bot.send_message(chat_id=update.message.chat_id, text = "Gràcies pel teu temps!")

    except Exception as e:
        print(e)

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('pie', pie, pass_args=True))
dispatcher.add_handler(CommandHandler('bar', bar, pass_args=True))
dispatcher.add_handler(CommandHandler('report', report))
dispatcher.add_handler(CommandHandler('quiz', quiz, pass_args=True, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text, msg, pass_user_data=True))

updater.start_polling()