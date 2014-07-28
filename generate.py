import template_engine
import markdown
import glob
import re
import json
import sys
import shutil

if len(sys.argv) > 1:
    compile_file = sys.argv[1]
else:
    compile_file = "compile.json"

with open(compile_file) as compile_file_handle:
    compile_options = json.loads(compile_file_handle.read())

for compile_folder in compile_options["compile_folders"]:
    if compile_folder["method"] == "markdown-page":
        for page in glob.glob(compile_folder["in"]):
            page_filename = re.search(compile_folder["in"].replace("*", "(.*?)").replace("\\", "\\\\"), page).group(1)
            with open(page) as page_file:
                page_contents = page_file.read().decode("utf-8").encode("ascii", "xmlcharrefreplace") #UTF-8 Character Support
            page_title = re.search("#(.*?)#", page_contents).group(1)

            markdown_contents = markdown.markdown(page_contents)
            values = {}
            values["contents"] = markdown_contents
            values["title"] = page_title
            values.update(compile_options["page_variables"])

            if "template_file" in compile_folder:
                template_filename = compile_folder["template_file"]
            else:
                template_filename = compile_options["template_file"]
            with open(template_filename) as template_file:
                generated_page = template_engine.apply_template(template_file.read(), values)

            with open(compile_folder["out"].replace("*", page_filename).replace("\\\\", "\\"), "w+") as html_file:
                html_file.write(generated_page)
    elif compile_folder["method"] == "static-file":
        for static_file in glob.glob(compile_folder["in"]):
            in_folder = compile_folder["in"] + "$"
            file_name = re.search(in_folder.replace("*", "(.*?)").replace("\\", "\\\\"), static_file).group(1)
            dest_name = compile_folder["out"].replace("*", file_name).replace("\\\\", "\\")
            shutil.copy2(static_file, dest_name)
