#!/usr/bin/env python3

"""
** Help for the documentation. **
---------------------------------

The *raisin* documentation is made to be generated automatically from the *pdoc3* tool.

* If you want to generate the documentation yourself, please follow the steps below:
    * *install pdoc3* : ``pip install pdoc3``
    * *generate documentation* : ``pdoc3 raisin/ -c latex_math=True --force --http localhost:8080``
    * *display documentation* : in a browser, explore http://localhost:8080/raisin/
* If you want to consult the official documentation:
    * Go to the site http://raisin-docs.ddns.net/.
"""

import inspect


def make_pdoc(obj_names, obj_refs):
    """
    ** Allows to simplify the description of object aliases. **

    Parameters
    ----------
    obj_names : list
        The list of object names, often the constant *__all__*.
    obj_refs : dict
        To each object name, associate the object itself.
        This dictionary can be retrieved with *globals()* or *locals()*.

    Returns
    -------
    __pdoc__ : dict
        Each object or attribute name is associated with
        a short description that refers to the full description.
        This dictionary must be associated to the variable __pdoc__ which is interpreted by *pdoc3*.
    """
    return {
        **{
            obj: 'Alias to ``raisin.{}.{}``'.format(
                (inspect.getsourcefile(obj_refs[obj]).split('raisin/')[-1][:-3])
                .replace('/', '.')
                .replace('.__init__', ''),
                obj,
            )
            for obj in obj_names
            if inspect.ismodule(obj) or inspect.isclass(obj)
            or inspect.ismethod(obj) or inspect.isfunction(obj)
        },
        **{
            f'{cl}.{meth}': False
            for cl in obj_names
            if obj_refs[cl].__class__.__name__ == 'type'
            for meth in obj_refs[cl].__dict__
            if not meth.startswith('_')
        },
    }
