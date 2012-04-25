#!/usr/bin/env python
# drj is testing ksh.
# Suspect that one of the environment variables is upsetting ksh.

import pexpect

script="""# see this comment
echo bar
"""

def doit(env={}):
    child = pexpect.spawn("ksh -i", env=env)

    child.expect('[$] ')
    for line in script.split('\n'):
        print "[send]", line
        child.sendline(line)
        child.expect('[$] ')
        print "[before]", child.before
        print "[after]", child.after

def raises_exception(env):
    """Run 'ksh -i' via pexpect and inject the script line by line;
    return True if an exception is raised, False otherwise.
    """
    child = pexpect.spawn("ksh -i", env=env)
    child.expect('[$] ')
    try:
        for line in script.split('\n'):
            child.sendline(line)
            child.expect('[$] ')
    except pexpect.EOF:
        return True
    return False

def try_env(env):
    """Try calling the script, with random subsets of environment
    variables."""

    import os
    import random

    keys = env.keys()
    keyA = [k for k in keys if random.random() > 0.5]
    keyB = set(keys) - set(keyA)
    envA = dict(env)
    envB = dict(env)
    for k in keyA:
        del envA[k]
    for k in keyB:
        del envB[k]

    print raises_exception(env), sorted(env)
    if len(env) <= 1:
        return
    try_env(envA)
    try_env(envB)

def main():
    import os
    try_env(os.environ)

if __name__ == '__main__':
    main()
