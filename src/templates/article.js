import React from "react";
import { graphql } from "gatsby";
import Layout from "../components/layout";
import Link from "gatsby-link";

export default function Template({ data }) {
  const { markdownRemark: post } = data
  const title = post.frontmatter.title;
  return (
    <Layout title={title}>
        <Link to="/blog">Articles</Link>
        <article>
          <h1>{title}</h1>
          <small>Posted {post.frontmatter.date} - {post.timeToRead} minute read</small>
          <div
            className="article-content"
            dangerouslySetInnerHTML={{ __html: post.html }}
          />
        </article>
    </Layout>
  );
};

export const pageQuery = graphql`
  query BlogPostByPath($path: String!) {
    markdownRemark(frontmatter: { path: { eq: $path } }) {
        html
        frontmatter {
          date(fromNow: true)
          title
        }
        timeToRead
    }
  }
`;