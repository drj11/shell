1Page () {
    size=$(stty size)
    rows=${size% *}
    head -n $rows
}
