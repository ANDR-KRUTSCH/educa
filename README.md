Create project's directory, for example: "educa", and copy the following folders and files to it from the current repository:
    - config (folder)
    - docker-compose.yml
    - Dockerfile
    - requirements.txt
    - wait-for-it.sh

Then clone this repository to it folder and after it, when you are in educa folder, use the following commands:
    - docker compose up
    - docker compose exec web python /code/educa/manage.py makemigrations
    - docker compose exec web python /code/educa/manage.py migrate
    - docker compose exec web python /code/educa/manage.py collectstatic