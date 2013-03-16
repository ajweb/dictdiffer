#!/usr/bin/env python
"""
A dictionary difference calculator
Originally posted as:
http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary/1165552#1165552
"""


class DictDiffer(object):
    """
   >>> a = {'a': 1, 'b': 1, 'c': 0}
   >>> b = {'a': 1, 'b': 2, 'd': 0}
   >>> d = DictDiffer(b, a)
   >>> print "Added:", d.added()
   Added: ('d',)
   >>> print "Removed:", d.removed()
   Removed: ('c',)
   >>> print "Changed:", d.changed()
   Changed: ('b',)
   >>> print "Unchanged:", d.unchanged()
   Unchanged: ('a',)

   # nested dictionaries
   >>> a = dict(a=1, b=3, c=dict(d=1, e=3, x=dict(z=1)), f=5)
   >>> b = dict(a=1,b=2, c=dict(d=1,e=2, x=dict(z=1, y=dict(h=4,i=3))))
   >>> d = DictDiffer(b, a)
   >>> print "Added:", d.added()
   Added: (('c', ('x', 'y')),)
   >>> print "Removed:", d.removed()
   Removed: ('f',)
   >>> print "Changed:", d.changed()
   Changed: ('c', 'b', ('c', 'x'), ('c', 'e'))
   >>> print "Unchanged:", d.unchanged()
   Unchanged: ('a', ('c', 'd'), ('c', ('x', 'z')))
   """
    # TODO: on changed() avoid returning duplicate keys.
    # for instance, in the sample in testdoc above, we should get this for changed:
    # ('b', ('c', 'x'), ('c', 'e')),
    """
        Compares two dictionaries, traversing nested dictionaries,
        and provides four simple methods to access the differences between them:
            changed(), removed(), added(), unchanged()

         All four methods return a tuple of tuples of keys.
         When a given key is a nested one, it returns a tuple containing
         all the keys in the path to that key. For instance, given the sample above,
         the second "b" dict bellow contains the new "y" key under "x" and this in turn under "c",
         so it returns on tuple: ('c', ('x', 'y'))

    """

    def __init__(self, current_dict, past_dict):
        self._added,self._removed,self._changed,self._unchanged = self.diff_dicts(current_dict, past_dict)

        for key in (self._changed + self._unchanged):
            if isinstance(current_dict[key[-1]], dict) and isinstance(past_dict[key[-1]], dict):
                self._extend( key[-1], self.__class__(current_dict[key[-1]], past_dict[key[-1]]) )

    def diff_dicts(self, current_dict, past_dict):
        """
        This is the original functionality for simple (not nested) dicts:
            Compares current_dict and past_dict and returns
            (added, removed, changed, unchanged) keys
        """
        set_current, set_past = set(current_dict.keys()), set(past_dict.keys())
        intersect = set_current.intersection(set_past)
        added = list(set_current - intersect)
        removed = list(set_past - intersect)
        changed = list(o for o in intersect if past_dict[o] != current_dict[o])
        unchanged = list(o for o in intersect if past_dict[o] == current_dict[o])
        return added, removed, changed, unchanged

    def _extend(self, parent, diff):
        """
            Adds the given differences to the appropriate members.
            Used with nested dicts.
        """
        self._added += [tuple([parent, o]) for o in diff._added]
        self._removed += [tuple([parent, o]) for o in diff._removed]
        self._changed += [tuple([parent, o]) for o in diff._changed]
        self._unchanged += [tuple([parent, o]) for o in diff._unchanged]

    def added(self):
        return tuple(self._added)
    def removed(self):
        return tuple(self._removed)
    def changed(self):
        return tuple(self._changed)
    def unchanged(self):
        return tuple(self._unchanged)


if __name__ == '__main__':
    from doctest import testmod
    testmod()