const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;
const cors = require('cors')

app.use(cors())
app.use(bodyParser.json());
app.use(express.static('public')); 

app.post('/chat', async (req, res) => {
    const userMessage = req.body.message;

    if (!userMessage) {
        return res.status(400).json({ error: "Message is required" });
    }

    try {
        const aiResponse = `AI: You said "${userMessage}"`;

        res.json({ response: aiResponse });
    } catch (error) {
        console.error("Error processing request:", error.message);
        res.status(500).json({ error: "Failed to process request" });
    }
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});


const corsOptions = {
    origin: '"http://localhost:3000"',
    methods : ['GET', 'POST'],
    Credentials: true,
    };    

app.use(cors(corsOptions));