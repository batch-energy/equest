import os, utils

def src_dir()
    return os.path.dirname(__file__)

def template_dir():
    return os.path.join(src_dir(), 'templates')
    
def client_seed_file(client):
    return os.path.join(template_dir(), 'seed_' + client + '.inp')

def project_pd2_text(project_name):
    with open(os.path.join(template_dir, 'template_project.pd2')) as f:
        text = f.read()
    return text.replace('"Template_Project"', '"%s"' % project_name)
