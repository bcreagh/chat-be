#!/usr/bin/bash

command=$1
export chatgpt_key=$(cat key.txt)
export OPENAI_API_KEY=$(cat key.txt) 

function usage {
    echo "Usage: $0 <command>"
    echo "Commands:"
    echo "  run: Run the backend"
    echo "  pip: Install requirements"
    echo "  trans <name>: convert a transcript into book format and flashcards, note you must populate .storage/input.txt with video transcript."
    echo ""
    echo "Note: Before running the backend, make sure to populate the 'key.txt' file with the ChatGPT API key."
}

if [ -z "$chatgpt_key" ]; then
    usage
    exit
fi

case $command in
    run)
        fastapi dev main.py
        ;;
    pip)
        pip install -r requirements.txt
        ;;
    trans)
        transcript=$(cat ./storage/input.txt)
        name=$2
        curl -X POST "http://127.0.0.1:8000/transcript" -H "Content-Type: application/json" -d "{\"name\": \"${name}\", \"transcript\": \"${transcript}\"}"
        ;;
    *)
        echo "Invalid command"
        usage
        exit
        ;;
esac





