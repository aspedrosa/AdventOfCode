use std::collections::{HashMap, HashSet};
use std::io;

#[inline]
fn is_symbol(c: char) -> bool {
    !c.is_digit(10) && c != '.'
}

/// Checks around given coordinates (l, c) for symbols
///
/// # Arguments
///
/// * `l`: line index to look around
/// * `c`: column index to look around
/// * `matrix`: matrix of the engine
///
/// returns: (is_near_symbol: bool, gear_candidates: HashSet<(usize, usize)>)
/// is_near_symbol is true if a symbol character is found around the provided coordinates.
/// gear_candidates is a set of coordinates which contain the symbol '*'
///
/// # Examples
///
/// ```
/// // lets assume a matrix with the following content
/// // 467..114..
/// // ...*......
/// // ..35..633.
/// // ......#...
/// // 617*......
/// // .....+.58.
/// // ..592.....
/// // ......755.
/// // ...$.*....
/// // .664.598..
///
/// let (is_near_symbol, gear_candidates) = check_nearby(0, 2, matrix);
/// assert!(is_near_symbol);
/// assert_eq!(gear_candidates.iter().collect::<Vec<_>>(), vec![(1, 3)]);
///
/// let (is_near_symbol, gear_candidates) = check_nearby(0, 5, matrix);
/// assert!(!is_near_symbol);
/// assert_eq!(gear_candidates.iter().collect::<Vec<_>>(), vec![]);
///
/// let (is_near_symbol, gear_candidates) = check_nearby(2, 6, matrix);
/// assert!(is_near_symbol);
/// assert_eq!(gear_candidates.iter().collect::<Vec<_>>(), vec![]);
/// ```
fn check_nearby(l: usize, c: usize, matrix: &Vec<Vec<char>>) -> (bool, HashSet<(usize, usize)>) {
    let mut near_symbol = false;
    let mut gears_candidates = HashSet::new();

    for li in -1i32..=1 {
        for ci in -1i32..=1 {
            let new_l = l as i32 + li;
            let new_c = c as i32 + ci;

            if new_l >= 0
                && new_l < matrix.len() as i32
                && new_c >= 0
                && new_c < matrix[new_l as usize].len() as i32 {
                    let new_l = new_l as usize;
                    let new_c = new_c as usize;

                    let character = matrix[new_l][new_c];

                    if is_symbol(character) {
                        near_symbol = true;

                        if character == '*' {
                            gears_candidates.insert((new_l, new_c));
                        }
                    }
            }
        }
    }

    return (near_symbol, gears_candidates);
}

fn main() {
    let input: Vec<_> = io::stdin().lines().map(|l| l.unwrap()).collect();

    // transform data into a matrix of chars
    let engine_matrix: Vec<_> = input.iter().map(|l| l.chars().collect::<Vec<_>>()).collect();

    let mut part1_sum = 0;
    let mut gears_candidates: HashMap<(usize, usize), Vec<u32>> = HashMap::new();

    let mut curr_number: Vec<char> = Vec::new();
    let mut near_symbol = false;
    let mut gear_candidates_with_curr_number: HashSet<(usize, usize)> = HashSet::new();
    for l in 0..engine_matrix.len() {
        for c in 0..engine_matrix[l].len() {

            if engine_matrix[l][c].is_digit(10) {
                curr_number.push(engine_matrix[l][c]);

                let (is_near_symbol, found_gear_candidates) = check_nearby(l, c, &engine_matrix);
                near_symbol |= is_near_symbol;
                gear_candidates_with_curr_number.extend(found_gear_candidates);

                // if the next character is outside bounds or is not a digit, then the current number ended
                if c + 1 == engine_matrix[l].len() || !engine_matrix[l][c + 1].is_digit(10) {
                    let result_number = curr_number.iter().collect::<String>().parse::<u32>().unwrap();

                    // for part1 we must only sum to the total sum if it was near a symbol
                    if near_symbol {
                        part1_sum += result_number;
                    }

                    // associate the current number to every gear candidate found
                    for candidate in &gear_candidates_with_curr_number {
                        gears_candidates.entry(*candidate).or_default().push(result_number);
                    }

                    // reset aux vars
                    curr_number.clear();
                    near_symbol = false;
                    gear_candidates_with_curr_number.clear();
                }
            }
        }
    }

    println!("part 1");
    println!("{}", part1_sum);

    // gears are the ones that have only two numbers nearby
    let gears: Vec<_> = gears_candidates
        .iter()
        .filter(|(_, engine_parts)| engine_parts.len() == 2).collect();

    //gears.iter().for_each(|(k, v)| println!("{:?} {:?}", k, v));
    // multiple numbers near each gear, sum them together
    let answer2 = gears
        .iter()
        .map(|(_, engine_parts)| engine_parts.iter().fold(1, |acc, item| acc * item))
        .sum::<u32>();

    println!();
    println!("part 2");
    println!("{}", answer2);
}