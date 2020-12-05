final case class Bounds(lower: Int, upper: Int)

sealed trait Direction
final object Lower extends Direction
final object Upper extends Direction

object Main {
  val fbBounds = Bounds(lower = 0, upper = 128)
  val lrBounds = Bounds(lower = 0, upper = 8)

  def main(args: Array[String]): Unit = {
    runTests()

    val seatIds = io.Source.stdin
      .getLines()
      .map(findSeat(fbBounds = fbBounds, lrBounds = lrBounds, _, 0))
      .map(getSeatId)
      .toList

    val maxSeatId = seatIds.max
    println(s"Max seat ID: $maxSeatId")

    val missingSeatId = seatIds.sorted
      .zip(12 to maxSeatId)
      .find { case (actual, expected) => actual != expected }
      .map { case (actual, expected) => expected.toString }
      .getOrElse("<not found>")
    println(s"Your seat ID: $missingSeatId")
  }

  def findSeat(
      fbBounds: Bounds,
      lrBounds: Bounds,
      pattern: String,
      index: Int
  ): (Int, Int) = {
    if (index == pattern.length) {
      (fbBounds.lower, lrBounds.lower)
    } else {
      pattern(index) match {
        case 'F' =>
          findSeat(
            fbBounds = updateBounds(fbBounds, Lower),
            lrBounds = lrBounds,
            pattern,
            index + 1
          )
        case 'B' =>
          findSeat(
            fbBounds = updateBounds(fbBounds, Upper),
            lrBounds = lrBounds,
            pattern,
            index + 1
          )
        case 'L' =>
          findSeat(
            fbBounds = fbBounds,
            lrBounds = updateBounds(lrBounds, Lower),
            pattern,
            index + 1
          )
        case 'R' =>
          findSeat(
            fbBounds = fbBounds,
            lrBounds = updateBounds(lrBounds, Upper),
            pattern,
            index + 1
          )
        case direction => sys.error(f"Unrecognized seat direction: $direction")
      }
    }
  }

  def getSeatId(seat: (Int, Int)): Int = {
    val (row, column) = seat
    (row * 8) + column
  }

  def updateBounds(bounds: Bounds, direction: Direction): Bounds = {
    val midpoint = (bounds.upper + bounds.lower) / 2
    direction match {
      case Lower => bounds.copy(upper = midpoint)
      case Upper => bounds.copy(lower = midpoint)
    }
  }

  def runTests(): Unit = {
    assert(updateBounds(Bounds(0, 128), Lower) == Bounds(0, 64))
    assert(updateBounds(Bounds(0, 64), Upper) == Bounds(32, 64))
    assert(updateBounds(Bounds(32, 64), Lower) == Bounds(32, 48))
    assert(updateBounds(Bounds(32, 48), Upper) == Bounds(40, 48))
    assert(updateBounds(Bounds(40, 48), Upper) == Bounds(44, 48))
    assert(updateBounds(Bounds(44, 48), Lower) == Bounds(44, 46))
    assert(updateBounds(Bounds(44, 46), Lower) == Bounds(44, 45))

    assert(
      findSeat(
        fbBounds = fbBounds,
        lrBounds = lrBounds,
        "BFFFBBFRRR",
        0
      ) == (70, 7)
    )
    assert(getSeatId((70, 7)) == 567)

    assert(
      findSeat(
        fbBounds = fbBounds,
        lrBounds = lrBounds,
        "FFFBBBFRRR",
        0
      ) == (14, 7)
    )
    assert(getSeatId((14, 7)) == 119)

    assert(
      findSeat(
        fbBounds = fbBounds,
        lrBounds = lrBounds,
        "BBFFBBFRLL",
        0
      ) == (102, 4)
    )
    assert(getSeatId((102, 4)) == 820)
  }
}
