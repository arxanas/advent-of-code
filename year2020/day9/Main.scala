import scala.math.BigInt

object Main {
  def main(args: Array[String]): Unit = {
    val preambleLength = args(1).toInt

    val nums = io.Source.stdin
      .getLines()
      .map(BigInt(_))
      .toList
    val invalidNum = findInvalid(nums, preambleLength)
    println(s"Invalid number: $invalidNum")

    val sequence = findSequenceAddingUpTo(nums, targetNum = invalidNum)
    val minNum = sequence.min
    val maxNum = sequence.max
    val sum = minNum + maxNum
    println(s"Min num: $minNum, max num: $maxNum, sum: $sum")
  }

  def findInvalid(nums: List[BigInt], windowSize: Int): BigInt = {
    nums
      .sliding(windowSize + 1, 1)
      .flatMap { nums =>
        val leadingNums = nums.take(windowSize)
        val targetNum = nums.last

        val pairs =
          for (first <- leadingNums; second <- leadingNums)
            yield (first, second)

        if (
          pairs.exists {
            case (first, second)
                if first != second && first + second == targetNum =>
              true
            case _ => false
          }
        ) {
          List.empty
        } else {
          List(targetNum)
        }
      }
      .next()
  }

  def findSequenceAddingUpTo(nums: List[BigInt], targetNum: BigInt): List[BigInt] = {
    (2 until nums.length)
      .view // Force `flatMap` to be lazy.
      .flatMap(windowSize => nums.sliding(windowSize, 1))
      .find(window => window.sum == targetNum)
      .get
  }
}
