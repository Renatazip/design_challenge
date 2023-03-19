# Design challenge

To give product designers power to grow at BigTech companies and show them the world.

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/Renatazip/design_challenge.git
```

Move to directory:

```bash
cd design_challenge 
```

Install the requirements:

```bash
pip3 install -r requirements.txt
```

Create the database:

```bash
python3 manage.py migrate
```
```bash
python3 manage.py makemigrations
```

Finally, run the development server:

```bash
python3 manage.py runserver
```

The project will be available at **127.0.0.1:8000**.

