An LLM agent is just an LLM with tools.

Usual stuff:
```
python3 -venv .env
source .env/bin/activate
python3 -r requirements.txt
```

Put your OpenAI key in env.env and source it:
```
source env.env
```

Current arsenal of tools are basic functions in `tools.py`.

Example of agents:

### French comedian:
- Creates a joke in English
- Translates to French
```
python3 french_comedian.py
```

### Leetcode solver: 
- Attempt a solution
- Check if test cases are passed
- Repeat

```
> leetcode_solver.ipynb
```

To add:
- Email sender
- Web finder