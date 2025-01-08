# MoruJournal
Moru Journal is a blogging platform that lets users create, manage, and share their blog posts with ease.

## Setup Instructions
### 1. Clone this repository
```bash
$ git clone https://github.com/sudipX0/MoruJournal.git
$ cd MoruJournal
```
### 2. Create and activate virtual environment
**For Windows**
```bash
$ python -m venv venv
$ .\venv\Scripts\activate
```

**For Linux/macOS**
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
### 3. Install Dependencies
Once virtual environment is activated, install the required dependencies.
```bash
$ pip install -r requirements.txt
```
### 4. Set up the database
Ensure you have a SQLite or other compatible database set up. If you're using SQLite, the application will automatically create the database file.
If using a different database, configure the connection in the `config.py `file.
To initialize the database, run the following command:
```bash
$ flask db upgrade
```
### 5. Run the application
To run the application locally, use the following command:
```bash
$ flask run
```
By default the application will be available at `http://127.0.0.1:5000`
### 6. Visit the application
Open your browser and navigate to:
`https://127.0.0.1:5000`. Alternatively, simply type: `localhost:5000`


