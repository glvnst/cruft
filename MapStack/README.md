# MapStack

MapStack is a python module which provides Stack, a MutableMapping which implements a sequential key search through a stack of other MutableMapping-style objects and a unionfs-like whiteout facility for terminating the key search early. One practical application is a dict with transaction layers. 

A quick note about speed:

- Operations that are relatively fast: `__getitem__()`, `__setitem__()`, `__delitem__()`, `__contains__()`, `append_layer()`, `pop_layer()`, `merge_layer()`

- Operations that are relatively slow: `keys()`, `fastkeys()`, `values()`, `items()`, `len()`, `flattened()`, 

The slower operations are slow because they often involve working with every layer of the stack, and sometimes every key/value pair of each layer.

MapStack is based on collections.MutableMapping, so it mostly acts like a dict. Here's an example python session:

    $ python
    >>> import MapStack
    >>> x=MapStack.Stack()
    >>> x['type']='orange'
    >>> x['color']='orange'
    >>> x['peelcolor']='orange'
    >>> x['what']='food'

So far, very dict-ish. Now we add a couple dict layers on top with `append_layer`.
    
    >>> x.append_layer()
    >>> x['type']='apple'
    >>> x['color']='red'
    >>> del x['peelcolor']
    >>> x.append_layer()
    >>> x['type']='avocado'
    >>> x['color']='greenish'
    >>> x['prep']='broil with soy sauce'
    >>> x.items()
    [('color', 'greenish'), ('type', 'avocado'), ('prep', 'broil with soy sauce'), ('what', 'food')]
    >>> len(x)
    4
    
Each layer's keys show through, upper layers override lower layers if there are key collisions. Deletions persist upward. Let's take a look at what's going on. 
    
    >>> x
    Stack([
    {'color': 'orange', 'peelcolor': 'orange', 'type': 'orange', 'what': 'food'},
    {'color': 'red', 'peelcolor': MapStack.Whiteout(), 'type': 'apple'},
    {'color': 'greenish', 'type': 'avocado', 'prep': 'broil with soy sauce'}])
    >>> x['peelcolor']
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "MapStack.py", line 55, in __getitem__
        raise KeyError
    KeyError
    
As you'd expect, the 'peelcolor' key doesn't resolve. MapStack actually has a value associated with that key, but it's an instance of a special MapStack.Whiteout class.
    
    >>> x.pop_layer()
    {'color': 'greenish', 'type': 'avocado', 'prep': 'broil with soy sauce'}
    >>> x.items()
    [('color', 'red'), ('type', 'apple')]
    >>> x.pop_layer()
    {'color': 'red', 'peelcolor': MapStack.Whiteout(), 'type': 'apple'}
    >>> x.items()
    [('color', 'orange'), ('peelcolor', 'orange'), ('type', 'orange'), ('what', 'food')]
 
The `pop_layer` method pops the layer stack. The other Stack methods `flattened` and `merge_layer` are similar; `flattened` returns an `items()`-like dict based on the current state of the stack, `merge_layer` merges the top layer with the one below it.
