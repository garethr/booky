#!/usr/bin/env python

"Make file for book project"

# TODO: logging
# TODO: tests
# TODO: pylint
# TODO: file exceptions
# TODO: per function import exceptions

import os
import sys
import getopt
from tempfile import NamedTemporaryFile

def usage():
    print """Build tool for books. Takes files from a source directory and 
generates output in the build directory.

-o, --output [format]      supports html (default), txt or pdf
-p, --processor [engine]   supports textile (default), markdown or none
-c, --clean                removes all files from the build directory
-h, --help                 display this help message
"""

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
    from BeautifulSoup import BeautifulSoup
    # create file containing contents in build 
    output = open("build/output.html", 'w')
    styles = open("source/css/html.css", 'r')
    soup = BeautifulSoup(content)
    try:
        title = soup.h1.string
    except AttributeError:
        title = ""
    header = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <title>%s</title>
    <style type="text/css" media="screen">
    %s
    </style>
</head>
<body>
    """ % (title, styles.read())
    footer = "</body></html>"
    # write contents to file
    output.write("%s%s%s" % (header, content.replace("<pdf:nextpage />", ""), footer))
    return content

def generate_txt(content):
    output = open("build/output.txt", 'w')
    output.write(content.replace("<pdf:nextpage />", ""))
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

def buffer(content):
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

class Builder:
    
    def __init__(self):
        self.callbacks = []
        self.content = ""
    
    def register(self, callback):
        """Registers a callback into the callback queue"""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
            return True
        else:
            return False, "A callback called '%s' has already been "\
                "registered" % callback

    def get_callbacks(self):
        """Returns the callbacks dict"""
        return self.callbacks
        
    def run(self):
        for callback in self.callbacks:
            self.content = callback(self.content)

def main(argv):
    "Build routine for compiling multiple text files into a pdf or html file"

    try:
        opts, args = getopt.getopt(argv, "ho:p:c", ["help", "output=", "processor=", "clean"]) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)

    # set default output to html
    output = "html"   
    # set the default processor to textile
    processor = "textile"
         
    for opt, arg in opts:
        if opt in ("-h", "--help"):      
            usage()
            sys.exit()
        elif opt in ("-c", "--clean"):      
            clean()
            sys.exit()
        elif opt in ("-o", "--output"): 
            if arg in ["html", "pdf", "txt"]:
                output = arg
            else:
                usage()
                sys.exit()
                
        # we only get here if we have a valid output
        if opt in ("-p", "--processor"): 
            if arg in ["textile", "markdown", "none"]:
                processor = arg
            else:
                usage()
                sys.exit()

    # instantiate the builder
    builder = Builder()
    
    builder.register(buffer)
    
    if processor == "markdown":
        builder.register(from_markdown)
    elif processor == "none":
        pass
    else:
        builder.register(from_textile)
        
    builder.register(load_code)
    
    # check if we need to generate a pdf
    if output == "pdf":
        builder.register(generate_pdf)
    elif output == "txt":
        builder.register(generate_txt)
    # alternatively generate html
    else:
        builder.register(generate_html)

    # run any registered callbacks
    builder.run()

if __name__ == '__main__':
    main(sys.argv[1:])