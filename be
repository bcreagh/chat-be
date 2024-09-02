#!/usr/bin/bash

command=$1
export chatgpt_key=$(cat key.txt)
export OPENAI_API_KEY=$(cat key.txt) 

function usage {
    echo "Usage: $0 <command>"
    echo "Commands:"
    echo "  run: Run the backend"
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
    *)
        echo "Invalid command"
        usage
        exit
        ;;
esac





