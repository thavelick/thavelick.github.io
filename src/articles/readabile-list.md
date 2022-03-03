---
path: /readable-list
title: A Library for Making List Webpages "Readable"
date: "2022-03-02"
---
This started as a README for a potential open source project. I decided
to make a a blog post to maybe get some feedback or suggestions.

## Status

Just an idea at this point.

## Description

There are "readability" libraries such as:
* https://github.com/mozilla/readability
* https://github.com/buriy/python-readability

These take a webpage containing an article and strip out all the navigation
and ads. Most of these work great for pages that are articles and some, like Mozilla's
do a pretty good job of identifying when a page is NOT an article. However,
there isn't much these libraries can currently do with pages that are lists
of articles like:

* https://coloradosun.com/category/news/housing/
* https://drewdevault.com/
* https://www.npr.org/sections/culture/
* https://www.cnn.com/health

Here, I'm considering making a library that strips out extraneous side 
navigation/ads/other junk from web pages like these, and either returning a
list of article URLs or a very simple page with article links in a bulleted list.

By combining this with a standard readability algorithm/library, one could 
create a simple and/or text-only view of a website than what is typically
rendered by text browsers like w3m and lynx.

A browser built with this at core sit in a missing place in the continuum of 
browser complexity:

```
Offpunk < THIS THING < w3m/lynx/elinks < visurf/netsurf/surf < qutebrowser/chrome/firefox
```

## Possible Algorithm
1. Start with a given HTTP URL
1. retrieve that page
1. Parse the page and get a list of all the links on that page
1. Remove any links that are to domains other than the one from the original link
1. Retrieve a few, say 10,maybe random links from  the remaining of the list
1. Get a similar list of links for each of those pages
1. Get a list of the links that are common across all of the retrieved pages. 
  It is a reasonable assumption that these would we be navigational links.
1. Finally, we'd return to the list of links from the original page, and
  remove the links we've determined are navigational
1. At this point, we're left with links only to unique content pages!

### Flaws
* If a website makes heavy use of cross linking in articles, those articles may
  be unfairly excluded from the final list of articles
* For some sites, this would be redundant with RSS/Atom feeds a be of lower quality
* This probably wouldn't work (out of the box) for sites that rely on 
  client-side JavaScript to render content.

