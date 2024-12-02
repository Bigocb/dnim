from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t


router = APIRouter()
# Single Page Actiona
@router.get("/page")
async def get_page(self):
    pass


@router.post("/page/ins")
async def insert_page(self):
    pass


@router.post("/page/upd")
async def update_page(self):
    pass


@router.post("/page/rem")
async def remove_page(self):
    pass

@router.post("/page/rem")
async def remove_page_version(self):
    pass