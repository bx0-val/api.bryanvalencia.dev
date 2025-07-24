from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import xml.etree.ElementTree as ET
import requests
import os
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/oplog", response_class=HTMLResponse)
async def oplog(request: Request):
    tree = ET.parse("oplog/oplog.xml")
    entries = tree.findall("entry")
    entries_list = []
    for entry in entries:
        entries_list.append({'id': entry.attrib['id'],'text': entry.attrib['message'], 'date': entry.attrib['date']})

    print(entries_list)
    entries_list.reverse()
    return templates.TemplateResponse(name="oplog.html", context={'request': request, 'data': entries_list})

@app.get("/commits", response_class=HTMLResponse)
async def commits(request: Request):
    token = os.getenv('GITHUB_TOKEN')
    headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
    'X-GitHub-Api-Version': '2022-11-28',
    }

    repos = requests.get('https://api.github.com/user/repos', headers=headers)
    repos_list = [repo['name'] for repo in repos.json()] 
    print(repos_list)

    all_commits = {}
    for repo in repos_list:
        response = requests.get(f'https://api.github.com/repos/bx0-val/{repo}/commits', headers=headers)
        commit_history = [(commit['html_url'], commit['sha'][:7],commit['commit']['author']['date'],commit['commit']['message']) for commit in response.json()]
        all_commits[repo] = commit_history

    # print(all_commits)
    # with open("commits.json", "a") as f:
    #     f.write(json.dumps(all_commits))
    return templates.TemplateResponse(name="commits.html", context={'request': request, 'data': all_commits})