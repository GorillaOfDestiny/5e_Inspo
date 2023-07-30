from PIL import Image, ImageDraw, ImageFont
import os 
import random
import textwrap
from datetime import datetime
import json
import pickle

def save_list(fname,list):
    with open(fname, "wb") as fp:   #Pickling
        pickle.dump(list, fp)

def load_list(fname):
    with open(fname, "rb") as fp:
        b = pickle.load(fp)
    return(b)

def generate_monster_caption():
    monster_list = load_list("Lists/monsters")
    intros = ["Remember, [X]s don't exist",
              "Wake up like a [X]",
              f"Work like you have to fight a [X] at {random.randint(1,12)}{random.choice(['PM','AM'])}",
              "A [X] isn't scared of emails",
              "Don't be a [X]",
              "Be the [X] you know you are",
              "Tell the world you're a [X]",
              "Will it still matter if you saw a [X]",
              "Be a [X]",
              "Find your inner [X]",
              "You are worth more than a [X]",
              "You aren't a [X], so don't put too much pressure on yourself"]
    save_list("Lists/intro_monsters",intros)
    intros = load_list("Lists/intro_monsters")
    monster = random.choice(monster_list)
    intro = random.choice(intros)
    if monster[0] in ["A","E","I","O","U"]:
        print(monster)
        intro.replace("A ","An ").replace(" a "," an ")
    return(intro.replace("[X]", monster))
def generate_caption(mode = None):
    modes = ["Monster"]

    if mode == None:
        mode = random.choice(modes)
        print(f"{datetime.now()}: randomly selecting {mode}")
    elif mode not in modes:
        prev_mode = mode
        mode = random.choice(modes)
        print(f"{datetime.now()}: {prev_mode} not in {modes} therefore randomly selecting {mode}")
    
    if mode == "Monster":
        caption = generate_monster_caption()

    print(f"{datetime.now()}: Caption Generated")
    return(caption)

def add_caption(img_path,caption,font_size = 50,output_name = "Test_output/output.jpg",font = "impact.ttf"):
    
    img = Image.open(img_path)
    d = ImageDraw.Draw(img)
    x_size = img.size[0]
    y_size = img.size[1]
    x0 = font_size
    y0 = font_size

    caption_y_size =(y_size+font_size)*1.25

    while caption_y_size >= y_size:
        #could likely speed up with a calculator to figure out the right size but this is a 
        # lazy approach that works well enough

        wrapped_caption = textwrap.wrap(caption,2*x_size/font_size)
        caption_y_size = (font_size*len(wrapped_caption) +y0)*1.25
        #print(font_size)
        if caption_y_size >= y_size:
            font_size -= 1
            x0 -= 1
            y0 -= 1
            print(f'{datetime.now()}: Reducing font_size to {font_size}')

    caption = "\n".join(wrapped_caption)
    font = ImageFont.truetype(font, size=font_size)
    d.text((x0,y0), caption, fill='white', font=font,
        stroke_width=2, stroke_fill='black')
    
    if output_name == None:
        format = img_path.split(".")[-1]
        output_name = img_path.replace(f".{format}",f"-output.{format}")
    print(f'{datetime.now()}: Saving Image to {output_name}')
    img.save(output_name)

if __name__ == "__main__":
    example_dir = "Test_images/"
    example_out = "Test_output/"
    example_images = os.listdir("Test_images/")
    chosen_image = example_dir + random.choice(example_images)

    caption = generate_caption("Monster")


    add_caption(chosen_image,caption)
    