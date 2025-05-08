# This is used to setup the Ollama LLMs
FROM ollama/ollama

RUN apt-get update && apt-get install -y curl

# Downloading the models
# We decided to download all the models so there would be no "buffer" with the user's experience
# This will increase used space on the system, but there will be less latency.
RUN ollama serve & sleep 5 && \
    ollama pull llama3.2 && \
    ollama pull deepseek-r1:7b && \
    ollama pull qwen2.5:0.5b &&\
    ollama pull qwen2.5:14b &&\
    ollama pull deepseek-r1:14b &&\
    ollama pull gemma3:12b

# Expose the default Ollama port
EXPOSE 11434

# Start Ollama
ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]
