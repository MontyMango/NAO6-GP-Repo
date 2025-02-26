// TO RUN THIS FILE DO: npm run start
// Import the API
import  {
    chatToModel,
    downloadModel,
    loadModel,
    unloadModel,
    deleteModel,
    getModelInformation,
    getRunningModels,
    getDownloadedModels
} from './Ollama/Ollama-API.js';

import express from 'express';

// Things that can be changed without destroying anything!!!
const port = 45679;
const TIMEOUT_TIME_IN_SECONDS = 1;


// Tell express.js to expect JSON requests.
const app = express();
app.use(express.json());
app.listen().setTimeout(5000);

// CHAT WITH THE AI
// Expected Request Format: { model: 'modelName', message: 'message', streamedText: True/False }
app.get('/chat', (req, res) =>  {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        const response = chatToModel(jsonData.model, jsonData.message, jsonData.streamedText)
        res.send(response);
    } catch (error) {
        console.log('/chat error', error);
    }
});

// GET MODEL INFORMATION
// Expected Request Format: { model: 'modelName' }
app.get('/modelinfo', (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.json(getModelInformation(jsonData.model));
    } catch (error) {
        console.log('/modelinfo error', error);
    }
});

// GET RUNNING MODELS
// Expected Request Format: { }
app.get('/modelsrunning', (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.json(getRunningModels())
    } catch (error) {
        console.log('/mdelsrunning error', error);
    }
});

// GET DOWNLOADED MODELS
// Expected Request Format: { }
app.get('/downloaded-models', (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.json(getDownloadedModels())
    } catch (error) {
        console.log('/modelsrunning error', error);
    }
});

// DOWNLOAD A MODEL
// Expected Request Format: { model: 'modelName' }
app.put('/download', (req, res) => {
    res.setTimeout(TIMEOUT_TIME_IN_SECONDS, () =>   {
        console.error("Request has timed out.")
        res.status(408).send('Request timeout.')
    });
    const jsonData = req.body;
    console.log(jsonData);
    
    try {
        res.json(downloadModel(jsonData.model));
    } catch (error) {
        console.log('/download error', error);
    }
});

// LOAD MODEL
// Expected Request Format: { model: 'modelName}
app.put('/load', (req, res) =>  {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.json(loadModel(jsonData.model));
    } catch (error) {
        console.log('/unload error', error);
    }
});

// UNLOAD MODEL
// Expected Request Format: { model: 'modelName' }
app.put('/unload', (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.json(unloadModel(jsonData.model));
    } catch (error) {
        console.log('/unload error', error);
    }
});

// DELETE A MODEL
// Expected Request Format: { model: 'modelName' }
app.delete('/remove', (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.json(deleteModel(jsonData.model));
    } catch (error) {
        console.log('/remove error', error);
    }
});

// TIMEOUT
// https://stackoverflow.com/questions/21708208/express-js-response-timeout#21708822
function haltOnTimedout (req, res, next) {
    if(!req.timedout)   {
        next();
    }
    else    {
        console.error("Request timed out :(")
    }
}

app.listen(port, () =>  {
    console.log(`Server is running at: http://localhost:${port}`);
});