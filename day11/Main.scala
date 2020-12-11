import scala.annotation.tailrec
import scala.collection.immutable.Stream.Empty

object Main {
  sealed trait SeatStatus
  final case object Floor extends SeatStatus
  final case object EmptySeat extends SeatStatus
  final case object FullSeat extends SeatStatus

  type Grid = Vector[Vector[SeatStatus]]

  def main(args: Array[String]): Unit = {
    val grid = io.Source.stdin
      .getLines()
      .map(row =>
        row.map {
          case '.' => Floor
          case 'L' => EmptySeat
          case '#' => FullSeat
        }.toVector
      )
      .toVector

    val newGrid1 = simulate1(grid)
    val numFullSeats1 = newGrid1
      .map(row =>
        row.count {
          case FullSeat          => true
          case EmptySeat | Floor => false
        }
      )
      .sum
    println(s"Num full seats 1: $numFullSeats1")

    val newGrid2 = simulate2(grid)
    val numFullSeats2 = newGrid2
      .map(row =>
        row.count {
          case FullSeat          => true
          case EmptySeat | Floor => false
        }
      )
      .sum
    println(s"Num full seats 2: $numFullSeats2")
  }

  val deltas =
    for (di <- List(-1, 0, 1); dj <- List(-1, 0, 1) if !(di == 0 && dj == 0))
      yield (di, dj)

  @tailrec
  def simulate1(grid: Grid): Grid = {
    val newGrid = grid.zipWithIndex.map { case (row, i) =>
      row.zipWithIndex.map { case (column, j) =>
        val numAdjacentFullSeats = deltas.count { case (di, dj) =>
          index(grid, i + di, j + dj) == Some(FullSeat)
        }
        grid(i)(j) match {
          case EmptySeat if numAdjacentFullSeats == 0 => FullSeat
          case FullSeat if numAdjacentFullSeats >= 4  => EmptySeat
          case other                                  => other
        }
      }
    }

    if (newGrid == grid) {
      newGrid
    } else {
      simulate1(newGrid)
    }
  }

  def index(grid: Grid, i: Int, j: Int): Option[SeatStatus] = {
    grid.lift(i).flatMap(subvec => subvec.lift(j))
  }

  @tailrec
  def look(grid: Grid, i: Int, j: Int, di: Int, dj: Int): Option[SeatStatus] = {
    index(grid, i + di, j + dj) match {
      case None                              => None
      case Some(Floor)                       => look(grid, i + di, j + dj, di, dj)
      case seat @ Some(EmptySeat | FullSeat) => seat
    }
  }

  def simulate2(grid: Grid): Grid = {
    val newGrid = grid.zipWithIndex.map { case (row, i) =>
      row.zipWithIndex.map { case (column, j) =>
        val numAdjacentFullSeats = deltas.count { case (di, dj) =>
          look(grid, i, j, di, dj) == Some(FullSeat)
        }
        grid(i)(j) match {
          case EmptySeat if numAdjacentFullSeats == 0 => FullSeat
          case FullSeat if numAdjacentFullSeats >= 5  => EmptySeat
          case other                                  => other
        }
      }
    }

    if (newGrid == grid) {
      newGrid
    } else {
      simulate2(newGrid)
    }
  }
}
