
---

# ArticlesDB API

This is a Django REST framework-based API for managing articles, comments, and tags. Follow the instructions below to set up the project, add sample data, and run the API.

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Adding Sample Data](#adding-sample-data)
3. [Running the API](#running-the-api)
4. [Filtering](#filtering)
4. [Export CSV](#export-csv)
5. [Important Notes](#notes)

---

## Project Setup

### Prerequisites

1. **Python 3.x** installed on your system.
2. **PostgreSQL** installed and running.
3. **Virtualenv** (optional).

### Steps to Set Up the Project

1. Clone the repository:

    ```bash
    git clone https://github.com/tryfkalt/articlesDB.git
    cd articlesDB
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv venv # or python -m venv venv
    source venv/bin/activate  
    # I personally used Linux 
    # For Windows use: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up PostgreSQL:

    - Create a database in PostgreSQL (can be done through the pgAdmin4 DBMS as well):

    On Linux, open a Terminal and run the commands:

        ```bash
        sudo -i -u postgres
        psql -U postgres
        CREATE DATABASE articlesdb;
        CREATE USER postgres WITH PASSWORD 'postgres';
        GRANT ALL PRIVILEGES ON DATABASE articlesdb TO postgres;
        ```
5. In your settings.py file you should have be matching database configurations (typically should be stored in an .env file but for now you can use these):
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'articlesdb',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            # 'PORT': '5432',
        }
    }
    ```
6. Apply the migrations to set up the database schema:

    ```bash
    python manage.py migrate
    ```
7. **Note**: For easy data management and representation i used pgAdmin4 as my DBMS. 

---

## Adding Sample Data

There are two ways to add sample data to the database:

### 1. Via Django Admin Panel

1. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```

2. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

3. Visit `http://127.0.0.1:8000/admin/` and log in using the superuser credentials.

4. Add articles, tags, and comments through the Django Admin interface.

### 2. Using Django Rest Framework (DRF) 

1. **Create a superuser**:

    ```bash
    python manage.py createsuperuser
    ```
After creating the superuser, login at:
    ```
    http://127.0.0.1:8000/admin/login/?next=/admin/login``` to be able to perform actions to the api. 

2. Start the server using the command:

    ```bash
    python manage.py runserver
    ```

3. The API will be available at `http://127.0.0.1:8000/`.

4. The following endpoints are available:
   - `/api/articles/` – View, create, and manage articles.
   - `/api/tags/` – Manage tags.
   - `/api/comments/` – Manage comments.
   - `/api/articles/export_csv/` – Export articles as a CSV file.

5. To create a Tag you can access the endpoint:
`http://127.0.0.1:8000/api/tags/` , where you can POST a new tag through Raw data input or in HTML form, providing the name (e.g "Cooking"). After POST, the Tag will obtain a unique id.
6. To create a new article you can access the endpoint:
`http://127.0.0.1:8000/api/articles/`, where you can create an article providing either Raw data (JSON input) or filling the fields in HTML form.

**Important Note**: The backend is designed to have separated entities for Article, Tag, Comment and Author (User entity), so in order to successfully add the Authors and Tags fields, an author and a tag instance must already be created in advance. A new user can only be registered through the admin panel (**when creating user in the admin panel make sure you give theme superuser and staff status perimissions in order to be able to log in and change between users**), though it is reasonable to scale the functionality to register a new user through a login form (with the appropriate frontend). The tag creation is mentioned in step 4. Upon creation, the author is automatically set to be the user using POST operation **PLUS** whoever the user is picking as his co-author(can be nobody -- and the article author is just the user).
After creation the backend is configured to return the full details for the author users instead of just the IDs.  
Example input for article creation through Raw data input:

```
{
    "title": "New article",
    "abstract": "An abstract for this new article",
    "authors": [1,3], # Providing the users exist
    "tags": [3,6] # Providing the tags are already created and have a unique ID
}
```
Example response after POST:
```
{
    "id": 23,
    "title": "New article",
    "abstract": "An abstract for this new article",
    "publication_date": "2024-09-10",
    "authors": [
        {
            "id": 1,
            "username": "tryf",
            "email": "",
            "first_name": "",
            "last_name": ""
        },
        {
            "id": 3,
            "username": "tryf3",
            "email": "",
            "first_name": "",
            "last_name": ""
        }
    ],
    "tags": [
        {
            "id": 3,
            "name": "Sports"
        },
        {
            "id": 6,
            "name": "Cooking"
        }
    ]
}
```
**Note**: User details such as first_name and email can be modified in the admin panel.

7. To create a Tag you can access the endpoint:
`http://127.0.0.1:8000/api/comments/`, where you can either add a comment through Raw data input or in HTML form. For the HTML form, you can select one article from the dropdown window that contains the available articles.Also there is a Content field to add the comment. Example input for Raw data:
```
{
    "article": 1, # or the article ID of your choice 
    "content": "Pretty cool!"
}
```
### 3. Using Django Fixtures

You can load predefined sample data using Django fixtures. 

**Importart**: To follow the user flow logic the fixtures must be inserted in order. 

### Prerequisite: 
In order for the fixtures (which are static data) to work correctly, you must have 3 users already created and given the superuser and staff status. The first is already created through the ```python manage.py createsuperuser``` command. The others can be created in the admin panel. 

**Important Note**: If you need to re-load the fixtures after already loading them, make sure there are the same 3 users you created from the start. If you deleted one user (e.g user1) and created another (e.g user4), the load will not work as it is not matching the sequence ID of the users. 

In order to load the fixtures again you must delete all users, and then run the custom script:
```
python manage.py reset_user_sequence
```
to reset user IDs to 1. Then you can create 2 more users again and load the fixtures correctly.

Same rule applies to tags, so to restart the tag sequence, after deleting all tags, run the script:
```
python manage.py reset_tag_sequence
```

#### a. First load the tags data using the command:

```bash
python manage.py loaddata tags_data.json  
```

#### b. Then, insert the articles data running this command:

```bash
python manage.py loaddata articles_data.json  
```

#### c. Finally, add the comments data with the command:

```bash
python manage.py loaddata comments_data.json  
```

To migrate the data to the database run the command:

```bash
python manage.py migrate
```
Now running the api, or in the DBMS pgAdmin4 you can see that the database is populated with the data.

**IF FOR SOME REASON YOU RECEIVE AN ERROR LIKE THE FOLLOWING, CLEAR GOOGLE CHROME COOKIES**
```
{
    "detail": "CSRF Failed: CSRF token missing."
}
```
---


## Running the API

### Steps to Start the API Server

1. Ensure the PostgreSQL database is running.
2. Start the development server using the command:

    ```bash
    python manage.py runserver
    ```

3. The API will be available at `http://127.0.0.1:8000/`.

4. The following endpoints are available:
   - `/api/articles/` – View, create, and manage articles.
   - `/api/tags/` – Manage tags.
   - `/api/comments/` – Manage comments.
   - `/api/articles/export_csv/` – Export articles as a CSV file.

---

## Filtering
The filtering functionality is available with the use of DRF.

Visit the endpoint http://127.0.0.1:8000/api/articles/

Clicking the Filters button it is possible to filter returned articles based on publication year, publication month, authors, tags or keyword searches such as title and abstract. 

Else, you can use request query parameters to GET the filtered articles 

For example:

```
http://127.0.0.1:8000/api/articles/?year=&month=&keywords=collection
```
returns articles that have the word collection in the title or in the abstract.


## Export CSV
The export to CSV functionality can be accesses through the API in two ways:

1. Through the endpoint: http://127.0.0.1:8000/articles/export_csv?year={year}&month={month}&tags={tags}&keywords={titleORabstract},
where you can substitute the curly brackets with values (e.g keywords=collection).

2. By pressing the export button in the DRF (Extra Actions --> Export csv) through the endpoint: http://127.0.0.1:8000/api/articles/.
If not any filter parameters are passed, all articles are returned.
Providing filters in the search, the CSV file contains only the filtered articles.  


## Important Notes
As requested, when a user (e.g User1) has created an article, ONLY he is allowed to modify or delete it.

For example, User1 is connected to the DRF. 
User1 creates the article 1 with the following JSON as a request body 
```
<!-- Endpoint: http://127.0.0.1:8000/api/articles/ -->

request body:

{
  "title": "Article 1",
  "abstract": "A new article",
  "authors": [1,2], # The IDs of the authors  
  "tags": [3] # The IDs of the tags
}

```
The created article is now populated with a unique ID.
Now all users can see/read the created article using the endpoint:

http://127.0.0.1:8000/api/articles/{ID}

For any non-author user the options to Update or Delete the article are hidden.
On the contrary, the author and co-author have PUT and DELETE permissions for the specific article.

If the User1 that created the article (and has access to Update permissions) chooses to change the authors to (e.g User2 and User3), he has no longer the ability modify the article and is prompted with Permissions Error, while User2 and User3 can now modify the article.

Comment permissions are similar to the article, which means that only the writer of a comment is able to modify or delete it and if a user is trying to access and modify a comment that did not write, is prompted with Permission Error.




