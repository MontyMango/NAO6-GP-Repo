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
import fs from 'fs';

// Things that can be changed without destroying anything!!!
const port = 45679;
const TRANSCRIPTION_SERVER = "http://10.0.60.4:45689/transcribe"
const app = express();
app.use(express.json());                        // Tell express.js to expect JSON requests.
app.listen().setTimeout(15000);                 // Set the timeout to 15 seconds.
const upload = multer({ dest: os.tmpdir() });   // Upload the audio files to a temporary directory.

// CHAT WITH THE AI
// Expected Request Format: { model: 'modelName', audioFile: file.ogg or file.wav, streamedText: True/False }
app.post('/chat', upload.single('audioFile'), async (req, res) =>  {
    const jsonData = req.body;
    const audioFile = req.file;
    
    console.log(jsonData);
    console.log(audioFile);
    console.log(`Saved file in ` + os.tmpdir());

    // Ensure the file is correctly appended to the FormData object
    const form = new FormData();
    const audioFileBlob = audioFile.blob();

    form.append("file", fs.createReadStream(audioFile.path), `${audioFile.filename}`);
    console.log(form);

    const options = {
        method: 'POST',
        body: form,
        headers: {
            'Context-Type': 'multipart/form-data'
        }
    };

    try {
        const response = await fetch(TRANSCRIPTION_SERVER, options);
        const data = await response.json();
        console.log(data);
        return res.send(data); // Handle the success response object
    } catch (error) {
        console.log(error); // Handle the error response object
        return res.status(500).send("Error occurred while transcribing audio");
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