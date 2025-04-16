FROM ollama/ollama

RUN apt-get update && apt-get install -y curl

# Download the models
RUN ollama serve & sleep 5 && \
    ollama pull llama3.2 && \
    ollama pull deepseek-r1:7b && \
    ollama pull qwen2.5:14b &&\
    ollama pull deepseek-r1:14b &&\
    ollama pull gemma3:12b

# Expose the default Ollama port
EXPOSE 11434

# Start Ollama
ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]
