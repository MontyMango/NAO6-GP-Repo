// Links to what helped here:
//
// Making async functions (To return json data successfully): https://zellwk.com/blog/async-await-express/
// Using Multer to upload files: https://expressjs.com/en/resources/middleware/multer.html

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
import multer from 'multer';
import os from 'node:os';

// Things that can be changed without destroying anything!!!
const port = 45679;
const TRANSCRIPTION_SERVER = "http://10.0.60.4:45689/transcribe"
const app = express();
app.use(express.json());                        // Tell express.js to expect JSON requests.
app.listen().setTimeout(15000);                 // Set the timeout to 15 seconds.
const upload = multer({ dest: os.tmpdir() });   // Upload the audio files to a temporary directory.

// CHAT WITH THE AI
// Expected Request Format: { model: 'modelName', audioFile: file.ogg, streamedText: True/False }
app.post('/chat', upload.single('audioFile'), async (req, res) =>  {
    const jsonData = req.body;
    const audioFile = req.file;
    
    console.log(jsonData);
    console.log(audioFile);
    console.log(`Saved file in ` + os.tmpdir());

    // Send the audio file to be transcribed to the speech-recognition-server
    // https://stackoverflow.com/questions/36067767/how-do-i-upload-a-file-with-the-js-fetch-api
    // https://flaviocopes.com/how-to-upload-files-fetch/


    const formData = new FormData();
    formData.append('file', audioFile);
    console.log(formData);

    const options = {
        method: 'POST',
        header: {
            'Content-Type': 'multipart/form-data; boundary=---011000010111000001101001',
        }
    }

    options.body = formData;

    const transcribedAudio = fetch(TRANSCRIPTION_SERVER, options)
        .then(function(response)    {
            return response // if the response is a JSON object
        }
        ).then(function(data)   {
            console.log(data);
            return data; // Handle the success response object
        }
        ).catch(
            error => console.log(error) // Handle the error response object
    );

    var isRequestIncomplete = false;
    var incompleteRequestJSON = {};
    if(!jsonData.model)  {
        incompleteRequestJSON.model = "model needs to be filled when chatting with the robot!"
        isRequestIncomplete = true;
    }
    if(jsonData.streamedText == "")  {
        console.log("Note: Defaulting streamed text to false")
    }

    // If everything checks out, send a response to the AI server
    if(isRequestIncomplete == true)    {
        const response = await chatToModel(jsonData.model, transcribedAudio, Boolean(jsonData.streamedText));
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