object Main {
  def main(args: Array[String]): Unit = {
    val lines = io.Source.stdin.getLines().toList

    val result = List((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
      .map(calculateNumTrees(lines, _))
      .map(x => { println(x); x })
      .product
    println(s"Result: $result")
  }

  def calculateNumTrees(lines: List[String], slope: Tuple2[Int, Int]): BigInt = {
    val (dColumn, dRow) = slope
    var row = 0
    var column = 0
    var numTrees = 0
    while (row < lines.length) {
      if (lines(row)(column) == '#') {
        numTrees += 1
      }
      row += dRow
      column += dColumn
      column %= lines(0).length
    }
    numTrees
  }
}
