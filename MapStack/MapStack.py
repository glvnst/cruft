#!/usr/bin/python
"""
This module provides Stack, a MutableMapping which implements a sequential key
search through a stack of MutableMapping-style objects and a unionfs-like
whiteout facility for terminating the key search early.

One practical application is a dict with transaction layers. In this
application the whiteout facility lets keys be deleted in a transaction which
can later be rolled-back.
"""
import collections


class Whiteout(object):
    """
    This class is used as a token inside a stack of mapping objects to
    represent an item that has been deleted. Instances communicate the
    deletion to superior layers in the stack. This is intended to be similar
    to the unionfs whiteout facility.
    """

    def __repr__(self):
        return 'MapStack.Whiteout()'


class Stack(collections.MutableMapping):
    """
    A MutableMapping subclass which implements a sequential key search through
    a stack of MutableMapping-style objects and a unionfs-like whiteout
    facility for terminating the search early
    """
    layers = None

    def __init__(self, layers=None):
        """
        Accepts an initial layers argument which is a list of dicts
        """
        if layers:
            self.layers = layers
        else:
            self.layers = []
            self.append_layer()

    def __getitem__(self, key):
        """
        Return the value of key from the layers stack, searching in reverse
        order from layers[-1] to layer[0]. Raise KeyError if the key is not
        found or if a matching whiteout is encountered
        """
        for layer in reversed(self.layers):
            if key in layer:
                item = layer[key]
                if isinstance(item, Whiteout):
                    # A whiteout emulates a failed key search
                    raise KeyError
                return item
        # The search completed, there were no matches
        raise KeyError

    def __contains__(self, item):
        """
        Return true if the layers stack contains item and it is not currently
        deleted ("whited-out"). Implemented by calling our __getitem__
        """
        try:
            self.__getitem__(item)
        except KeyError:
            return False
        return True

    def __setitem__(self, key, val):
        """ Set key=val in the top layer """
        self.layers[-1][key] = val

    def __delitem__(self, key):
        """
        Delete key from the top layer. If key does not exist in the top layer
        then store a whiteout
        """
        if key in self.layers[-1]:
            del self.layers[-1][key]
        else:
            self.layers[-1][key] = Whiteout()

    def __iter__(self):
        """ Return iter() for a flattened copy of self """
        return iter(self.flattened())

    def __len__(self):
        """ Return len() for a flattened copy of self """
        return len(self.fastkeys())

    def __repr__(self):
        """ Return a text representation of self """
        layer_reps = [layer.__repr__() for layer in self.layers]
        return '{}([{}])'.format(type(self).__name__, ", ".join(layer_reps))

    def fastkeys(self):
        """
        Return a set of non-whiteout keys in the layer stack. Faster than the
        keys method, but parity between .fastkeys and .values is not
        guaranteed
        """
        result = set()
        for layer in self.layers:
            whiteouts = set([key for (key, value) in layer.items()
                             if isinstance(value, Whiteout)])
            result = (set(layer.keys()) | result) - whiteouts

        return result

    def flattened(self):
        """
        Return a dict-based copy of self with all layers merged and all
        whiteouts resolved
        """
        # fixme: this is slow and memory intensive and hard to fix and is the
        # chief bottleneck of this module
        result = dict()
        for layer in self.layers:
            result.update(layer)
        return dict([(key, value) for (key, value) in result.items()
                     if not isinstance(value, Whiteout)])

    def keys(self):
        """ Return .keys() of a flattened copy of self """
        return self.flattened().keys()

    def values(self):
        """ Return .values() of a flattened copy of self """
        return self.flattened().values()

    def items(self):
        """ Return .items() of a flattened copy of self """
        return self.flattened().items()

    def update(self, *args, **kwargs):
        """ Update the top layer with the supplied dict arguments """
        self.layers[-1].update(*args, **kwargs)

    def merge_layer(self):
        """ Merge the top layer into the one below it """
        if len(self.layers) < 2:
            raise ValueError(("At least two layers are required to perform a "
                              "merge"))
        source_layer = self.layers.pop()
        self.layers[-1].update(source_layer)

    def append_layer(self, layer=None):
        """ Append a new layer to the layer stack """
        if layer is None:
            self.layers.append(dict())
        else:
            self.layers.append(layer)
        return

    def pop_layer(self):
        """ Pop the layer stack """
        if len(self.layers) < 2:
            raise IndexError("the base layer cannot be removed")
        return self.layers.pop()
