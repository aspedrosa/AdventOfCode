use std::collections::HashMap;
use std::io;

fn main() {
    let input: Vec<_> = io::stdin().lines().map(|l| l.unwrap()).collect();

    // lets first parse the data to be used on both exercises
    let parsed_data: Vec<_> = input.iter().map(|l| {
        let mut l_s = l.split(":");
        let game = l_s.next().unwrap().split(" ").last().unwrap().parse::<u32>().unwrap();

        let hands = l_s.next().unwrap().split(";");
        let hands: Vec<_> = hands.map(|h| {
            h.split(",").map(|dices| {
                let mut color_dices = dices.trim().split(" ");

                let amount = color_dices.next().unwrap().parse::<u32>().unwrap();
                let color = color_dices.last().unwrap();

                (color, amount)
            })
            .collect::<Vec<_>>()  // Vec<(color, amount)>
        })
        .collect();  // Vec<Vec<(color, amount)>>

        (game, hands)
    })
    .collect();

    // for the exercise 1 we have a limited set of dices per color
    let maxs = HashMap::from([
        ("red", 12),
        ("green", 13),
        ("blue", 14),
    ]);

    // lets filter the games where its possible to have the dices above than
    //  sum their IDs
    let answer1: u32 = parsed_data.iter().filter(|(_, hands)| {
        hands.iter().all(|dices| {
            dices.iter().all(|(color, amount)| amount <= &maxs[color])
        })
    }).map(|(g, _)| g).sum();

    println!("part 1");
    println!("{}", answer1);

    let answer2: Vec<_> = parsed_data.iter().map(|(game, hands)| {
        // for each game we get the max number of dices per color
        let mut game_maxs: HashMap<&str, u32> = HashMap::new();

        hands.iter().for_each(|dices| {
            dices.iter().for_each(|(color, amount)| {
                match game_maxs.get(color) {
                    Some(v) => {
                        if amount > v {
                            game_maxs.insert(color, *amount);
                        }
                    }
                    None => { game_maxs.insert(color, *amount); }
                };
            });
        });

        // using the keys in the maxs hashmap, we multiple the least amount for each amount
        //  using 0 for color that eventually dont appear (this last part maybe does not
        //  happen on the given input)
        let power = maxs
            .keys()
            .map(|color| game_maxs.get(color).unwrap_or(&0))
            .fold(1, |acc, amount| acc * amount);

        (game, power)
    }).collect();

    println!();
    println!("part 2");
    //answer2.iter().for_each(|(g, p)| println!("{} {}", g, p));
    println!("{}", answer2.iter().map(|(_, p)| p).sum::<u32>());
}