---
slug: /til/ctrl-z-bg-and-fg
categories: til, blog
title: Using ctrl-z to toggle between a program and the terminal
publish_date: 2022-09-11
---
# Using ctrl-z to toggle between a program and the terminal

In almost any terminal program you can hit `ctrl-z` to pause it, then run `fg`
to bring it back. With some zsh configuration you can make `ctrl-z` bring back
the program too.

First, I tried doing with this [Blog post](https://schulz.dk/2022/01/26/using-ctrl-z-to-toggle-process-in-fg-bg/)
suggested:

```zsh
# .zshrc
# use ctrl-z to toggle in and out of bg
if [[ $- == *i* ]]; then
  stty susp undef
  bind '"\C-z":" fg\015"'
fi
```

But my system doesn't seem to support the `bind` command. Thus I ended up with:

```zsh
# .zshrc
foreground() {
    fg
}

zle -N foreground
# use ctrl-z to toggle in and out of bg
if [[ $- == *i* ]]; then
  stty susp undef
  bindkey "^Z" foreground
fi
```

Which worked, but it didn't work from nvim which is where I thought I'd find
it most useful.  It turns out this is because I'm using Doom vim which disables
`crtrl-z` in `lua/doom/extras/keybindings/core.lua`:

```lua
mappings.map("n", "<c-z>", "<Nop>", opts, "Editor", "disable_suspending", "Disable suspending")
```

Commenting out the offending line fixed me up nicely.

From: https://social.linux.pizza/web/@solene@bsd.network/108973783539676780
and https://unix.stackexchange.com/questions/475310/how-to-bind-a-keyboard-shortcut-in-zsh-to-a-program-requiring-stdin
