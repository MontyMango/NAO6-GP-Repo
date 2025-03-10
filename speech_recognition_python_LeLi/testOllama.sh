curl -X POST http://localhost:11434/api/generate \
     -H "Content-Type: application/json" \
     -d '{
          "model": "deepseek-r1:7b",
          "prompt": "You are a conversational chatbot named Nao6, For the following prompt: What do you think is more important, eliminating hunger in Africa or sending people to the moon, make a short and concise one paragraph response of no more than 200 words.",
          "stream": false
         }'

