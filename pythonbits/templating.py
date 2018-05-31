# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *  # noqa: F401, F403

from functools import partial
from math import floor

from . import _release, _github


# tag like [name=value]
def tag(tag_name):
    def func(value=None):
        if value:
            return "[" + tag_name + "=" + str(value) + "]"
        return "[" + tag_name + "]"
    return func


# tag like [name=tv]ev[/name]
def tag_enc(tag_name):
    return lambda ev, tv=None: (tag(tag_name)(tv) + str(ev) +
                                tag('/' + tag_name)())


img = tag('img')
b = tag_enc('b')
link = tag_enc('url')
size = tag_enc('size')
quote = tag_enc('quote')
spoiler = tag_enc('spoiler')
mi = tag_enc('mediainfo')
s1 = partial(size, tv=1)
s2 = partial(size, tv=2)  # default
s3 = partial(size, tv=3)
s4 = partial(size, tv=4)
s7 = partial(size, tv=7)
align = tag_enc('align')
center = partial(align, tv='center')
color = tag_enc('color')
_list = tag_enc('list')


def list(x, style=None):
    v = "".join("[*]"+x for x in x)
    return _list(v, style)


# formats color tuple (255, 235, 85) to hexadecimal string "#ffeb55"
def fmt_col(c):
    return "#" + "{:02x}{:02x}{:02x}".format(*c)


def h(x):
    s = ""
    for c in x:
        if c.isupper():
            s += s3(c)
        else:
            s += c.upper()
    return b(s)


def section(name, content):
    return center(h(name)) + quote(content)


release = align(link(color(s1("Generated by " + _release), '#999'),
                     _github), 'right')


def format_rating(rating, max, limit=10, s=None, fill=None, empty=None):
    if rating is None:
        return "No rating"

    s = s or '★'
    fill = fill or [0xff, 0xff, 0x00]
    empty = empty or [0xa0, 0xa0, 0xa0]

    limit = min(max, limit)
    num_stars = rating * limit / max
    black_stars = int(floor(num_stars))
    partial_star = num_stars - black_stars
    white_stars = limit - black_stars - 1

    pf = [comp * partial_star for comp in fill]
    pe = [comp * (1 - partial_star) for comp in empty]
    partial_color = fmt_col(tuple(map(lambda x, y: int(x+y), pf, pe)))

    stars = (color(s * black_stars, fmt_col(fill)) +
             color(s,               partial_color) +
             color(s * white_stars, fmt_col(empty)))
    return str(rating) + '/' + str(max) + ' ' + stars
