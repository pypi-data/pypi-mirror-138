import networkx as nx
import matplotlib.pyplot as plt
import ast


num = 0
names = dict()
g = nx.DiGraph()

def createGraph(v, add_name=""):
    global num
    global names
    global g
    curNum = num
    num += 1
    if type(v) == ast.FunctionDef:
        names[curNum] = "Function:" + v.name
        g.add_node(curNum)
        g.add_edge(curNum, createGraph(v.args))
        for u in v.body:
            g.add_edge(curNum, createGraph(u))
    elif type(v) == ast.arguments:
        names[curNum] = "Args"
        for u in v.args:
            g.add_edge(curNum, createGraph(u))
    elif type(v) == ast.arg:
        names[curNum] = str(v.arg)
        g.add_node(curNum)
    elif type(v) == ast.If:
        names[curNum] = "If"
        g.add_edge(curNum, createGraph(v.test))
        numNodeBody = num
        num += 1
        names[numNodeBody] = "Body"
        g.add_edge(curNum, numNodeBody)
        for u in v.body:
            g.add_edge(numNodeBody, createGraph(u))
        numNodeElse = num
        num += 1
        names[numNodeElse] = "else"
        g.add_edge(curNum, numNodeElse)
        for u in v.orelse:
            g.add_edge(numNodeElse, createGraph(u))
    elif type(v) == ast.Compare:
        names[curNum] = "Compare"
        g.add_edge(curNum, createGraph(v.left, "left: "))
        g.add_edge(curNum, createGraph(v.ops[0], "op: "))
        g.add_edge(curNum, createGraph(v.comparators[0], "right: "))
    elif type(v) == ast.Constant:
        names[curNum] = add_name + str(v.value)
        g.add_node(curNum)
    elif type(v) == ast.Name:
        names[curNum] = add_name + str(v.id)
        g.add_node(curNum)
    elif type(v) == ast.Return:
        names[curNum] = "Return"
        g.add_edge(curNum, createGraph(v.value))
    elif type(v) == ast.List:
        names[curNum] = "List"
        for u in v.elts:
            g.add_edge(curNum, createGraph(u))
    elif type(v) == ast.Assign:
        names[curNum] = add_name + "="
        for u in v.targets:
            g.add_edge(curNum, createGraph(u, "left: "))
        g.add_edge(curNum, createGraph(v.value, "right: "))
    elif type(v) == ast.BinOp:
        names[curNum] = add_name + "BinOp"
        g.add_edge(curNum, createGraph(v.left, "left: "))
        g.add_edge(curNum, createGraph(v.op, "op: "))
        g.add_edge(curNum, createGraph(v.right, "right: "))
    elif type(v) == ast.Call:
        names[curNum] = "Call function"
        g.add_edge(curNum, createGraph(v.func))
        numNodeArgs = num
        num += 1
        names[numNodeArgs] = "Args"
        g.add_edge(curNum, numNodeArgs)
        for u in v.args:
            g.add_edge(numNodeArgs, createGraph(u))
    elif type(v) == ast.Attribute:
        names[curNum] = "Attribute"
        g.add_edge(curNum, createGraph(v.value))
        numNode2 = num
        num += 1
        names[numNode2] = str(v.attr)
        g.add_edge(curNum, numNode2)
    elif type(v) == ast.Subscript:
        names[curNum] = "Subscript"
        g.add_edge(curNum, createGraph(v.value, "name: "))
        g.add_edge(curNum, createGraph(v.slice, "ind: "))
    elif type(v) == ast.UnaryOp:
        if type(v.op) == ast.USub:
            curNum = createGraph(v.operand, add_name + "-")
    elif type(v) == ast.Expr:
        names[curNum] = "Expr"
        g.add_edge(curNum, createGraph(v.value))
    elif type(v) == ast.For:
        names[curNum] = "for"
        g.add_edge(curNum, createGraph(v.target))
        g.add_edge(curNum, createGraph(v.iter))
        numNodeBody = num
        num += 1
        names[numNodeBody] = "Body"
        g.add_edge(curNum, numNodeBody)
        for u in v.body:
            g.add_edge(numNodeBody, createGraph(u))
    elif type(v) == ast.LtE:
        names[curNum] = add_name + "<="
        g.add_node(curNum)
    elif type(v) == ast.Eq:
        names[curNum] = add_name + "=="
        g.add_node(curNum)
    elif type(v) == ast.Sub:
        names[curNum] = add_name + "-"
        g.add_node(curNum)
    elif type(v) == ast.Add:
        names[curNum] = add_name + "+"
        g.add_node(curNum)
    return curNum


def showGraph():
    file = ""
    with open("Easy.py", 'r') as f:
        file = f.read()
    ast_obj = ast.parse(file)
    createGraph(ast_obj.body[0])
    subax = plt.subplot(121)
    nx.draw(g, with_labels=True, labels=names)
    fig = plt.gcf()
    fig.set_size_inches(20, 15)
    fig.savefig('artifacts/graph.pdf')
