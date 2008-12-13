#!/usr/bin/env python

"Make file for book project"

# TODO: logging
# TODO: tests
# TODO: help information
# TODO: html template to include header and footer

import os
import sys
import getopt
from tempfile import NamedTemporaryFile

def usage():
    print "help info"

def clean():
    file_list = os.listdir(os.path.join(os.path.abspath(
        os.path.dirname(os.path.realpath(__file__))), 'build'))
    for individual_file in file_list: 
        file_path = "build/%s" % individual_file
        if os.path.isfile(file_path):
            os.unlink(file_path)

def from_textile(content):
    import textile
    return textile.textile(content)

def from_markdown(content):
    import markdown
    return markdown.markdown(content)

def load_code(content):
    from idiopidae.runtime import Composer
    composer = Composer()
    temporary_file = open("build/code.txt", "w")
    temporary_file.write(content)
    temporary_file.close()
    output = composer.process(temporary_file.name)
    os.unlink(temporary_file.name)
    return output
    
def generate_html(content):
    # create file containing contents in build 
    fp = open("build/output.html", 'w')
    # write contents to file
    fp.write(content)
    return content
    
def generate_pdf(content):
    import ho.pisa as pisa
    pisa.showLogging()
    filename = "build/output.pdf"
    if os.path.isfile(filename):
        os.unlink(filename)
    css = open("source/css/pdf.css", "r")
    pdf = pisa.CreatePDF(content, file(filename, "wb"), default_css=css.read())
    return content

class Builder:
    
    def __init__(self):
        self.callbacks = {}
    
    def register(self, callback, **kwargs):
        """Registers a callback into the callback queue"""

        if callback not in self.callbacks:
            self.callbacks[callback] = kwargs
            return True
        else:
            return False, "A callback called '%s' has already been "\
                "registered" % callback

    def unregister(self, callback, type_):
        """Un-registers a callback into the callback queue"""

        if callback in self.callbacks:
            del self.callbacks[callback]
            return True
        else:
            return False, "No callback called '%s' is present in the queue" % \
                callback

    def get_callbacks(self):
        """Returns the callbacks dict"""
        return self.callbacks
        
    def buffer(self):
        # get a list of all files in source
        file_list = os.listdir(os.path.join(os.path.abspath(
            os.path.dirname(os.path.realpath(__file__))), 'source'))
        # get contents of all files in source
        # and add all contents together into one string
        content = ""
        for individual_file in file_list: 
            file_path = "source/%s" % individual_file
            if os.path.isfile(file_path):
                fp = open(file_path, 'r')
                # add a line break between files
                content = content + fp.read() + "\n"
        return content
        
    def run(self):
        content = self.buffer()
        for callback in self.callbacks:
            content = callback(content)

def main(argv):
    "Build routine for compiling multiple text files into a pdf or html file"

    try:
        opts, args = getopt.getopt(argv, "ho:c", ["help", "output=", "clean"]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)

    # set default output to html
    output = "html"        
    for opt, arg in opts:
        if opt in ("-h", "--help"):      
            usage()
            sys.exit()
        elif opt in ("-c", "--clean"):      
            clean()
            sys.exit()
        elif opt in ("-o", "--output"): 
            if arg in ["html", "pdf"]:
                output = arg
            else:
                usage()
                sys.exit()

    # instantiate the builder
    builder = Builder()
    
    builder.register(from_textile)
    builder.register(load_code)
    
    # check if we need to generate a pdf
    if output == "pdf":
        builder.register(generate_pdf)
    # alternatively generate html
    else:
        builder.register(generate_html)

    # run any registered callbacks
    builder.run()

if __name__ == '__main__':
    main(sys.argv[1:])