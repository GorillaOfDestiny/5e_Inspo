from PIL import Image, ImageDraw, ImageFont
import os 
import random
import textwrap
from datetime import datetime
import json
import pickle
import subprocess
import matplotlib.pyplot as plt
import numpy as np

def run_win_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        print(line)
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)
    

def load_and_save_api(thing):
    run_win_cmd(f'curl -X GET "https://www.dnd5eapi.co/api/{thing}/" -H "Accept: application/json" > "{thing}.json"')
    data = json.load(open(f"{thing}.json"))['results']
    data_list = []
    for d in data:
        data_list.append(d['name'])
    save_list(f"Lists/{thing}",data_list)
    os.remove(f'{thing}.json')
   
def save_list(fname,list):
    with open(fname, "wb") as fp:   #Pickling
        pickle.dump(list, fp)

def load_list(fname):
    with open(fname, "rb") as fp:
        b = pickle.load(fp)
    return(b)

def sort_a_an(intro,item1,item2):
    if item1[0] in ["A","E","I","O","U"]:
        intro = intro.replace("A [X]",f"An {item1}").replace(" a [X]",f" an {item1}")
    else:
        intro = intro.replace("[X]",item1)
    if item2[0] in ["A","E","I","O","U"]:
        intro = intro.replace("A [Y]",f"An {item2}").replace(" a [Y]",f" an {item2}")
    else:
        intro = intro.replace("[Y]",item2)
    return(intro)

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
              "You aren't a [X], so don't put too much pressure on yourself",
              "Be a [X] not a [Y]",
              "Be the [X] that defeats a [Y]",
              "Don't let the [X]s of the world lead the [Y]s"]
    save_list("Lists/intro_monsters",intros)
    intros = load_list("Lists/intro_monsters")
    monster = random.choice(monster_list)
    monster2 = random.choice(monster_list)
    intro = random.choice(intros)
    outro = sort_a_an(intro,monster,monster2)
    return(outro)

def generate_class_caption():
    class_list = ["Barbarian","Bard","Cleric","Druid","Fighter","Monk","Paladin","Ranger","Rogue","Sorcerer","Warlock","Wizard","DM"]
    save_list("Lists/classes",class_list)
    intros = ["Be the best [X] you can be",
              "Don't be a [X], be a [Y]",
              "Why would a [X] let a [Y] boss them around",
              "Don't worry about the [X]s of the world",
              "[X]s don't go to meetings",
              "Be proud to be a [X]",
              "[X]s were not meant to be understood",
              "Being a [X] is a lifestyle, not a hobby",
              "I hate [X]s",
              "I love [X]s",
              "Everyone should fear a [X] with agency",
              "A real [X] doesn't give up",
              "There is no need to respect a [X]",
              "You are a [X], you deserve respect",
              "A [X] should not be responsible for the actions of a [Y]"]
    save_list("Lists/intro_classes",intros)
    intro = random.choice(intros)
    class1 = random.choice(class_list)
    class2 = random.choice(class_list)
    outro = sort_a_an(intro,class1,class2)
    return(outro)

def generate_magic_item_caption():
    magic_item_list = load_list("Lists/magic-items")
    intros = ["Stop chasing [X]s",
              "Never take a [X] for a [Y]",
              "A [X] isn't worth it",
              "Noone actually likes [X]",
              "Noone actually wants a [X]",
              "Never trust a person with a [X]",
              "Get that [X]",
              "Find someone that makes you feel like a [X]",
              "Work hard so you can get a [X]",
              "[X]s aren't worth it",
              "Emulate a [X]",
              "Why are you after a [X]"]
    save_list("Lists/intro_magic_items",intros)
    item1 = random.choice(magic_item_list)
    item2 = random.choice(magic_item_list)
    intro = random.choice(intros)
    outro = sort_a_an(intro,item1,item2)
    return(outro)

def generate_caption(mode = None):
    modes = ["Monster","Class","Magic Item"]

    if mode == None:
        mode = random.choice(modes)
        print(f"{datetime.now()}: randomly selecting {mode}")
    elif mode not in modes:
        prev_mode = mode
        mode = random.choice(modes)
        print(f"{datetime.now()}: {prev_mode} not in {modes} therefore randomly selecting {mode}")
    
    if mode == "Monster":
        caption = generate_monster_caption()
    if mode == "Class":
        caption = generate_class_caption()
    if mode == "Magic Item":
        caption = generate_magic_item_caption()
    print(f"{datetime.now()}: Caption Generated")
    return(caption)

def add_caption(caption,img_path = None,font_size = None,output_name = "Test_output/output.jpg",font = "impact.ttf",wrap_factor = 2,updown = False,rgb1 = None,rgb2 = None,resx = 1920,resy = 1080):
    if img_path != None:
        img = Image.open(img_path)
    else:
        img = generate_gradient_image(rgb1 = rgb1,rgb2 = rgb2,updown = updown,resx = resx, resy = resy)
    d = ImageDraw.Draw(img)
    
    x_size = img.size[0]
    y_size = img.size[1]
    if font_size == None:
        font_size = int(0.5*x_size)
    print(font_size)
    x0 = font_size
    y0 = font_size

    caption_y_size =(y_size+font_size)*wrap_factor

    while caption_y_size >= y_size:
        #could likely speed up with a calculator to figure out the right size but this is a 
        # lazy approach that works well enough

        wrapped_caption = textwrap.wrap(caption,2*x_size//font_size)
        caption_y_size = (font_size*len(wrapped_caption) +y0)*wrap_factor
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

def generate_gradient_image(rgb1 = None,rgb2 = None,updown = True,resx = 1920,resy = 1080):
    print(f"{datetime.now()}: Making Gradient Image")

    if rgb1 == None:
        rgb1 = np.random.uniform(0,1,size = (3))
    if rgb2 == None:
        rgb2 = np.random.uniform(0,1,size = (3))
    print(f"{datetime.now()}: RGB1 set to {rgb1}")
    print(f"{datetime.now()}: RGB2 set to {rgb2}")
    x = np.ones((resy, resx, 3))
    x[:, :, 0:3] = rgb1

    y = np.ones((resy, resx, 3))
    y[:,:,0:3] = rgb2
    
    if updown == True:
        c = np.linspace(0, 1, resy)[:, None, None]
    else:
        c = np.linspace(0,1,resx)[None,:,None]
    gradient = x + (y - x) * c
    gradient = 255*gradient
    print(gradient.shape)
    return(Image.fromarray(gradient.astype(np.uint8)))

if __name__ == "__main__":
    example_dir = "Test_images/"
    example_out = "Test_output/"
    example_images = os.listdir("Test_images/")
    chosen_image = example_dir + random.choice(example_images)
    
    caption = generate_caption()
    add_caption(caption)
    #load_and_save_api("magic-items")
    
    