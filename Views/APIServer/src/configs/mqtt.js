import mqtt from 'mqtt'
import dotenv from 'dotenv'

dotenv.config()

const host = 'io.adafruit.com'
const port = '1883'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`
const connectUrl = `mqtt://${host}:${port}`


export const FEED_TEMP = process.env.AIO_USERNAME + "/feeds/bbc-temp"
export const FEED_LED = process.env.AIO_USERNAME + "/feeds/bbc-led"
export const FEED_INTENSITY = process.env.AIO_USERNAME + "/feeds/bbc-intensity"

export const topics = [
  FEED_TEMP,
  FEED_LED,
  FEED_INTENSITY,
]


export const client = mqtt.connect(connectUrl, {
  clientId,
  protocol: 'mqtt',
  clean: true,
  connectTimeout: 4000,
  username: process.env.AIO_USERNAME,
  password: process.env.AIO_KEY,
  reconnectPeriod: 1000,
})
