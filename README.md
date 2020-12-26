# entropeer

Searches through files and directories for high entropy strings and secrets. 

Similar to [trufflehog](https://github.com/dxa4481/truffleHog) but for local files rather than git repos. 
Based also on [entro.py](https://github.com/tehryanx/entro.py).

## Install
```bash
pip3 install entropeer
```

## What it does
entropeer will dig secrets out of a file or a folder returning strings with high shannon entropy or secrets matching some rules.
This can be used to quickly pull secret keys out of a large collection of files like a local sourcecode repo. 

## How to
Scan a single file:  
```bash
entropeer -f ./filename
```

Search all the files in the current directory: 
```bash
entropeer
```

Search all the files in a custom directory: 
```bash
entropeer -d /tmp/code
```

Recursively search all the files in the current directory and all of its subdirectories:  
```bash
entropeer -r
```

By default `entropeer` does Regex-based scan but you can change to Entropy-based scan with `-E` or `--entropy`
```bash
entropeer -Erd /tmp/code
```

Complete help dialog
```
usage: entropeer [-h] [-f FILE | -d DIRECTORY] [-r] [-E | -X] [--rules RULES] [-M] [-v] [-t THREADS] [-V]

Search files for strings with high shannon entropy.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --filename FILE
                        File to search.
  -d DIRECTORY, --directory DIRECTORY
                        Search all files in directory.
  -r, --recurse         Search directories recursively starting in the current directory. Use with -d
  -E, --entropy         Enable entropy checks
  -X, --regex           Enable high signal regex checks
  --rules RULES         Load external rules from json list file
  -M, --match-only      Print only the matching string
  -v, --verbose         Verbose output
  -t THREADS, --threads THREADS
                        Number of threads/processes to start
  -V, --version         show program's version number and exit

 ```
