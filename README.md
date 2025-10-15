# Basketball Analytics Platform

A full-stack web application for analyzing basketball player statistics and performance data. This platform provides comprehensive player analytics through a modern web interface powered by Django REST API and Angular frontend.

## 🏀 Features

- **Player Statistics Dashboard**: View comprehensive player performance metrics
- **Real-time Data Analysis**: Aggregated statistics with ranking calculations
- **Interactive Web Interface**: Modern Angular UI with responsive design
- **Spatial Data Visualization**: Court location tracking for shots, passes, and turnovers
- **RESTful API**: Clean Django REST API for data access
- **Database Export**: Complete PostgreSQL database backup functionality

## 🚀 Live Demo

**Deployed Application**: [https://frontend-production-0934.up.railway.app](https://frontend-production-0934.up.railway.app)

## 🏗️ Architecture

### Backend (Django REST API)
- **Framework**: Django with Django REST Framework
- **Database**: PostgreSQL with normalized schema
- **API Endpoints**: RESTful endpoints for player statistics
- **Data Processing**: Efficient aggregation and ranking algorithms

### Frontend (Angular)
- **Framework**: Angular 12 with Angular Material
- **UI Components**: Modern, responsive design
- **Routing**: Lazy-loaded modules for optimal performance
- **State Management**: Reactive programming with RxJS

### Database Design
- **Normalized Schema**: 5 main entities (Teams, Games, Players, Shots, Passes, Turnovers)
- **Spatial Data**: X,Y coordinates for court location tracking
- **Relationships**: Proper foreign key constraints ensuring data integrity
- **Performance**: Optimized queries with proper indexing

## 📊 Data Overview

The platform processes comprehensive basketball statistics:

- **10 Teams** with player rosters
- **39 Games** with complete event tracking
- **10 Players** with detailed performance metrics
- **192 Shots** with spatial coordinates and outcomes
- **165 Passes** with completion tracking and assist potential
- **14 Turnovers** with location and context data

## 🛠️ Technology Stack

### Backend
- Python 3.13
- Django 4.x
- Django REST Framework
- PostgreSQL
- psycopg2-binary
- gunicorn
- django-cors-headers

### Frontend
- Angular 12
- Angular Material
- TypeScript
- RxJS
- Node.js 16.20.2
- Express.js

### Deployment
- Railway (Backend & Frontend)
- PostgreSQL (Production Database)

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js 16.20.2+
- PostgreSQL
- npm 8.19.4+

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tanishdragonemperor/Basketball-analysis.git
   cd Basketball-analysis/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py load_sample_data
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000

## 📁 Project Structure

```
basketball-analytics/
├── backend/                 # Django REST API
│   ├── app/
│   │   ├── dbmodels/       # Database models
│   │   ├── views/          # API views
│   │   ├── helpers/        # Utility functions
│   │   └── management/     # Django management commands
│   ├── scripts/            # Data loading scripts
│   ├── raw_data/           # JSON data files
│   └── requirements.txt    # Python dependencies
├── frontend/               # Angular application
│   ├── src/app/
│   │   ├── player-summary/ # Player statistics component
│   │   ├── models/         # TypeScript interfaces
│   │   └── _services/      # API services
│   └── package.json        # Node.js dependencies
├── written_responses/      # Documentation
└── README.md              # This file
```

## 🔌 API Endpoints

### Player Summary
- **GET** `/api/v1/playerSummary/{playerID}`
- **Description**: Retrieves comprehensive player statistics with rankings
- **Response**: JSON object with aggregated player data

Example response structure:
```json
{
  "playerID": 1,
  "playerName": "Player Name",
  "teamName": "Team Name",
  "gamesPlayed": 10,
  "totalPoints": 150,
  "totalAssists": 45,
  "totalRebounds": 30,
  "rankings": {
    "points": 3,
    "assists": 1,
    "rebounds": 5
  }
}
```

## 🗄️ Database Schema

### Core Entities
- **Teams**: Team information and rosters
- **Games**: Game dates and context
- **Players**: Player details and team associations

### Event Entities
- **Shots**: Shot attempts with spatial coordinates
- **Passes**: Passing events with completion tracking
- **Turnovers**: Turnover events with location data

All location-based events include X,Y coordinates for spatial analysis and court visualization.

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📈 Performance Features

- **Database Optimization**: Efficient queries with proper indexing
- **Lazy Loading**: Angular modules loaded on demand
- **Caching**: Strategic caching for improved performance
- **Compression**: Gzip compression for API responses

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode setting

### Database Configuration
The application uses PostgreSQL with the following key settings:
- Normalized schema design
- Foreign key constraints
- Spatial data support
- Performance indexing

## 📝 Documentation

Additional documentation is available in the `written_responses/` directory:
- [Database Architecture](written_responses/database_architecture.md)
- [Implementation Summary](written_responses/implementation_summary.md)
- [System Design](written_responses/System%20Design/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of a technical assessment for a software engineering internship position.

## 👨‍💻 Author

**Tanish Gupta**
- Email: guptatanish336@gmail.com
- GitHub: [@tanishdragonemperor](https://github.com/tanishdragonemperor)

## 🙏 Acknowledgments

- Django REST Framework for robust API development
- Angular Material for modern UI components
- Railway for seamless deployment
- PostgreSQL for reliable data storage

---

*This project demonstrates full-stack web development skills with modern frameworks, database design, API development, and deployment practices.*