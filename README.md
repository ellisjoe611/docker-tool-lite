# docker-tool-lite
* Docker viewer &amp; manager tool based on FastAPI (Python)

## Environement
* Python 3.9.7
* Docker (IMPORTANT: Make sure that Docker service is installed and running on background)


## Hot to run?
1. Clone this repository.
```
git clone https://github.com/ellisjoe611/docker-tool-lite.git
```

2. Create virtual environment and activate it (You may change its name, but you should add its name on <strong>.gitignore</strong>)
```
python -m venv venv_docker
source venv_docker/Scripts/activate
```
3. Install all required libraries from <strong>requirements.txt</strong>
```
pip install -r requirements.txt
```
4. Run the Server
```
python -m uvicorn main:app --host 127.0.0.1 --port 5000 
```