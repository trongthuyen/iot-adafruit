import dotenv from 'dotenv'
import express from "express";
import bodyParser from "body-parser";
import cors from 'cors';
import { Server } from 'socket.io';
import { createServer } from 'http';
import { client as mqtt, FEED_TEMP, FEED_LED, FEED_INTENSITY } from './src/config/mqtt.js';
import { connect } from './src/db/connect.js';
import { subscribeFeeds } from './src/services/mqtt.js';
// import { processRequest, sendRealtimeData } from "./services/listenEventSocket.io";
require('events').EventEmitter.defaultMaxListeners = 0;

dotenv.config();
const app = express();
const port = process.env.PORT || 6969;
const server = createServer(app);
const io = new Server(server, {cors: { origin: "*" }});

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

connect();

// mqtt
subscribeFeeds(mqtt);

// socket.io
// processRequest(io, mqtt);

// sendRealtimeData(io, mqtt);

server.listen(port, () => {
	console.log("Backend Nodejs is running on the port: " + port)
});
