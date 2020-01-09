# Generated from Enquestes.g by ANTLR 4.7.1
from antlr4 import *
import networkx as nx

if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser

# This class defines a complete generic visitor for a parse tree produced by EnquestesParser.

class EnquestesVisitor_o(ParseTreeVisitor):

    def __init__(self):
        
        self.current_resposta = 0
        self.anterior = 'E'
        self.alternativa = 0
        self.digraph = nx.DiGraph()
        self.item = {}

    def visitRoot(self, ctx:EnquestesParser.RootContext):
        self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#expr.
    def visitExpr(self, ctx:EnquestesParser.ExprContext):
        n = next(ctx.getChildren())

        if n.getSymbol().type == EnquestesParser.IDP:
            g = ctx.getChildren()
            l = [next(g) for i in range(4)]
            self.digraph.add_node(n.getText(),pregunta = l[2].getText(), valors = {})
            self.visit(l[3])
        
        elif (n.getSymbol().type == EnquestesParser.IDR):
            g = ctx.getChildren()
            l = [next(g) for i in range(4)]
            self.current_resposta = n.getText()
            self.digraph.add_node(n.getText(),respostes = [[]])
            self.visit(l[2])
            self.visit(l[3])
        
        elif (n.getSymbol().type == EnquestesParser.IDI):
            g = ctx.getChildren()
            l = [next(g) for i in range(6)]
            idpregunta = l[2].getText()
            idresposta = l[4].getText()
            self.digraph.add_edge(idpregunta,idresposta,color = 'blue',name = l[0].getText(), tipus = 'item')
            self.item[l[0].getText()] = l[2].getText()
            self.visit(l[5])
      
        elif (n.getSymbol().type == EnquestesParser.IDA):
            g = ctx.getChildren()
            l = [next(g) for i in range(4)]
            self.visit(l[2])
            self.visit(l[3])
        
        elif (n.getText() == 'E: ENQUESTA'):
            g = ctx.getChildren()
            l = [next(g) for i in range(3)]
            self.digraph.add_node('E')
            self.visit(l[1])
            self.visit(l[2])
        else:
            self.digraph.add_node('END')
            nx.write_gpickle(self.digraph,"test.gpickle")
        
    # Visit a parse tree produced by EnquestesParser#alternativa.
    def visitAlternativa(self, ctx:EnquestesParser.AlternativaContext):
        g = ctx.getChildren()
        l = [next(g) for i in range(3)]
        self.alternativa = l[0].getText()
        self.visit(l[2])
        self.visitChildren(ctx)


    # Visit a parse tree produced by EnquestesParser#opcions.
    def visitOpcions(self, ctx:EnquestesParser.OpcionsContext):
        if (ctx.getChildCount() == 6):
            g = ctx.getChildren()
            l = [next(g) for i in range(6)]
            self.digraph.add_edge(self.item[self.alternativa],self.item[l[3].getText()],color = 'green', name = l[1].getText(), tipus = 'alternativa')
            self.visit(l[5])
        else:
            g = ctx.getChildren()
            l = [next(g) for i in range(4)]
            self.digraph.add_edge(self.item[self.alternativa],self.item[l[3].getText()],color = 'green', name = l[1].getText(), tipus = 'alternativa')
        self.visitChildren(ctx)


    # Visit a parse tree produced by EnquestesParser#resposta.
    def visitResposta(self, ctx:EnquestesParser.RespostaContext):
        
        if (ctx.getChildCount() == 5):
            g = ctx.getChildren()
            l = [next(g) for i in range(5)]
            self.digraph._node[self.current_resposta]['respostes'].append(l[2].getText()[1:-2])
            self.visit(l[4])

        else:
            g = ctx.getChildren()
            l = [next(g) for i in range(3)]
            self.digraph._node[self.current_resposta]['respostes'].append(l[2].getText()[1:-2])

        self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#enquesta.
    def visitEnquesta(self, ctx:EnquestesParser.EnquestaContext):
        
        if (ctx.getChildCount() == 2):
            g = ctx.getChildren()
            l = [next(g) for i in range(2)]
            self.digraph.add_edge(self.anterior,self.item[l[0].getText()],color = 'black', name = "", tipus = 'enquesta')
            self.anterior = self.item[l[0].getText()]
            self.visit(l[1])
        
        else:
            g = ctx.getChildren()
            l = [next(g) for i in range(1)]
            self.digraph.add_edge(self.anterior,self.item[l[0].getText()],color = 'black', name = "", tipus = 'enquesta')
            self.digraph.add_edge(self.item[l[0].getText()],'END',color = 'black', name = "", tipus = 'enquesta')

        self.visitChildren(ctx)

#del EnquestesParser