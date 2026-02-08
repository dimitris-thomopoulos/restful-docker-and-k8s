# Copilot Instructions: Student Service REST API

## Architecture Overview

This is a **Connexion/Flask REST API server** backed by **MongoDB**, auto-generated from OpenAPI (Swagger) specification. The service manages student records with grade information.

**Key layers:**
- **API Layer**: `swagger_server/controllers/default_controller.py` - Entry points mapping OpenAPI operationIds
- **Business Logic**: `swagger_server/service/student_service.py` - MongoDB operations (CRUD)
- **Models**: `swagger_server/models/` - Auto-generated data classes with `to_dict()` and `from_dict()` conversions
- **API Definition**: `swagger_server/swagger/swagger.yaml` - OpenAPI 3.0 spec driving request routing

## Critical Developer Workflows

### Running the Server
```bash
pip3 install -r requirements.txt
python3 -m swagger_server        # Starts on http://localhost:8080
```

### Running Tests
```bash
pip install tox
tox                              # Uses nose test runner per tox.ini
```

### Docker Deployment
```bash
docker build -t student_service .
docker run -p 8080:8080 student_service
```
**With MongoDB** (docker-compose):
```bash
docker-compose up                # Brings up student_service + MongoDB
```

## Project-Specific Patterns

### Controller-to-Service Flow
Controllers import entire service module (`from swagger_server.service.student_service import *`) and call service functions directly. Controllers handle:
- JSON request parsing via `connexion.request.get_json()`
- Model instantiation (`Student.from_dict(...)`)
- HTTP status code responses as tuples: `return value, 200` or `return error_msg, 409`

**Example** ([controllers/default_controller.py](swagger_server/controllers/default_controller.py#L5)):
```python
def add_student(body=None):
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())
        return add(body)
    return 500, 'error'
```

### MongoDB ID Generation
IDs are auto-incremented integers (not MongoDB ObjectIds). Service finds max `_id`, increments by 1 ([student_service.py#L18-L23](swagger_server/service/student_service.py#L18-L23)):
```python
cursor = student_collection.find({}).sort("_id", -1).limit(1)
next_id = 1
for d in cursor:
    next_id = d["_id"] + 1
```

### Duplicate Detection
Students are identified by `first_name + last_name` combination; insertions fail with 409 if duplicate exists.

### Configuration from Environment
MongoDB connection details via env vars ([config.py](swagger_server/config.py)):
- `MONGO_URI`: defaults to `mongodb://localhost:27017`
- `MONGO_DB_NAME`: defaults to `student_db`
Docker-compose sets these automatically.

## API Endpoints (Connexion-routed)

| Method | Path | Operation | Handler |
|--------|------|-----------|---------|
| POST | `/student` | `add_student` | Create student |
| GET | `/student/{student_id}` | `get_student_by_id` | Fetch single student |
| DELETE | `/student/{student_id}` | `delete_student` | Remove student |
| UI | `/ui/` | Swagger UI | Interactive API docs |

Routes defined in [swagger.yaml](swagger_server/swagger/swagger.yaml) with `x-openapi-router-controller` pointing to `default_controller`.

## Key Dependencies

- **Connexion < 3.0.0**: Maps OpenAPI to Flask handlers
- **Flask ~2.2.2**: Underlying web framework
- **PyMongo >= 4.0.0**: MongoDB driver
- **swagger-ui-bundle**: Auto-generated API docs at `/uva-302/tutorial/1.0.0/ui/`

## Model Serialization

Auto-generated models inherit from `base_model_.Model` with:
- `to_dict()`: Converts model to dictionary for MongoDB/responses
- `from_dict()`: Reconstructs model from JSON (validates types)
- `swagger_types` and `attribute_map`: Metadata for field conversion

## Testing Notes

Tests use **nosetests** (see [tox.ini](tox.ini)). Place test files following convention in [swagger_server/test/](swagger_server/test/).

## DevOps Context

- **Docker image**: Multi-stage build unnecessary (Alpine + Python 3.8 is minimal)
- **Exposed port**: 8080 (defined in [Dockerfile](Dockerfile) and app startup)
- **Database**: External MongoDB (see [docker-compose.yaml](docker-compose.yaml) - separate `mongo:4` service)
- **Image registry**: Configured for `dimitristho/student_service` (pushable to Docker Hub)

**Persistence note:** By default the project `docker-compose.yaml` may not have included a volume for MongoDB, which means data will be lost if the MongoDB container is removed. Ensure `docker-compose.yaml` mounts a persistent volume to `/data/db` for the `mongo` service. Example (already applied here):

```
    mongo:
        image: mongo:4
        ports:
            - "27017:27017"
        volumes:
            - mongo-data:/data/db

volumes:
    mongo-data:
```

When this volume is present, data survives `docker-compose down` / `up` and container recreation.
