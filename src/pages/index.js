import React from 'react';
import Link from 'gatsby-link';
import me from './me.jpg';
import Layout from "../components/layout";
import { graphql } from 'gatsby';


const IndexPage = ({ data }) => {
  const articles = data.allMarkdownRemark.edges;
  return(
    <Layout>
        <h1>Me in 10 seconds</h1>
        <p>
            I'm a thinker, software engineer and manager, reader, arm chair scientist, and amateur philosopher. I believe in focusing on the long term over the short, and that done is better than perfect. I grew up and live in the Denver area but have a soft spot for San Francisco and Portland.
        </p>
        
        <h1>Newest Articles</h1>
        <ul>
          {articles.map(({ node }) => (
            <li>
              <Link to={node.frontmatter.path}>{node.frontmatter.title}</Link>
            </li>
          ))}
         
        </ul>
        <ul style={{ listStyleType: 'none' }}>
            <li><Link to='/blog'>All Articles</Link> - <Link to='/rss.xml'>RSS</Link></li>
        </ul>
        
        <h1>Books </h1>
        <p>See what I've been <Link to='/books'>reading</Link></p>

        <h1>Music</h1>
        <p>See what I've been <Link to='/music'>listening to</Link></p>

        <div className="h-card">
            <h1>Around the web</h1>
            <ul>
                <li><a className="u-url" href="https://www.facebook.com/thavelick" rel="me">Facebook</a></li>
                <li><a className="u-url" href="https://twitter.com/thavelick/" rel="me">Twitter</a></li>
                <li><a className="u-url" href="https://github.com/thavelick/" rel="me">GitHub</a></li>
                <li><a className="u-url" href="https://stackoverflow.com/users/30529/tristan-havelick" rel="me">Stack Overflow</a></li>
            </ul>
        </div>

        <h1>Contact</h1>
        <p>
          Please feel free to introduce yourself. I may respond slowly or not at all. Note, I'm not currently looking for any job opportunities.
        </p>
        <ul>
          <li>Phone/Signal: <a href="sms:3034757244" className="u-tel"> 303-475-7244</a></li>
          <li>Email: <a href="mailto:tristan@havelick.com" className="u-email">tristan@havelick.com</a></li>
        </ul>

        <img className="mePhoto u-photo" src={me} alt="Tristan Havelick"/>
    </Layout>
  )
};

export default IndexPage;

export const query = graphql`
query {
  allMarkdownRemark(
    sort: { order: DESC, fields: [frontmatter___date] }
    limit: 5
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