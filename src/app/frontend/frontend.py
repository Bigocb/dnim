from fastapi import FastAPI
from data.db import Database, Page
from nicegui import app, ui, events
from datetime import datetime
import difflib

import markdown

# todo: Refactor
db = Database()
search_field = None
results = ui.row()

class Helpers:
    def __init__(self):
        pass

    def handle_click(self, arg):
            db.insert_topic(arg)
            self.get_topic.refresh

    def get_diff(self, old, current):
        old_doc = db.get_page_version(old['topic'], old['_id'])
        current_doc = db.get_page_version(current['topic'], current['_id'])
        diff = self.markdown_diff(old_doc['body'],current_doc['body'])
        return diff

    def markdown_diff(self, old_doc, current_doc):
        current = markdown.markdown(current_doc)
        old = markdown.markdown(old_doc)
        differ = difflib.HtmlDiff()
        html = differ.make_file(old.splitlines(),current.splitlines())
        return html
    
    def get_headers(self):
        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
            ui.label('HEADER')
        with ui.left_drawer(fixed=False, top_corner=True, bottom_corner=True).style('background-color: #d7e3f4') as left_drawer:
            ui.label('LEFT DRAWER')
            ui.link('Topics','/topics')
            ui.link('New Topic','/new')
    
    def get_footers(self):
        with ui.footer().style('background-color: #3874c8'):
            ui.label('FOOTER')


def init(fastapi_app: FastAPI) -> None:
    h = Helpers()
    @ui.page('/')
    def show():
        async def search(e: events.ValueChangeEventArguments) -> None:
            global search_field
            global results
            results.clear()
            response = db.get_pages(e.value)
            if not response:
                return
            with results: 
                for topic in response:
                    with ui.label(topic).classes('w-64'):
                        ui.label(topic).classes('absolute-bottom text-subtitle2 text-center')

        h.get_headers()

        with ui.grid(columns=4).classes('gap-4 w-full h-screen p-4'):
            with ui.card().classes('col-span-4 md:col-span-2 row-span-2 h-full'):
                ui.separator()
                search_field = ui.input(on_change=search).props('autofocus outlined rounded item-aligned input-class="ml-3"') \
                    .classes('w-96 self-center mt-24 transition-all')
                results = ui.row()
                ui.separator()
            with ui.card().classes('col-span-4 md:col-span-2 row-span-2 h-full') as preview:
                ui.separator()
                with ui.list().props('dense separator'):
                    tops = db.get_last_n_topics(5)
                    for i in tops:
                        with ui.card().props('flat bordered'):
                            ui.link(f"{i['topic']}", f"/topics/{i['topic']}")
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')
        h.get_footers()

    ui.run_with(
        fastapi_app,
        mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )

    @ui.page('/topics')
    def show():
        h.get_headers()
        ui.label("Topics")
        
        p = db.get_pages()
        
        for i,v in enumerate(p):
            with ui.row().classes('items-center'):
                with ui.card().props('flat bordered'):
                    ui.link(f"{v}", f"/topics/{v}")
        h.get_footers()
        ui.run_with(
            fastapi_app,
                mount_path='/topics',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
                storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
            )
    
    
    @ui.refreshable
    def get_topic(topic: str):

        res = db.get_page(topic)
        
        new_page = Page(
                topic=res['topic'],
                body=None,
                ts = datetime.now(),
                tags=res['tags']
            )
        with ui.card().classes('col-span-4 md:col-span-4 row-span-1 h-full'):
                ui.separator()
                with ui.row():
                    ui.label(f"{res['topic']}").style('color: #6E93D6; font-size: 200%; font-weight: 300')
                    switch = ui.switch()
                    ui.button('refresh', on_click=lambda: get_topic.refresh)
                    ui.chip(icon='save', on_click=lambda: db.insert_topic(new_page)).bind_visibility_from(switch, 'value')
                ui.separator()
                p = ui.codemirror(f"{res['body']}",language='Python').classes('h-32').bind_value_to(
                target_object=new_page, target_name="body").classes('h-full').bind_visibility_from(switch, 'value')
                # a ui markdown component that is visible with the switch variable is off
                ui.markdown()
                ui.markdown().bind_content_from(p, 'value',
                                backward=lambda v: f'{v}')
                ui.separator()
                resp = db.get_versions(res['topic'])

        with ui.card().classes('col-span-4 md:col-span-4 row-span-1 h-full') as preview:
            ui.label(f"Versions").style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.separator()
            for i in resp:
                with ui.card().classes('col-span-1 md:col-span-1 row-span-1 h-full w-full'):
                    with ui.dialog() as dialog, ui.card().classes('w-full h-full').style('max-width: none'):
                        ui.label(f"{i['ts']} vs. Current")
                        ui.html(h.get_diff(i, res))
                        ui.button('Close', on_click=dialog.close)
                    ui.button(f"{i['ts']}", on_click=dialog.open)

    @ui.page('/topics/{topic}')
    def show_page_single(topic:str):

        h.get_headers()
        
        
        with ui.grid(columns=4).classes('gap-4 w-full h-screen p-4'):
            get_topic(topic)
            
                        
        h.get_footers()

    @ui.page('/new')
    def show():
        h.get_headers()
        ui.menu()
        ui.separator()
        page = Page(
                topic=None,
                body=None,
                ts = datetime.now(),
                tags=[""]
            )
        with ui.grid(columns=4).classes('gap-4 w-full h-screen p-4'):
            with ui.card().classes('col-span-4 md:col-span-2 row-span-2 h-full'):
                ui.separator()
                topic = ui.input(placeholder="Topic").bind_value(
                target_object=page, target_name="topic"
                )

                ui.chip('save', icon='ads_click', on_click=lambda: db.insert_topic(page))

                body = ui.codemirror(language='Python').classes('h-32').bind_value_to(
                    target_object=page, target_name="body"
                )
            with ui.card().classes('col-span-4 md:col-span-2 row-span-2 h-full') as preview:
                ui.markdown().bind_content_from(topic, 'value',
                                backward=lambda o: f'{o}')
                ui.separator()
                ui.markdown().bind_content_from(body, 'value',
                                backward=lambda v: f'{v}')

        h.get_footers()
        ui.run_with(
            fastapi_app,
                mount_path='/topics',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
                storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
            )


