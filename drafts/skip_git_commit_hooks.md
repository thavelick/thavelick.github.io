--- 
slug: /til/skip_git_commit_hooks
categories: til, blog
title: Skip git Commit Hooks
publish_date: 2025-03-14
---
# Skip git Commit Hooks
On my work laptop, I've got git hooks set up so git will complain if I forget 
certain things that make my commits more professional, like:

* Making sure I've got ticket numbers in branch names and commit messages
* Making sure I'm conforming to our commitlint rules
* Make sure I'm not committing to the directly to the main, production branch

But sometimes I'm committing to a personal repo like this one or my 
[dotfiles repo](https://github.com/thavelick/dotfiles) and I don't care about
this stuff. After messing with a series of silly ways prevent the hooks from
running I learned that you can just use a simple flag, either `--no-verify` or
`-n` to skip the hooks:
    
```bash
git commit -n -m "my unprofessional commit message"
```

## Resources
* https://stackoverflow.com/questions/7230820/skip-git-commit-hooks
