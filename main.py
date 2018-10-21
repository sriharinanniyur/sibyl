from flask import *

data = []
params = []

def getdata():
    global params, data
    params = []
    data = []
    with open('DATA', 'r') as fin:
        for line in fin.readlines():
            row = []
            i = 0
            for bit in line.split():
                if len(params) <= i:    params.append('d[' + str(i) + ']')
                row.append(True if bit == '1' else False)
                i += 1
            data.append(row)

def populate(lst):
    nodes = [elem for elem in lst]
    edges = []
    for n1 in nodes:
        for n2 in nodes:
            if n2 != n1 and [n2, n1] not in edges:
                edges.append([n1, n2])
    return nodes, edges

def compute(nodes, edges):
    if len(nodes) < 1:  raise Exception('must have 1-4 parameters.')
    if len(nodes) == 1:
        return nodes[0].replace('d[', '').replace(']', '').replace('!=', 'xor').replace(
            '0', 'a').replace('1', 'b').replace('2', 'c').replace('3', 'd').replace('4', 'f').upper()
    nodes = list(set(nodes))
    expr_scores = []
    for edge in edges:
        and_score = 0
        or_score  = 0
        xor_score = 0
        nf_score = 0
        ns_score = 0
        and_str = '(' + edge[0] + ' and ' + edge[1] + ')'
        or_str = '(' + edge[0] + ' or ' + edge[1] + ')'
        xor_str = '(' + edge[0] + ' != ' + edge[1] + ')'
        nf_str = '(not ' + edge[0] + ')'
        ns_str = '(not ' + edge[1] + ')'
        for d in data:
            and_score += (1 if eval(and_str) else -1)
            or_score  += (1 if eval(or_str)  else -1)
            xor_score += (1 if eval(xor_str) else -1)
            nf_score  += (1 if eval(nf_str)  else -1)
            ns_score  += (1 if eval(ns_str)  else -1)
        largest = max([and_score, or_score, xor_score, nf_score, ns_score])
        if   and_score == largest:  expr_scores.append([and_str, 0])
        elif xor_score == largest:  expr_scores.append([xor_str, 0])
        elif or_score  == largest:  expr_scores.append([or_str,  0])
        elif nf_score  == largest:  expr_scores.append([nf_str,  0])
        elif ns_score  == largest:  expr_scores.append([ns_str,  0])
    for e in expr_scores:
        for d in data:
            e[1] += (1 if eval(e[0]) else -1)
    expr_scores = sorted(expr_scores, key=lambda escore: escore[1])
    new_exprs = []
    for i in range(len(expr_scores) // 2, len(expr_scores)):
        new_exprs.append(expr_scores[i][0])
    n, e = populate(new_exprs)
    return compute(n, e)

app = Flask(__name__)
@app.route('/')
def home(result=None):
    global params, data
    getdata()
    n, e = populate(params)
    return render_template('index.html', result=compute(n, e))
