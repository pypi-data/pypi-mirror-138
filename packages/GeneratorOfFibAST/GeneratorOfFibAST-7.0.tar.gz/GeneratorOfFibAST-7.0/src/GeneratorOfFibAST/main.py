import networkx as nx
# import pygraphviz
import ast
from GeneratorOfFibAST.astgraph import AstVisitor
import os

def main():
    with open('/Library/anaconda3/lib/python3.9/site-packages/GeneratorOfFibAST/fib.py', 'r') as sourse:
        # i have no idea why i need full path...
        tree = ast.parse(sourse.read())

    # делаем гарф
    G = AstVisitor()
    G.visit(tree)

    # осталось вывести граф
    newG = nx.drawing.nx_agraph.to_agraph(G.graph)

    pos = newG.layout('dot')

    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")

    newG.draw(path="artifacts/AstTree.png", format='png')

if __name__ == '__main__':
    main()