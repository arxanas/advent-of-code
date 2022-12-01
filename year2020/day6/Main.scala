object Main {
  def main(args: Array[String]): Unit = {
    val forms = io.Source.stdin
      .getLines()
      .foldLeft(List[List[String]]()) { (acc, line) =>
        (acc, line) match {
          case (Nil, _)  => List(List(line))
          case (acc, "") => List() :: acc
          case (head :: tail, line) =>
            (line :: head) :: tail
        }
      }

    val anyoneAnsweredYesCount = forms
      .map(forms => forms.flatten.toSet.size)
      .sum
    println(s"Sum of anyone-answered-yes questions: $anyoneAnsweredYesCount")

    val everyoneAnsweredYesCount = forms.map { forms =>
      forms
        .map(_.toSet)
        .reduce(_.intersect(_))
        .size
    }.sum
    println(s"Sum of everyone-answered-yes questions: $everyoneAnsweredYesCount")
  }
}
