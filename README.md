# Neuroevolution

Replication of [Uber AI Labs Neuroevolution paper](https://arxiv.org/pdf/1712.06567.pdf).


## ToDo

- cloudformation scripts for first run
    - num workers
    - environment
    - choice of vpc, etc.
- first run
- better ECS image map in cloudformation
    - also note that you need to open spot fleet in console to create role
- full environment list in cloudformation


## Approach

I use a master-worker architecture, with:

- Golang master
    - gRPC server that controls the genetic algorithm internals
    - Sends sequences of seeds (individuals) to workers
- Python workers
    - Each has a copy of the policy network and environment
    - Swaps out full network weights on each evaluation (without rebuilding network)
    - Sends seeds and their scores back to master

This results in a simpler system than Uber / OpenAIs approach, which uses redis as an intermediary,
and requires workers to synchronise.


## Deployment

Both master and worker are packaged as docker containers. Either pull the containers from docker-hub,
or build them yourself:
```
# Download
docker pull cshenton/neuro:worker
docker pull cshenton/neuro:master

# Build
docker build -t cshenton/neuro:worker -f worker/Dockerfile .
docker build -t cshenton/neuro:master -f master/Dockerfile .
```

Cloudformation scripts deploy the experiment. The following information is required:
- Availability Zone
- Target VPC

Then the cloudformation scripts create:
- Master
    - Security group (Open on 80)
    - On-demand instance (c4.large)
    - ECS Task
    - Single container ECS Service
- Workers
    - Security group (no ingress)
    - Spot instance auto-scaling group of desired size (c4.large)
    - ECS Task (1 vCPU per container)
    - ECS Service with 4 * nMachines tasks

The spot price I'm working against is $0.0307 for the c4.large, which at a budget of $0.035 is at most
$0.0175 per vCPU per hour. Therefore, running a 1 master, 499 worker fleet for an hour will mean 998
separate worker processes, and will cost:
```
(1 + 499) * 0.035 = $17.50
```
Which is pretty affordable, considering the



## Protobufs

`gRPC` is used to enable simple communication between workers and master. Server, client stubs
are generated as follows.

```
# python
python -m grpc_tools.protoc -I . proto/neuroevolution.proto --python_out=. --grpc_python_out=.

# golang
protoc -I . proto/neuroevolution.proto --go_out=plugins=grpc:.
```


```python
import datetime
import gym
import numpy as np

from worker.policy import Policy

# How long does it take to initialize on a 10 seed individual?
seeds = np.random.randint(1e8, size=10)
p = Policy(6)
t = datetime.datetime.now()
p.set_weights(seeds, 0.005)
print("initialization time:", datetime.datetime.now() - t) # 0:00:02.267878

e = gym.make('Pong-v0')

# How long does it take to do 20sk frames (max evaluation length)
t = datetime.datetime.now()

for i in range(10):
    seeds = np.random.randint(1e8, size=10)
    p.set_weights(seeds, 0.005)
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