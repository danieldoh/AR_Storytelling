with open("./input_prompt.txt", "r") as f:
    text = f.readlines()
    text = [t.replace(" ","_") for t in text]
    text = [t.replace("\n","") for t in text]
    text = [t.replace(".",".mp4") for t in text]
    with open("./video_src.txt", "w") as srcFile:
        srcFile.write(text[0])
    text = [t.replace(".mp4",".png") for t in text]
    with open("./image_src.txt", "w") as srcImageFile:
        srcImageFile.write(text[0])


video_path = ""
image_path = ""

with open("./video_src.txt", "r") as f:
    video_path = f.readlines()[0]

with open("./image_src.txt", "r") as f:
    image_path = f.readlines()[0]

print(video_path)
print(image_path)
