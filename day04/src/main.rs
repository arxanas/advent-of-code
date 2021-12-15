use std::collections::HashSet;
use std::io::Read;

#[cfg(test)]
static TEST_INPUT: &'static str = "\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7";

type Board = Vec<Vec<usize>>;

fn parse_bingo_board(board: &str) -> Board {
    board
        .trim()
        .lines()
        .map(|line| {
            line.split_ascii_whitespace()
                .map(|num| num.parse::<usize>().unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>()
}

#[test]
fn test_parse_bingo_board() {
    let board = "
1 2 3
4  5  6
7 8 9";
    assert_eq!(
        parse_bingo_board(board),
        vec![vec![1, 2, 3], vec![4, 5, 6], vec![7, 8, 9]]
    );
}

fn parse_input(input: &str) -> (Vec<usize>, Vec<Board>) {
    let parts: Vec<_> = input.split("\n\n").collect();
    let nums: Vec<usize> = parts[0]
        .split(",")
        .map(|num| num.parse().unwrap())
        .collect();
    let boards: Vec<Board> = parts[1..]
        .iter()
        .map(|board| parse_bingo_board(board))
        .collect();
    (nums, boards)
}

#[test]
fn test_parse_input() {
    let (nums, boards) = parse_input(TEST_INPUT);
    assert_eq!(
        nums,
        vec![
            7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19,
            3, 26, 1
        ]
    );
    assert_eq!(boards.len(), 3);
}

fn iter_columns<'a>(board: &'a Board, column_index: usize) -> impl Iterator<Item = usize> + 'a {
    board.iter().map(move |row| row[column_index])
}

fn has_board_won(board: &Board, marked_nums: &HashSet<usize>) -> bool {
    assert_eq!(board.len(), board[0].len());
    let dim = board.len();

    for row in board {
        if row.iter().all(|num| marked_nums.contains(num)) {
            return true;
        }
    }

    for column_index in 0..dim {
        let mut column = iter_columns(board, column_index);
        if column.all(|num| marked_nums.contains(&num)) {
            return true;
        }
    }

    return false;
}

#[test]
fn test_has_board_won() {
    let board = vec![vec![1, 2, 3], vec![4, 5, 6], vec![7, 8, 9]];
    assert!(has_board_won(
        &board,
        &vec![1, 4, 5, 6].into_iter().collect()
    ));
    assert!(has_board_won(
        &board,
        &vec![1, 4, 6, 7].into_iter().collect()
    ));
    assert!(!has_board_won(
        &board,
        &vec![1, 4, 6, 8].into_iter().collect()
    ));
}

fn find_winning_board<'a>(
    nums: &[usize],
    boards: &'a [Board],
) -> (&'a Board, usize, HashSet<usize>) {
    let mut marked_nums = HashSet::new();
    for num in nums {
        marked_nums.insert(*num);
        for board in boards {
            if has_board_won(board, &marked_nums) {
                return (board, *num, marked_nums);
            }
        }
    }
    panic!("No winning board found");
}

fn part1(nums: &[usize], boards: &[Board]) -> usize {
    let (winning_board, called_num, marked_nums) = find_winning_board(nums, boards);
    let unmarked_nums_sum: usize = winning_board
        .iter()
        .flatten()
        .copied()
        .filter(|num| !marked_nums.contains(num))
        .sum();
    unmarked_nums_sum * called_num
}

#[test]
fn test_part1() {
    let (nums, boards) = parse_input(TEST_INPUT);
    assert_eq!(part1(&nums, &boards), 4512);
}

fn part2(nums: &[usize], boards: &[Board]) -> usize {
    let mut marked_nums = HashSet::new();
    let mut won_boards = Vec::new();
    let mut won_board_indexes = HashSet::new();
    for num in nums {
        marked_nums.insert(*num);
        for (i, board) in boards.iter().enumerate() {
            if won_board_indexes.contains(&i) {
                continue;
            }
            if has_board_won(board, &marked_nums) {
                won_boards.push((board, *num, marked_nums.clone()));
                won_board_indexes.insert(i);
            }
        }

        if won_boards.len() == boards.len() {
            break;
        }
    }

    let (last_winning_board, called_num, marked_nums) = won_boards.last().unwrap();
    let unmarked_nums_sum: usize = last_winning_board
        .iter()
        .flatten()
        .copied()
        .filter(|num| !marked_nums.contains(num))
        .sum();
    unmarked_nums_sum * called_num
}

#[test]
fn test_part2() {
    let (nums, boards) = parse_input(TEST_INPUT);
    assert_eq!(part2(&nums, &boards), 1924);
}

fn main() {
    let input = {
        let mut buf = String::new();
        std::io::stdin().lock().read_to_string(&mut buf).unwrap();
        buf
    };
    let (nums, boards) = parse_input(&input);
    println!("part 1: {}", part1(&nums, &boards));
    println!("part 2: {}", part2(&nums, &boards));
}
