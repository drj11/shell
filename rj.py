#!/usr/bin/env python
# rj.py
# Render Jinja

usage = """rj.py file ..."""

import sys

def render(out, filename):
    """Render to the stream *out* the file *filename* (treating
    it as a jinja2 template).  An additonal final newline is
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

class Shell(object):
    """A class of callable instances that implement a Jinja2
    filter for piping scripts through a shell.  When calling,
    pass the filename of the script to run.
    """

    def __init__(self):
        self.opts = ['--norc']

    def __call__(self, filename):
        return shinp(open(filename), args=self.opts)

    def opt(self, opt):
        """Return an instance with *opt* added as a shell option.
        """

        # http://docs.python.org/release/2.6.7/library/copy.html#module-copy
        import copy

        res = copy.copy(self)
        res.opts = self.opts + ['-'+opt]
        return res

sh = Shell()

def shc(commands):
    """(A Jinja2 filter that) returns the output resulting from
    running the string *commands* as a shell command."""

    import StringIO

    return shinp(StringIO.StringIO(commands))

def shinp(inp, args=[]):
    """Pipes *inp*, which should be an iterable yielding strings,
    into shell (*args* are passed as arguments to the
    shell---usually options).  The output is returned as a single
    string."""

    # http://docs.python.org/library/subprocess.html
    import subprocess

    child = subprocess.Popen(['bash'] + args,
      env=dict(PS1='$ '),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)

    return ''.join(pipe_to_child(child, inp))

def pipe_to_child(child, input):
    """Send *input* to the *child* stdin, and retrieve any
    output that *child* writes on stdout.  Each fragment of
    output if yielded.  *input* should be an iterable of lines.

    Because no attempt is made to read stderr (or any other file
    descriptor the child may be writing to), this works best if
    stderr is closed or redirected to stdout.
    """

    import os
    # http://docs.python.org/library/select.html
    import select

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
            yield frag
        else:
            try:
                line = input.next()
            except StopIteration:
                child.stdin.close()
                writable = []
                continue
            ws[0].write(line)

def test_pwd():
    import os

    assert os.getcwd() in shc("pwd\n")

def main(argv=None):
    if argv is None:
        argv = sys.argv
    for f in argv[1:]:
        render(sys.stdout, f)

contents = locals()
contents['sh.i'] = sh.opt('i')

if __name__ == '__main__':
    main()
