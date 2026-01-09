# Alumni Connect Frontend

Next.js 14 frontend application for the Alumni Connect platform.

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth routes (login, register)
│   ├── students/           # Student routes
│   ├── alumni/             # Alumni routes
│   └── layout.tsx          # Root layout
├── components/             # React components
│   ├── ui/                # Reusable UI components
│   ├── students/          # Student-specific components
│   └── alumni/            # Alumni-specific components
├── lib/                    # Utilities and helpers
│   ├── api.ts             # API client
│   └── utils.ts            # Utility functions
├── hooks/                  # Custom React hooks
├── context/                # React context providers
├── types/                  # TypeScript type definitions
└── public/                 # Static assets
```

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand (client), TanStack Query (server)
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios

## Development

- **Run dev server**: `npm run dev`
- **Build**: `npm run build`
- **Start production**: `npm start`
- **Lint**: `npm run lint`



