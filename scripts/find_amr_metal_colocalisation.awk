BEGIN {
  FS = OFS = "\t"
}

# First file: AMR acquired genes
NR == FNR {
  key = $11 "|" $12 "|" $13
  amr[key] = $0
  contig[key] = $11
  start[key] = $12
  end[key] = $13
  next
}

# Second file: metal acquired genes
{
  for (k in amr) {
    if ($11 == contig[k] &&
        $12 >= start[k] - 10000 &&
        $13 <= end[k] + 10000) {
      print amr[k], $0
    }
  }
}
