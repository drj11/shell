ls -1 -- $(IFS=':'; printf "%s/$1\n" $PATH) 2>&-
