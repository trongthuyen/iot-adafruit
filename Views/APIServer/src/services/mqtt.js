import { topics } from '../configs/mqtt.js';

export const subscribeFeeds = (client) => {
  client.on('connect', () => {
    topics.map(topic => {
      client.subscribe([topic], () => {
        console.log(`Subscribe to topic '${topic}'`)
      })
    })
  })
}