import scala.collection.immutable.Nil
object Main {
  sealed trait Bit
  final case object Zero extends Bit
  final case object One extends Bit
  type Mask = List[Option[Bit]]

  sealed trait Instruction
  final case class SetMaskInstruction(mask: Mask) extends Instruction
  final case class SetValueInstruction(address: Long, value: Long)
      extends Instruction

  final case class State(mask: Mask, memory: Map[Long, Long])
  val emptyState = State(mask = List(), memory = Map.empty)

  def main(args: Array[String]): Unit = {
    runTests()

    val instructions = io.Source.stdin
      .getLines()
      .map(parseInstruction(_))
      .toList

    val memorySum1 = instructions
      .foldLeft(emptyState) { (state, instruction) =>
        instruction match {
          case SetMaskInstruction(mask) => state.copy(mask = mask)
          case SetValueInstruction(address, value) =>
            state.copy(memory =
              state.memory + (address -> applyMask1(state.mask, value))
            )
        }
      }
      .memory
      .values
      .sum
    println(s"Memory sum 1: $memorySum1")

    val memorySum2 = instructions
      .foldLeft(emptyState) { (state, instruction) =>
        instruction match {
          case SetMaskInstruction(mask) => state.copy(mask = mask)
          case SetValueInstruction(address, value) =>
            val addresses = makeAddresses(state.mask, toBits(address))
            val memoryUpdates =
              addresses.map(address => (toAddress(address) -> value))
            state.copy(memory = state.memory ++ memoryUpdates)
        }
      }
      .memory
      .values
      .sum
    println(s"Memory sum 2: $memorySum2")
  }

  val SetMaskInstructionRegex = "mask = ([X01]{36})".r
  val SetValueInstructionRegex = "mem\\[([0-9]+)\\] = ([0-9]+)".r
  def parseInstruction(line: String): Instruction = {
    line match {
      case SetMaskInstructionRegex(value) =>
        SetMaskInstruction(value.map {
          case 'X' => None
          case '0' => Some(Zero)
          case '1' => Some(One)
        }.toList)

      case SetValueInstructionRegex(address, value) =>
        SetValueInstruction(address = address.toInt, value = value.toLong)
    }
  }

  def toBits(value: Long): List[Bit] = {
    value.toBinaryString.reverse
      .padTo(36, '0')
      .reverse
      .map {
        case '0' => Zero
        case '1' => One
      }
      .toList
  }

  def applyMask1(mask: Mask, value: Long): Long = {
    val resultString = toBits(value)
      .zip(mask)
      .map {
        case (Zero, None)    => 0
        case (One, None)     => 1
        case (_, Some(Zero)) => 0
        case (_, Some(One))  => 1
      }
      .mkString
    java.lang.Long.parseLong(resultString, 2)
  }

  def toAddress(mask: List[Bit]): Long = {
    val addressString = mask.map {
      case Zero => '0'
      case One  => '1'
    }.mkString
    java.lang.Long.parseLong(addressString, 2)
  }

  def makeAddresses(mask: Mask, address: List[Bit]): Seq[List[Bit]] = {
    makeAddressesHelper(mask.zip(address))
  }

  def makeAddressesHelper(data: List[(Option[Bit], Bit)]): Seq[List[Bit]] = {
    data match {
      case Nil                             => Seq.empty
      case (Some(Zero), addressBit) :: Nil => Seq(List(addressBit))
      case (Some(One), addressBit) :: Nil  => Seq(List(One))
      case (None, _addressBit) :: Nil      => Seq(List(Zero), List(One))
      case (Some(Zero), addressBit) :: tl =>
        makeAddressesHelper(tl).map(mask => addressBit :: mask)
      case (Some(One), addressBit) :: tl =>
        makeAddressesHelper(tl).map(mask => One :: mask)
      case (None, _addressBit) :: tl =>
        List(Zero, One)
          .flatMap(bit => makeAddressesHelper((Some(Zero), bit) :: tl))
    }
  }

  def runTests(): Unit = {
    assert(toAddress(List(One, Zero, One)) == 5)

    assert(
      makeAddresses(
        List(Some(Zero), None, Some(Zero), None, None),
        List(One, One, Zero, One, Zero)
      ) == List(
        List(One, Zero, Zero, Zero, Zero),
        List(One, Zero, Zero, Zero, One),
        List(One, Zero, Zero, One, Zero),
        List(One, Zero, Zero, One, One),
        List(One, One, Zero, Zero, Zero),
        List(One, One, Zero, Zero, One),
        List(One, One, Zero, One, Zero),
        List(One, One, Zero, One, One)
      )
    )
  }
}
