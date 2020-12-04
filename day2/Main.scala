object Main {
  def main(args: Array[String]): Unit = {
    val numValidEntries = io.Source.stdin
      .getLines()
      .count(line => {
        val Array(rangeStr, charStr, password) = line.split(" ")
        val Array(rangeStartStr, rangeEndStr) = rangeStr.split("-")
        val rangeStart = rangeStartStr.toInt
        val rangeEnd = rangeEndStr.toInt
        val char = charStr(0)
        val firstCharCorrect = (password(rangeStart - 1) == char)
        val secondCharCorrect = (password(rangeEnd - 1) == char)
        firstCharCorrect ^ secondCharCorrect
      })
    println(s"Num valid entries: $numValidEntries")
  }
}
