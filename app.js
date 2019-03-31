'use strict';

const line = require('@line/bot-sdk');
const express = require('express');

const defaultAccessToken = 'h4A/0EsqXaNhrkUTvd5GrtIle2lu65p0j79t6nEpt70ZBKEUfYBCCzsK9dwv+WIx0TpEM8n9YTrOBcP3ifRfWp/AnqEnTCv/6o/yUAoQNXUsuh7qMSjsVbX5j4i3uP7mS7SanV4kCf9XAJu2zDXT4wdB04t89/1O/w1cDnyilFU=';
const defaultSecret = 'aa374d45e8f358df5be55b2c54525695';

// create LINE SDK config from env variables
const config = {
  channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN || defaultAccessToken,
  channelSecret: process.env.CHANNEL_SECRET || defaultSecret,
};

// create LINE SDK client
const client = new line.Client(config);

// create Express app
// about Express itself: https://expressjs.com/
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

// register a webhook handler with middleware
// about the middleware, please refer to doc
app.post('/webhook', line.middleware(config), (req, res) => {
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result) => res.json(result));
});

// event handler
function handleEvent(event) {
  if (event.type !== 'message' || event.message.type !== 'text') {
    // ignore non-text-message event
    return Promise.resolve(null);
  }

  // create a echoing text message
  const echo = { type: 'text', text: event.message.text };

  // use reply API
  return client.replyMessage(event.replyToken, echo);
}

// listen on port
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`listening on ${port}`);
});
