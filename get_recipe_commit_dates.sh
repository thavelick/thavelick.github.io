#!/usr/bin/env bash
files=(
    "recipes/cajun-sausage-and-beans/index.html"
    "recipes/chicken-tinga/index.html"
    "recipes/pizza-dough/index.html"
    "recipes/the-rice/index.html"
)
for file in "${files[@]}"; do
  echo "$file:"
  git log --reverse --format="%ad" --date=short "$file" | head -n 1
  echo ""
done
