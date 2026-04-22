from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# This points to your existing UI folder
templates = Jinja2Templates(directory="ui")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.get("/alerts", response_class=HTMLResponse)
def alerts_page(request: Request):
    return templates.TemplateResponse(
        "alerts.html",
        {"request": request}
    )


@router.get("/ec2", response_class=HTMLResponse)
def ec2_page(request: Request):
    return templates.TemplateResponse(
        "ec2.html",
        {"request": request}
    )


@router.get("/ec2/{instance_id}", response_class=HTMLResponse)
def ec2_instance_page(request: Request, instance_id: str):
    return templates.TemplateResponse(
        "ec2-instance.html",
        {
            "request": request,
            "instance_id": instance_id
        }
    )