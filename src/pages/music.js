import React from "react";
import Layout from "../components/layout"
import { graphql } from "gatsby";
export default ({ data }) => {
  const tracks = data.allRecentTrack.edges;

  return (
    <Layout>
      <div>
        <h1>What I've Been Listening To</h1>
        <ul className="showBullets">
          {tracks.map(({ node }) => (

            <li>
              {node.name} by {node.artist} from {node.album}
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  );
};

export const query = graphql`
  query RecentTracksQuery {
    allRecentTrack {
      edges {
        node {
          name
          album
          artist
          timestamp
        }
      }
    }
  }
`;
