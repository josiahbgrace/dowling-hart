#helperfunctions
import os
import markdown
import codecs
from flask import render_template
from jinja2 import Template

class UtilityFunc:
    """
    This is a blanket class that will be used for smart generation and
    computation, e.g. only generating the name_year object when it has 
    changes, etc. It is mostly flags and "generate" methods that will
    call the methods contained in the utility class outside of this 
    UtilityFunc 
    """

    def __init__(self):
        self.template_render = None
        self.name_year = None

    def generate_file_years(self, path):
        self.name_year = return_file_years(path)

def return_file_years(path):
    """
    Loop through the files specified by the path and parse the top level
    comment, return a dictionary mapping file-name to file years.
    Summarize the result dictionary with a count of the distance between
    the two years.
    Also return a string containing the html of the given markdown file. 
    """
    name_year = {}
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        for entry in files:
            file_path = os.path.join(root, entry)
            name_year[entry] = parse_markdown_headers(file_path)
            name_year[entry]["md"] = return_html(file_path)

    return (summarize_years(name_year), name_year)

def parse_markdown_headers(path):
    """
    Markdown headers are in the form of html comments, <!-- key:value, -->
    Return a dictionary mapping keys to values.  
    """
    return_dict = {}
    with open(path, 'r') as f:
        key_val = f.readline()[4:-4].rstrip().split(",")
        for key in key_val:
            temp = key.split(":")
            return_dict[temp[0].strip()] = temp[1]
    return return_dict

def summarize_years(name_year):
    """
    Return the number of years between the bottom and top entry in the
    input name to year dictionary. And the year of the bottom entry. 
    """
    temp = sorted([f for f in name_year.items() \
        if not f[1]["date"] == "none"], key=lambda x: int(x[1]["date"]))

    return (int(temp[-1][1]["date"]) - int(temp[0][1]["date"]),  \
            int(temp[0][1]["date"]))

def return_html(path):
    """
    Given an input path, return an html string of the corresponding input
    markdown. Also use jinja macro to process figures in the text.
    """
    f = codecs.open(path, mode="r", encoding="utf-8")
    html = markdown.markdown(f.read(), output_format="html5", safe_mode=False)
    t = Template("""
      {% macro figure(src, caption) -%}
      <figure class="cap-top">
	      <a href="{{ src }}">
             <img src="{{ src }}" alt="{{ caption }}">
		  </a>
      <figcaption>
          {{ caption }}
      </figcaption>
      </figure>
      {%- endmacro %}
	  """ + html)
    return t.render()


