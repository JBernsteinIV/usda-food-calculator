# usda-food-calculator
USDA Food Calculator that talks to USDA FDC (Food Data Central API)

For now make sure you have an API key in a file called "apikey.txt". That should be located in the parent folder / main folder.

Then to run the server, you will need uvicorn and some dependencies for FastAPI.

uvicorn main:app --reload

Then open http://localhost:8000/docs to use Swagger / OpenAPI auto-docs (really cool feature for testing and debugging in FastAPI).

Then for example you can query "Avocado" and get back a JSON result in 100 gram measurements.

The front end is kind of broken and I think its written in ReactJS.

