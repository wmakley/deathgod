# Death God

PyGame Roguelike engine with genetic AI algorithm tester.
(Student project.)

## Background

This was originally a side project in college because I wanted to
learn Python and I was obsessed with the anime *Bleach*,
and desperately wanted a Roguelike about it to exist. Later, I
needed to complete an assignment for an AI elective class and
spawned a bunch of frogs and gave them genetically generated decision
trees. (Loosely, as I never developed a way to visualize the trees.
The frogs do *seem* to get better at killing the player as the game
goes on, however.)

Because this was a college project I worked on over ten years ago, I
have not made any changes to substandard style or engineering choices.
I leave judgment in the hands of the reader. :) I provide it here for
three reasons:

1. Fun.
2. To demonstrate that I know Python.
3. I enjoy hacking on it occasionally to keep it working on modern OSes.

## Dependencies

* Python 3 ([3.6 on Mac OS](https://stackoverflow.com/questions/52718921/problems-getting-pygame-to-show-anything-but-a-blank-screen-on-macos-mojave))
* [Pygame 1.9.4](https://www.pygame.org/wiki/GettingStarted)

## Running it

Option 1, manual:

`python3 main.py`

Option 2, Virtualenv:

```sh
./bin/create-virtualenv.sh
./bin/deathgod
```

## Known Issues

* Currently broken in Mac OS Mojave (shows a blank screen). [Python 3.6 downgrade may fix it](https://stackoverflow.com/questions/52718921/problems-getting-pygame-to-show-anything-but-a-blank-screen-on-macos-mojave), but having trouble getting Homebrew to install it.
