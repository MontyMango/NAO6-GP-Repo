// Cameron Harter 2025

/*
Links that helped here: 
1. https://www.freecodecamp.org/news/javascript-post-request-how-to-send-an-http-post-request-in-js/
2. https://www.freecodecamp.org/news/make-api-calls-in-javascript/#heading-how-to-choose-an-api
3. Make the JSON streamable: https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
4. Fix undefined non-streamable functions: https://stackoverflow.com/questions/40385133/retrieve-data-from-a-readablestream-object#40403285
*/

// Change the LLAMAURL if you are deploying the llama in a different location than your local environment!
const LLAMAURL = 'http://172.16.238.0:11434/api/';

// Available large language models | More Models Here: https://ollama.com/search
// Key - Name to display on the website, Value - Model to use in API
const LLM_MODELS = {
    "DeepSeek-R1 (8b)" : "deepseek-r1:8b",   // 8b parameters
    "Llama 3.1 (8b)" : "llama3.1",           // 8b parameters
    "Llama 3.2 (3b)" : "llama3.2",           // 3b parameters
    "Gemma (7b)": "gemma:7b",                // 7b parameters
    "Qwen 2.5 (0.5b)" : "quen2.5:0.5b"       // 0.5b parameters (Used for testing!)
}

// (For the long stretch) Available Vision LLMs
const VISION_LLM_MODELS = {
    "LLaVa 1.6 (7b)" : "llava:7b",                  // 7b parameters
    "Llama 3.2 - Vision (11b)" : "llama3.2-vision"  // 11b parameters
}



/*
EXAMPLE JSON:
{
  models: [
    {
      name: 'qwen2.5:0.5b',
      model: 'qwen2.5:0.5b',
      modified_at: '2025-02-16T15:36:23.190656979Z',
      size: 397821319,
      digest: 'a8b0c51577010a279d933d14c2a8ab4b268079d44c5c8830c0a93900f1827c67',
      details: [Object]
    },
    {
      name: 'qwen:0.5b',
      model: 'qwen:0.5b',
      modified_at: '2025-02-16T14:42:25.869442966Z',
      size: 394998579,
      digest: 'b5dc5e784f2a3ee1582373093acf69a2f4e2ac1710b253a001712b86a61f88bb',
      details: [Object]
    }
  ]
}
*/
const getDownloadedModels = () => {
    console.log("Getting list of models from: " + `${LLAMAURL}tags`)
    fetch(`${LLAMAURL}tags`)
        .then(function(response)    {
            return response.json()
        })
        .then(function(data)    {
            console.log(data);
            return data;
        });
}





const getRunningModels = () =>  {
    console.log("Getting list of currently running models from: " + `${LLAMAURL}ps`)
    fetch(`${LLAMAURL}ps`)
        .then(function(response)    {
            return response.json()
        })
        .then(function(data)    {
            console.log(data);
            return data;
    });
}





const getModelInformation = (model) =>  {
    console.log("Getting model information from: " + `${LLAMAURL}pull`)
    fetch(`${LLAMAURL}show`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": model
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(function(response)    {
        return response.json()
    })
    .then(function(data)    {
        console.log(data);
        return data;
    });
}





const downloadModel = (modelToDownload) =>    {
    console.log("Downloading " + modelToDownload);
    fetch(`${LLAMAURL}pull`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": modelToDownload
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => response.body)
        .then((rb) => {
            const reader = rb.getReader();

            return new ReadableStream({
                start(controller) {
                    // The following function handles each data chunk
                    function push() {
                    // "done" is a Boolean and value a "Uint8Array"
                    reader.read().then(({ done, value }) => {
                        // If there is no more data to read
                        if (done) {
                            console.log("done", done);
                            controller.close();
                            return;
                        }
                        // Get the data and send it to the browser via the controller
                        controller.enqueue(value);
                        // Check chunks by logging to the console
                        console.log(done, value);
                        push();
                    });
                }

                push();
            },
            });
        })
        .then((stream) =>
            // Respond with our stream
            new Response(stream, { headers: { "Content-Type": "text/html" } }).text(),
        )
        .then((result) => {
            // Do things with result
            console.log(result);
            return result;
    });
    // If {"status":"success"}, this means that the model has been pulled.
}



// deleteModel: Delete a model if it's no longer needed.
/*
Example #1:
done true

Example #2:
{"error":"model 'qwen:0.5b' not found"}
*/
const deleteModel = (modelToDelete) =>  {
    console.log("Deleting model: " + modelToDelete);
    fetch(`${LLAMAURL}delete`,  {
        "method": "DELETE",
        "body": JSON.stringify({
            "model": `${modelToDelete}` 
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(function(response)    {
        return response.text()
    })
    .then(function(data)    {
        console.log(data);
        return data;
    });
}





// unloadModel: Use if you need to unload a model!
/*
Example JSON #1: unloadModel("qwen2.5:0.5b");
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
    console.log("Unloading model: " + modelToUnload);
    fetch(`${LLAMAURL}chat`,    {
        "method": "POST",
        "body": JSON.stringify({
            "model": modelToUnload,
            "messages": [],
            "keep_alive": 0
        }),
        "headers":    {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(function(response)    {
        return response.json()
    })
    .then(function(data)    {
        console.log(data);
        return data;
    });
}

// The only way to load the model is to use the "chat" API, but use an empty array for the message 
// This might not be used because you can pull the model and then chat. You don't need to "load the model" at all.
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
    if(shouldTextbeStreamed)    {
        // Handles streamed text
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
        .then((response) => response.body)
        .then((rb) => {
            const reader = rb.getReader();

            return new ReadableStream({
                start(controller) {
                    // The following function handles each data chunk
                    function push() {
                    // "done" is a Boolean and value a "Uint8Array"
                    reader.read().then(({ done, value }) => {
                        // If there is no more data to read
                        if (done) {
                            console.log("done", done);
                            controller.close();
                            return;
                        }
                        // Get the data and send it to the browser via the controller
                        controller.enqueue(value);
                        // Check chunks by logging to the console
                        console.log(done, value);
                        push();
                    });
                }

                push();
            },
            });
        })
        .then((stream) =>
            // Respond with our stream
            new Response(stream, { headers: { "Content-Type": "text/html" } }).text(),
        )
        .then((result) => {
            // Do things with result
            console.log(result);
            return result;
        });
    }

    else    {
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
        .then(function(response)    {
            return response.json();
        })
        .then(function(data)    {
            console.log(data);
            return data;
        });
    }
}




// FOR TESTING PURPOSES ONLY 
// getDownloadedModels();
// getRunningModels();

// deleteModel('qwen2.5:0.5b');

// chatToModel("qwen2.5:0.5b", "hello", false);
// getModelInformation("qwen2.5:0.5b");
// downloadModel("qwen2.5:0.5b");
// loadModel("qwen2.5:0.5b");
// unloadModel("qwen2.5:0.5b");