import scala.util.matching.Regex

object Main {
  final case class Tile(id: Int, lines: Vector[String])

  sealed trait TileFlip
  final case object NotFlipped extends TileFlip
  final case object Flipped extends TileFlip

  sealed trait TileRotation
  final case object TileRotation0 extends TileRotation
  final case object TileRotation90 extends TileRotation
  final case object TileRotation180 extends TileRotation
  final case object TileRotation270 extends TileRotation

  sealed trait EdgeType
  final case object TopEdge extends EdgeType
  final case object RightEdge extends EdgeType
  final case object BottomEdge extends EdgeType
  final case object LeftEdge extends EdgeType

  final case class Edge(
      lhsId: Int,
      lhsEdgeType: EdgeType,
      rhsReversed: Boolean,
      rhsEdgeType: EdgeType,
      rhsId: Int
  )
  type Graph = Set[Edge]

  type UnsolvedImage = Vector[Vector[Option[Tile]]]
  type SolvedImage = Vector[Vector[Tile]]

  val seaMonsterPattern = Vector(
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
  )

  def main(args: Array[String]): Unit = {
    runTests()

    val TileId = "Tile ([0-9]+):".r
    val lines = io.Source.stdin.getLines().toList
    val tiles = splitByEmptyLines(lines).map { tileLines =>
      tileLines.reverse match {
        case Nil                 => sys.error("empty tile")
        case TileId(id) :: lines => Tile(id.toInt, lines.toVector)
        case badId :: lines      => sys.error(s"bad ID: $badId")
      }
    }.toSet

    val graph = buildGraph(tiles)
    val cornerTiles = tiles.filter { tile =>
      val numEdgesInvolvingTile = graph.count {
        case Edge(lhsId, _, _, _, rhsId) =>
          lhsId == tile.id
      }
      numEdgesInvolvingTile <= 2
    }.toSet
    val cornerTileIds = cornerTiles.map(tile => BigInt(tile.id))
    println(s"Corner tiles $cornerTileIds product = ${cornerTileIds.product}")

    val image =
      buildImage(graph, cornerTiles, tiles, makeEmptyImage(tiles), 0).get
    val canonicalImageLines = renderImage(image)
    val imageVariations =
      for (
        tileFlip <- Seq(NotFlipped, Flipped);
        tileRotation <- Seq(
          TileRotation0,
          TileRotation90,
          TileRotation180,
          TileRotation270
        );
        tile = Tile(id = 0, lines = canonicalImageLines)
      ) yield applyTileOrientation(tile, tileFlip, tileRotation).lines

    val numSeaMonsters = imageVariations
      .map(imageLines => countPatternInstances(imageLines, seaMonsterPattern))
      .max
    println(s"Num sea monsters: $numSeaMonsters")

    val hashesPerSeaMonster = seaMonsterPattern.flatten.count {
      case '#' => true
      case _ => false
    }
    val totalNumHashes = imageVariations.head.flatten.count {
      case '#' => true
      case _ => false
    }
    val roughWaterCount = totalNumHashes - (numSeaMonsters * hashesPerSeaMonster)
    println(s"Rough water count: $roughWaterCount")
  }

  def splitByEmptyLines(lines: List[String]): List[List[String]] = {
    lines.foldLeft(List[List[String]]()) { (acc, line) =>
      line match {
        case "" => List() :: acc
        case line =>
          acc match {
            case Nil      => List(List(line))
            case hd :: tl => (line :: hd) :: tl
          }
      }
    }
  }

  def getTileEdge(tile: Tile, edgeType: EdgeType): String = {
    edgeType match {
      case TopEdge    => tile.lines.head
      case RightEdge  => tile.lines.map(_.last).mkString
      case BottomEdge => tile.lines.last.reverse
      case LeftEdge   => tile.lines.map(_.head).mkString.reverse
    }
  }

  def buildGraph(tiles: Set[Tile]): Graph = {
    tiles.flatMap { lhsTile =>
      val edgeInfos =
        for (
          edgeType <- Seq(TopEdge, RightEdge, BottomEdge, LeftEdge);
          reversed <- Seq(false, true)
        ) yield (edgeType, reversed)
      for (
        rhsTile <- (tiles - lhsTile);
        (lhsEdgeType, _) <- edgeInfos;
        (rhsEdgeType, rhsReversed) <- edgeInfos
        if getTileEdge(lhsTile, lhsEdgeType) == {
          val rhsEdge = getTileEdge(rhsTile, rhsEdgeType)
          if (rhsReversed) {
            rhsEdge.reverse
          } else {
            rhsEdge
          }
        }.reverse
      )
        yield Edge(
          lhsId = lhsTile.id,
          lhsEdgeType = lhsEdgeType,
          rhsReversed = rhsReversed,
          rhsEdgeType = rhsEdgeType,
          rhsId = rhsTile.id
        )
    }
  }

  def makeEmptyImage(tiles: Set[Tile]): UnsolvedImage = {
    val dimension = Math.sqrt(tiles.size).toInt
    Vector.fill(dimension)(Vector.fill(dimension)(None))
  }

  def buildImage(
      graph: Graph,
      cornerTiles: Set[Tile],
      tiles: Set[Tile],
      image: UnsolvedImage,
      index: Int
  ): Option[SolvedImage] = {
    if (index >= image.length * image.head.length) {
      Some(image.map(row => row.map(tile => tile.get)))
    } else {
      val row = index / image.head.length
      val column = index % image.head.length
      val candidateTiles = {
        // Optimization: start with a corner tile to significantly reduce the
        // search space.
        if ((row, column) == (0, 0)) {
          cornerTiles
        } else {
          tiles
        }
      }

      val solutions =
        for (
          candidateTile <- candidateTiles;
          nextTiles = tiles - candidateTile;
          tileFlip <- Seq(NotFlipped, Flipped);
          tileRotation <- Seq(
            TileRotation0,
            TileRotation90,
            TileRotation180,
            TileRotation270
          );
          nextImage = updateImageIndex(
            image,
            row,
            column,
            applyTileOrientation(candidateTile, tileFlip, tileRotation)
          );
          nextIndex = index + 1;
          if isValidTilePlacement(nextImage, row, column)
        ) yield buildImage(graph, cornerTiles, nextTiles, nextImage, nextIndex)

      solutions.collectFirst { case Some(solution) =>
        solution
      }
    }
  }

  def updateImageIndex(
      image: UnsolvedImage,
      row: Int,
      column: Int,
      value: Tile
  ): UnsolvedImage = {
    image.updated(row, image(row).updated(column, Some(value)))
  }

  def transposeStringVector(vector: Vector[String]): Vector[String] = {
    val charVector: Vector[Vector[Char]] = vector.map(_.toVector)
    charVector.transpose.map(_.mkString)
  }

  def applyTileOrientation(
      tile: Tile,
      tileFlip: TileFlip,
      tileRotation: TileRotation
  ): Tile = {
    val rotatedLines: Vector[String] = tileRotation match {
      case TileRotation0   => tile.lines
      case TileRotation90  => transposeStringVector(tile.lines.reverse)
      case TileRotation180 => tile.lines.map(_.reverse).reverse
      case TileRotation270 => transposeStringVector(tile.lines).reverse
    }
    val flippedLines: Vector[String] = tileFlip match {
      case Flipped    => rotatedLines.reverse
      case NotFlipped => rotatedLines
    }
    Tile(id = tile.id, lines = flippedLines)
  }

  def isValidTilePlacement(
      image: UnsolvedImage,
      row: Int,
      column: Int
  ): Boolean = {
    val tile = image(row)(column).get
    lazy val matchesPreviousRow = {
      if (row > 0) {
        val upperTile = image(row - 1)(column).get
        getTileEdge(upperTile, BottomEdge) == getTileEdge(tile, TopEdge).reverse
      } else {
        true
      }
    }
    lazy val matchesPreviousColumn = {
      if (column > 0) {
        val previousTile = image(row)(column - 1).get
        getTileEdge(previousTile, RightEdge) == getTileEdge(
          tile,
          LeftEdge
        ).reverse
      } else {
        true
      }
    }

    // Since we're placing the tiles from the top-left proceeding in reading
    // order, we only need to check the adjacent row and column to the up and
    // left.
    matchesPreviousRow && matchesPreviousColumn
  }

  def trimTileLines(tile: Tile): Vector[String] = {
    tile.lines.init.tail.map(line => line.slice(1, line.length - 1))
  }

  def renderImage(image: SolvedImage): Vector[String] = {
    image.flatMap(row =>
      row.foldLeft(Vector.empty[String]) { (acc, tile) =>
        val tileLines = trimTileLines(tile)
        if (acc == Vector.empty) {
          tileLines
        } else {
          acc.zip(tileLines).map { case (lhs, rhs) => lhs + rhs }
        }
      }
    )
  }

  def countPatternInstances(
      lines: Vector[String],
      pattern: Vector[String]
  ): Int = {
    val patternLength = pattern.head.length
    val patternRegexes = pattern.map(patternLine =>
      new Regex("(?=" + patternLine.replace(' ', '.') + ")")
    )
    lines
      .sliding(pattern.length, 1)
      .map { window =>
        patternRegexes.head.unanchored
          .findAllMatchIn(window.head)
          .map { m =>
            val column = m.start
            if (
              patternRegexes.tail.zip(window.tail).forall {
                case (regex, line) =>
                  // Can't `match` against the `Regex` directly when it uses a
                  // positive lookahead for some reason.
                  !regex
                    .findFirstMatchIn(
                      line.slice(column, column + patternLength)
                    )
                    .isEmpty
              }
            ) {
              1
            } else {
              0
            }
          }
          .sum
      }
      .sum
  }

  def runTests(): Unit = {
    val exampleTile1 = Tile(
      id = 123,
      lines = Vector(
        "##.",
        "..#",
        "..#"
      )
    )
    assert(getTileEdge(exampleTile1, TopEdge) == "##.")
    assert(getTileEdge(exampleTile1, RightEdge) == ".##")
    assert(getTileEdge(exampleTile1, BottomEdge) == "#..")
    assert(getTileEdge(exampleTile1, LeftEdge) == "..#")

    val exampleTile2 = Tile(
      id = 456,
      lines = Vector(
        "##.",
        "...",
        "..."
      )
    )
    val tiles = Set(exampleTile1, exampleTile2)
    assert(
      buildGraph(tiles) == Set(
        Edge(123, BottomEdge, false, LeftEdge, 456),
        Edge(123, LeftEdge, true, LeftEdge, 456),
        Edge(123, RightEdge, false, TopEdge, 456),
        Edge(123, TopEdge, true, TopEdge, 456),
        Edge(456, LeftEdge, false, BottomEdge, 123),
        Edge(456, LeftEdge, true, LeftEdge, 123),
        Edge(456, TopEdge, false, RightEdge, 123),
        Edge(456, TopEdge, true, TopEdge, 123)
      )
    )

    val unsolvedImage = Vector(Vector(None, None), Vector(None, None))
    assert(
      updateImageIndex(
        unsolvedImage,
        0,
        1,
        exampleTile1
      ) == Vector(
        Vector(
          None,
          Some(exampleTile1)
        ),
        Vector(None, None)
      )
    )

    assert(
      applyTileOrientation(
        exampleTile1,
        NotFlipped,
        TileRotation90
      ) == Tile(
        id = exampleTile1.id,
        lines = Vector(
          "..#",
          "..#",
          "##."
        )
      )
    )
    assert(
      applyTileOrientation(
        exampleTile1,
        Flipped,
        TileRotation90
      ) == Tile(
        id = exampleTile1.id,
        lines = Vector(
          "##.",
          "..#",
          "..#"
        )
      )
    )
    assert(
      applyTileOrientation(
        exampleTile1,
        NotFlipped,
        TileRotation180
      ) == Tile(
        id = exampleTile1.id,
        lines = Vector(
          "#..",
          "#..",
          ".##"
        )
      )
    )
    assert(
      applyTileOrientation(
        exampleTile1,
        NotFlipped,
        TileRotation270
      ) == Tile(
        id = exampleTile1.id,
        lines = Vector(
          ".##",
          "#..",
          "#.."
        )
      )
    )

    assert(
      !isValidTilePlacement(
        Vector(
          Vector(
            Some(exampleTile1),
            Some(exampleTile1)
          )
        ),
        row = 0,
        column = 1
      )
    )

    assert(
      isValidTilePlacement(
        Vector(
          Vector(
            Some(exampleTile1),
            Some(
              applyTileOrientation(exampleTile2, NotFlipped, TileRotation270)
            )
          )
        ),
        row = 0,
        column = 1
      )
    )

    assert(trimTileLines(exampleTile1) == Vector("."))
    assert(
      countPatternInstances(
        Vector(
          ".#...#",
          "#.#.#.",
          ".#...."
        ),
        Vector(".#", "#.")
      ) == 3
    )
    assert(
      countPatternInstances(
        Vector(
          ".####...#####..#...###..",
          "#####..#..#.#.####..#.#.",
          ".#.#...#.###...#.##.O#..".replace('O', '#'),
          "#.O.##.OO#.#.OO.##.OOO##".replace('O', '#'),
          "..#O.#O#.O##O..O.#O##.##".replace('O', '#')
        ),
        seaMonsterPattern
      ) == 1
    )
  }
}
