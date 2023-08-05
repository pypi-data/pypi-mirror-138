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

class Query:
    def __init__(self, obj):
        self.obj = obj
    def __call__(self):
        return [Query(obj) for obj in self.obj | hbds.OPSC() | hbds.OFIN()]
    def show(self):
        return [self.obj.name, [self.obj.i, self.obj.j]]


def Tree(query):
    treedata = sg.TreeData()    
    treedata.Insert("", 'q', *query.show())
    for i,q in enumerate(query()):
        treedata.Insert('q', 'q%d'%i, *q.show())

    tree = sg.Tree(data=treedata,
                        headings=['i', 'j'],
                        auto_size_columns=True,
                        #num_rows=20,
                        #col0_width=30,
                        key='_QT_',
                        show_expanded=False,
                        enable_events=True)
    return tree


layout = [
          [ Tree(Query(t))],
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
##        if len(select) == 0:
##            select.append('q')
        print(select)
        if 'q' in select:
            for i, q in enumerate([q1, q2]):
                for j,x in enumerate(q()):
                    window.Element('_QT_').Insert(
                        'q%d'%i,'q%d%d'%(i,j), *x.show())
            
        
