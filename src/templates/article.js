import React from "react";
import { graphql } from "gatsby";
import Layout from "../components/layout";
export default function Template({ data }) {
  const { markdownRemark: post } = data
  return (
    <Layout>
        <article></article>
        <h1>{post.frontmatter.title}</h1>
        <small>Posted {post.frontmatter.date}</small>
        <div
          className="article-content"
          dangerouslySetInnerHTML={{ __html: post.html }}
        />
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
    }
  }
`;