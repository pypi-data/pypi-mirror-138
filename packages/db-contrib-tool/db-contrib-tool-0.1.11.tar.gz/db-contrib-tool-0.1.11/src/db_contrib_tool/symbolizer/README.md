# `symbolize`

Symbolize MongoDB C++ stacktraces from any Evergreen-generated binary;
including release binaries, patch builds, & mainline waterfall runs.

## Usage
 Help message and list of options:
 ```bash
 $ db-contrib-tool symbolize -h
 ```

### Cheat Sheet of Common Use Cases
```bash
# Symbolize MongoDB stacktraces from any Evergreen binary (including release binaries).
db-contrib-tool symbolize < fassert.stacktrace

# Extract and symbolize stacktraces from logs of live mongod/s/q processes.
tail mongod.log | db-contrib-tool symbolize --live

# Backwards compatible with mongosymb.py
```

## Known Limitations

### Symbolizer service Authentication
The symbolizer service requires a browser to authenticate to Okta.
To work around this limitation when using the symbolizer service through
`ssh`, you would need to run the symbolizer on your local machine, then
copy the credentials file `~/.symbolizer_credentials.json` to the remote
machine. 

This is not expected to be a common use case for Core DB engineers
as Evergreen tests should have backtraces automatically symbolized.