#!/bin/bash

# Define the directory path relative to the script
target_dir="./src/chatcleaner/adapters/db/migrations/versions"

# Check if the directory exists
if [ ! -d "$target_dir" ]; then
  # Create the directory if it doesn't exist
  echo "Creating directory: $target_dir"
  mkdir -p "$target_dir"
fi

echo "Versions directory check complete."


# Conditional creation of .env file
if [[ -f ".env" ]]; then
  echo "env variables file found"
else
  echo "env variables file not found, creating..."
  printenv | sort > .env
fi

echo "environmnet variables set"

echo "Startup script complete."
