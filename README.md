# Okizeme Simulator

This is a web-based game built entirely with Svelte, backed by a 7th-order Multi-Markov Chain implemented in Python. The goal is to test whether a human player can outsmart the AI in a guessing game based on *okizeme* — a common situation in fighting games where one player tries to predict the opponent’s actions after a knockdown.

## How to Run

You’ll need `pnpm`, `npm`, `python3`, and Docker installed on your system.

### Frontend (Simulator)

1. Navigate to the `simulator/` directory.
2. Run:
   ```bash
   pnpm i
   pnpm run build
   docker compose up --build -d
```

The server should now be up and running.

### Backend (Markov Service)

1. Navigate to the `markov/service/` directory.
2. Run:
   ```bash
   docker compose up --build -d
   ```

This starts the backend service that handles the Markov Chain logic.

### What Data Is Collected?

Only the Markov states and match results. **Nothing more**.

### Why Does This Exist?

Because we love fighting games and AI.

