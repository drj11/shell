pow () {
  # Compute $1 ** $2.
  _pow "$1" "$2" 1
}

_pow () {
  case $2 in
    (0) echo $3; return;;
    (*[13579]) _pow $(($1*$1)) $(($2/2)) $(($1*$3)); return;;
  esac
  _pow $(($1*$1)) $(($2/2)) $3
  return
}

pow 2 21
