# Flask App

A simple and powerful Flask application framework for building web applications.

## Features

- **Simple and Lightweight**: Easy to learn and use
- **RESTful API Support**: Built-in API endpoints
- **Template Rendering**: Jinja2 templates for dynamic content
- **Static File Serving**: CSS, JavaScript, and image support
- **Configuration Management**: Environment-based configuration
- **Security Features**: Session management and security settings

## Quick Start

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Development Mode

```bash
python app.py
```

The application will be available at:
- [http://localhost:5000](http://localhost:5000) - Main application
- [http://localhost:5000/api/data](http://localhost:5000/api/data) - API endpoint

#### Production Mode

```bash
export FLASK_ENV=production
python app.py
```

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   └── about.html        # About page
├── static/               # Static files
│   ├── css/             # Stylesheets
│   │   └── style.css    # Main stylesheet
│   └── js/              # JavaScript files
│       └── app.js        # Main JavaScript
└── README.md             # This file
```

## Configuration

Configuration is managed through environment variables:

- `FLASK_ENV`: Environment (development, production, testing)
- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: Database connection string
- `CORS_ORIGINS`: Allowed CORS origins

## API Endpoints

### GET /api/data
Returns sample API data:

```json
{
  "message": "Hello from Flask API",
  "status": "success",
  "data": {
    "version": "1.0.0",
    "environment": "development"
  }
}
```

## Development

### Adding New Routes

1. Add route to `app.py`
2. Create corresponding template in `templates/`
3. Add static files to `static/` as needed

### Environment Variables

Create a `.env` file for local development:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

## Deployment

For production deployment, consider:

- Using a WSGI server like Gunicorn
- Setting up a reverse proxy with Nginx
- Configuring environment variables securely
- Enabling HTTPS

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For support and questions, please open an issue in the repository.
