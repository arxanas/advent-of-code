object Main {
  final case class BagDescription(descriptor: String, color: String)

  final case class BagContainee(count: Int, description: BagDescription)

  final case class BagRule(
      container: BagDescription,
      containees: List[BagContainee]
  )

  def main(args: Array[String]): Unit = {
    runTests()

    val rulesList = io.Source.stdin
      .getLines()
      .map(tokenize(_))
      .map(parse(_))
      .toList

    val possibleContainers = rulesList
      .flatMap(bagRule =>
        bagRule.containees.map(containee =>
          (containee.description, bagRule.container)
        )
      )
      .groupBy(_._1)
      .mapValues(_.map(_._2).toSet)
    val numPossibleContainers = findPossibleContainers(
      possibleContainers,
      BagDescription(descriptor = "shiny", color = "gold")
    ).size
    println(s"Num possible containers: $numPossibleContainers")

    val rules = rulesList.groupBy(_.container)
    val numContainedBags = findNumContainedBags(
      rules,
      BagDescription(descriptor = "shiny", color = "gold")
    ) - 1
    println(s"Num contained bags: $numContainedBags")
  }

  def tokenize(line: String): List[String] = {
    val tokenSeparator = "( |, |\\.)"
    line.split(tokenSeparator).toList
  }

  // NOTE: you definitely don't need a recursive-descent parser to do this
  // problem.
  def parse(tokens: List[String]): BagRule = {
    val (tokens2, container) = parseBagDescription(tokens)
    val ("contain" :: tokens3) = tokens2
    BagRule(container = container, containees = parseBagContainees(tokens3))
  }

  def parseBagDescription(
      tokens: List[String]
  ): (List[String], BagDescription) = {
    tokens match {
      case descriptor :: color :: ("bag" | "bags") :: rest =>
        (rest, BagDescription(descriptor = descriptor, color = color))
      case _ => sys.error(s"parseBagDescription: failed parse at $tokens")
    }
  }

  def parseBagContainees(tokens: List[String]): List[BagContainee] = {
    tokens match {
      case Nil => List()
      case nonempty =>
        parseBagContainee(tokens) match {
          case (tokens2, Some(containee)) =>
            containee :: parseBagContainees(tokens2)
          case (tokens2, None) => parseBagContainees(tokens2)
        }
    }
  }

  def parseBagContainee(
      tokens: List[String]
  ): (List[String], Option[BagContainee]) = {
    tokens match {
      case ("no" :: "other" :: "bags" :: Nil) => (List(), None)
      case (num :: tokens2) => {
        val (tokens3, description) = parseBagDescription(tokens2)
        val containee =
          BagContainee(count = num.toInt, description = description)
        (tokens3, Some(containee))
      }
      case _ => sys.error(s"parseBagContainee: failed parse at $tokens")
    }
  }

  def findPossibleContainers(
      possibleContainers: Map[BagDescription, Set[BagDescription]],
      bagDescription: BagDescription
  ): Set[BagDescription] = {
    val bagDescriptions = possibleContainers.getOrElse(bagDescription, Set())
    val nextBagDescriptions =
      bagDescriptions.flatMap(findPossibleContainers(possibleContainers, _))
    bagDescriptions union nextBagDescriptions
  }

  def findNumContainedBags(
      rules: Map[BagDescription, List[BagRule]],
      bagDescription: BagDescription
  ): Int = {
    val List(rule) = rules(bagDescription)
    1 + rule.containees.map { case BagContainee(count, description) =>
      count * findNumContainedBags(rules, description)
    }.sum
  }

  def runTests(): Unit = {
    assert(tokenize("foo, bar.") == List("foo", "bar"))
    assert(
      parseBagDescription(
        List("muted", "crimson", "bags")
      )._2 == BagDescription(
        descriptor = "muted",
        color = "crimson"
      )
    )
    assert(
      parseBagContainees(
        List(
          "1",
          "muted",
          "crimson",
          "bag",
          "4",
          "vibrant",
          "magenta",
          "bags"
        )
      ) == List(
        BagContainee(
          count = 1,
          description = BagDescription(descriptor = "muted", color = "crimson")
        ),
        BagContainee(
          count = 4,
          description =
            BagDescription(descriptor = "vibrant", color = "magenta")
        )
      )
    )

    assert(
      parseBagContainees(
        List(
          "no",
          "other",
          "bags"
        )
      ) == List()
    )
  }
}
