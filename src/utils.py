import os, utils, textwrap, re
from collections import defaultdict

def last_split_point(s, max):
    split_point = 0
    for i in range(max):
        if s[i] not in ' ,':
            continue
        elif s[:i].count('"')%2:
            continue
        elif i > 1 and s[i-1] == '=':
            continue
        elif not len(s) > i and s[i+1] == '=':
            continue
        else:
            split_point = i
    if not split_point:
        print s
        raise Exception('Could not find split point')
    else:
        return split_point

def splitter(s, max):

    # the text below indicate text which should be forced to a new line
    # this solution is a little awkward
    def known_new_lines(s):
        new_s = ''
        for i in range(len(s)):
            if any(s[i:i+len(sub)] == sub for sub in [' case ', '{switch', ' default', ' endswitch}']):
                new_s += '\n'
            new_s += s[i]
        return new_s.splitlines()

    lines = []
    for s in known_new_lines(s):
        remaining = s
        while len(remaining) > max:
            new_split_point = last_split_point(remaining, max)
            lines.append(remaining[:new_split_point])
            remaining = remaining[new_split_point:]

        lines.append(remaining)

    return '\n'.join(lines)

def wrap(s):
    return '"' + str(s) + '"'

def unwrap(s):
    return s[1:-1]

def rewrap(s, new_text):
    return wrap(unwrap(s) + new_text)

def suffix(s, new_text):
    return wrap(unwrap(s) + new_text)

def prefix(s, new_text):
    return wrap(new_text + unwrap(s))

def outdent(s, count):
    pat = r'^' + ' ' * count
    return re.sub(pat, '', s)

def merge_dicts(x, y):
    z = y.copy()
    z.update(x)
    return z

def dedupe(l):
    while l[0] == l[-1]:
        l.pop()
    i = 1
    n = len(l)
    while i < n:
        if l[i] == l[i-1]:
            del l[i]
            n -= 1
        else:
            i += 1

def overlap(bounds, bound_list, tol=-0.1):

    '''
    True if bounds overlap any in bounds list

      Positive tol is more permissive to membership,
      Negative tol is more restrictive to membership
    '''

    lower, upper = sorted(bounds)
    return any(upper > (l + tol) and lower < (u - tol)
        for l, u in [sorted(p) for p in bound_list])

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
            print ('  %s - %s') % (i, choice)
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

def input_file_name():
    return os.getcwd().split(os.sep)[-1] + '.inp'

def make_floor_data(data, positions):

    attrs = defaultdict(dict)
    for floor_name, floor_data in data.items():
        for key, value in zip(positions, floor_data):
            attrs[floor_name][key] = value

    return attrs
