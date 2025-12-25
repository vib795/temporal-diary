# Temporal Diary 🌌

> *Your ordinary Tuesday existed in a cosmic context. What does your life look like zoomed out?*

A time-shifted journaling application that places your daily reflections within the grand tapestry of cosmic and human history. When you write a journal entry, Temporal Diary shows you what was happening in space, in history, and in your local weather on the same day across different years.

## ✨ Features

- **Cosmic Context**: See NASA's Astronomy Picture of the Day, near-Earth asteroids, and Mars rover photos
- **Historical Events**: Discover what happened on this day throughout history
- **Weather History**: View historical weather data for your location
- **Beautiful UI**: Cosmic-themed interface with smooth animations and starfield backgrounds
- **Auto-save**: Your thoughts are automatically saved as you write
- **Time Travel**: Navigate through dates and see your past entries

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) NASA API key for better rate limits - get one free at https://api.nasa.gov/

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd temporal-diary
```

2. Create your environment file:
```bash
cp .env.example .env
```

3. (Optional) Add your NASA API key to `.env`:
```bash
NASA_API_KEY=your-api-key-here
```

4. Start the application:
```bash
docker-compose up
```

5. Open your browser:
- Frontend: http://localhost:5173
- API Documentation: http://localhost:8000/docs

That's it! The application will automatically:
- Set up PostgreSQL database
- Set up Redis for caching
- Start the FastAPI backend
- Start the SvelteKit frontend

## 🏗️ Architecture

### Backend (FastAPI + Python)

- **Framework**: FastAPI with async/await
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for API response caching
- **Package Manager**: uv (fast Python package manager)

**Key Services**:
- `nasa_service.py`: Fetches space data (APOD, Mars photos, asteroids)
- `history_service.py`: Retrieves historical events from Wikipedia
- `weather_service.py`: Gets historical weather from Open-Meteo
- `context_aggregator.py`: Combines all context sources

### Frontend (SvelteKit + TypeScript)

- **Framework**: SvelteKit with TypeScript
- **Styling**: Tailwind CSS
- **State**: Svelte stores
- **Date Handling**: date-fns

**Key Components**:
- `CosmicBackground.svelte`: Animated starfield background
- `ContextPanel.svelte`: Tabbed interface for space/history/weather
- `EntryEditor.svelte`: Rich text editor with auto-save
- `SpaceContext.svelte`: Displays NASA data
- `HistoryContext.svelte`: Shows historical events

## 📁 Project Structure

```
temporal-diary/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utilities
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # Svelte components
│   │   │   ├── stores/      # State management
│   │   │   ├── services/    # API clients
│   │   │   └── types/       # TypeScript types
│   │   └── routes/          # Pages
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## 🔌 API Endpoints

### Entries
- `GET /api/v1/entries` - List all entries (paginated)
- `GET /api/v1/entries/today` - Get today's entry
- `GET /api/v1/entries/{date}` - Get entry for specific date
- `POST /api/v1/entries` - Create new entry
- `PUT /api/v1/entries/{date}` - Update entry
- `DELETE /api/v1/entries/{date}` - Delete entry

### Context
- `GET /api/v1/context/{date}` - Get full temporal context
- `GET /api/v1/context/{date}/space` - Space context only
- `GET /api/v1/context/{date}/history` - Historical context only
- `GET /api/v1/context/{date}/weather` - Weather context only

## 🌐 External APIs Used

### Free APIs (No Key Required)
- **Wikipedia On This Day**: Historical events, births, deaths
- **Open-Meteo**: Historical weather data (1940-present)
- **Numbers API**: Year facts

### APIs Requiring Key
- **NASA API**: APOD, Mars photos, near-Earth objects
  - Free tier: 1000 requests/hour with `DEMO_KEY`
  - Get personal key: https://api.nasa.gov/ (instant, free, unlimited)

## 🛠️ Development

### Backend Development

```bash
cd backend

# Install uv if you don't have it
pip install uv

# Install dependencies
uv pip install -r pyproject.toml

# Run development server
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📊 Database

The application uses PostgreSQL with the following main tables:

- `users`: User accounts and preferences
- `entries`: Journal entries with metadata
- `context_cache`: Cached API responses

## 🎨 UI/UX Features

- **Cosmic Background**: Animated starfield with nebula effects
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Auto-save**: Entries save automatically every 2 seconds
- **Date Navigation**: Easy navigation between days
- **Context Tabs**: Switch between Space, History, and Weather views
- **Loading States**: Smooth loading animations
- **Word Counter**: Real-time word count

## 🔒 Privacy

- All entries are private by default
- No authentication required in MVP (single-user mode)
- Data stored locally in your PostgreSQL database
- No tracking or analytics

## 📝 Configuration

Edit `.env` to customize:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/temporal_diary

# NASA API
NASA_API_KEY=your-key-here

# Default Location (for weather)
DEFAULT_LATITUDE=30.2672
DEFAULT_LONGITUDE=-97.7431
DEFAULT_LOCATION_NAME=Austin, TX

# Cache TTL
CONTEXT_CACHE_TTL=86400
```

## 🐛 Troubleshooting

### Port already in use
```bash
# Stop running containers
docker-compose down

# Or change ports in docker-compose.yml
```

### Database issues
```bash
# Reset database
docker-compose down -v
docker-compose up
```

### Frontend not loading
```bash
# Rebuild frontend
docker-compose up --build frontend
```

## 🚧 Future Enhancements

- [ ] User authentication and multi-user support
- [ ] AI-generated cosmic perspectives (OpenAI integration)
- [ ] Timeline view of all entries
- [ ] Search and filter entries
- [ ] Export entries as PDF/Markdown
- [ ] Mobile app
- [ ] Dark/Light theme toggle
- [ ] Mood tracking over time
- [ ] Calendar view

## 📜 License

MIT License - feel free to use this for your own journaling!

## 🙏 Acknowledgments

- **NASA** for their incredible APIs
- **Wikipedia** for historical event data
- **Open-Meteo** for free historical weather data
- All the astronomers, historians, and data collectors who make this possible

---

*"Another day in the cosmic journey."*
