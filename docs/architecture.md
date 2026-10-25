# Architecture

The Flask application separates HTTP routes, SQLAlchemy models, validation/import services, and analytics calculations. SQLite makes the project runnable after cloning; setting `DATABASE_URL` switches the application to SQL Server. The browser calls REST-style endpoints and renders real data with Chart.js.
