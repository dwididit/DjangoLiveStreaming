# Live Streaming Application with Django and Vue.js

This project is a live streaming application developed using Django and Django Channels for WebSocket support. The application allows users to stream live video while viewers can watch and donate using multiple payment options, including integration with a payment gateway like Midtrans.

## Features
### User Authentication
- User registration and login with input validation. 
- Token-based authentication mechanism (e.g., JSON Web Tokens).

### Live Streaming
- Authenticated users can start live streaming sessions.
- Real-time video streaming display to viewers.
- Viewers can comment during streaming. 

### Donation with Payment Options
- Viewers can donate to streamers during the stream.
- The application provides multiple payment options:

**Option 1: Payment Gateway Integration (Midtrans)**
- Donations are processed online via a payment gateway.
- Handling of successful and failed transactions.
- Recommended as the primary option.

**Option 2: Manual Payment Method**
- Display manual payment information (Bank Transfer).
- Viewers make manual transfers.

**Donation Confirmation**
- Streamer must manually confirm receipt of donations.

**Donation Notifications**
- Real-time donation notifications on the streaming display, for both payment gateway and manual donations.
- Donation history saved for streamers and viewers.

**Error Handling**
- Handle errors gracefully with custom exception handling.
- Return data in a structured JSON format.

## Technology Stack
- Backend: Django, Django Channels (for WebSocket)
- Frontend: Vue.js
- Database: PostgreSQL
- Payment Gateway: Midtrans
- Message Broker: Redis

## Redis Integration
- Redis as a Message Broker: Used to send real-time notification messages between the backend and frontend via WebSocket (Django Channels).
  - Donation and new comment notifications are sent through the message broker to ensure reliable delivery and scalability.


- Redis as a Task Queue: Used to run background tasks.
  - Processing donations through the payment gateway (Midtrans).
  - Sending email notifications for donations.
  - Other tasks that require more time or do not need to be executed immediately.


### API Endpoints Documentation:
Using Swagger

### WebSocket Notifications:
- `/ws/stream/:stream_id/` : WebSocket endpoint for real-time updates during the streaming session, including donation and new comment notifications.


## UML Diagrams

### 1. Use Case Diagram

```plaintext
[User] --> (Register)
[User] --> (Login)
[Streamer] --> (Start Streaming)
[Viewer] --> (View Stream)
[Viewer] --> (Comment)
[Viewer] --> (Donate)
[Streamer] --> (Confirm Donation)
```

### 2. Class Diagram
```plaintext
+-------------------+
|       User        |
+-------------------+
| - username        |
| - password        |
| - is_streamer     |
+-------------------+
| + register()      |
| + login()         |
+-------------------+

          ^
          |
          |
          |
+-------------------+              +-------------------+
|     Stream        |<>------------|     Donation      |
+-------------------+              +-------------------+
| - title           |              | - amount          |
| - description     |              | - message         |
| - is_active       |              | - payment_method  |
| - streamer        |              | - status          |
| + startStream()   |              | - transaction_id  |
| + stopStream()    |              +-------------------+
+-------------------+              | + donate()        |
+-------------------+
^
|
|
|
+-------------------+
|     Comment       |
+-------------------+
| - content         |
| - user            |
| - stream          |
| + addComment()    |
+-------------------+
```

### 3. Sequence Diagram
```plaintext
+----------------+     +-----------------+      +----------------+
|     Viewer     |     |     Server      |      |     Streamer   |
+----------------+     +-----------------+      +----------------+
|                     |                        |
|  Login              |                        |
|-------------------->|                        |
|                     |                        |
|                     |                        |
|<--------------------|                        |
|                     |                        |
|  View Stream        |                        |
|-------------------->|                        |
|                     |                        |
|                     |                        |
|<--------------------|                        |
|                     |                        |
|  Comment            |                        |
|-------------------->|                        |
|                     |  Notify                |
|                     |----------------------->|
|                     |                        |
|                     |                        |
|                     |<-----------------------|
|                     |                        |
|  Donate             |                        |
|-------------------->|                        |
|                     |  Notify                |
|                     |----------------------->|
|                     |                        |
|                     |                        |
|                     |<-----------------------|
|                     |                        |
```


## Database Tables Description

#### User Table
| Column         | Type       | Attributes                  |
|----------------|------------|-----------------------------|
| id             | INTEGER    | PRIMARY KEY, AUTO INCREMENT |
| username       | VARCHAR    | UNIQUE, NOT NULL            |
| password       | VARCHAR    | NOT NULL                    |
| email          | VARCHAR    | UNIQUE, NOT NULL            |
| first_name     | VARCHAR    |                             |
| last_name      | VARCHAR    |                             |
| is_active      | BOOLEAN    | DEFAULT TRUE                |
| is_staff       | BOOLEAN    | DEFAULT FALSE               |
| is_superuser   | BOOLEAN    | DEFAULT FALSE               |
| last_login     | DATETIME   |                             |
| date_joined    | DATETIME   |                             |
| is_streamer    | BOOLEAN    | DEFAULT FALSE               |

#### Stream Table
| Column      | Type     | Attributes                           |
|-------------|----------|--------------------------------------|
| id          | INTEGER  | PRIMARY KEY, AUTO INCREMENT          |
| title       | VARCHAR  | NOT NULL                             |
| description | TEXT     |                                      |
| streamer_id | INTEGER  | FOREIGN KEY (User), NOT NULL         |
| is_active   | BOOLEAN  | DEFAULT FALSE                        |
| created_at  | DATETIME | AUTO NOW ADD                         |
| updated_at  | DATETIME | AUTO NOW                             |

#### Donation Table
| Column         | Type       | Attributes                           |
|----------------|------------|--------------------------------------|
| id             | INTEGER    | PRIMARY KEY, AUTO INCREMENT          |
| amount         | DECIMAL    | MAX DIGITS 10, DECIMAL PLACES 2, NOT NULL |
| message        | TEXT       |                                      |
| stream_id      | INTEGER    | FOREIGN KEY (Stream), NOT NULL       |
| donor_id       | INTEGER    | FOREIGN KEY (User), NOT NULL         |
| payment_method | VARCHAR    | MAX LENGTH 50                        |
| status         | VARCHAR    | MAX LENGTH 50, DEFAULT 'pending'     |
| transaction_id | UUID       | UNIQUE, DEFAULT UUID, NOT NULL       |
| created_at     | DATETIME   | AUTO NOW ADD                         |
| updated_at     | DATETIME   | AUTO NOW                             |

#### Comment Table
| Column      | Type     | Attributes                           |
|-------------|----------|--------------------------------------|
| id          | INTEGER  | PRIMARY KEY, AUTO INCREMENT          |
| content     | TEXT     | NOT NULL                             |
| user_id     | INTEGER  | FOREIGN KEY (User), NOT NULL         |
| stream_id   | INTEGER  | FOREIGN KEY (Stream), NOT NULL       |
| created_at  | DATETIME | AUTO NOW ADD                         |
| updated_at  | DATETIME | AUTO NOW                             |



## Entity-Relationship Diagram (ERD)

### User
- **id**: Integer, Primary Key, Auto Increment
- **username**: String, Unique
- **password**: String
- **email**: String, Unique
- **is_streamer**: Boolean, Default False
- **first_name**: String
- **last_name**: String
- **date_joined**: DateTime
- **last_login**: DateTime

### Stream
- **id**: Integer, Primary Key, Auto Increment
- **title**: String, Max Length 255
- **description**: Text
- **streamer_id**: Integer, Foreign Key (User)
- **is_active**: Boolean, Default False
- **created_at**: DateTime, Auto Add
- **updated_at**: DateTime, Auto Now

### Donation
- **id**: Integer, Primary Key, Auto Increment
- **amount**: Decimal, Max Digits 10, Decimal Places 2
- **message**: Text, Blank True
- **stream_id**: Integer, Foreign Key (Stream)
- **donor_id**: Integer, Foreign Key (User)
- **payment_method**: String, Max Length 50
- **status**: String, Max Length 50, Default 'pending'
- **transaction_id**: UUID, Unique, Default uuid4
- **created_at**: DateTime, Auto Add
- **updated_at**: DateTime, Auto Now

### Comment
- **id**: Integer, Primary Key, Auto Increment
- **content**: Text
- **user_id**: Integer, Foreign Key (User)
- **stream_id**: Integer, Foreign Key (Stream)
- **created_at**: DateTime, Auto Add
- **updated_at**: DateTime, Auto Now

### Relationships
- A **User** can have multiple **Streams** (One-to-Many)
- A **User** can make multiple **Donations** (One-to-Many)
- A **User** can post multiple **Comments** (One-to-Many)
- A **Stream** can have multiple **Donations** (One-to-Many)
- A **Stream** can have multiple **Comments** (One-to-Many)

Below is a visual representation of the ERD:

```plaintext
User
|-- id (PK)
|-- username
|-- password
|-- email
|-- is_streamer
|-- first_name
|-- last_name
|-- date_joined
|-- last_login

Stream
|-- id (PK)
|-- title
|-- description
|-- streamer_id (FK to User)
|-- is_active
|-- created_at
|-- updated_at

Donation
|-- id (PK)
|-- amount
|-- message
|-- stream_id (FK to Stream)
|-- donor_id (FK to User)
|-- payment_method
|-- status
|-- transaction_id
|-- created_at
|-- updated_at

Comment
|-- id (PK)
|-- content
|-- user_id (FK to User)
|-- stream_id (FK to Stream)
|-- created_at
|-- updated_at
```


## Getting Started
1. Clone the repository:
```bash
gh repo clone dwididit/DjangoLiveStreaming
cd DjangoLiveStreaming/
```

2. Create `.env` file.
```bash
# Database configuration
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
SQL_HOST=db
SQL_PORT=5432

# Redis configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Celery configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email configuration
EMAIL_HOST=smtp-host.com
EMAIL_PORT=587
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
MAIL_FROM_EMAIL=sender@example.com
MAIL_FROM_NAME=Live Streaming App By Dwi Didit Prasetiyo


# CORS configuration
CORS_ALLOWED_ORIGINS=http://localhost:8081
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True

# Frontend configuration
VUE_APP_BACKEND_URL=http://127.0.0.1:8000/api
```

4. Build and run with Docker Compose
```bash
docker-compose up --build
```

3. Generate dummy data
```bash
docker-compose run web python manage.py generate_dummy_data
```

4. Verify the Superuser and Data in Django Admin:
- Access the Django admin interface at http://127.0.0.1:8000/admin/
- Log in using the superuser credentials:
  - Username: admin 
  - Password: admin
- Verify that the dummy data for User, Stream, Donations, and Comment has been generated correctly.