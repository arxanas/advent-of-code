use std::cmp::Ordering;
use std::collections::HashSet;
use std::io::{stdin, BufRead};

#[cfg(test)]
static TEST_INPUT: &'static str = "\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
";

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Bit {
    Zero,
    One,
}

type BitString = Vec<Bit>;

#[derive(Clone, Debug, Default, PartialEq, Eq)]
struct Counts {
    num_zeros: usize,
    num_ones: usize,
}

fn count_bits(bits: impl IntoIterator<Item = Bit>) -> Counts {
    let mut counts = Counts::default();
    for bit in bits {
        match bit {
            Bit::Zero => counts.num_zeros += 1,
            Bit::One => counts.num_ones += 1,
        }
    }
    counts
}

fn count_all_bits(numbers: &[BitString]) -> Vec<Counts> {
    let indices = 0..numbers[0].len();
    indices
        .map(|index| count_bits(numbers.iter().map(|number| number[index])))
        .collect()
}

#[test]
fn test_count_bits() {
    use Bit::*;
    assert_eq!(
        count_all_bits(&[vec![Zero, One, Zero], vec![One, One, Zero]]),
        vec![
            Counts {
                num_zeros: 1,
                num_ones: 1,
            },
            Counts {
                num_zeros: 0,
                num_ones: 2,
            },
            Counts {
                num_zeros: 2,
                num_ones: 0,
            },
        ]
    );
}

fn line_to_bitstring(line: &str) -> BitString {
    line.trim()
        .chars()
        .map(|char| match char {
            '0' => Bit::Zero,
            '1' => Bit::One,
            other => panic!("Unrecognized bit value: {:?}", other),
        })
        .collect()
}

#[test]
fn test_line_to_bitstring() {
    use Bit::*;
    assert_eq!(line_to_bitstring("\n0110\n"), vec![Zero, One, One, Zero]);
}

fn calc_gamma_rate(numbers: &[BitString]) -> BitString {
    count_all_bits(numbers)
        .iter()
        .map(|elem| match elem.num_zeros.cmp(&elem.num_ones) {
            Ordering::Equal => panic!("Equal number of zeros and ones"),
            Ordering::Less => Bit::One,
            Ordering::Greater => Bit::Zero,
        })
        .collect()
}

fn calc_epsilon_rate(gamma_rate: &BitString) -> BitString {
    gamma_rate
        .iter()
        .map(|elem| match elem {
            Bit::Zero => Bit::One,
            Bit::One => Bit::Zero,
        })
        .collect()
}

fn bitstring_to_usize(number: &BitString) -> usize {
    let string: String = number
        .iter()
        .map(|elem| match elem {
            Bit::Zero => '0',
            Bit::One => '1',
        })
        .collect();
    usize::from_str_radix(&string, 2).unwrap()
}

#[test]
fn test_bitstring_to_usize() {
    use Bit::*;
    assert_eq!(bitstring_to_usize(&vec![One, Zero, One, One, Zero]), 22);
}

fn calc_power_consumption(numbers: &[BitString]) -> usize {
    let gamma_rate = calc_gamma_rate(numbers);
    let epsilon_rate = calc_epsilon_rate(&gamma_rate);
    let gamma_rate = bitstring_to_usize(&gamma_rate);
    let epsilon_rate = bitstring_to_usize(&epsilon_rate);
    gamma_rate * epsilon_rate
}

#[test]
fn test_calc_rates() {
    use Bit::*;
    let input: Vec<_> = TEST_INPUT.lines().map(line_to_bitstring).collect();
    let gamma_rate = calc_gamma_rate(&input);
    assert_eq!(gamma_rate, vec![One, Zero, One, One, Zero]);
    let epsilon_rate = calc_epsilon_rate(&gamma_rate);
    assert_eq!(epsilon_rate, vec![Zero, One, Zero, Zero, One]);
    assert_eq!(calc_power_consumption(&input), 198);
}

fn keep_numbers_matching_criteria(numbers: &[BitString], f: impl Fn(&Counts) -> Bit) -> BitString {
    fn inner(
        numbers: &[BitString],
        f: impl Fn(&Counts) -> Bit,
        index: usize,
        mut remaining_keys: HashSet<usize>,
    ) -> BitString {
        let counts = count_bits(remaining_keys.iter().map(|k| numbers[*k][index]));
        let bit_to_keep = f(&counts);
        remaining_keys = remaining_keys
            .into_iter()
            .filter(|k| numbers[*k][index] == bit_to_keep)
            .collect();
        if remaining_keys.is_empty() {
            panic!("No more remaining keys")
        } else if remaining_keys.len() == 1 {
            let index = remaining_keys.into_iter().next().unwrap();
            numbers[index].clone()
        } else {
            inner(numbers, f, index + 1, remaining_keys)
        }
    }
    inner(numbers, f, 0, (0..numbers.len()).into_iter().collect())
}

fn calc_oxygen_rating(numbers: &[BitString]) -> BitString {
    keep_numbers_matching_criteria(numbers, |counts| {
        match counts.num_zeros.cmp(&counts.num_ones) {
            Ordering::Less | Ordering::Equal => Bit::One,
            Ordering::Greater => Bit::Zero,
        }
    })
}

fn calc_co2_rating(numbers: &[BitString]) -> BitString {
    keep_numbers_matching_criteria(numbers, |counts| {
        match counts.num_zeros.cmp(&counts.num_ones) {
            Ordering::Less | Ordering::Equal => Bit::Zero,
            Ordering::Greater => Bit::One,
        }
    })
}

fn calc_life_support_rating(numbers: &[BitString]) -> usize {
    let oxygen_rating = calc_oxygen_rating(numbers);
    let co2_rating = calc_co2_rating(numbers);
    bitstring_to_usize(&oxygen_rating) * bitstring_to_usize(&co2_rating)
}

#[test]
fn test_calc_ratings() {
    use Bit::*;
    let input: Vec<_> = TEST_INPUT.lines().map(line_to_bitstring).collect();
    assert_eq!(calc_oxygen_rating(&input), vec![One, Zero, One, One, One]);
    assert_eq!(
        calc_co2_rating(&input),
        vec![Zero, One, Zero, One, Zero]
    );
    assert_eq!(calc_life_support_rating(&input), 230);
}

fn main() {
    let input: Vec<_> = stdin()
        .lock()
        .lines()
        .map(|line| line_to_bitstring(&line.unwrap()))
        .collect();
    println!("part 1: {}", calc_power_consumption(&input));
    println!("part 2: {}", calc_life_support_rating(&input));
}
