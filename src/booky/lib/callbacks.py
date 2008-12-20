import sys
import os
from tempfile import NamedTemporaryFile

def usage():
    print """Booky. Build tool for books. Takes files from a source directory and 
generates output in the build directory in different formats.

-o, --output [format]      supports html (default), txt or pdf
-p, --processor [from]     supports textile (default), markdown or none
-c, --clean                removes all files from the build directory
-h, --help                 display this help message
"""

def clean():
    file_list = os.listdir('build')
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

def upload_pdf_to_s3(content):
    import S3
    import mimetypes
    from booky.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
        BUCKET_NAME
    
    conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    filename = "output.pdf"  
    filedata = open("build/%s" % filename, 'rb').read()
    content_type = mimetypes.guess_type(filename)[0]
    conn.put(BUCKET_NAME, filename, S3.S3Object(filedata), 
        {'x-amz-acl': 'public-read', 'Content-Type': content_type})
    return content

def content_buffer(content):
    # get a list of all files in source
    file_list = os.listdir('source')
    # get contents of all files in source
    # and add all contents together into one string
    content = ''
    for individual_file in file_list: 
        file_path = "source/%s" % individual_file
        if os.path.isfile(file_path) and file_path[7] != '.':
            fp = open(file_path, 'r')
            # add a line break between files
            content = content + fp.read() + "\n"
    return content