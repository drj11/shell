### @export "def"
manylines () {
  for a in 0 1 2 3 4 5 6 7 8 9 ; do
    for b in 0 1 2 3 4 5 6 7 8 9 ; do
      for c in 0 1 2 3 4 5 6 7 8 9 ; do
        for d in 0 1 2 3 4 5 6 7 8 9 ; do
          echo .. $a$b$c$d
        done
      done
    done
  done | dd obs=10000
}
### @export "run"
manylines 2>&- | { head -1 > /dev/null; head -2; }
