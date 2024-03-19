# Conditional creation of .env file
if [[ -f ".env" ]]; then
  echo "env variables file found"
else
  echo "env variables file not found, creating..."
  printenv | sort > .env
fi

echo "environmnet variables set"
