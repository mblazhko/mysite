# PollWorld

This is a Django web app with an API implemented using Django Rest Framework(DRF).

## Functionality

- Creation, editing, and deletion of polls.
- Adding questions to polls.
- Adding answer choices to questions.
- Ability to answer questions and view poll results.

## Endpoints

### Polls

- **GET /polls/** - View a list of all polls.
- **GET /polls/{slug}/** - View a specific poll by its unique slug.
- **POST /polls/create-poll/** - Create a new poll.
- **DELETE /polls/{slug}/delete-poll** - Delete an existing poll.
- **GET /user/profile/** - View a user profile with settings and actions with user's polls

## API Documentation

API documentation can be found in the **/api/schema/doc/**.

## Django Project

This project is built using Django, a high-level web framework for Python. It follows the Model-View-Template (MVT) architectural pattern.

## Environment Variables

To customize the behavior of the project, you can set the following environment variables:

- `DJANGO_DEBUG`: Set to `True` for development mode.
- `DJANGO_SECRET_KEY`: Django secret key for cryptographic operations.
- `ALLOWED_HOSTS`: Hosts, as default you can set "127.0.0.1 localhost"
- `EMAIL_HOST_USER`: E-mail host for sending email, in the project we use Google
- `EMAIL_HOST_PASSWORD`: App password from a Google account
- `REDIS_CACHE_LOCATION`: Path to Redis cache location
- `DB_NAME`: Database name.
- `DB_USER`: Database username.
- `DB_PASSWORD`: Database password.
- `DB_HOST`: Database host.
- `DB_PORT`: Database port.

If you want to use some third party providers provide variables below:
1. For GitHub login:
   - `GITHUB_CLIENT`: GITHUB_CLIENT
   - `GITHUB_SECRET`: GITHUB_SECRET
2. For Google:
   - `GOOGLE_CLIENT`: GOOGLE_CLIENT
   - `GOOGLE_SECRET`: GOOGLE_SECRET
3. For Facebook:
   - `FACEBOOK_CLIENT`: FACEBOOK_CLIENT
   - `FACEBOOK_SECRET`: FACEBOOK_SECRET


## Usage

- To start the project, make sure you have Docker installed, and then run the following command:

   ```docker-compose up```

- Go to `localhost:8000`

- If you want to have a lot of default data, you have to:
  1. Get container id: `docker ps`
  2. Go to the `mysite-web` container:
     `docker exec -it <container_id> bash`

  3. Run the following command:
     `python manage.py generate_data`
  4. Then you can use those credentials to log in:
     - Email: `admin@admin.com`
     - Password: `V!5WucFeReMQ7fg`

- If you want to have a superuser only, run the command below inside the docker container:
    `python manage.py make_superuser`

  Note: This command creates a large amount of data and takes some time to populate the database. Please be patient.
    

