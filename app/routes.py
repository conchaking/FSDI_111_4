from flask import (
    Flask, 
    request,
    render_template
)
import requests 

BACKEND_URL = "http://127.0.0.1:5000"
app = Flask(__name__)


@app.get("/")
def index():
    return render_template("pages/home.html")

@app.get("/about")
def about():
    return render_template("pages/about.html")

@app.get("/tasks")
def task_list():
    url = "%s/%s" % (BACKEND_URL, "tasks")
    response = requests.get(url)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("tasks/list.html", tasks=task_list)
    return (
        render_template("error.html", err=response.status_code), 
        response.status_code
    )   

@app.get("/tasks/<int:pk>")
def task_detail(pk):
    url = "%s/%s/%s" % (BACKEND_URL, "tasks", pk)
    response = requests.get(url)
    if response.status_code == 200:
        task = response.json().get("task")
        return render_template("tasks/detail.html", task=task)
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/edit")
def edit_task(pk):
    url = "%s/%s/%s/" % (BACKEND_URL, "tasks", pk)
    response = requests.get(url)
    if response.status_code == 200:
        task = response.json().get("task")
        return render_template("edit.html", task=task)
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit")
def edit_task_request(pk):
    url = "%s/%s/%s" % (BACKEND_URL, "tasks", pk)
    task_data = request.form
    response = requests.put(url, json=task_data)
    if response.status_code == 204:
        return render_template("success.html")
    return (
        render_template("error.html", err=response.status_code),
        response.status.code
    )