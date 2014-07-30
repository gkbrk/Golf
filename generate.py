# -*- coding: utf-8 -*-
import template_engine
import markdown
import glob
import re
import json
import sys
import shutil
import os

if len(sys.argv) > 1:
    compile_file = sys.argv[1]
else:
    compile_file = "compile.json"

with open(compile_file, encoding="utf-8") as compile_file_handle:
    compile_options = json.loads(compile_file_handle.read())

for compile_folder in compile_options["compile_folders"]:
    if compile_folder["method"] == "markdown-page":
        for page in glob.glob(compile_folder["in"]):
            page = os.path.normpath(page)
            page_filename = re.search(os.path.normpath(compile_folder["in"]).replace("*", "(.*?)").replace("\\", "\\\\"), page).group(1)
            with open(page, encoding="utf-8") as page_file:
                page_contents = page_file.read()
            page_title = re.search("#(.*?)#", page_contents).group(1)

            markdown_contents = markdown.markdown(page_contents)
            values = {}
            values["contents"] = markdown_contents
            values["title"] = page_title
            values.update(compile_options["page_variables"])

            if "page_variables" in compile_folder:
                values.update(compile_folder["page_variables"]) #Allow changing the variables based on the folder.

            if "template_file" in compile_folder:
                template_filename = os.path.normpath(compile_folder["template_file"])
            else:
                template_filename = os.path.normpath(compile_options["template_file"])
            with open(template_filename) as template_file:
                generated_page = template_engine.apply_template(template_file.read(), values)

            with open(os.path.normpath(compile_folder["out"].replace("*", page_filename)), "w+", encoding="utf-8") as html_file:
                html_file.write(generated_page)
    elif compile_folder["method"] == "static-file":
        for static_file in glob.glob(compile_folder["in"]):
            static_file = os.path.normpath(static_file)
            file_name = re.search(os.path.normpath(compile_folder["in"]).replace("*", "(.*?)").replace("\\", "\\\\") + "$", static_file).group(1)
            dest_name = os.path.normpath(compile_folder["out"].replace("*", file_name))
            shutil.copy2(static_file, dest_name)
    elif compile_folder["method"] == "blog-from-file":
        with open(os.path.normpath(compile_folder["config_file"]), encoding="utf-8") as configfile:
            parsed_blogfile = json.loads(configfile.read())
        blog_dir = os.path.dirname(os.path.normpath(compile_folder["config_file"]))
        for blog_post in parsed_blogfile["posts"]:
            with open(os.path.join(blog_dir, blog_post["filename"]), encoding="utf-8") as post_markdown:
                post_markdown_contents = post_markdown.read()
            post_markdown_values = {}
            post_markdown_values.update(blog_post)
            post_markdown_values["content"] = post_markdown_contents
            with open(os.path.normpath(compile_folder["blogpost_template"]), encoding="utf-8") as template_file:
                post_markdown_contents = template_engine.apply_template(template_file.read(), post_markdown_values)
            markdown_contents = markdown.markdown(post_markdown_contents)

            values = {}
            values["contents"] = markdown_contents
            values["title"] = blog_post["title"]
            values.update(compile_options["page_variables"])

            if "page_variables" in compile_folder:
                values.update(compile_folder["page_variables"])

            if "template_file" in compile_folder:
                template_filename = os.path.normpath(compile_folder["template_file"])
            else:
                template_filename = os.path.normpath(compile_options["template_file"])

            with open(template_filename, encoding="utf-8") as template_file:
                generated_page = template_engine.apply_template(template_file.read(), values)

            with open(os.path.normpath(compile_folder["out"].replace("*", blog_post["url"])), "w+", encoding="utf-8") as html_file:
                html_file.write(generated_page)

        values = {}
        values["title"] = compile_options["page_variables"]["sitename"]
        values["contents"] = ""
        values.update(compile_options["page_variables"])

        if "page_variables" in compile_folder:
            values.update(compile_folder["page_variables"])

        for i, blog_post in enumerate(parsed_blogfile["posts"]):
            if i > 5:
                break

            with open(os.path.join(blog_dir, blog_post["filename"]), encoding="utf-8") as post_markdown:
                post_markdown_contents = post_markdown.read()
            post_markdown_values = {}
            post_markdown_values.update(blog_post)
            post_markdown_values["content"] = post_markdown_contents
            with open(os.path.normpath(compile_folder["blogpost_template"]), encoding="utf-8") as template_file:
                generated_page = template_engine.apply_template(template_file.read(), post_markdown_values)
            values["contents"] += generated_page

        values["contents"] = markdown.markdown(values["contents"])
        with open(template_filename, encoding="utf-8") as template_file:
                generated_page = template_engine.apply_template(template_file.read(), values)

        with open(os.path.normpath(compile_folder["out"].replace("*", "index")), "w+", encoding="utf-8") as html_file:
            html_file.write(generated_page)


        values = {}
        values["title"] = "Blog Archive"
        values["contents"] = ""
        values.update(compile_options["page_variables"])

        if "page_variables" in compile_folder:
            values.update(compile_folder["page_variables"])

        for blog_post in parsed_blogfile["posts"]:
            values["contents"] += "<a href=\"%s.html\">%s</a> - %s<br/>" % (blog_post["url"], blog_post["title"], blog_post["datetime"])


        if "template_file" in compile_folder:
            template_filename = os.path.normpath(compile_folder["template_file"])
        else:
            template_filename = os.path.normpath(compile_options["template_file"])

        with open(template_filename, encoding="utf-8") as template_file:
            generated_page = template_engine.apply_template(template_file.read(), values)

        with open(os.path.normpath(compile_folder["out"].replace("*", "archive")), "w+", encoding="utf-8") as html_file:
            html_file.write(generated_page)
