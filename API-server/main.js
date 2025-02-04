// https://www.freecodecamp.org/news/make-api-calls-in-javascript/#heading-how-to-choose-an-api

const LLAMAURL = 'http://localhost:11434/api/';

const listModels = () => {
    console.log("Getting list of models from: " + `${LLAMAURL}tags`)
    fetch(`${LLAMAURL}tags`)
        .then(response => {
            if (!response.ok)   {
                throw new Error('API didn\'t respond');
            }
            else    {
                console.log("Getting models...")
            }
        })
        .then(data => {
            if(!data)   {
                console.log("There are no models available.");
            }
            else    {
                console.log(data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



listModels()