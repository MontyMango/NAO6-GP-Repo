// Links to what helped here:
//
// Making async functions (To return json data successfully): https://zellwk.com/blog/async-await-express/

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

import express, { response } from 'express';

// Things that can be changed without destroying anything!!!
const port = 45679;


// Tell express.js to expect JSON requests.
const app = express();
app.use(express.json());
app.listen().setTimeout(15000);

// CHAT WITH THE AI
// Expected Request Format: { model: 'modelName', message: 'message', streamedText: True/False }
app.post('/chat', async (req, res) =>  {
    const jsonData = req.body;
    console.log(jsonData);

    // Check if data is complete (TODO: FIX THIS, IT'S NOT WORKING)
    var isRequestIncomplete = false;
    var incompleteRequestJSON = {};
    if(jsonData.model == "")  {
        incompleteRequestJSON.model = "model needs to be filled when chatting with the robot!"
        isRequestIncomplete = true;
    }
    if(jsonData.message == "")   {
        console.log("Note: message is not filled out, defaulting to hello");
    }
    if(jsonData.streamedText == "")  {
        console.log("Note: Defaulting streamed text to false")
    }

    // If everything checks out, send a response to the AI server
    if(isRequestIncomplete == false)    {
        const response = await chatToModel(jsonData.model, jsonData.message, Boolean(jsonData.streamedText));
        try {
            return res.send(response);
        } catch (error) {
            console.log('/chat error', error);
            return res.status(400).send("Error has occured in /chat");
        }
    }
    else    {
        return res.send(incompleteRequestJSON);
    }
});

// GET MODEL INFORMATION
// Expected Request Format: { model: 'modelName' }
app.get('/modelinfo', async (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await getModelInformation(jsonData.model);
    try {
        res.json(response);
    } catch (error) {
        console.log('/modelinfo error', error);
    }
});

// GET RUNNING MODELS
// Expected Request Format: { }
app.get('/modelsrunning', async (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await getRunningModels();
    try {
        res.json(response);
    } catch (error) {
        console.log('/mdelsrunning error', error);
    }
});

// GET DOWNLOADED MODELS
// Expected Request Format: { }
app.get('/downloaded-models', async (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await getDownloadedModels();
    console.log(response);
    try {
        res.json(response);
    } catch (error) {
        console.log('/modelsrunning error', error);
    }
});

// DOWNLOAD A MODEL
// Expected Request Format: { model: 'modelName' }
app.put('/download', async (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await downloadModel(jsonData.model)
    try {
        res.json(response);
    } catch (error) {
        console.log('/download error', error);
    }
});

// LOAD MODEL
// Expected Request Format: { model: 'modelName}
app.put('/load', async (req, res) =>  {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await loadModel(jsonData.model)
    try {
        res.json(response);
    } catch (error) {
        console.log('/unload error', error);
    }
});

// UNLOAD MODEL
// Expected Request Format: { model: 'modelName' }
app.put('/unload', async (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await unloadModel(jsonData.model) 
    try {
        res.json(response);
    } catch (error) {
        console.log('/unload error', error);
    }
});

// DELETE A MODEL
// Expected Request Format: { model: 'modelName' }
app.delete('/remove', async (req, res) => {
    const jsonData = req.body;
    console.log(jsonData);
    const response = await deleteModel(jsonData.model);
    try {
        res.json(response);
    } catch (error) {
        console.log('/remove error', error);
    }
});

app.listen(port, () =>  {
    console.log(`Server is running at: http://localhost:${port}`);
});