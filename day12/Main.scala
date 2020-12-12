import scala.annotation.tailrec

object Main {
  sealed trait Command
  final case class North(amount: Int) extends Command
  final case class South(amount: Int) extends Command
  final case class East(amount: Int) extends Command
  final case class West(amount: Int) extends Command
  final case class Left(angle: Int) extends Command
  final case class Right(angle: Int) extends Command
  final case class Forward(amount: Int) extends Command

  final case class State1(x: Int, y: Int, angle: Int)
  final case class State2(
      shipX: Int,
      shipY: Int,
      waypointX: Int,
      waypointY: Int
  )

  def main(args: Array[String]): Unit = {
    val commands = io.Source.stdin
      .getLines()
      .map(parseCommand)
      .toList

    val state1 = move1(State1(x = 0, y = 0, angle = 0), commands)
    println(state1)
    println(
      s"${state1.x.abs} + ${state1.y.abs} = ${state1.x.abs + state1.y.abs}"
    )

    val state2 = move2(
      State2(shipX = 0, shipY = 0, waypointX = 10, waypointY = 1),
      commands
    )
    println(state2)
    println(
      s"${state2.shipX.abs} + ${state2.shipY.abs} = ${state2.shipX.abs + state2.shipY.abs}"
    )
  }

  def parseCommand(line: String): Command = {
    val command = line(0)
    val amount = line.substring(1).toInt
    command match {
      case 'N' => North(amount)
      case 'S' => South(amount)
      case 'E' => East(amount)
      case 'W' => West(amount)
      case 'L' => Left(amount)
      case 'R' => Right(amount)
      case 'F' => Forward(amount)
    }
  }

  @tailrec
  def move1(state: State1, commands: List[Command]): State1 = {
    commands match {
      case Nil => state
      case North(amount) :: commands =>
        move1(state.copy(y = state.y + amount), commands)
      case South(amount) :: commands =>
        move1(state.copy(y = state.y - amount), commands)
      case East(amount) :: commands =>
        move1(state.copy(x = state.x + amount), commands)
      case West(amount) :: commands =>
        move1(state.copy(x = state.x - amount), commands)
      case Left(angle) :: commands =>
        move1(state.copy(angle = state.angle + angle), commands)
      case Right(angle) :: commands =>
        move1(state.copy(angle = state.angle - angle), commands)
      case Forward(amount) :: commands =>
        val equivalentCommand = modulo(state.angle, 360) match {
          case 0   => East(amount)
          case 90  => North(amount)
          case 180 => West(amount)
          case 270 => South(amount)
        }
        move1(state, equivalentCommand :: commands)
    }
  }

  @tailrec
  def move2(state: State2, commands: List[Command]): State2 = {
    commands match {
      case Nil => state
      case North(amount) :: commands =>
        move2(state.copy(waypointY = state.waypointY + amount), commands)
      case South(amount) :: commands =>
        move2(state.copy(waypointY = state.waypointY - amount), commands)
      case East(amount) :: commands =>
        move2(state.copy(waypointX = state.waypointX + amount), commands)
      case West(amount) :: commands =>
        move2(state.copy(waypointX = state.waypointX - amount), commands)
      case Left(angle) :: commands =>
        val (waypointX, waypointY) = angle match {
          case 0   => (state.waypointX, state.waypointY)
          case 90  => (-state.waypointY, state.waypointX)
          case 180 => (-state.waypointX, -state.waypointY)
          case 270 => (state.waypointY, -state.waypointX)
        }
        move2(
          state.copy(waypointX = waypointX, waypointY = waypointY),
          commands
        )
      case Right(angle) :: commands =>
        val (waypointX, waypointY) = angle match {
          case 0   => (state.waypointX, state.waypointY)
          case 270 => (-state.waypointY, state.waypointX)
          case 180 => (-state.waypointX, -state.waypointY)
          case 90  => (state.waypointY, -state.waypointX)
        }
        move2(
          state.copy(waypointX = waypointX, waypointY = waypointY),
          commands
        )
      case Forward(0) :: commands =>
        move2(state, commands)
      case Forward(amount) :: commands =>
        move2(
          state.copy(
            shipX = state.shipX + state.waypointX,
            shipY = state.shipY + state.waypointY
          ),
          Forward(amount - 1) :: commands
        )
    }
  }

  @tailrec
  def modulo(amount: Int, base: Int): Int = {
    if (amount < 0) {
      modulo(amount + base, base)
    } else {
      amount % base
    }
  }
}
