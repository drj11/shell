x () { if [ "$1" -eq 0 ];then return;fi;echo "$2";x $(($1-1)) "$2";}
