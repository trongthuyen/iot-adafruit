import dotenv from 'dotenv'
import mongoose from "mongoose"

dotenv.config()

// const URI = `mongodb+srv://${process.env.USERNAME_DB}:${process.env.PASSWORD_DB}@cluster0.zpuvb.mongodb.net/${process.env.DB_NAME}?retryWrites=true&w=majority`
const URI = `mongodb+srv://${process.env.DB_USERNAME}:${process.env.DB_PASSWORD}@cluster0.uke0u.mongodb.net/${process.env.DB_NAME}/?retryWrites=true&w=majority`


export const connect = async () => {
    try {
        await mongoose.connect(URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        })
        console.log('Connect successfully to mongoose db!')
    } catch (error) {
        console.log(error)
        process.exit(1)
    }
}
