// Cameron Harter 2025

/*
Links that helped here: 
1. https://www.freecodecamp.org/news/javascript-post-request-how-to-send-an-http-post-request-in-js/
2. https://www.freecodecamp.org/news/make-api-calls-in-javascript/#heading-how-to-choose-an-api
*/

// Change the LLAMAURL if you are deploying the llama in a different location than your local environment!
const LLAMAURL = 'http://172.16.238.0:11434/api/';


// Returns undefined, trying to fix.
const getDownloadedModels = () => {
    console.log("Getting list of models from: " + `${LLAMAURL}tags`)
    fetch(`${LLAMAURL}tags`)
        .then(response => {
            if (!response.ok)   {
                console.log('API didn\'t respond');
                return  {
                    "error": "Ollama API cannot be reached"
                }
            }
            else    {
                console.log("Getting models...");
                response.json();
            }
        })
        .then(json => {
            console.log(json);
            return json;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Returns undefined, trying to fix.
const getRunningModels = () =>  {
    console.log("Getting list of running models from: " + `${LLAMAURL}ps`)
    fetch(`${LLAMAURL}ps`)
        .then(response => {
            if (!response.ok)   {
                console.log('API didn\'t respond');
                return  {
                    "error": "Ollama API cannot be reached"
                }
            }
            else    {
                console.log("Getting running models...");
                response.json()
            }
        })
        .then(json => {
            console.log(json);
            return json;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// STREAMED JSON, WORKING ON FIXING THE RESULTS HERE
const getModelInformation = (model) =>  {
    console.log("Getting model information from: " + `${LLAMAURL}pull`)
    fetch(`${LLAMAURL}pull`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": model
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => response)
    .then((json) => {
        console.log(json);
        return json;
    })
}


// STREAMED JSON, WORKING ON FIXING THE RESULTS HERE
const downloadModel = (modelToDownload) =>    {
    fetch(`${LLAMAURL}pull`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": modelToDownload
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => response)
    .then((json) => console.log(json))
    // If {"status":"success"}, this means that the model has been pulled.
}

// unloadModel: Use if you need to unload a model!
/*
Example JSON #1: unloadModel("qwen:0.5b");
{
  model: 'qwen:0.5b',
  created_at: '2025-02-09T05:26:25.157585038Z',
  message: { role: 'assistant', content: '' },
  done_reason: 'load',
  done: true
}

Example JSON #2: unloadModel("notAModel");
{ error: 'model "notAModel" not found, try pulling it first' }
*/
const unloadModel = (modelToUnload) =>  {
    fetch(`${LLAMAURL}chat`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": modelToUnload,
            "messages": []
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
        return json;
    })
}

// The only way to load the model is to use the "chat" API, but use an empty array for the message 
const loadModel = (modelToLoad) =>  {
    return chatToModel(modelToLoad);
}


// chatToModel: Use if you need to chat to the model!
// DO NOT USE 'shouldTextbeStreamed = true', this doesn't work yet!
/* 
Example JSON #1: chatToModel("qwen:0.5b", "hi", false);
{
  model: 'qwen:0.5b',
  created_at: '2025-02-09T04:58:05.767485778Z',
  message: {
    role: 'assistant',
    content: "Hello! How can I help you today? If there is anything specific you need assistance with, please let me know. I'm here to help!"
  },
  done_reason: 'stop',
  done: true,
  total_duration: 964654148,
  load_duration: 21546764,
  prompt_eval_count: 9,
  prompt_eval_duration: 76000000,
  eval_count: 31,
  eval_duration: 865000000
}

Example JSON #2: chatToModel("notAModel", "whoops", false);
{ error: 'model "notAModel" not found, try pulling it first' }
*/
const chatToModel = (modelToUse, message=[], shouldTextbeStreamed=false) =>    {
    fetch(`${LLAMAURL}chat`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": modelToUse,
            "messages": [
                {
                "role": "user",
                "content": `${message}`
                }
            ],
            "stream": shouldTextbeStreamed
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    // What should we do with the response?
    .then((response) => response.json())
    // What should we do with the json?
    .then((json) => {
        console.log(json);
        return json;
    });
}

getDownloadedModels();
getRunningModels();
await downloadModel("qwen:0.5b");
chatToModel("notAModel", "whoops", false);
unloadModel("notAModel");
