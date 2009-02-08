#!/usr/bin/env python

import unittest

from booky.lib.builder import Builder

class BuilderTest(unittest.TestCase):
        
    def assert_equal(self, *args, **kwargs):
        "Assert that two values are equal"
        return self.assertEqual(*args, **kwargs)      

    def assert_not_equal(self, *args, **kwargs):
        "Assert that two values are not equal"
        return not self.assertEqual(*args, **kwargs)
        
    def test_builder_init(self):
        builder = Builder()
        self.assert_equal(builder.callbacks, [])
        self.assert_equal(builder.content, "")

    def test_builder_registration(self):
        def func(): 
            pass
        builder = Builder()
        function = func
        builder.register(function)
        self.assert_equal(builder.get_callbacks(), [function])

    def test_run_builder(self):
        def ret(content):
            return "return"
        builder = Builder()
        function = ret
        builder.register(function)
        self.assert_equal(builder.content, "")
        builder.run()
        self.assert_equal(builder.content, "return")
        
    def test_duplicate_registration_with_builder(self):
        def ret(content):
            return "return"
        builder = Builder()
        function = ret
        builder.register(function)
        self.assert_equal(builder.get_callbacks(), [function])
        builder.register(function)
        self.assert_equal(builder.get_callbacks(), [function])
        self.assert_equal(builder.content, "")
        builder.run()
        self.assert_equal(builder.content, "return")
        
if __name__ == "__main__":
    unittest.main()