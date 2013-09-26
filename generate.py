import template_engine
import markdown
import glob
import re

def generate_page(pagename):
    page_filename = re.search("pages/(.*?).markdown", pagename).group(1)
    page_contents = open(pagename).read().decode("utf-8").encode("ascii", "xmlcharrefreplace")
    page_title = re.search("#(.*?)#", page_contents).group(1)
    
    contents = markdown.markdown(page_contents)
    values={}
    values["contents"] = contents
    values["title"] = page_title
    values["sitename"] = "Golf"
    values["siteslogan"] = "A Static WEbsite Generator"
    values["copyright"] = "Gokberk YALTIRAKLI"
    generated_page = template_engine.apply_template(open("template.html").read(), values)
    open("site/%s.html" % page_filename, "w+").write(generated_page)

for page in glob.glob("pages/*.markdown"):
    generate_page(page)
