# Chronic Care Planner

A React application built with Vite for managing and planning chronic care patient information.

## Features

- Fast development environment with Vite and Hot Module Replacement (HMR)
- React 19 for building interactive UI components
- Tailwind CSS for utility-first styling
- Lucide React icons for consistent, customizable icons
- ESLint configuration for code quality

## Tech Stack

- **Frontend Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Linting**: ESLint

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

Create a new Vite React project:

```bash
npm create vite@latest chronic-care-planner -- --template react
cd chronic-care-planner
npm install
```

Install additional dependencies:

```bash
npm install lucide-react@latest --legacy-peer-deps
npm install tailwindcss @tailwindcss/vite
```

### Development

Start the development server with hot reload:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Create a production build:

```bash
npm run build
```

### Preview

Preview the production build locally:

```bash
npm run preview
```

### Linting

Run ESLint to check code quality:

```bash
npm run lint
```

## Project Structure

```
chronic-care-planner/
├── src/
│   ├── App.jsx           # Main App component
│   ├── App.css           # App styles
│   ├── main.jsx          # Application entry point
│   ├── index.css         # Global styles
│   └── assets/           # Static assets
├── public/               # Public assets
├── package.json          # Project dependencies and scripts
├── vite.config.js        # Vite configuration
├── eslint.config.js      # ESLint rules
└── index.html            # HTML entry point
```

## Development Notes

- The project uses React's fast refresh feature for instant updates during development
- Tailwind CSS provides responsive, utility-first styling
- ESLint is configured to help maintain code quality and best practices
