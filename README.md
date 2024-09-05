# Python FastAPI Simple Rest API Application

This project is a simple REST API built with FastAPI.

## Project Setup

Follow these steps to set up and run the project:

1. Clone the repository:

   ```
   git clone <repository-url>
   cd fast-api
   ```

2. Create a Python virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Start the application:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`. You can access the following endpoints:

- Home page: `http://localhost:8000/`
- About page: `http://localhost:8000/about`

To view the interactive API documentation, go to `http://localhost:8000/docs`.
