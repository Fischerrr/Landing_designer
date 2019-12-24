import re
from itertools import groupby


def groupby_specifications(specifications):
    list_group = []
    group_spec = groupby(specifications, key=lambda x: getattr(x, 'group_parameter'))
    for group, list_gr in group_spec:
        if group:
            tuple_group = (group, list(list_gr))
            list_group.append(tuple_group)
        else:
            list_group.extend(list(list_gr))
    return list_group


def svg_code(svg):
    svg_re = re.findall(r'<svg[\D\d]+</svg>', svg.read().decode('utf-8'))[0]
    str_svg = re.sub(r'fill=([\S]+)', '', svg_re)

    return str_svg
