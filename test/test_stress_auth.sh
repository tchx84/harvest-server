#!/usr/bin/env bash
ab -n 1000 -c 1000 -p data/data.json -T application/json -H "x-api-key: wrong-key" https://localhost:443/rpc/store
