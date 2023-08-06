import networkx as nx
# import pygraphviz
import ast
from astgraph import AstVisitor
import os

def main():
    with open('GeneratorOfFibAST/fib.py', 'r') as sourse:
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