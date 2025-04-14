FROM ollama/ollama

RUN apt-get update && apt-get install -y curl

# Download the models
RUN ollama serve & sleep 5 && \
    ollama pull llama3.2 && \
    ollama pull deepseek-r1:7b && \
    ollama pull qwen2.5:0.5b &&\
    ollama pull qwen2.5-coder &&\
    ollama pull gemma 

# Expose the default Ollama port
EXPOSE 11434

# Start Ollama
ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]
