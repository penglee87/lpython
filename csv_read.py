import csv
import time
import datetime
import re
from operator import itemgetter
from multiprocessing import Pool
import itertools
import networkx as nx
"""
读取CSV数据并作图,待验证
"""

def chunks(l,n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c,n))
        if not x:
            return
        yield x

def csv2nodes(r):
    strptime = time.strptime
    mktime = time.mktime
    l = []
    ppl = set()
    pattern = re.compile(r"""[A-Za-z0-9"/]+?(?=[,\n])""")
    for row in r:        
        with pattern.findall(row) as f:
        #f = pattern.findall(row)
            cell = int(f[3])
            id = int(f[2])
            st = mktime(strptime(f[0],'%d/%m/%Y'))
            ed = mktime(strptime(f[1],'%d/%m/%Y'))
        # collect list
        l.append([(id,cell,{1:st,2: ed})])
        # collect separate sets
        ppl.add(id)
    return (l,ppl)

def csv2graph(source):
    MG=nx.MultiGraph()
    # Remember that I use integers for edge attributes, to save space! Dic above.
    # start: 1
    # end: 2
    p = Pool()
    node_divisor = len(p._pool)
    node_chunks = list(chunks(source,int(len(source)/int(node_divisor))))
    num_chunks = len(node_chunks)
    pedgelists = p.map(csv2nodes,
                       node_chunks)
    ll = []
    ppl = set()
    for l in pedgelists:
        ll.append(l[0])
        ppl.update(l[1])
    MG.add_edges_from(ll)
    return (MG,ppl)

with open('test.csv','r') as source:
    r = source.readlines()
    MG,ppl = csv2graph(r)