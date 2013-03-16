from unittest import TestCase

from src.dictdiffer import DictDiffer


class TestDictDiffer(TestCase):
    def setUp(self):
        a = {'a': 1, 'b': 1, 'c': 0}
        b = {'a': 1, 'b': 2, 'd': 0}
        self.d = DictDiffer(b, a)

    def test_added(self):
        self.assertEqual(self.d.added(), ('d',))

    def test_removed(self):
        self.assertEqual(self.d.removed(), ('c',))

    def test_changed(self):
        self.assertEqual(self.d.changed(), ('b',))

    def test_unchanged(self):
        self.assertEqual(self.d.unchanged(), ('a',))


class TestNestedDictDiffer(TestCase):
    def setUp(self):
        self.a = {
            'a':1,
            'b':3,
            'c':{
                'd':1,
                'e':3,
                'x':{
                    'z':1
                }
            },
            'f':5
        }
        self.b = {
            'a':1,
            'b':2,
            'c':{
                'd':1,
                'e':2,
                'x':{
                    'z':1,
                    'y':{
                        'h':4
                    }
                }
            }
        }
        self.d = DictDiffer(self.b, self.a)

    def test_nested_added(self):
        self.assertEqual(self.d.added(), (('c', ('x', 'y')),))

    def test_nested_removed(self):
        self.assertEqual(self.d.removed(), ('f',))

    def test_nested_unchanged(self):
        self.assertEqual(self.d.unchanged(), ('a', ('c', 'd'), ('c', ('x', 'z'))) )

    def test_nested_changed(self):
        self.assertEqual(self.d.changed(), ('c', 'b', ('c', 'x'), ('c', 'e')))
