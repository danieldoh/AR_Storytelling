from typing import List
from fastapi import FastAPI, File, UploadFile, Request, Form, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing_extensions import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI(debug=True)

# origins_docker = [
#    "http://128.46.36.79:8888",
# ]
#
# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins_docker,
#    allow_credentials=True,
#    allow_methods=["GET", "POST"],
#    allow_headers=["*"],
# )

templates = Jinja2Templates(directory="./templates")

# app.mount("/pose_video", StaticFiles(directory="static/pose_video"), name="pose_video")
app.mount("/static", StaticFiles(directory="./static"))


@app.post("/save_text/")
async def save_text(request: Request, text: str = Form(...)):
    try:
        with open("input_prompt.txt", "w") as file:
            file.write(text + "\n")
        return templates.TemplateResponse("index.html", {"request": request, "message": "Text saved to file successfully!"})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "message": f"Error saving text to file: {e}"})


@app.post("/save_sound_text/")
async def save_sound_text(request: Request, text: str = Form(...)):
    try:
        with open("sound.txt", "w") as file:
            file.write(text + "\n")
        return templates.TemplateResponse("sound.html", {"request": request, "message": "Text saved to file successfully!"})
    except Exception as e:
        return templates.TemplateResponse("sound.html", {"request": request, "message": f"Error saving text to file: {e}"})


@app.post("/save_selected_text/")
async def save_selected_text(text_data: dict):
    try:
        text = text_data.get("text", "")
        with open("input_prompt.txt", "w") as file:
            file.write(text)
        file.close()
        return {"message": "Text saved to file successfully!"}
    except Exception as e:
        return {"message": f"Error saving text to file: {e}"}

# async def run_script():
#    num_text = 0
#    with open("./input_prompt.txt", "r") as f:
#        texts = f.readlines()
#        texts = [t.replace('\n', '') for t in texts]
#        if '' in texts:
#            texts.remove('')
#        num_text = len(texts)
#    if num_text == 0:
#        print("No texts to process")
#    elif num_text == 1:
#        subprocess.run(["./single_run.sh"], cwd="./", shell=True)
#    elif num_text > 1:
#        subprocess.run(["./run_1.sh"], cwd="./", shell=True)

# @app.post("/run_script/")
# async def run_script(request: Request):
#    try:
#        subprocess.run("./run_1.sh", shell=True, check=True)
#        result = "Script executed successfully."
#    except subprocess.CalledProcessError as e:
#        result = f"Error occured: {e}"
#    return templates.TemplateResponse("text.html", {"request": request, "result": result})


@app.get("/generate_sound/")
async def generate_sound():
    try:
        subprocess.run(["./run_sound.sh"], shell=True, check=True)
        return {"message": "Bash script executed successfully"}
    except subprocess.CalledProcessError:
        return {"message": "Failed to execute Bash script"}


@app.post("/run_script/")
async def run_script_endpoint():
    subprocess.run(["python display.py"], cwd="./", shell=True)
    # subprocess.run(["./run_zero.sh"], cwd="./", shell=True)
    return {"message": "Script completed successfully!"}


@app.post("/run_image_script/")
async def run_image_script_endpoint():
    subprocess.run(["python image_display.py"], cwd="./", shell=True)
    # subprocess.run(["./run_zero.sh"], cwd="./", shell=True)
    return {"message": "Script completed successfully!"}


@app.post("/run_motion_script/")
async def run_motion_script_endpoint():
    subprocess.run(["python script.py"], cwd="./", shell=True)
    return {"message": "Script completed successfully!"}


@app.post("/run_avatar_script/")
async def run_motion_script_endpoint():
    subprocess.run(["python script.py"], cwd="./", shell=True)
    return {"message": "Script completed successfully!"}


def get_request():
    return Request


# @app.get("/")
# async def display(request: Request, show_gif: bool = True):
    # video_path = "/pose_video/skel/skel_00.mp4"
    # return templates.TemplateResponse("index.html", {"request": request, "video_path": video_path, "show_gif": show_gif})


# @app.get("/get_gif/")
# async def get_gif():
    # gif_path = "/workspace/animation_from_TP/static/fupose_video/animation.gif"
    # return FileResponse(gif_path, headers={"Cache-Control": "no-cache"})


@app.get("/get_video/")
async def get_video():
    # video_path = "/workspace/animation_from_TP/The_astronaut_is_dancing_on_the_moon.mp4"
    video_path = ""
    with open("./video_src.txt", "r") as f:
        video_path = f.readlines()[0]
    video_path = "static/animation/" + video_path.lower()
    return FileResponse(video_path, headers={"Cache-Control": "no-cache"})


# @app.get("/get_avatar_image/")
# async def get_avatar_image():
    # image_path = "/workspace/animation_from_TP/static/Desktop/user_interaction.png"
    # return FileResponse(image_path, headers={"Cache-Control": "no-cache"})


# @app.get("/get_spatial_temporal_video/")
# async def get_spatial_video(request: Request, index: int = 0):
#    default_path = "/workspace/animation_from_TP/static/Desktop/Spatial_Temporal/"
#    video_paths = ["1.mkv", "2.mkv", "3.mkv", "4.mkv", "5.mkv", "6.mkv", "Spatial_Temporal.mkv"]
#    video_index = index % len(video_paths)
#    video_path = default_path + video_paths[video_index]
#    return FileResponse(video_path, headers={"Cache-Control": "no-cache"})
#
#
# @app.get("/get_without_context_video/")
# async def get_without_context_video(request: Request, index: int = 0):
#    default_path = "/workspace/animation_from_TP/static/Desktop/Without_Context/"
#    video_paths = ["1.mkv", "2.mkv", "3.mkv", "4.mkv", "5.mkv", "6.mkv", "Without_context.mkv"]
#    video_index = index % len(video_paths)
#    video_path = default_path + video_paths[video_index]
#    return FileResponse(video_path, headers={"Cache-Control": "no-cache"})


@app.get("/get_image/")
async def get_image():
    # video_path = "/workspace/animation_from_TP/The_astronaut_is_dancing_on_the_moon.mp4"
    # video_path = "static/animation/Superman_is_playing_guitar_on_the_beach.png"
    image_path = ""
    with open("./image_src.txt", "r") as f:
        image_path = f.readlines()[0]
    image_path = "static/animation/" + image_path.lower()
    return FileResponse(image_path, headers={"Cache-Control": "no-cache"})


@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/menu")
async def go_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@app.get("/draw")
async def go_draw(request: Request):
    return templates.TemplateResponse("draw.html", {"request": request})


@app.get("/story")
async def go_story(request: Request):
    return templates.TemplateResponse("story.html", {"request": request})


@app.get("/sound")
async def go_sound(request: Request):
    return templates.TemplateResponse("sound.html", {"request": request})


@app.get("/avatar")
async def go_avatar(request: Request):
    return templates.TemplateResponse("avatar.html", {"request": request})


@app.get("/avatar2")
async def go_avatar2(request: Request):
    return templates.TemplateResponse("avatar2.html", {"request": request})

@app.get("/userstudy")
async def go_userstudy(request: Request):
    return templates.TemplateResponse("userstudy.html", {"request": request})

#
@app.get("/get-content")
async def get_content(file_name: str):
   try:
       txt_file_path = f"./static/story/{file_name}.txt"

       with open(txt_file_path, "r") as txt_file:
           file_contents = txt_file.read()

       return {"content": file_contents}
   except Exception as e:
       return {"error": str(e)}


# @app.post("/upload/")
# async def upload_file(file_path: str):
#    try:
#        full_path = f"static/pose_video/{file_path.split('/')[-1]}"
#        with open(full_path, "rb") as file:
#            content = file.read()
#            with open(f"static/pose_video/{file_path.split('/')[-1]}", "wb") as f:
#                f.write(content)
#        return {"message": "File uploaded successfully"}
#    except Exception as e:
#        return {"error": str(e)}
