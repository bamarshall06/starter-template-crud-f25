#!/usr/bin/env python3
import pymysql
import sys

# Database connection parameters
DB_HOST = 'nnmeqdrilkem9ked.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
DB_USER = 'u5uwi9l6o9vcvsod'
DB_PASSWORD = 'ckrlwgnamuw5bupy'
DB_NAME = 'uh5oeler3o62qpdf'
DB_PORT = 3306

def setup_database():
    try:
        # Connect to MySQL database
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Connected to database successfully")

        with connection.cursor() as cursor:
            # Drop table if exists (for fresh start)
            drop_table_sql = "DROP TABLE IF EXISTS sample_table"
            cursor.execute(drop_table_sql)
            print("Dropped existing table (if any)")

            # Create sample_table
            create_table_sql = """
            CREATE TABLE sample_table (
                sample_table_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                date_of_birth DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_sql)
            print("Created sample_table")

            # Create indexes
            index_name_sql = "CREATE INDEX idx_sample_table_name ON sample_table (last_name, first_name)"
            cursor.execute(index_name_sql)
            print("Created name index")

            index_dob_sql = "CREATE INDEX idx_sample_table_dob ON sample_table (date_of_birth)"
            cursor.execute(index_dob_sql)
            print("Created date of birth index")

            # Insert seed data
            seed_data = [
                ('John', 'Smith', '1990-05-15'),
                ('Jane', 'Doe', '1985-08-22'),
                ('Michael', 'Johnson', '1992-12-03'),
                ('Sarah', 'Williams', '1988-03-17'),
                ('David', 'Brown', '1995-09-08'),
                ('Emily', 'Davis', '1987-11-25'),
                ('Christopher', 'Miller', '1991-07-14'),
                ('Ashley', 'Wilson', '1993-01-30'),
                ('Matthew', 'Moore', '1989-06-12'),
                ('Jessica', 'Taylor', '1994-04-28')
            ]

            insert_sql = """
            INSERT INTO sample_table (first_name, last_name, date_of_birth)
            VALUES (%s, %s, %s)
            """

            cursor.executemany(insert_sql, seed_data)
            print(f"Inserted {len(seed_data)} sample records")

            # Verify data was inserted
            cursor.execute("SELECT COUNT(*) as count FROM sample_table")
            result = cursor.fetchone()
            print(f"Verified: {result['count']} records in sample_table")

            # Show sample data
            cursor.execute("SELECT * FROM sample_table LIMIT 3")
            sample_records = cursor.fetchall()
            print("\nSample records:")
            for record in sample_records:
                print(f"  ID: {record['sample_table_id']}, Name: {record['first_name']} {record['last_name']}, DOB: {record['date_of_birth']}")

        # Commit the changes
        connection.commit()
        print("\nDatabase setup completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()
            print("Database connection closed")

    return True

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)