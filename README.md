## Checkin System FastAPIs

### Introduction

The RESTful APIs are referenced from [here](https://github.com/Coli-co/Check_in_system_api/tree/master).

### Usage

##### Prerequisites

- Python
- Docker

##### Steps

1. Clone the repo

```
git clone https://github.com/Coli-co/Check_in_system_FastAPI.git
```

2. Move into the folder

```
cd Check_in_system_FastAPI/
```

3. Create an `.env` file based on `.env.example`. Please remember to fill in the rest values.

```
cat .env.example >> .env
```

5. Choose one of the following to run the application, and then you can send request to `http://localhost:8000` or test apis with [API Doc](http://localhost:8000/docs).

```
chmod +x start.sh && sh start.sh
```

```
chmod +x start.sh && ./start.sh
```

6. Shut down the application.

```
docker compose down
```
