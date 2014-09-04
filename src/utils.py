import os, utils, textwrap

def splitter(s):
    pad = ' '*9
    if s.count(',') > 1:
        # put items of comma separated list on separate lines
        text = '   ' + (',\n' + pad).join([i.strip() for i in s.split(',')])

    else:
        # otherwise, just make sure it's not more than 75 charaters
        wrapper = textwrap.TextWrapper(width=75, subsequent_indent=pad)
        text = '\n'.join(wrapper.wrap(s))

    return text


def src_dir():
    return os.path.dirname(__file__)

def template_dir():
    return os.path.join(src_dir(), 'templates')

def client_seed_file(client):
    return os.path.join(template_dir(), 'seed_' + client + '.inp')

def project_pd2_text(project_name):
    with open(os.path.join(template_dir(), 'seed.pd2')) as f:
        text = f.read()
    return text.replace('"Template_Project"', '"%s"' % project_name)

def choices(l, quit=False):

    while True:
        for i, choice in enumerate(l, 1):
            print ('%s - %s') % (i, choice)
        print
        resp = raw_input('  > ')
        if resp:
            if resp.isdigit() and (int(resp) <= (len(l))):
                return l[int(resp) - 1]
            if resp[0].lower() == 'q' and quit:
                return None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        