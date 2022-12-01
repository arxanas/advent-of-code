import scala.annotation.tailrec
object Main {
  final case class Equation(remainder: BigInt, base: BigInt)

  def main(args: Array[String]): Unit = {
    runTests()

    val timestamp = io.StdIn.readLine().toInt
    val routeIds = io.StdIn
      .readLine()
      .split(",")
      .map {
        case "x"     => None
        case routeId => Some(routeId.toInt)
      }
      .toList

    val (bestRouteId, waitingTime) = routeIds
      .collect { case Some(x) => x }
      .map(routeId =>
        (routeId, findWaitingTime(routeId = routeId, timestamp = timestamp))
      )
      .minBy { case (_, waitingTime) =>
        waitingTime
      }
    println(s"$bestRouteId * $waitingTime = ${bestRouteId * waitingTime}")

    val equations = makeEquations(routeIds)
    val solution = solveEquations(equations)
    println(s"Solution: $solution")
  }

  def findWaitingTime(routeId: Int, timestamp: Int): Int = {
    routeId - (timestamp % routeId)
  }

  def makeEquations(routeIds: List[Option[Int]]): List[Equation] = {
    routeIds.zipWithIndex.collect { case (Some(routeId), index) =>
      Equation(remainder = -index, base = routeId)
    }
  }

  def solveEquations(equations: List[Equation]): BigInt = {
    val finalEquation = equations.reduce[Equation] {
      case (e1 @ Equation(a1, n1), e2 @ Equation(a2, n2)) =>
        val (m1, m2) = calculateBezoutCoefficients(n1, n2)
        val x = (a1 * m2 * n2) + (a2 * m1 * n1)
        val base = n1 * n2
        // Set remainder %= base here -- not mathematically necessary, but the
        // program is too slow without it.
        val remainder = x % base
        Equation(remainder = remainder, base = base)
    }
    getPositiveSolution(finalEquation)
  }

  @tailrec
  def getPositiveSolution(equation: Equation): BigInt = {
    equation match {
      case Equation(remainder, base) if remainder >= 0 => remainder % base
      case Equation(remainder, base) =>
        getPositiveSolution(Equation(remainder + base, base))
    }
  }

  /** See https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    */
  def calculateBezoutCoefficients(a: BigInt, b: BigInt): (BigInt, BigInt) = {
    extendedGcd(old_r = a, r = b, old_s = 1, s = 0, old_t = 0, t = 1)
  }

  @tailrec
  def extendedGcd(
      old_r: BigInt,
      r: BigInt,
      old_s: BigInt,
      s: BigInt,
      old_t: BigInt,
      t: BigInt
  ): (BigInt, BigInt) = {
    if (r == 0) {
      (old_s, old_t)
    } else {
      val quotient = old_r / r
      extendedGcd(
        old_r = r,
        r = (old_r - quotient * r),
        old_s = s,
        s = (old_s - quotient * s),
        old_t = t,
        t = (old_t - quotient * t)
      )
    }
  }

  def runTests(): Unit = {
    assert(findWaitingTime(routeId = 59, timestamp = 939) == 5)
    assert(calculateBezoutCoefficients(240, 46) == (-9, 47))
    assert(
      makeEquations(List(Some(5), None, Some(9))) == List(
        Equation(remainder = 0, base = 5),
        Equation(remainder = -2, base = 9)
      )
    )
    assert(
      solveEquations(
        List(
          Equation(remainder = 0, base = 3),
          Equation(remainder = 3, base = 4),
          Equation(remainder = 4, base = 5)
        )
      ) == 39
    )

    assert(
      solveEquations(
        makeEquations(List(Some(17), None, Some(13), Some(19)))
      ) == 3417
    )
    assert(
      solveEquations(
        makeEquations(List(Some(1789), Some(37), Some(47), Some(1889)))
      ) == 1202161486
    )
  }
}
