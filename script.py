import sys
import networkx as nx
from networkx import *
import tkinter
import matplotlib.pyplot as plt

from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from antlr4.InputStream import InputStream
from EnquestesVisitor_o import EnquestesVisitor_o

if len(sys.argv) > 1:
    input_stream = FileStream(sys.argv[1])
else:
    input_stream = InputStream(input('? '))

lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()

#print(tree.toStringTree(recog=parser))

visitor = EnquestesVisitor_o()
visitor.visit(tree)


G = nx.read_gpickle("test.gpickle")
pos = nx.circular_layout(G)

labels1 = {}
labels2 = {}
edges = list(G.edges)

for i in range(len(edges)):
    t = G[edges[i][0]][edges[i][1]]['tipus']
    
    if 'item' == t:
    	labels1[(edges[i][0], edges[i][1])] = G[edges[i][0]][edges[i][1]]['name']
    elif 'alternativa' == t:
    	labels2[(edges[i][0], edges[i][1])] = G[edges[i][0]][edges[i][1]]['name']

edges = G.edges() 
colors = [G[u][v]['color'] for u,v in edges]
nx.draw(G, pos, edge_color=colors,with_labels=True)
nx.draw_networkx_edge_labels(G,pos, edge_labels=labels1, font_color = 'b')
nx.draw_networkx_edge_labels(G,pos, edge_labels=labels2, font_color = 'g')

plt.savefig("Graph.png", format="PNG")


