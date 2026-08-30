# AI Market Research Crew

A polished, zero-dependency web application that demonstrates an agentic market-research workflow. Users can brief a crew of specialist AI agents, watch a coordinated research run, browse previous reports, manage agents, and export a structured market brief.

![AI Market Research Crew](https://img.shields.io/badge/CrewAI-inspired-15975c?style=flat-square) ![No dependencies](https://img.shields.io/badge/dependencies-none-15211c?style=flat-square)

## Features

- Multi-agent research composer with region and depth controls
- Animated live run with four specialist agents
- Research report library with search and detail views
- Export and clipboard actions
- Agent library with enable/disable controls
- Responsive mobile navigation
- Light and dark themes
- No build step or external JavaScript dependencies

## Run locally

Open `index.html` directly, or serve the directory with any static file server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Project structure

```text
.
├── index.html   # Application markup and views
├── styles.css   # Design system, responsive layout and animation
└── app.js       # App state, interactions and simulated agent workflow
```

## Important

This repository is a front-end product demonstration. Research runs and report findings are simulated and clearly labeled as such. Connect the composer to your preferred agent orchestration backend to turn it into a production research system.

## License

MIT
