import PySimpleGUI as sg
from ADT import hbds

class Thing(metaclass=hbds.Class):
    name = str
    i = int
    j = 1.2

Contain = hbds.Link(Thing, 'Contain', Thing)

t = Thing('t', 0)
t1 = Thing('t1', 1)
t2 = Thing('t2', 2)
Contain(t, t1); Contain(t, t2)
t11 = Thing('t11', 11)
t12 = Thing('t12', 12)
Contain(t1, t11); Contain(t1, t12)
t21 = Thing('t21', 21)
t22 = Thing('t22', 22)
Contain(t2, t21); Contain(t2, t22)

class QueryTree:
    def __init__(self, obj):
        self.obj = obj
        self.sub_queries = None
    def __call__(self):
        if not self.sub_queries:
            self.sub_queries = [QueryTree(obj) for obj in self.obj | hbds.OPSC() | hbds.OFIN()]
        return self.sub_queries
    def show(self):
        return [self.obj.name, [self.obj.i, self.obj.j]]
    @property
    def key(self):
        return str(id(self))

class Tree(sg.Tree):
    def __init__(self, query, **kargs):
        self.queries_by_key = {query.key: query}
        treedata = sg.TreeData()    
        treedata.Insert("", query.key, *query.show())
        for q in query():
            self.queries_by_key[q.key] = q
            treedata.Insert(query.key, q.key, *q.show())
        super().__init__(data=treedata, **kargs)
    def ask(self, window, a_key):
        try:
            query = self.queries_by_key[a_key]
        except KeyError:
            return
        for q in query():
            for sq in q():
                self.queries_by_key[sq.key] = sq
                window.Element(self.Key).Insert(q.key, sq.key, *sq.show())
        
tree = Tree(QueryTree(t), headings=['i', 'j'], 
                        key='_QT_',
                        show_expanded=False,
                        enable_events=True)
layout = [
          [ tree],
##          [ sg.Button('Add'), sg.Button('Remove')]
          ]

window = sg.Window('QueryTree Test').Layout(layout)
select = []
new = 0
while True:    
    event, values = window.Read()
    if event is None:
        break
    print(event, values)
    
    if event == '_QT__EXPAND_':
        select = values['_QT_']
        print(select)
        tree.ask(window, select[0])
            
        
