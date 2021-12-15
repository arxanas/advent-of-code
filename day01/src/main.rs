use std::io::Read;

use itertools::Itertools;

#[cfg(test)]
static TEST_INPUT: &'static str = "
199
200
208
210
200
207
240
269
260
263
";

fn parse_input(input: &str) -> Vec<usize> {
    input
        .trim()
        .lines()
        .map(|element| element.parse::<usize>().unwrap())
        .collect_vec()
}

#[test]
fn test_parse_input() {
    assert_eq!(parse_input(&TEST_INPUT).len(), 10);
}

fn part1(measurements: &[usize]) -> usize {
    measurements
        .iter()
        .tuple_windows()
        .filter(|(first, second)| second > first)
        .count()
}

#[test]
fn test_part1() {
    let input = parse_input(TEST_INPUT);
    assert_eq!(part1(&input), 7);
}

fn part2(measurements: &[usize]) -> usize {
    measurements
        .iter()
        .tuple_windows()
        .map(|(first, second, third)| first + second + third)
        .tuple_windows()
        .filter(|(first, second)| second > first)
        .count()
}

#[test]
fn test_part2() {
    let input = parse_input(TEST_INPUT);
    assert_eq!(part2(&input), 5);
}

fn main() {
    let input = {
        let mut input = String::new();
        std::io::stdin().lock().read_to_string(&mut input).unwrap();
        input
    };
    let input = parse_input(&input);
    println!("part 1: {}", part1(&input));
    println!("part 2: {}", part2(&input));
}
