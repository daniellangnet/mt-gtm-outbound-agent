# GTM Outbound Agent

This repository contains a simple Temporal worker and workflow that we use for outbound GTM purposes. 

These instructions are focused on macOS and show how to run everything from the project root using `python -m`.

## Prerequisites (macOS)
- Python 3.10+ installed (check with `python3 --version`).
- Homebrew recommended to install Python if needed: `brew install python`.
- Poetry installed (used as package manager)

## Setup
1. Clone the repo and open the project directory in a terminal.
3. Run `poetry install` to install all the packages
4. Environment variables:
   - Copy the sample env file and edit values:
     - `cp .env.sample .env`
   - Update `.env` with your Temporal settings (address, namespace, API key, task queue, TLS flag, etc.).

## Developing
All run commands below are executed from the repo root with the virtual environment activated.

- Activate virtual environment
  - `poetry env activate`

- Start local Temporal Server
  - Use this method for local development. Make sure to use the localhost setings in your env file
  - `temporal server start-dev`

- Start the worker (listens on your configured task queue):
  - `python -m scripts.run_worker`

- Run the sample workflow (invokes SayHello via the client):
  - `python -m scripts.run_workflow`

## Deploying
- We use Fly.io for hosting
- Install using `brew install flyctl`

You should see logs indicating a connection to the Temporal service, then worker activity and workflow execution. The workflow result will be printed to the console.

## Tips
- Make sure the worker is running before you execute the workflow command, so the workflow can be picked up and completed.
- If you change dependencies, re-run `python -m pip install -r requirements.txt`.
- To deactivate the virtual environment later, run `deactivate`.
