# encoding utf-8
"""
Produit une structure json à partir d'un objet ou d'une listes d'objets
HBDS.
Pour les relations, seuls les objets avec des rôles sont pros en compte.
"""

from . import hbds, fonctors, basictypes

def tojson(objs, excluded_attrs=[]):
    """
    Pour l'instant objs doit être une instance de classe HBDS,
    sinon il est considéré comme un itérable.
    """
    if not isinstance(type(objs), hbds.Class):
        return [tojson(o, excluded_attrs) for o in objs]
    return dict([(a,basic(getattr(objs,a))) for a in objs | fonctors.attrs \
                 if a not in excluded_attrs])

def basic(val):
    """
    Convertie si nécessaire une valeur d'un type basic en une valeur compatible
    avec json.
    Pour l'instant, seule les datetime sont converties.
    """
    if isinstance(val, basictypes.datetime):
        return val.isoformat()
    return val
