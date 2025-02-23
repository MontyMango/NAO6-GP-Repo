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
const app = express();
const port = 45679;

// Tell express.js to expect JSON requests.
app.use(express.json());

// CHAT WITH THE AI
// Expected Request Format: { model: 'modelName', message: 'message', streamedText: True/False }
app.get('/chat', (req, res) =>  {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.send(chatToModel(jsonData.model, jsonData.message, jsonData.streamedText));
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
        res.send(getModelInformation(jsonData.model));
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
        res.send(getRunningModels())
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
        res.send(getDownloadedModels())
    } catch (error) {
        console.log('/modelsrunning error', error);
    }
});

// DOWNLOAD A MODEL
// Expected Request Format: { model: 'modelName' }
app.put('/download', (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    try {
        res.send(downloadModel(jsonData.model));
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
        res.send(loadModel(jsonData.model));
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
        res.send(unloadModel(jsonData.model));
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
        res.send(deleteModel(jsonData.model));
    } catch (error) {
        console.log('/remove error', error);
    }
});


app.listen(port, () =>  {
    console.log(`Server is running at: http://localhost:${port}`);
});