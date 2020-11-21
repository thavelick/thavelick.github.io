const env = process.env.NODE_ENV || 'development';
require('dotenv').config({path: `./.env.${env}`});

module.exports = {
  siteMetadata: {
    title: 'Tristan Havelick'
  },
  plugins: [
    'gatsby-plugin-react-helmet',
    'gatsby-transformer-remark',
    {
      resolve: 'gatsby-source-filesystem',
      options: {
        name: 'src',
        path: `${__dirname}/src/articles/`
      }
    },
    {
      resolve: 'gatsby-source-spotify',
      options: {
        clientId: process.env.SPOTIFY_CLIENT_ID,
        clientSecret:process.env.SPOTIFY_CLIENT_SECRET,
        refreshToken: process.env.SPOTIFY_REFRESH_TOKEN,
    
        fetchPlaylists: false, 
        fetchRecent: true,
      },
    },
  ]
};
