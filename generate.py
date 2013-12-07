import template_engine
import markdown
import glob
import re

def get_config():
    config = {
    'sitename': 'GKBRK',
    'siteslogan': 'A Developers Website',
    'copyright': 'Gokberk Yaltirakli'
    }
    return config

def generate_page(pagename):
    page_filename = re.search("pages/(.*?).markdown", pagename).group(1)
    page_contents = open(pagename).read().decode("utf-8").encode("ascii", "xmlcharrefreplace") #UTF-8 Character Support
    page_title = re.search("#(.*?)#", page_contents).group(1)
    
    contents = markdown.markdown(page_contents)
    values={}
    values["contents"] = contents
    values["title"] = page_title
    values.update(get_config())
    with open("template.html") as template_file:
        generated_page = template_engine.apply_template(template_file.read(), values)
    
    with open("site/%s.html" % page_filename, "w+") as site_file:
        site_file.write(generated_page)

for page in glob.glob("pages/*.markdown"):
    generate_page(page)
