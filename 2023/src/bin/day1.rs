use std::io;
use regex::{Match, Regex};

#[inline]
fn convert_to_number(s: &str) -> char {
    match s {
        "one"   => '1',
        "two"   => '2',
        "three" => '3',
        "four"  => '4',
        "five"  => '5',
        "six"   => '6',
        "seven" => '7',
        "eight" => '8',
        _       => '9',
    }
}

/// Function to find the last match of a given regex in a string. This function was created
///  because rust's regex doesn't give us overlapping matches.
///
/// # Arguments
///
/// * `s`: string to search regex in
/// * `regex`: regex to found
///
/// returns:
/// - None: if regex in not found in the string
/// - Some((idx: u32, m: Match)): a match m was found for the regex in the string. idx is the start
///     of the match on the original string. This index in needed because the match can be of a
///     substring.
///
/// # Examples
///
/// ```
/// let result = find_last_match("oneight", Regex::new("one|eight"));
/// assert!(result.is_some())
/// assert_eq!(result.unwrap().0, 2);
/// ```
fn find_last_match<'a>(s: &'a str, regex: &'a Regex) -> Option<(i32, Match<'a>)> {
    let matches = regex.find_iter(s);
    match matches.last() {
        Some(m) => {
            // lets check if we start from the second char we found another last match (e.g oneight -> neight)
            match find_last_match(&s[m.start() + 1..], regex) {
                Some((inner_start, inner_m)) => Some((m.start() as i32 + 1 + inner_start, inner_m)),
                None => Some((m.start() as i32, m))
            }
        },
        None => None
    }
}

fn main() {
    let input: Vec<_> = io::stdin().lines().map(|l| l.unwrap()).collect();

    let answer1: Vec<_> = input.iter()
        .map(|l| {
            // leave only integers
            let mut it = l.chars().filter(|c| c.is_digit(10));

            // get the first an last characters
            let first = it.next().unwrap_or('0');
            match it.last() {
                Some(last) => (l, format!("{}{}", first, last).parse::<u32>().unwrap()),
                None => (l, format!("{}{}", first, first).parse::<u32>().unwrap())
            }
        })
        .collect();

    println!("part 1");
    //answer1.iter().for_each(|(l, d)| println!("{} {}", l, d));
    println!("answer {}", answer1.iter().map(|(_, d)| d).sum::<u32>());


    let numbers_regex = Regex::new(r"one|two|three|four|five|six|seven|eight|nine").unwrap();

    //let answer2: u32 = input.iter()
    let answer2: Vec<_> = input.iter()
        .map(|l| {
            // lets first check the digits. lets get the first and last
            let mut it = l
                .chars()
                .enumerate()
                .filter(|(_, c)| c.is_digit(10))
                .map(|(i, c)| (i as i32, c));

            // these are (i: index where it was found, d: the digit found)
            let first_digit = it.next();
            let last_digit = it.last().unwrap_or(
                match first_digit {
                    Some(first_dig) => first_dig,
                    None => (-1, '0')
                }
            );
            let first_digit = first_digit.unwrap_or((l.len() as i32 - 1, '0'));

            // now lets check for numbers with words
            let mut matches = numbers_regex.find_iter(&*l);
            let first_match = matches.next();

            // by default lets put the found digits as the first and last numbers for the final number
            let mut first = first_digit.1;
            let mut last = last_digit.1;

            if let Some(first_match) = first_match {
                if (first_match.start() as i32) < first_digit.0  {
                    first = convert_to_number(first_match.as_str())
                }

                // to check the last number with letters with need to check after the first character
                //  of the first match since rust's regex doesn't support overlapping searches.
                // we also need to return the start index because the match object returned can be
                //  of a substring, so the start index would be wrong.
                let rest = &l[first_match.start() + 1..];
                let mut last_match = find_last_match(rest, &numbers_regex);

                if last_match.is_none() {
                    // this is -1 because on the ifs below we are adding (first_match.start() + 1)
                    //  to the idx of the last_match (first element of this tuple)
                    last_match = Some((-1, first_match));
                }

                if let Some((start_idx, last_match)) = last_match {
                    if first_match.start() as i32 + 1 + start_idx > last_digit.0 {
                        last = convert_to_number(last_match.as_str())
                    }
                }
            }

            (l, format!("{}{}", first, last).parse::<u32>().unwrap())
        })
        .collect();

    println!();

    println!("part 2");
    //answer2.iter().for_each(|(l, d)| println!("{} {}", l, d));
    println!("answer: {}", answer2.iter().map(|(_, d)| d).sum::<u32>());
}