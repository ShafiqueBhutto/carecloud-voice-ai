# CareCloud Voice AI — Patient Registration System

A voice-based AI patient registration system that allows callers to provide demographic information naturally over the phone. The system validates the information, confirms the collected details, and persists the patient record through a REST API backed by PostgreSQL.

## Features

* 📞 Inbound voice-based patient registration
* 🤖 AI conversational agent using Vapi
* 🗣️ Natural conversational data collection
* ✅ Input validation and re-prompting for invalid information
* 🔄 Ability to handle corrections during the conversation
* 📋 Confirmation of collected information before saving
* 🗄️ PostgreSQL database persistence using Neon
* 🔐 Duplicate patient detection using phone number
* 🌐 REST API built with FastAPI
* 🔎 Patient search by last name, date of birth, or phone number
* ✏️ Partial patient updates
* 🗑️ Soft-delete functionality
* 📚 Interactive Swagger/OpenAPI documentation
* 🌍 Public API access through ngrok

---

## Architecture

```text
                    ┌─────────────────────┐
                    │      Phone Call     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Vapi Voice AI    │
                    │  CareCloud Agent    │
                    └──────────┬──────────┘
                               │
                       Patient confirmed
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI REST API  │
                    │      /patients      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      SQLAlchemy     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Neon PostgreSQL DB │
                    └─────────────────────┘
```

---

## Technology Stack

### Voice AI

* Vapi
* Conversational AI / LLM
* Phone-based inbound calling

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* PostgreSQL
* Neon
* SQLAlchemy ORM

### Development & Deployment

* Git
* GitHub
* ngrok
* Swagger / OpenAPI

---

## Patient Information

### Required Fields

* First name
* Last name
* Date of birth
* Sex
* 10-digit U.S. phone number
* Address
* City
* State
* ZIP code

### Optional Fields

* Email
* Address line 2
* Insurance provider
* Insurance member ID
* Preferred language
* Emergency contact name
* Emergency contact phone

The API also maintains:

* Patient UUID
* Created timestamp
* Updated timestamp
* Deleted timestamp

---

## REST API

Base URL:

```text
https://scallop-lukewarm-washhouse.ngrok-free.dev
```

### Health Check

```http
GET /health
```

Returns the current API health status.

### List Patients

```http
GET /patients/
```

Optional filters:

```text
last_name
date_of_birth
phone_number
```

Example:

```http
GET /patients/?last_name=Smith
```

### Get Patient

```http
GET /patients/{patient_id}
```

### Create Patient

```http
POST /patients/
```

Creates a new patient after validation.

The API prevents duplicate active patients using the same phone number.

### Update Patient

```http
PUT /patients/{patient_id}
```

Supports partial updates of patient information.

### Delete Patient

```http
DELETE /patients/{patient_id}
```

The endpoint performs a **soft delete** by setting `deleted_at` rather than physically removing the database record.

---

## API Response Format

Successful responses follow a consistent structure:

```json
{
  "data": {},
  "error": null
}
```

List responses:

```json
{
  "data": [],
  "error": null
}
```

---

## Validation

The system validates patient information before persistence.

Examples include:

* Required fields cannot be empty
* Phone numbers must contain a valid 10-digit U.S. phone number
* ZIP codes must contain 5 digits
* Sex must use an accepted value
* Date of birth must be a valid date
* Duplicate active phone numbers are rejected
* Invalid voice input results in a conversational re-prompt

---

## Voice Agent Flow

The CareCloud voice agent follows this general flow:

```text
Incoming Call
     ↓
Greeting
     ↓
Collect Patient Information
     ↓
Validate Information
     ↓
Re-prompt Invalid Information
     ↓
Offer Optional Information
     ↓
Review Complete Information
     ↓
Ask for Confirmation
     ↓
Save Confirmed Patient
     ↓
Confirm Successful Registration
     ↓
End Call
```

The patient information is only intended to be persisted after the caller confirms the collected information.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShafiqueBhutto/carecloud-voice-ai.git
cd carecloud-voice-ai
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
```

Do not commit `.env` or database credentials to GitHub.

### 5. Start the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Public Access with ngrok

For demonstration, the local FastAPI service can be exposed using ngrok:

```bash
ngrok http 8000
```

This provides a public HTTPS URL that can be used by the Vapi voice agent.

Example:

```text
https://your-ngrok-domain.ngrok-free.dev
```

### Important

The free ngrok URL may change when a new tunnel is started. Therefore, the Vapi server/tool configuration may need to be updated with the new public URL after restarting ngrok.

---

## Database Persistence

The application uses PostgreSQL through Neon.

Patient records persist independently of the FastAPI process, so restarting the application does not remove registered patients.

The database schema includes timestamps and a `deleted_at` field for soft deletion.

---

## Testing

The API was tested through the automatically generated Swagger/OpenAPI interface.

Tested functionality includes:

* Health check
* Patient creation
* Duplicate phone validation
* Patient listing
* Patient filtering
* Patient retrieval by ID
* Patient updates
* Soft deletion
* PostgreSQL persistence

The voice agent was also tested through an inbound phone call with dummy patient information.

---

## Security & Privacy

This project is a technical demonstration.

**Do not enter or store real patient/medical information.**

Use fictional/dummy patient information when testing or demonstrating the application.

Database credentials and other secrets must be stored in environment variables and must not be committed to source control.

---

## Limitations / Trade-offs

### ngrok

The demonstration uses ngrok to expose the locally running API. This avoids requiring paid cloud hosting during development but means the public URL is temporary.

### Voice Call Costs

Vapi/telephony usage may incur costs depending on the configured provider and account balance.

### Production Deployment

For a production healthcare environment, additional infrastructure and security controls would be required, including appropriate authentication, authorization, encryption, auditing, monitoring, and compliance considerations.

This project is intended as a technical assessment/demo and is not a production healthcare system.

---

## Project Structure

```text
carecloud-voice-ai/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routes.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Demo Information

### Voice Agent

**CareCloud Receptionist**

The voice agent is configured as an inbound patient registration assistant.

### API

```text
https://scallop-lukewarm-washhouse.ngrok-free.dev
```

### API Documentation

```text
https://scallop-lukewarm-washhouse.ngrok-free.dev/docs
```

### Source Code

```text
https://github.com/ShafiqueBhutto/carecloud-voice-ai
```

---

## Disclaimer

This application was developed as a technical assessment project demonstrating conversational AI, telephony integration, REST API development, validation, and persistent database storage.

No real patient data should be used with this demonstration.
