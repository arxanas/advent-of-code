import scala.annotation.tailrec

object Main {
  sealed trait Instruction
  final case class Acc(amount: Int) extends Instruction
  final case class Jmp(offset: Int) extends Instruction
  final case class Nop(param: Int) extends Instruction

  final case class ProgramState(
      code: Vector[Instruction],
      pc: Int,
      seenInstructions: Set[Int],
      acc: Int
  )

  final case class ProgramRunResult(terminatedNormally: Boolean, lastAcc: Int)

  def main(args: Array[String]): Unit = {
    val code = io.Source.stdin
      .getLines()
      .map(assemble)
      .toVector

    val ProgramRunResult(terminatedNormally, lastAcc) = run(
      ProgramState(code = code, pc = 0, seenInstructions = Set(), acc = 0)
    )
    println(s"Last acc: $lastAcc")

    val accAfterChange = (0 until code.length)
      .map(changeInstruction(code, _))
      .map(code =>
        run(
          ProgramState(code = code, pc = 0, seenInstructions = Set(), acc = 0)
        )
      )
      .find { case ProgramRunResult(terminatedNormally, lastAcc) =>
        terminatedNormally
      }
      .map { case ProgramRunResult(terminatedNormally, lastAcc) => lastAcc }
    println(s"Acc after change: $accAfterChange")
  }

  def assemble(line: String): Instruction = {
    val Array(instruction, param) = line.split(" ", 2)
    val paramInt = param.toInt
    instruction match {
      case "nop" => Nop(param = paramInt)
      case "acc" => Acc(amount = paramInt)
      case "jmp" => Jmp(offset = paramInt)
    }
  }

  def changeInstruction(
      code: Vector[Instruction],
      index: Int
  ): Vector[Instruction] = {
    code.updated(
      index,
      code(index) match {
        case Nop(param)  => Jmp(offset = param)
        case Jmp(offset) => Nop(param = offset)
        case Acc(amount) => Acc(amount = amount)
      }
    )
  }

  @tailrec
  def run(state: ProgramState): ProgramRunResult = {
    if (state.seenInstructions.contains(state.pc)) {
      ProgramRunResult(terminatedNormally = false, lastAcc = state.acc)
    } else if (state.pc == state.code.length) {
      ProgramRunResult(terminatedNormally = true, lastAcc = state.acc)
    } else {
      val state2 =
        state.copy(seenInstructions = state.seenInstructions + state.pc)
      val state3 = state2.code(state2.pc) match {
        case Nop(_param) =>
          state2.copy(pc = state2.pc + 1)
        case Acc(amount) =>
          state2.copy(pc = state2.pc + 1, acc = state2.acc + amount)
        case Jmp(offset) =>
          state2.copy(pc = state2.pc + offset)
      }
      run(state3)
    }
  }
}
