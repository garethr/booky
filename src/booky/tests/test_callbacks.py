#!/usr/bin/env python

import unittest

from booky.lib.callbacks import from_textile, from_markdown, _clean

class CallbackTest(unittest.TestCase):
        
    def assert_equal(self, *args, **kwargs):
        "Assert that two values are equal"
        return self.assertEqual(*args, **kwargs)      
        
    def test_textile_converstion(self):
        textile = "h1. heading"
        output = from_textile(textile)
        self.assert_equal(output, "<h1>heading</h1>")

    # need to install markdown library
    def markdown_converstion(self):
        textile = "para"
        output = from_markdown(textile)
        self.assert_equal(output, "<p>para</p>")
    
    def test_clean_pdf_markup(self):
        input_text = "<pdf:nextpage /><pdf:toc />test<pdf:pagenumber />"
        output = _clean(input_text)
        self.assert_equal(output, "test")
        
if __name__ == "__main__":
    unittest.main()