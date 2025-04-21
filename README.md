How to startup

Notebooks:
Create python virtual environment
Select venv kernel in Jupyter Notebook files
Run each cell one by one

Python virtual environment steps:
```bash
python3 -m venv venv
source venv/bin/activate OR source venv/Scripts/activate
pip install -r requirements.txt
```
Doing this will download all dependencies in /notebook

Backend:
Create python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate OR source venv/Scripts/activate
pip install -r requirements.txt
```
Do this and then you can run uvicorn main:app --reload
http://localhost:8000/api/colourise-image to test endpoint


Frontend:
In /frontend install dependencies
```bash
npm install
npm run dev
```
You can then click on the link in the terminal


Make sure both frontend and backend are running on two separate terminals for it to work correctly