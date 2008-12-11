#!/usr/bin/env python

"Make file for book project"

import os
from optparse import OptionParser

def main(output):
    "Build routine for compiling multiple text files into a pdf or html file"
    # get a list of all files in source
    file_list = os.listdir(os.path.join(os.path.abspath(
        os.path.dirname(os.path.realpath(__file__))), 'source'))
    # get contents of all files in source
    # and add all contents together into one string
    contents = ""
    for individual_file in file_list: 
        file_path = "source/%s" % individual_file
        if os.path.isfile(file_path):
            fp = open(file_path, 'r')
            # add a line break between files
            contents = contents + fp.read() + "\n"
    # create file containing contents in build 
    fp = open("build/output.txt", 'w')
    # write contents to file
    fp.write(contents)
    # check if we need to generate a pdf
    if output == "pdf":
        # TODO: generate pdf
        pass
    # alternatively generate html
    else:
        # TODO: generate html file
        pass

if __name__ == '__main__':
    # instantiate the arguments parser
    PARSER = OptionParser()
    # add an option so we can set the output format
    PARSER.add_option('--output', 
                        action='store', 
                        dest='output', 
                        default='html',
                        type='choice', 
                        choices=['html', 'pdf'],
                        help="output either html or pdf"
                        ),
    # parse the command arguments
    (OPTIONS, ARGS) = PARSER.parse_args()
        
    # run the build script with the passed output option
    main(OPTIONS.output)