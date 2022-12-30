# Copilot, for your Jupyter Notebook

`%plz` is a Jupyter magic command that generates programs from human-readable descriptions in Jupyter notebooks.


https://user-images.githubusercontent.com/11509740/210084133-61f2cb2d-9968-4b01-8a67-85fcb92eb312.mov


## Installation

You can install `plz` in your Python virtual environment by running the following command in your terminal:

```bash
pip install plz
```

## Usage

`plz` uses [GPT-3](https://beta.openai.com/). To use it, you'll need to:

- Activate billing on your OpenAI [account](https://beta.openai.com/account/billing/overview).
- Grab an API key from [your dashboard](https://beta.openai.com/).
- Save the key as an environment variable named `OPENAI_API_KEY`.
  - *Note*: you can also save it in your `bash/zsh profile` files for persistence between sessions.

```bash
export OPENAI_API_KEY='sk-XXXXXXXX'
```

Once you have configured your environment, run `plz` followed by (optionally, the desired output format) and what you want to do. Example:

```bash
%plz "create a function that generates a random walk in the form of an array."
```

Or markdown guides:

```bash
%plz --markdown "Provide a step-by-step guide on how to identify anomalies in a list of numbers."
```

## Credit

This tool is inspired by [plz-cli](https://github.com/m1guelpf/plz-cli) (designed for the command line).

## License

This project is open-sourced under the MIT license. See [the License file](LICENSE) for more information.
