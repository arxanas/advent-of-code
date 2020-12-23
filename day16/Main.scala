import scala.annotation.tailrec

object Main {
  // Inclusive on both sides.
  final case class ValidFieldRange(start: Int, end: Int)

  type ValidFieldRangeMap = Map[String, List[ValidFieldRange]]
  type Constraints = Map[Int, Set[String]]
  type Ticket = Array[Int]

  def main(args: Array[String]): Unit = {
    val List(validFieldRangeLines, yourTicketLines, nearbyTicketLines) =
      splitByEmptyLines(io.Source.stdin.getLines().toList)

    val validFieldRanges = parseValidFieldRangeLines(validFieldRangeLines)
    val nearbyTickets = nearbyTicketLines.tail
      .map(parseTicket(_))
      .toList
    val invalidNearbyTicketValues =
      nearbyTickets.flatMap(findInvalidTicketValues(validFieldRanges, _))
    println(s"Ticket scanning error rate: ${invalidNearbyTicketValues.sum}")

    val yourTicket = parseTicket(yourTicketLines(1))
    val validNearbyTickets = nearbyTickets.filter(ticket =>
      findInvalidTicketValues(validFieldRanges, ticket).isEmpty
    )

    val constraints1 = makeInitialConstraints(validFieldRanges, yourTicket)
    val constraints2 =
      applyConstraints(validFieldRanges, constraints1, validNearbyTickets)
    val constraints3 = simplifyConstraints(constraints2)
    val solvedConstraints = constraints3.map { case (index, values) =>
      if (values.size == 1) {
        (index, values.head)
      } else {
        sys.error(s"no solution for index $index")
      }
    }
    println(s"Deciphered fields: $solvedConstraints")

    val interestingIndices = solvedConstraints.collect { case (index, fieldName) if fieldName.startsWith("departure") => index }
    val interestingValues = interestingIndices.map(index => BigInt(yourTicket(index)))
    println(s"Product of ticket values $interestingValues is ${interestingValues.product}")
  }

  def splitByEmptyLines(lines: List[String]): List[List[String]] = {
    lines
      .foldLeft(List[List[String]]()) { (acc, line) =>
        line match {
          case "" => List() :: acc
          case line =>
            acc match {
              case Nil      => List(List(line))
              case hd :: tl => (line :: hd) :: tl
            }
        }
      }
      .map(_.reverse)
      .reverse
  }

  val ValidFieldRangeRegex =
    "([a-zA-Z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)".r

  def parseValidFieldRangeLines(
      lines: List[String]
  ): ValidFieldRangeMap = {
    lines.map { line =>
      line match {
        case ValidFieldRangeRegex(
              name,
              rangeStart1,
              rangeEnd1,
              rangeStart2,
              rangeEnd2
            ) =>
          (name -> List(
            ValidFieldRange(start = rangeStart1.toInt, end = rangeEnd1.toInt),
            ValidFieldRange(start = rangeStart2.toInt, end = rangeEnd2.toInt)
          ))
      }
    }.toMap
  }

  def parseTicket(line: String): Ticket = {
    line.split(",").map(_.toInt)
  }

  def findInvalidTicketValues(
      validFieldRanges: ValidFieldRangeMap,
      ticket: Ticket
  ): List[Int] = {
    ticket.collect {
      case value if !isValidFieldValue(validFieldRanges, value) => value
    }.toList
  }

  def isInValidFieldRanges(
      ranges: List[ValidFieldRange],
      value: Int
  ): Boolean = {

    ranges.exists { case ValidFieldRange(start, end) =>
      (start <= value && value <= end)
    }
  }

  def isValidFieldValue(
      validFieldRanges: ValidFieldRangeMap,
      value: Int
  ): Boolean = {
    validFieldRanges.values.exists { validFieldRange =>
      isInValidFieldRanges(validFieldRange, value)
    }
  }

  def makeInitialConstraints(
      validFieldRanges: ValidFieldRangeMap,
      yourTicket: Ticket
  ): Constraints = {
    val validFields = validFieldRanges.keySet
    (0 until yourTicket.length).map(index => (index -> validFields)).toMap
  }

  @tailrec
  def applyConstraints(
      validFieldRanges: ValidFieldRangeMap,
      constraints: Constraints,
      tickets: List[Ticket]
  ): Constraints = {
    tickets match {
      case Nil => constraints
      case ticket :: tl =>
        val updatedConstraints = constraints.map {
          case (index, currentPossibleFields) =>
            val ticketValueAtIndex = ticket(index)
            val impossibleFields = validFieldRanges.collect {
              case (fieldName, validFieldRanges)
                  if !isInValidFieldRanges(
                    validFieldRanges,
                    ticketValueAtIndex
                  ) =>
                fieldName
            }.toSet
            val constrainedPossibleFields =
              currentPossibleFields -- impossibleFields
            (index, constrainedPossibleFields)
        }
        applyConstraints(validFieldRanges, updatedConstraints, tl)
    }
  }

  @tailrec
  def simplifyConstraints(constraints: Constraints): Constraints = {
    val uniqueFieldValues = constraints.collect {
      case (_, values) if values.size == 1 => values.head
    }
    val newConstraints = constraints.map { case (index, values) =>
      if (values.size > 1) {
        (index, values -- uniqueFieldValues)
      } else {
        (index, values)
      }
    }
    if (newConstraints == constraints) {
      newConstraints
    } else {
      simplifyConstraints(newConstraints)
    }
  }
}
