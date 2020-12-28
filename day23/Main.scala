import scala.annotation.tailrec
object Main {
  final case class State(cups: Vector[Int], currentCup: Int)

  def main(args: Array[String]): Unit = {
    runTests()

    println(
      playTurns(
        State(
          cups = cupsStringToVector("327465189"),
          currentCup = 0
        ),
        100
      )
    )

  }

  def playTenMillion(state: State): Vector[Int] = {
    val State(cups2, _) = playTurns(
      State(
        cups = cupsStringToVector("327465189") ++ (10 to 1000000).toVector,
        currentCup = 0
      ),
      10000000
    )
    val indexOf1 = cups2.indexOf(1)
    val nextTwoCups = cups2.slice(indexOf1 + 1, indexOf1 + 3)
    nextTwoCups
  }

  @tailrec
  def playTurns(state: State, numTurns: Int): State = {
    println(s"$numTurns remaining")
    if (numTurns == 0) {
      state
    } else {
      playTurns(playTurn(state), numTurns - 1)
    }
  }

  def playTurn(state: State): State = {
    val State(cups, currentCup) = state
    val threeCups1 = cups.slice(currentCup + 1, currentCup + 4)
    val threeCups2 = cups.slice(0, (3 - threeCups1.length))
    val threeCups = threeCups1 ++ threeCups2
    val cupsMinusThree = cups.filterNot(cup => threeCups.contains(cup))
    val insertionIndex = {
      val minCup = cups.min
      val maxCup = cups.max
      val lesserCups = (cups(currentCup) - 1).to(minCup, -1)
      val greaterCups = maxCup.to(minCup, -1)
      (lesserCups ++ greaterCups).collectFirst {
        case insertionCup if cupsMinusThree.contains(insertionCup) =>
          cupsMinusThree.indexOf(insertionCup)
      }.get
    }
    val (lhsCups, rhsCups) = cupsMinusThree.splitAt(insertionIndex + 1)
    val nextCups = lhsCups ++ threeCups ++ rhsCups
    val nextCurrentCup =
      (nextCups.indexOf(cups(currentCup)) + 1) % nextCups.length
    State(
      cups = nextCups,
      currentCup = nextCurrentCup
    )
  }

  def cupsStringToVector(cupsString: String): Vector[Int] = {
    cupsString.map(_.toString().toInt).toVector,
  }

  def runTests(): Unit = {
    assert(
      playTurn(
        State(
          cups = cupsStringToVector("389125467"),
          currentCup = 0
        )
      ) == State(
        cups = cupsStringToVector("328915467"),
        currentCup = 1
      )
    )
    assert(
      playTurn(
        State(
          cups = cupsStringToVector("325467891"),
          currentCup = 2
        )
      ) == State(
        cups = cupsStringToVector("346725891"),
        currentCup = 6
      )
    )

    assert(
      playTenMillion(
        State(cups = cupsStringToVector("389125467"), currentCup = 0)
      ) == Vector(934001, 159792)
    )
  }
}
