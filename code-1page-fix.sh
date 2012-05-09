1Page () {
    size=$(stty size <&2)
    rows=${size% *}
    head -n $rows
}
