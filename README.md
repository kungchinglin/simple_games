# Simple Games

This project is for me to learn how to make games with Python. I have always been amazed how lines of codes can become a highly interactive game instead of just some scripts, so I want to use this project to actually achieve that by myself.

I used the package called **pyame** to make the games, so make sure to install this package before executing the files. In total, I made three games, and they are [tic-tac-toe](tic_tac_toe.py), [snake](Snake.py), and [Monster Dungeon](platform.py). 

## Game Descriptions

### [Tic-Tac-Toe](tic_tac_toe.py)

This is my first attempt in making a game, and as the name suggests, it lets you play tic-tac-toe with your friend. Whoever gets three of their symbol lined up wins the game. The AI part was not written, so you have to play with other people.

### [Snake](Snake.py)

The second game is Snake, where you are a snake trying to eat as many treats as possible, growing in size along the way. The player can use WASD as the keys to move the snake. The treats are randomly generated, and a new one will appear once the existing one was eaten. Every time the snake gets a treat, the length of it will increase by one, making the game harder as one progresses. The speed also picks up according to the length, so the player's reflex gets challenged as time goes on.

### [Monster Dungeon](platform.py)

This game is my latest work, which is a 2D platforming game. In addition to WASD, the player can also press the spacebar to fire shots towards the monsters. The goal is to move from the lower left corner to the upper right one in order to proceed. At the third and the last level, a boss monster will appear, and the player wins the game if the boss is defeated.

I spent quite some time working on the physical engine, making sure the player and monsters won't fall through the walls. I also added in the animation when either the player or the monster dies. Moreover, although it is a bit subtle, I added in the difference between pressing W and holding W to jump. While holding W, the player jumps higher so they can jump over certain obstacles easily, while the small jump helps the player clear some spike traps.

## Conclusion

It took me quite a number of sessions to write up these games, and it would mean the world of it if you enjoy playing them:)
