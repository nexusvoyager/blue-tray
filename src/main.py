import multiprocessing.process
import atproto as at
import flet as ft
from dotenv import load_dotenv
import os

load_dotenv()


BSKY_HANDLE = os.getenv("BSKY_HANDLE")
BSKY_PASS = os.getenv("BSKY_PASS")      

client = at.Client(base_url="https://bsky.social")
client.login(BSKY_HANDLE, BSKY_PASS)
data = client.get_profile(actor="nexusvoyager.bsky.social")

postContents = ft.TextField(hint_text="What's happening?", max_length=300, multiline=True)
postButton = ft.FilledButton(text="Post!", icon=ft.icons.SEND)

postUi = ft.Column(
    [
        postContents,
        postButton

    ], 
)


userUi = ft.Row(
    [
        ft.CircleAvatar(content=ft.Icon(ft.icons.PERSON), foreground_image_src=data.avatar),            
        ft.Row([ft.Column([ft.Text(data.display_name),  ft.Text(f"@{data.handle}")], spacing=0, expand=True)], expand=True),
    ]
)

def main(page: ft.Page):
    page.title = "Blue tray"
    page.window.width = 400 
    page.window.height = 300
    page.window.resizable = False
    page.window.maximizable = False
    page.window.always_on_top = True


    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),    
)
    
    def sendPost(e):    
        if not postContents.value or postContents.value.strip() == "":
            page.snack_bar = ft.SnackBar(content=ft.Text("Post cannot be empty!"))
            page.snack_bar.open = True
            page.update()
        else:
            client.send_post(postContents.value)
            page.snack_bar = ft.SnackBar(content=ft.Text("Post sent!"))
            page.snack_bar.open = True
            postContents.value = ""
            page.update()


    
    postButton.on_click = sendPost
    

    page.add(
        ft.Column(
            [
                userUi,
                postUi
                
            ], 
        )
        
    )

def about(page: ft.Page):
    page.add(
        ft.Text("Well this is a about page!")
    )

        
if __name__ == "__main__":
    app = multiprocessing.Process(target=ft.app(main))
    app.start()
