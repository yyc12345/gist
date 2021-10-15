from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("./", encoding="utf-8"),
    autoescape=select_autoescape()
)

tmpl_dict = {}

def render(tmpl_path, file_path, param_value):
    global tmpl_dict
    global env
    
    template = tmpl_dict.get(tmpl_path, None)
    if template is None:
        template = env.get_template(tmpl_path)
        tmpl_dict[tmpl_path] = template

    with open(file_path, 'w') as f:
        f.write(template.render(**param_value))

    print("Rendering: {}".format(file_path))

