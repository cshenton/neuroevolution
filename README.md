# neuroevolution
Replication of Uber Neuroevolution paper


## How fast is the agent?

```python
import datetime
import gym
import numpy as np

from worker.policy import Policy

# How long does it take to initialize on a 10 seed individual?
seeds = np.random.randint(1e8, size=10)
t = datetime.datetime.now()
p = Policy(6)
p.set_weights(seeds, 0.005)
print("initialization time:", datetime.datetime.now() - t) # 0:00:02.267878

e = gym.make('Pong-v0')

# How long does it take to do 20k frames (max evaluation length)
t = datetime.datetime.now()

for i in range(10):
    j = 0
    done = False
    state = e.reset()
    while not done:
        action = p.act(state)
        state, reward, done, _ = e.step(action)
        j += 1
    print("episode {} took {} steps".format(i, j))

print("10 episodes took:", datetime.datetime.now() - t) # 0:00:44.055469
```

## Protobufs

Generate python stubs:
```
python -m grpc_tools.protoc -I . proto/neuroevolution.proto --python_out=. --grpc_python_out=.
```

Generate golang stubs:
```
protoc -I . proto/neuroevolution.proto --go_out=plugins=grpc:.
```
