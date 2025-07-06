# ScoutLens aka ProjView aka Scoutview
An app to be...

# Developer instructions
The app consists of two parts. A backend written in Python and a frontend written in React. The frontend is however not written yet...

## Python setup
The requirements.txt file is in the pyapp directory. Use that to set up an virtual environment. The backend is tested with Python 3.12, but any version from 3.8 and higher will probably work.

The app is the run with
```bash
uvicorn "app.main:app" --host 0.0.0.0 --port 8000
```

or, if using VSCode:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000"
            ],
            "cwd": "${workspaceFolder}/pyapp",
            "jinja": true,
            "env": {
                "AUTH_DISABLED": "true",
                "PYTHONDEVMODE": "1"
            },
            "justMyCode": true
        }
    ]
}
```

The backend will respond to
```bash
curl localhost:8000
```
and a Swagger UI is available at http://localhost:8000/docs.

A special environment variable AUTH_DISABLED can be set to "true" to disable the authentication requirements, which is useful when testing the API's with Swagger. The authentication will still work as normal when provided by the client.
This variable MUST NOT be set in production.


## React setup
The client is based on Vite.
Install the required packages with
```bash
npm install
```

and then start the development environment with
```bash
npm run dev
```

All the configuration for running the client in development are included. The file vite.config.js contains the directive to proxy all API-calls to a running instance of the backend.

## Environment variables
The following environment variables used for authentication needs to be set for the backend:

| Name                     | Description                                                                |
| ------------------------ | ---------------------------------------------------------------------------|
| `keycloak_url`           | The URL for the Keycloak server handling the authentication.               |
| `keycloak_realm`         | The realm used in the Keycloak server.                                     |
| `keycloak_client_id`     | The client id for this client.                                             |

The environment variables can be stored in an ".env" file located in pyapp directory, where it will picked up be the server during development. When running as a container they need to be provided as environment variables.

When the app is running in a container, these variables will be injected into the "index.html" file, where it can be picked up by the client.

If running in development, for the client to be able to use them, they need to be stored in an ".env" file in the client directory. And they need to be prefixed with "VITE_", e.g. they are named VITE_KEYCLOAK_URL, VITE_KEYCLOAK_REALM and VITE_KEYCLOAK_CLIENT_ID respectively.

The following environment variables are specific for the python application:

| Name                        | Description                                                                | Default value             |
| ----------------------------| ---------------------------------------------------------------------------|---------------------------|
| `app_name`                  | The name of the app.                                                       | ScoutView                 |
| `scoutnet_base`             | The base URL for the ScoutNet API.                                         | https://scoutnet.se/api   |
| `scoutnet_activity_id`      | The ID of the activity.                                                    |                           |
| `scoutnet_participants_key` | The key for the participants API.                                          |                           |
| `scoutnet_questions_key`    | The key for the questions API.                                             |                           |
| `scoutnet_checkin_key`      | The key for the checkin API.                                               |                           |
| `scoutview_debug_email`     |                                                                            |                           |
| `scoutview_roles`           |                                                                            |                           |


The same rules as above as where to store them, applies to these variables.

# Buildning the app
The app is built with Docker using the supplied Dockerfile. The build process will combine the backend and the frontend into a single container. The Python backend will serve the client with all necessary files.

