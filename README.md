# whatsapp

Code for a whatsapp chat

## Run Locally (Windows)

Clone the project

```bash
  git clone https://github.com/webmasterfacinnova/whatsapp.git
```

Go to the project directory

```bash
  cd whatsapp
```

create a virtual environment

```bash
python -m venv venv
```

activate the virtual environment

```bash
 venv\Scripts\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the developer server

```bash
  uvicorn main:app --reload
```

for production server use

```bash
    fastapi run
```

to generate or update requirements.txt run

```bash
    pip freeze > requirements.txt
```

## Documentation

[FastApi](https://fastapi.tiangolo.com)
