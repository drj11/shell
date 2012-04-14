while
  a=$(dd bs=1 count=1 2>&-)
  case $a in
    ('') printf '\n'; false;;
    (*) printf '%s' "$a"; true;;
  esac
do : ;
done
