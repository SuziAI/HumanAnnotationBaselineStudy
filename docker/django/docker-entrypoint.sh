#!/bin/bash
set -e

# Define the folder to check ownership
TARGET_FOLDER=${TARGET_FOLDER:-/app}

# Get the UID and GID of the target folder
HOST_UID=$(stat -c "%u" "$TARGET_FOLDER")
HOST_GID=$(stat -c "%g" "$TARGET_FOLDER")

# Create a group with the host GID if it doesn't exist
if ! getent group "$HOST_GID" >/dev/null; then
    groupadd -g "$HOST_GID" user
fi

# Create a user with the host UID if it doesn't exist
if ! id -u "$HOST_UID" >/dev/null 2>&1; then
    useradd -u "$HOST_UID" -g "$HOST_GID" -m user
fi

# Switch to the host user and execute the command
exec gosu "$HOST_UID":"$HOST_GID" "$@"
