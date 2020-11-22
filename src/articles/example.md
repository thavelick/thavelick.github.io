---
path: /example
title: Just a quick example
date: "2016-05-22"
---

Neato mosquito!
# h1
## h2

### h3

#### h4
Some ideas: 
* bullet
* list
* here

Here are the important steps:

1. numbered
1. list
1. here

```
{
  allMarkdownRemark(sort: {fields: [frontmatter___date], order: DESC}) {
    edges {
      node {
        frontmatter {
          title
          date
        }
        html
      }
    }
  }
}

```
