const axios = require('axios');
const crypto = require('crypto');

exports.sourceNodes = async ({ boundActionCreators }) => {
  const { createNode } = boundActionCreators;
  const recentTracks = () => axios.get('https://libre.fm/2.0/?method=user.getrecenttracks&user=thavelick&page=1&limit=10&format=json');
  const res = await recentTracks();

  res.data.recenttracks.track.map((track, i) => {
    const trackNode = {
      id: `${i}`,
      parent: '__SOURCE__',
      internal: {
        type: 'recentTrack'
      },
      children: [],
      artist: track.artist['#text'],
      album: track.album['#text'],
      name: track.name,
      timestamp: track.date.uts
    };
    const contentDigest = crypto
          .createHash('md5')
          .update(JSON.stringify(trackNode))
          .digest('hex');

    trackNode.internal.contentDigest = contentDigest;
    createNode(trackNode);
  });
};
