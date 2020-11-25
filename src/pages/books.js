import React from "react";
import Layout from "../components/layout"
import { graphql } from "gatsby";
export default ({ data }) => {
  const books = data.allGoodreadsBook.edges;

  return (
    <Layout>
      <div>
        <h1>What I've Been Reading</h1>
        <ul>
          {books.map(({ node }) => (

            <li>
              {node.book.title} by {node.book.authors[0].name} [{node.review.rating}/5 stars]
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  );
};

export const query = graphql`
query RecentBooks {
    allGoodreadsBook(sort: {fields: review___dateUpdated, order: DESC}, filter: {shelfNames: {eq: "read"}, review: {rating: {ne: null}}}, limit: 6) {
      edges {
        node {
          book {
            title
            authors {
              name
            }
          }
          review {
            dateUpdated
            rating
          }
          shelfNames
        }
      }
    }
  }
  
`;
