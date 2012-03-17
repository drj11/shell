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

def sh(filename):
    """(A Jinja2 filter that) returns the output resulting from
    running *filename* as a shell script."""
    return shc(open(filename).read())

def shc(inp):
    """(A Jinja2 filter that) pipes the *inp* string into shell,
    and returns the output."""

    import os
    # http://docs.python.org/library/select.html
    import select
    # http://docs.python.org/library/subprocess.html
    import subprocess
    import StringIO

    def asiter():
        return StringIO.StringIO(inp)

    result = ''
    inpiter = asiter()

    child = subprocess.Popen(['bash', '--norc', '-i'],
      env=dict(PS1='$ '),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)
    # The algorithm for reading/writing the child is to loop
    # using select.  If there is anything to read, read it; if
    # we can write, write the next line; when we run out of stuff
    # to write, close the pipe.  In routine operation, closing
    # the pipe connected to child.stdin will cause the child to
    # exit, the stdout pipe will become selectable.
    writable = [child.stdin]
    while True:
        rs,ws,_ = select.select([child.stdout], writable, [])
        if rs:
            frag = os.read(rs[0].fileno(), 1000)
            # If select() told us that we could read from the
            # child, but we don't get anything, that's
            # end-of-file.
            if not frag:
                break
            result += frag
        else:
            try:
                line = inpiter.next()
            except StopIteration:
                child.stdin.close()
                writable = []
                continue
            ws[0].write(line)
    return result

def test():
    print shc("pwd\n")

def main(argv=None):
    if argv is None:
        argv = sys.argv
    for f in argv[1:]:
        render(sys.stdout, f)

contents = locals()

if __name__ == '__main__':
    main()
