# PNX (will be merged with MI5IX)

A Python wrapper for OpenAI Assistant. Utilizes structured inputs to delivered structured outputs for more controllable actions.

## Quickstart

You'll need to create custom problems and actions using the example in [research.py](pnx/research.py):

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

```python
class Problem(BaseModel):
    owner: str = ""
    goal: str
    location: str = ""
    constraints: str = ""


class Action(BaseModel):
    task: str
    additional_instructions: str
    expected_output: str
    tool_choice: str = "auto"
```

### Learnings

* Keep prompts as compact as possible.

* Reduce hallucinations by forcing the use of tools.

* Separate the persona from the task.

* Ask the system to explain its reasoning to help it fix its mistakes.
