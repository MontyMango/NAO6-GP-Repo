// Do `node --env-file=.env main.js` to run this
// You will need @google/generative-ai before running!
require('dotenv').config();
const {
  GoogleGenerativeAI,
  HarmCategory,
  HarmBlockThreshold,
} = require("@google/generative-ai");
const { error } = require('node:console');
const fs = require('node:fs');

const apiKey = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: "gemini-2.0-flash",
});

const generationConfig = {
  temperature: 1,     // Creativity (0 - 2)
  topP: 0.95,
  topK: 40,
  maxOutputTokens: 8192,
  responseMimeType: "text/plain",
};

async function run() {
  const chatSession = model.startChat({
    generationConfig,
    history: loadFromHistoryFile(),
  });

  const result = await chatSession.sendMessage("Hello!");
  console.log(result.response.text());
}

// Use this if the Robot should have a long-term memory!
async function writeToHistoryFile(text) {
  historyFilePath = "./history.json";

  try {
    fs.writeFileSync(historyFilePath, text, 
      {
        encoding: "utf-8", 
        flag: 'w+'
      }, 
      err => {
        console.log(err);
    });
  } catch (error) {
    console.log(error)
  }
}

// Load the history on boot up.
// This won't be asyncronous due history being needed when querying the AI.
function loadFromHistoryFile()  {
  historyFilePath = "./history.json";

  // Check if the file exists
  if (fs.existsSync(historyFilePath)) {
    fs.readFile(historyFilePath, 'utf8', function(error, data)  {
      console.log('File exists:');
      console.log(data);

      return JSON.parse(data);
    });
  } 
  else {
    fs.writeFile(historyFilePath, '[]');
    console.log('File does not exist. File created!');
    return [];
  } 
}

run();