#!/bin/bash

NODE_MODULES=/workspace/node_modules
cd /workspace

# Check if modules are present
if [ -z "$(ls -A ${NODE_MODULES})" ]; then
   npm config set user 0
   npm i
fi

# start the main process (if wanted)
# npm run dev
