from jinja2 import Environment, FileSystemLoader

def get_templates():
    """Get Jinja2 templates environment"""
    return Environment(loader=FileSystemLoader("app/templates"))
