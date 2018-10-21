class Node():
	def __init__(self, expr):
		self.expr = expr

nodes = []

class Connection():
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.and_score = self.or_score = self.xor_score = 0

conns = []

#----------------EXAMPLE DATA----------------------------
params = ['d["a"]', 'd["b"]', 'd["c"]', 'd["d"]']
data = [
    {'a':True, 'b':False, 'c':True, 'd':False}, # => True
    {'a':True, 'b':False, 'c':True, 'd':True}, # => True
    {'a':True, 'b':True, 'c':False, 'd':False}, # => True
]
#---------------------------------------------------------

def populate(vlist):
    global nodes, conns
    nodes = []
    conns = []
    visited = []
    for elem in vlist:
        nodes.append(Node(elem))
    for n1 in nodes:
        for n2 in nodes:
            if n2 != n1 and [n2, n1] not in visited:
                conns.append(Connection(n1, n2))
                visited.append([n1, n2])

def compute():
    global nodes, conns
    while len(nodes) > 1:
        new_exprs = []
        expr_scores = []
        for conn in conns:
            and_str = '(' + conn.first.expr + ' and ' + conn.second.expr + ')'
            xor_str = '(' + conn.first.expr + ' != ' + conn.second.expr + ')'
            or_str = '(' + conn.first.expr + ' or ' + conn.second.expr + ')'
            for d in data:
                conn.and_score += (1 if eval(and_str) else -1)
                conn.or_score += (1 if eval(or_str) else -1)
                conn.xor_score += (1 if eval(xor_str) else -1)
            largest = max([conn.and_score, conn.or_score, conn.xor_score])
            if conn.and_score == largest:
                new_exprs.append(and_str)
            elif conn.xor_score == largest:
                new_exprs.append(xor_str)
            elif conn.or_score == largest:
                new_exprs.append(or_str)
        for e in new_exprs:
            expr_scores.append([e, 0])
        for e in expr_scores:
            for d in data:
                e[1] += (1 if eval(e[0]) else -1)
        expr_scores = sorted(expr_scores, key=lambda escore: escore[1])
        new_exprs = []
        for i in range(len(expr_scores) // 2, len(expr_scores)):
            new_exprs.append(expr_scores[i][0])
        populate(new_exprs)
    return nodes[0].expr.replace('"', '').replace('d[', '').replace(']', '').replace('!=', '^').replace('and', '&').replace('or', '|')

populate(params)
print(compute())
