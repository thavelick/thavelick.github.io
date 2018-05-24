---
title: Just a quick example
date: "2016-05-22"
---

Neato mosquito!

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
