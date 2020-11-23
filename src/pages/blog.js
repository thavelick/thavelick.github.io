import React from 'react';
import Link from 'gatsby-link';
import Layout from "../components/layout";
import { graphql } from 'gatsby';

const ArticleListPage = ({ data }) => {
    const articles = data.allMarkdownRemark.edges;
    return(
        <Layout>
            <h1>Articles</h1>
            <ul>
            {articles.map(({ node }) => (
                <li>
                <Link to={node.frontmatter.path}>{node.frontmatter.title}</Link>
                </li>
            ))}
            </ul>
        </Layout>
    );
};

export default ArticleListPage;

export const query = graphql`
query {
  allMarkdownRemark(
    sort: { order: DESC, fields: [frontmatter___date] }
  ) {
    edges {
      node {
        frontmatter {
          title
          path
        }
      }
    }
  }
}
`;