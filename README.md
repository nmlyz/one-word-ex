# one-word-ex

[![make.fun · u-puan-describe-your-ex-in-one-word-9fc6ebe7](https://make.fun/badge/u-puan-describe-your-ex-in-one-word-9fc6ebe7.svg)](https://make.fun/c/u-puan-describe-your-ex-in-one-word-9fc6ebe7?utm_source=github&utm_medium=readme&utm_campaign=u-puan-describe-your-ex-in-one-word-9fc6ebe7)
[![rank](https://make.fun/badge/u-puan-describe-your-ex-in-one-word-9fc6ebe7/nmlyz/one-word-ex/rank.svg)](https://make.fun/c/u-puan-describe-your-ex-in-one-word-9fc6ebe7/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-puan-describe-your-ex-in-one-word-9fc6ebe7)
[![reward](https://make.fun/badge/u-puan-describe-your-ex-in-one-word-9fc6ebe7/nmlyz/one-word-ex/reward.svg)](https://make.fun/c/u-puan-describe-your-ex-in-one-word-9fc6ebe7?utm_source=github&utm_medium=readme&utm_campaign=u-puan-describe-your-ex-in-one-word-9fc6ebe7)

A tiny program that writes one word describing an ex to a text file.
The word is `Subscription`: the ex who keeps charging you long after
you thought you cancelled, the cancel button hidden three menus deep,
the renewal you never agreed to.

## Run it

```sh
python3 main.py
```

It writes the word to `/output/entry.txt` (`MAKEFUN_OUTPUT_DIR`
overrides the directory). Running it twice produces byte-identical
output: exactly twelve bytes, `Subscription`, with no trailing newline.

Before writing, the program checks the word against the brief: one
to one hundred and eleven characters, exactly one word, letters only,
no leading or trailing white space. If any check fails it prints the
problem and exits without writing a file.
