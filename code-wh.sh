IFS=':'
for p in $PATH
do
    ls "$p/$1" 2>&-
done
