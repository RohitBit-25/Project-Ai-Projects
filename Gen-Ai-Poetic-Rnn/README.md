Gen-Ai-Poetic-Rnn
==================

Small character-level RNN generator trained on a subset of Shakespeare.

Quick start
-----------

1. Create and activate a virtualenv (Python 3.11 recommended):

```zsh
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

2. Run generation using the pretrained model (the repo includes `shakespeare_model.h5`):

```zsh
python main.py --length 400 --temperature 1.0
```

Options
-------

- `--model`: path to the saved model (default: `shakespeare_model.h5`)
- `--length`: number of characters to generate (default: 400)
- `--temperature`: sampling temperature (default: 1.0)
- `--seed`: optional seed text to start generation (truncated to 40 chars)

Notes
-----
- This project expects Python 3.10/3.11 and will not install TensorFlow on unsupported Python versions.
- For Apple Silicon, prefer `tensorflow-macos` and `tensorflow-metal` for GPU support.
