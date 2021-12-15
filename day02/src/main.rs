use std::io::Read;

#[cfg(test)]
static TEST_INPUT: &'static str = "
forward 5
down 5
forward 8
up 3
down 8
forward 2
";

#[derive(Debug, PartialEq, Eq)]
enum Instruction {
    Forward(isize),
    Down(isize),
    Up(isize),
}

fn parse_instruction(line: &str) -> Instruction {
    let line = line.trim();
    let (command, amount) = line.split_once(' ').expect("expected <command> <amount>");
    let amount: isize = amount.parse().unwrap();
    match command {
        "forward" => Instruction::Forward(amount),
        "down" => Instruction::Down(amount),
        "up" => Instruction::Up(amount),
        _ => {
            panic!("Unrecognized command: {}", amount);
        }
    }
}

#[test]
fn test_parse_instruction() {
    assert_eq!(parse_instruction("forward 3"), Instruction::Forward(3));
    assert_eq!(parse_instruction("\nforward 3\n"), Instruction::Forward(3));
}

fn parse_input(input: &str) -> Vec<Instruction> {
     input.trim().lines().map(parse_instruction).collect()
}

#[test]
fn test_parse_input() {
    assert_eq!(parse_input(TEST_INPUT).len(), 6);
}

fn part1(input: &[Instruction]) -> isize{
    let mut depth= 0;
    let mut position = 0;
    for instruction in input {
        match instruction {
            Instruction::Forward(amount) => position += amount,
            Instruction::Down(amount) => depth += amount,
            Instruction::Up(amount) => depth -= amount,
        }
    }
    depth * position
}

#[test]
fn test_part1() {
    assert_eq!(part1(&parse_input(TEST_INPUT)), 150);
}


fn part2(input: &[Instruction]) -> isize{
    let mut aim= 0;
    let mut depth = 0;
    let mut position = 0;
    for instruction in input {
        match instruction {
            Instruction::Forward(amount) => {
                position += amount;
                depth += aim * amount;
            }
            Instruction::Down(amount) => aim += amount,
            Instruction::Up(amount) => aim -= amount,
        }
    }
    depth * position
}

#[test]
fn test_part2() {
    assert_eq!(part2(&parse_input(TEST_INPUT)), 900);
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
