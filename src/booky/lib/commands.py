import sys
import getopt

from booky.lib.builder import Builder
from booky.lib.callbacks import usage, clean, from_textile, from_markdown, \
    load_code, generate_html, generate_txt, generate_pdf, content_buffer

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
    
    builder.register(content_buffer)
    
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