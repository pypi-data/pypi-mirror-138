### Timeout
Random timeout between minimum and maximum values

`pip install python-timeout`

```
from timeout import timeout

timeout(10, 20) # Random timeout between 10 and 20 seconds
timeout(60, 120) # Random timeout between one minute (60 seconds) and two minutes (120 seconds)
```