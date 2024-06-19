# PNX (will be merged with MI5IX)

A Python wrapper for OpenAI Assistant. Utilizes structured inputs to delivered structured outputs for more controllable actions.

## Quickstart

You'll need to create custom problems and actions using the example in [prospector.py](pnx/prospector.py):

```bash
# Install repo
git clone https://github.com/JimothyJohn/PNX
cd PNX
pip install -U poetry
poetry install
# Run program
poetry run python pnx
```

[Prompt schema](pnx/models.py)

```py
class Problem(BaseModel):
    owner: str = ""
    location: str = ""
    statement: str = ""

class Action(BaseModel):
    expected_output: str = ""
    tool_choice: str = "auto"
    goal: str = ""
    constraints: str = ""
```

### Learnings

* Keep prompts as compact as possible.

* Reduce hallucinations by making tool_choice "required".

* Separate the persona from the task.

* Ask the system to explain its reasoning to help it fix its mistakes.

* IMPORTANT - When you ask an AI to plan it will frequently take an identical route. Learn a good route and program it in.

## TODO

[ ] Integrate with Azure
