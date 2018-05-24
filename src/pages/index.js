import React from 'react';
import Link from 'gatsby-link';
import me from './me.jpg';

const IndexPage = () => (
  <div className="h-card">
    <h1>Me in 10 seconds</h1>
    <p className="u-note">
      I'm a thinker, software engineer and manager, reader, arm chair scientist, and amateur philosopher. I believe in focusing on the long term over the short, and that done is better than perfect. I grew up and live in the Denver area but have a soft spot for San Francisco and Portland.
    </p>
    <h1>Around the web</h1>
    <ul>
      <li><a className="u-url" href="https://www.facebook.com/thavelick" rel="me">Facebook</a></li>
      <li><a className="u-url" href="https://twitter.com/thavelick/" rel="me">Twitter</a></li>
      <li><a className="u-url" href="https://github.com/thavelick/" rel="me">GitHub</a></li>
      <li><a className="u-url" href="https://stackoverflow.com/users/30529/tristan-havelick" rel="me">Stack Overflow</a></li>
    </ul>

    <h1>Contact</h1>
    <p>
      Please feel free to introduce yourself. I may respond slowly or not at all. Note, I'm not currently looking for any job opportunities.
    </p>
    <ul>
      <li>Phone/Signal: <a href="sms:3034757244" className="u-tel"> 303-475-7244</a></li>
      <li>Email: <a href="mailto:tristan@havelick.com" className="u-email">tristan@havelick.com</a></li>
    </ul>

    <h1>Photo</h1>
    <img className="mePhoto u-photo" src={me} alt="photo of Tristan Havelick"/>

    <h1>Music</h1>
    <p>See what I've been <Link to='/music'>listening to</Link></p>

  </div>
);

export default IndexPage;
