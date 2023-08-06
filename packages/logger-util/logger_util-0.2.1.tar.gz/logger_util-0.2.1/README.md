# logger_util
Dead simple Python logger.

This library redirects the stdout and stderr to a Log object that saves the text printed to the console to a file.  The file is auto-generated and is named based on the number of files in the log directory.  Adding simple LogLevel attributes at the start of your printed debug text allows the log to be parsed and separately into severity levels.

Install using: `pip install logger-util==0.2`

```py
from logger_util import CreateLogger, log_startup

if __name__ == "__main__":
    CreateLogger()
    log_startup()
    print("INFO: This is a test message.")
```

Calling CreateLogger will instantiate all the necessary variables, files, and directories.  Nothing more needs to be done other than writing to the console.

This library is licensed under the MIT license.
