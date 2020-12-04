import scala.util.Try;
import scala.util.matching.Regex;
import scala.annotation.meta.field

object Main {
  def main(args: Array[String]): Unit = {
    runTests()

    val result = io.Source.stdin
      .getLines()
      .foldLeft(List[List[String]]()) { (acc, line) =>
        acc match {
          case Nil => List(List(line))
          case head :: tail => {
            line match {
              case ""   => List() :: (head :: tail)
              case line => (line :: head) :: tail
            }
          }
        }
      }
      .map(_.mkString(" "))
      .count(isValidRecord)
    println(s"Num valid passports: $result")
  }

  def isValidRecord(line: String): Boolean = {
    val requiredFields = Set("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
    val actualFields = line
      .split(" ")
      .map(field => {
        val Array(fieldName, fieldValue) = field.split(":", 2)
        (fieldName, fieldValue)
      })
      .filter { case (fieldName, fieldValue) =>
        isValidField(fieldName, fieldValue)
      }
      .toMap

    requiredFields.subsetOf(actualFields.keySet)
  }

  def tryToInt(s: String): Option[Int] = {
    Try(s.toInt).toOption
  }

  def isValidField(fieldName: String, fieldValue: String): Boolean = {
    fieldName match {
      case "byr" =>
        tryToInt(fieldValue)
          .filter(year => (1920 <= year && year <= 2002))
          .nonEmpty
      case "iyr" =>
        tryToInt(fieldValue)
          .filter(year => (2010 <= year && year <= 2020))
          .nonEmpty
      case "eyr" =>
        tryToInt(fieldValue)
          .filter(year => (2020 <= year && year <= 2030))
          .nonEmpty
      case "hgt" => {
        val Pattern = "([0-9]+)(cm|in)".r
        fieldValue match {
          case Pattern(value, "cm") => (
            150 <= value.toInt && value.toInt <= 193
          )
          case Pattern(value, "in") => (59 <= value.toInt && value.toInt <= 76)
          case _                    => false
        }
      }
      case "hcl" => {
        val Pattern = "#([0-9a-f]{6})".r
        fieldValue match {
          case Pattern(_) => true
          case _          => false
        }
      }
      case "ecl" => {
        fieldValue match {
          case "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => true
          case _                                                     => false
        }
      }
      case "pid" => {
        val Pattern = "([0-9]{9})".r
        fieldValue match {
          case Pattern(_) => true
          case _          => false
        }
      }
      case "cid" => true
      case other => sys.error(s"Unknown field: $other")
    }
  }

  def runTests(): Unit = {
    assert(isValidField("byr", "2002"))
    assert(!isValidField("byr", "2003"))

    assert(isValidField("iyr", "2010"))
    assert(isValidField("iyr", "2019"))
    assert(!isValidField("iyr", "2009"))
    assert(!isValidField("iyr", "2021"))

    assert(isValidField("eyr", "2020"))
    assert(isValidField("eyr", "2030"))
    assert(!isValidField("eyr", "2019"))
    assert(!isValidField("eyr", "2031"))

    assert(isValidField("hgt", "60in"))
    assert(isValidField("hgt", "190cm"))
    assert(!isValidField("hgt", "190in"))
    assert(!isValidField("hgt", "190"))

    assert(isValidField("hcl", "#123abc"))
    assert(!isValidField("hcl", "#123abz"))
    assert(!isValidField("hcl", "123abc"))

    assert(isValidField("ecl", "brn"))
    assert(!isValidField("ecl", "wat"))

    assert(isValidField("pid", "000000001"))
    assert(!isValidField("pid", "0123456789"))
  }
}
