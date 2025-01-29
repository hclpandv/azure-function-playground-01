## Azure playground to develop azure functions

* Azure function python v2 model setup locally and deploy to an azure function app.

> Important concepts to understand: Triggers, input bindings, output bindings

1. Use `az login` to login to the Azure account.
2. Use `deploy-azurefunctionapp.sh` script to deploy azure function app. (python)
3. Create a new python (v2 model) function  

```bash
func init python_demo_project_01 --python -m v2

```
4. Setup virtual env for developement and install dependencies

```bash
cd python_demo_project_01
python -m venv .venv
# you can pip list to see the existing python packages
pip list
# Install packages from requirements.txt file
pip install -r requirements.txt 
```

5. You may wanna use a template to add a function code based on a perticular trigger. This will add new def(function) into `function_app.py` file 

```bash
func new --name http_example --template "HTTP trigger"
# you can simply type below and then you get to choose apropriate option to start witha template
func new
```

6. Use `func start` to test the function app locally. This will give you a localhost url for testing

7. Now, after succsefull testing you may publish it to azure

```bash
export APP_NAME='functionappdemoae3bb7'
func azure functionapp publish $APP_NAME
```