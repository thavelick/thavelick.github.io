import React from "react";
import Layout from "../components/layout"
import { graphql } from "gatsby";
export default ({ data }) => {
  const tracks = data.allSpotifyRecentTrack.edges;

  return (
    <Layout title="Music">
      <div>
        <h1>What I've Been Listening To</h1>
        <ul>
          {tracks.map(({ node }) => (

            <li>
              {node.track.name} by {node.track.artists[0].name} from {node.track.album.name}
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  );
};

export const query = graphql`
query RecentTracks {
  allSpotifyRecentTrack(limit: 15, sort: {order: DESC, fields: played_at}) {
    edges {
      node {
        track {
          name
          artists {
            name
          }
          album {
            name
          }
        }
      }
    }
  }
}

`;
