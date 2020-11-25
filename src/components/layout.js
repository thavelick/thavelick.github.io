import React from 'react';
import PropTypes from 'prop-types';
import Helmet from 'react-helmet';
import { StaticQuery, graphql } from "gatsby";
import Header from '../components/header';
import './layout.css';

const Layout = ( props ) => (
  <StaticQuery
    query={graphql`
      query SiteTitleQuery {
        site {
          siteMetadata {
            title
          }
        }
      }
    `}
    render={data => {
      let fullTitle = data.site.siteMetadata.title;
      if (props.title) {
        fullTitle = `${fullTitle} : ${props.title}`;
      }

      return (
        <div>
          <Helmet
            title={fullTitle}
            meta={[
              { name: 'description', content: 'Sample' },
              { name: 'keywords', content: 'sample, something' },
            ]}
          />
          <Header siteTitle={data.site.siteMetadata.title} />
          <div
            style={{
              margin: '0 auto',
              maxWidth: 960,
              padding: '0px 1.0875rem 1.45rem',
              paddingTop: 0
            }}
          >
            {props.children}
          </div>
        </div>
      )
    }} />
  
);

Layout.propTypes = {
  children: PropTypes.func,
  title: PropTypes.string,
};

export default Layout;

