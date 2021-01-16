# WiseAI-CLI

A client for WiseAgent to automated-deploy.

![image](https://github.com/WiseAI-Lab/WiseAgent/blob/main/logo.png)

## Quick Start

#### 1. Log in WiseAI.

```shell
> wiseai token {token}
Succefully login!!! Welcome {user_name}!!!
```

#### 2. check all agent list

```
> wiseai agent ps -a

ID | AgentName | status
1  | TestAgent:v1 | not local
```

#### 3. Deploy your agent by ID.

```
> wiseai agent build 1 

Start to deploy agent ==> TestAgent:v1...
Authonity...
Success!!!
Get agent's configuration...
Success!!!
Download agent...
Success!!!
Build agent locally...
Success!!!
Agent ==> TestAgent:v1 is ready!!!

# check agent list again.
> wiseai agent ps

ID | AgentName | status
1  | TestAgent:v1 | ready
```

#### 4. Start the agent

```
> wiseai agent start 1
Check the status of TestAgent:v1.
Normal!
Stating...
Agent ==> TestAgent:v1 is running!!!
You can check the status of agent in {host}:{port}
```

## More Details
```shell
> wiseai token {token}  # set and update token.
> wiseai agent stop 1  # stop agent 1.
> wiseai agent log 1 # check the log file for agent 1.
...
```
