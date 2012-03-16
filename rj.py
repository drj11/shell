#!/usr/bin/env python
# rj.py
# Render Jinja

import sys

def render(out, filename):
    """Render to the stream *out* the file *filename* (treating
    it as a jinja2 template.  An additonal final newline is
    written (to compensate for the fact that jinja2 removes
    one)."""
    import jinja2

    e = jinja2.Environment()
    e.filters.update(contents)
    t = e.from_string(open(filename).read())
    out.write(t.render())
    out.write('\n')

def content(filename):
    """(A Jinja2 filter that) returns the contents of the file
    named *filename*."""

    return open(filename).read()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    for f in argv[1:]:
        render(sys.stdout, f)

contents = locals()

if __name__ == '__main__':
    main()
