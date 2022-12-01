import scala.collection.mutable
import scala.math.BigInt

object Main {
  def main(args: Array[String]): Unit = {
    val adapterJoltages = io.Source.stdin
      .getLines()
      .map(_.toInt)
      .toList
    val targetJoltage = adapterJoltages.max + 3

    val joltageChain = (0 :: targetJoltage :: adapterJoltages).sorted
    val joltageDifferences = joltageChain
      .sliding(2, 1)
      .collect { case List(lhs, rhs) =>
        rhs - lhs
      }
      .toList
      .groupBy(identity(_))
      .mapValues(_.size)
    val numJoltage1 = joltageDifferences(1)
    val numJoltage3 = joltageDifferences(3)
    val productJoltage13 = numJoltage1 * numJoltage3
    println(s"$numJoltage1 * $numJoltage3 = $productJoltage13")

    val cache = mutable.Map[(Int, Int), BigInt]()
    val numJoltageChains = countJoltageChains(
      sourceJoltage = 0,
      targetJoltage = targetJoltage,
      adapterJoltages = adapterJoltages.toSet,
      cache = cache
    )
    println(s"Num joltage chains: $numJoltageChains")
  }

  def countJoltageChains(
      sourceJoltage: Int,
      targetJoltage: Int,
      adapterJoltages: Set[Int],
      cache: mutable.Map[(Int, Int), BigInt]
  ): BigInt = {
    cache.getOrElseUpdate(
      (sourceJoltage, targetJoltage), {
        if (sourceJoltage == targetJoltage) {
          1
        } else if (sourceJoltage > targetJoltage) {
          0
        } else {
          (1 to 3)
            .map(_ + sourceJoltage)
            .filter(nextJoltage =>
              nextJoltage == targetJoltage || adapterJoltages.contains(
                nextJoltage
              )
            )
            .map(nextJoltage =>
              countJoltageChains(
                sourceJoltage = nextJoltage,
                targetJoltage = targetJoltage,
                adapterJoltages = adapterJoltages,
                cache = cache
              )
            )
            .sum
        }
      }
    )
  }
}
