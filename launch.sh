#!/bin/bash
echo -e "Python-Rag server launcher \n\n supported flags \n\n --production IP_ADDRESS\n --python PATH_TO_PYTHON\n"

# check if python is provided and use the user provided python script 
if [[ "$1" == "--python" ]]; then
  localPy="$2"
  shift 2
else
  echo "No supplied --python argument, using default python3"
  localPy="python3"
fi

# check which OS we are using and install json tools accordingly
if ! command -v jq >/dev/null 2>&1; then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get >/dev/null 2>&1; then
            # Debian or Ubuntu
            sudo apt-get update
            sudo apt-get install -y jq
        elif command -v yum >/dev/null 2>&1; then
            # CentOS or Fedora
            sudo yum install -y jq
        else
            echo "Unsupported Linux distribution. Please install jq manually."
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew >/dev/null 2>&1; then
            # Homebrew
            brew install jq
        else
            echo "Homebrew not found. Please install jq manually."
        fi
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        if command -v choco >/dev/null 2>&1; then
            # Chocolatey
            choco install jq
        else
            echo "Chocolatey not found. Please install jq manually."
        fi
    else
        echo "Unsupported operating system. Please install jq manually."
    fi
fi


# check on installation status
if [ ! -f "index_config.json" ]; then
  ./scripts/install.sh
  while [ ! -f "index_config.json" ]; do
    sleep 1
  done
fi

#  check if the index is built 
if [ -f "index_config.json" ]; then
  if command -v jq >/dev/null 2>&1; then
    vector_index_count=$(jq '.vector_index | length' index_config.json)
    if [ "$vector_index_count" -eq 0 ]; then
      ./scripts/buildIndex.sh
      while [ "$(jq '.vector_index | length' index_config.json)" -eq 0 ]; do
        sleep 1
      done

    fi
  else
    echo "jq command not found. Please install jq."
    exit 1
  fi  
fi
echo "Launching Server..."
# check if we want production version or regular version
source pyrag_index_env/bin/activate

if [[ "$1" == "--production" ]]; then
  pip install gunicorn
  ip_address=$2
    if [[ -z "$ip_address" ]]; then
      echo "Please provide an IP address with the --production flag"
      exit 1
    fi
    gunicorn --bind $ip_address:3592 app:app
else
  if command -v flask >/dev/null 2>&1; then
    flask run --reload --port 3592
  else
    echo "flask command not found. Please install Flask."
    exit 1
  fi
fi
