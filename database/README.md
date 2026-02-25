# Database Setup

This directory contains the database structure and sample data for the Flask starter kit.

## Files

- `schema.sql` - Database table definitions and structure
- `seed_data.sql` - Sample data for testing and development

## Setup Instructions

### 1. Prerequisites
- MySQL server installed and running
- Database created (you can name it anything)
- Database credentials configured in your `.env` file

### 2. Create Database Structure
Run the schema file to create the required tables:

```bash
mysql -h [host] -u [username] -p [database_name] < database/schema.sql
```

Or using your database management tool, execute the contents of `schema.sql`.

### 3. Load Sample Data (Optional)
To populate the database with sample records for testing:

```bash
mysql -h [host] -u [username] -p [database_name] < database/seed_data.sql
```

## Database Structure

### sample_table
- `sample_table_id` (INT, Primary Key, Auto Increment)
- `first_name` (VARCHAR(50), NOT NULL)
- `last_name` (VARCHAR(50), NOT NULL) 
- `date_of_birth` (DATE, NOT NULL)
- `created_at` (TIMESTAMP, Default: Current timestamp)
- `updated_at` (TIMESTAMP, Auto-update on modification)

## Notes

- The schema includes helpful indexes for common query patterns
- Timestamps are automatically managed by MySQL
- Sample data includes 10 test records with realistic names and dates

## Connection Options

This starter kit supports two ways to connect to MySQL:

### Option 1: JAWS DB URL (Heroku Production)

When you add the JAWS DB add-on to your Heroku app, it automatically sets the `JAWSDB_URL` config var. The app detects this and uses it automatically.

```bash
# Heroku sets this automatically when you provision JAWS DB
heroku addons:create jawsdb:kitefin
```

The connection string format is:
```
mysql://username:password@host:port/database
```

### Option 2: Separate Variables (Local Development)

For local development, use separate environment variables in your `.env` file:

```
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

### Priority

If both `JAWSDB_URL` and the separate variables are set, `JAWSDB_URL` takes priority.