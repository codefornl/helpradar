#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin"
# make sure cron has access to the environment variables
. <(xargs -0 bash -c 'printf "export %q\n" "$@"' -- < /proc/1/environ)

function fail {
  echo $1 >&2
  exit 1
}

function retry {
  local n=1
  local max=5
  local delay=15
  while true; do
    "$@" && break || {
      if [[ $n -lt $max ]]; then
        ((n++))
        echo "Command failed. Attempt $n/$max:"
        sleep $delay;
      else
        fail "The command has failed after $n attempts."
      fi
    }
  done
}

cd /usr/helpradar
# Alembic connection will be retried 5 times when necessary. This is needed because docker-compose doesn't wait for postgres to start
retry alembic upgrade head
