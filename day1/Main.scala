object Main {
    def main(args: Array[String]): Unit = {
        val nums = io.Source.stdin.getLines.map(_.toInt).toList
        for (l1 <- nums; l2 <- nums; l3 <- nums) {
                    if (l1 + l2 + l3 == 2020) {
                        val result = l1 * l2 * l3
                        println(s"$l1 * $l2 * $l3 = $result")
                        return
                    }
        }
    }
}
