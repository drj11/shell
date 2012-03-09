manylines () {
  while : ; do echo ''; done |
  head -9999 |
  nl -ba |
  while read a; do
    printf "%07d\n" "$a"
  done
}
