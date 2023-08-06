# Blueqat cloud SDK (bqcloud)
Client SDK for Blueqat cloud.

## Install
`pip install blueqat-cloud`

# Handling API key
## Register API
```py
import bqcloud
api = bqcloud.register_api("Your API key here")
```

Your API key is stored to `$HOME/.bqcloud/api_key`.
If you don't want to save API key, use insteads following codes.

```py
import bqcloud
api = bqcloud.api.Api("Your API key here")
```

## Load API
Once API key is saved, the key can be loaded from file.

```py
import bqcloud
api = bqcloud.load_api()
```

# Gate

## Create a task
```py
from blueqat import Circuit
from bqcloud import load_api, Device
api = load_api()

task = api.execute(Circuit().h[0].cx[0, 1], Device.IonQDevice, 10)
```

### Show a status
```py
print(task.status())
```

### Update a task
```py
task.update()
```

## Wait a task
```py
# Wait until task is done. It may takes so long time.
result = task.wait()
print(result.shots())
```

```py
# Wait 10 sec. If complete, result is returned, otherwise, None is returned.
result = task.wait(timeout=10)
if result:
    print(result.shots())
else:
    print("timeout")
```

## Get fetched result again
```py
# Once updated or waited after task completed, task.result() returns the result.
result = task.result()
if result:
    print(result.shots())
else:
    print("result is not fetched")
```

# List tasks
```py
tasks = api.tasks()
print(list(tasks))
if tasks[0].result() is not None:
    print(tasks[0].result().shots())
```

# Annealing
```py
import bqcloud
api = bqcloud.load_api()
api.annealing([[-1, 0], [0, 0.5]], 5, 10)
```
