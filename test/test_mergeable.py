import os
import unittest
import shutil

from able import Mergeable

class TestMergeable(unittest.TestCase):

    def setUp(self) -> None:
        # setup
        self.template = 'Hi from <<A>>, looking at <<B>>.'
        self.nv_list = [{'name': '<<A>>', 'value': 'a'}, {'name': '<<B>>', 'value': 'b'}]

    def test_init(self):
        class Example(str, Mergeable):
            def __init__(self, string_value, nv_list=[]):
                Mergeable.__init__(self)

            def __new__(cls, string_value, nv_list=[]):
                merged_value = string_value
                for nv in nv_list:
                    merged_value = merged_value.replace(nv['name'], nv['value'])

                instance = super().__new__(cls, merged_value)
                return instance

            def create_instance(self):
                return Example(self.merged_value)

        assert (Example(self.template).merge('<<A>>', 'a')=='Hi from a, looking at <<B>>.')
        assert (Example(self.template).merge('<<B>>', 'b')=='Hi from <<A>>, looking at b.')
        assert (Example(self.template).merge('<<A>>', 'a')
                                      .merge('<<B>>', 'b')=='Hi from a, looking at b.')

        assert (Example(self.template).merges(self.nv_list)=='Hi from a, looking at b.')


if __name__ == '__main__':
    unittest.main()