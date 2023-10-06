# Introduction   🖐️
**DamikMamik** - that’s what I called my dating app, but this is not a complete application, it’s only the backend part written in fastapi python. His front-end part is written in Android Java, but since I think it’s complete crap, I don’t know yet whether I’ll publish it or not :). This is a full-fledged API for a dating application. Everything is here! Registration, login, generation of user profiles, chat system and etc.

- **.env_example**: Example configuration file (for usage change to .env).
- **.gitignore**: Git ignore file.
- **alembic.ini**: Database migration configuration.
- **app**: Main application directory.
- **broadcaster**: Customized library (not mine).
- **Dockerfile**: Docker configuration.
- **requirements.txt**: Python package dependencies.


## Technologies Used 🦾

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) library.
- **PostgreSQL**: A powerful, open-source relational database system.
- **asyncpg**: An efficient PostgreSQL database driver for Python.
- **JWT (JSON Web Tokens)**: Used for user authentication.
- **Amazon S3**: Used for storing user profile photos.
- **WebSocket**: Used for real-time chat functionality.
- **Redis Pub/Sub**: Enables real-time chat communication.
-  **And other cool things**
  
## Features 💫

- User registration and authentication.
- Profile matching and recommendation engine.
- History of matching
- Real-time chat functionality with WebSocket and Redis Pub/Sub.
- Integration with Amazon S3 for storing user photos.
- Endpoint for generating user profiles and matching.

## Getting Started 🍉

1. Clone this repository to your local machine.
2. Create a virtual environment using `venv` or `virtualenv`.
3. Install dependencies using `pip install -r requirements.txt`.
4. Set up your environment variables by creating a `.env` file (use `.env_example` as a template).
6. Run database migrations using Alembic: `alembic upgrade head`.
7. Start the FastAPI server: `uvicorn app.main:app --reload`.

## Usage 🐣

- Refer to the API documentation for detailed usage instructions and endpoints.
- Use tools like [Swagger](https://swagger.io/tools/swagger-ui/) or [Postman](https://www.postman.com/) to interact with the API.

## Contributing 🤝

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please create an issue or a pull request.

## License

This project is licensed under the MIT License

## Author 😎

- **Author Amir, contact [Telegram](https://t.me/Popinfu)**
