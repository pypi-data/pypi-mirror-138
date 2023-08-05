import PySimpleGUI as sg
from ADT import hbds
import types

class QueryTree:
    """
    One instance of QueryTree means a item of a Tree and request to
    give sub items. This class doesn't produce any sub query.
    It will be convenient to refined it to define real query. 
    """
    def __init__(self, obj):
        """
        Ceate a query with *obj* on which excute the query.
        """
        self.obj = obj
        self.sub_queries = []
        self.already_exec = False

    def __call__(self):
        """
        Execute the query if it didn't already executed
        and return the resulting sub queries.
        """
        if not self.already_exec:
            self.sub_queries = self.exec()
            self.already_exec = True
        return self.sub_queries
    
    def exec(self):
        """
        Execute the query to retrieve sub queries.
        You must refine this method to produce your own queries.
        """
        return []
    
    @property
    def attrs(self):
        """
        Return list of values to be display.
        By default, return the *obj* as python *str* carried by the query.
        """
        return [str(self.obj)]
    
    @property
    def icon(self):
        """
        Return icon, None by default.
        """
        return None
    
def create_QueryTree(name, attrs=None, icon=None):
    """
    Facility function for define QueryTree without declare a class.
    *name* is a name of created query class that will inherit from QueryTree,
    *attrs* must be a function, *icon* an object.
    If *attrs* and *icon* are None, ...
    """
    def update(clsdic):
        if attrs:
            clsdic['attrs'] = property(fget=attrs)
        if icon:
            clsdic['icon'] = property(fget=lambda i: icon)
    return types.new_class(name, bases=(QueryTree,), exec_body=update)
    
class Tree(sg.Tree):
    def __init__(self, query, **kargs):
        kargs['key'] = self._key(query)
        self.queries_by_key = {self._key(query): query}
        treedata = sg.TreeData()
        treedata.Insert("", self._key(query),
                        text=query.attrs[0], values=query.attrs[1:],
                        icon=query.icon)
        self._exec(query, treedata)
        super().__init__(data=treedata, enable_events=True, **kargs)
##                            show_expanded=False,
    def _exec(self, query, treedata=None):
        """
        Insert sub queries of *query* into the tree.
        """
        # on execute la première query pour savoir s'il elle produit des sous queries
        for q in query():
            if self._key(q) in self.queries_by_key:
                continue
            self.queries_by_key[self._key(q)] = q
            if treedata:
                treedata.Insert(self._key(query), self._key(q),
                                text=q.attrs[0], values=q.attrs[1:],
                                icon=q.icon)
            else:
                self.Insert(self._key(query), self._key(q),
                            text=q.attrs[0], value=q.attrs[1:],
                            icon=q.icon)
        

    def _key(self, query):
        return str(id(query))
    
    def treeview_open(self, event):
        super().treeview_open(event)
        try:
            query = self.queries_by_key[self.SelectedRows[0]]
        except KeyError:
            print('error')
            return
        for q in query():
            self._exec(q)
    
def test():
    import inspect
    from ADT import images

    class Qmodule(QueryTree):
        """*obj* of the query is a module"""
        def exec(self):
            sub = []
            for n in dir(self.obj):
                o = getattr(self.obj, n)
                if inspect.ismodule(o):
                    if o.__name__ != 'builtins': 
                        sub.append(Qmodule(o))
                elif inspect.isclass(o):
                    sub.append(Qclass(o))
                elif inspect.isfunction(o):
                    sub.append(Qfunction(o))
                else:
                    sub.append(Qother(o))
            return sub
        @property
        def attrs(self):
            return [self.obj.__name__]
        @property
        def icon(self):
            return images.pymodule
        

    Qclass = create_QueryTree('Qclass', attrs=lambda self: [self.obj.__name__],
                              icon=images.pyclass)
    Qfunction = create_QueryTree('Qfunction', attrs=lambda self: [self.obj.__name__],
                                 icon=images.pyfunction)
    Qother = create_QueryTree('Qother', attrs=lambda self: [str(self.obj), type(self.obj)])

        
    import sys
    current_module = sys.modules[ globals()['__name__']]
    tree = Tree(Qmodule(current_module), col0_width=30, max_col_width=40, num_rows=30,
                headings=[ 'type'])
    layout = [
        [ tree ],
    ]

    window = sg.Window('QueryTree Test', resizable=True).Layout(layout)
    while True:    
        event, values = window.Read()
        if event is None:
            break
        if event == '__TIMEOUT__': continue
        query_key = values[event][0]
        if query_key in tree.queries_by_key:
            q = tree.queries_by_key[query_key]
            print('query obj', q.obj, q.attrs)
        else:
            print(event, values)

if __name__ == '__main__':
    test()
        
