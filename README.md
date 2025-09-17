# GTM Outbound Agent

This is our AI-based outbound go-to-market agent. The goal is to do a bunch of BDR work autonomously and support our lead generation efforts.

This is very much a work-in-progress and given the uncertain nature of this project, we expect to rapidly evolve and experiment here. Because of that, there's a good chance that this README is outdated at any time. So here we're basically trying to describe the overall goals and architecture.

How it works:
- Start with a list of target accounts
  - These will live in a Postgres database for now
  - Later on, we might automatically feed them from Snowflake, or have a simple web interface
- Research these target accounts using LLM calls
  - This could include using web tools (from OpenAI for example) to find interesting pieces of information on the website, Instagram, etc
- Draft outbound messages
  - (unclear at this point if we do only email or also try SMS)
- Have a human-in-the-loop step to review & approve draft messages
  - (unclear as of now if we'll build a simple web interface ourselves or use something like Superblocks)
- Send approved messages using a service such as Sendgrid or Twilio
  - Sending will be done from a BDR-like persona with a real looking email address
  - For email, we plan to use a different domain so as to not get in trouble in case we get spam reports

Technical architecture:
- Fully written in Python
- Using Temporal.io (cloud service) for orchestration and "durable execution"
- Using Neon Postgres as an application database (where we maintain state, draft messages, etc)
- Uses Fly.io for hosting and Github Action to deploy from `master` branch

## Prerequisites (macOS)
- Python 3.10+ installed (check with `python3 --version`).
  - `brew install python`. 
- Pipx installed
  - Used to install Python CLI applications globally (such as Poetry)
  - `brew install pipx`
- Poetry installed
  - Package manager that we use instead of Pip (works better many reasons)
  - `pipx install poetry`
- dbmate installed
  - Simple database migration tool that we use. Needed for local development
  - `brew install dbmate`
- Flyctl installed
  - We're hosting on Fly.io. To deploy & view logs from terminal you'll neet flyctl
  - `brew install flyctl`
- Local Postgres server for development

## Setup
1. Run `poetry install` to install all the packages
2. Environment variables:
   - Copy the sample env file:
     - `cp .env.sample .env`
   - Update `.env` with your settings (local Postgres database, etc)

## Developing
- Activate virtual environment
  - `poetry env activate`

- Start local Temporal Server
  - Use this method for local development. Make sure to use the localhost setings in your env file
  - `temporal server start-dev`

- Start the worker (listens on your configured task queue):
  - `python -m scripts.run_worker`

- Run the sample workflow (invokes SayHello via the client):
  - `python -m scripts.run_workflow`

- For quick & easy local development, you can use a dev harness like `python -m scripts.dev` 

## Migrations
We're using dbmate for simple, raw SQL database migrations.

Usage:
- To create a new migration: `dbmate new create_users`
  - This will create a new file in `db/migrations/` that you can then edit
- Run migrations: `dbmate up`
  - Locally you have to run migrations manually against the development database
    - It will automatically read the DATABASE_URL from your local `.env` file
  - We automatically run migrations once per Fly.io deploy
    - See `Dockerfile` for how we download the dbmate binary and `fly.toml` for the release command

## Deploying
We're using Github Actions to automatically deploy from the `master` branch. This will also run database migrations. 

If there's any need to deploy from local to Fly.io, you can run the `fly deploy` command while being authenticated.
