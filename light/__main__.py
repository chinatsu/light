import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--brightness", help="Desired brightness in percent (range [3, 100])", type=int)
parser.add_argument("--color", help="Desired color temperature in Kelvin (range [2900, 7000])", type=int)
parser.add_argument("--ip", help="the local IP address for the Elgato Ring Light", type=str, default="192.168.10.103")
parser.add_argument("--toggle", help="toggle the light on or off, depending on its state", action="store_true")
parser.add_argument("--status", help="print the current state of the light", action="store_true")
args = parser.parse_args()


ENDPOINT = f"http://{args.ip}:9123/elgato/lights"

def set_light(brightness=100, color_temp=144, on=1):
     data = {"lights":[{"on": on, "temperature": color_temp, "brightness": brightness}], "numberOfLights": 1}
     r = requests.put(ENDPOINT, json=data)
     if r.status_code == 200:
         return r.json()

def get_light():
    r = requests.get(ENDPOINT)
    if r.status_code == 200:
        return r.json()

def translate_kelvin(value):
    leftSpan = 200
    rightSpan = 2900 - 7000
    valueScaled = float(value - 144) / float(leftSpan)
    return int(-rightSpan + 2900 + (valueScaled * rightSpan))

def translate_temperature(value):
    leftSpan = 2900 - 7000
    rightSpan = 200
    valueScaled = float(value - 2900) / float(leftSpan)
    return int(rightSpan + 144 + (valueScaled * rightSpan))

def print_response(res):
    print("ON\tBRIGHTNESS\tCOLOR")
    light = res["lights"][0]
    on = bool(light["on"])
    brightness = light["brightness"]
    temperature = translate_kelvin(light["temperature"])
    print(f"{on}\t{brightness}%\t\t{temperature} K")


if args.status:
    state = get_light()
    if state:
        print_response(state)
    else:
        print("Couldn't get state :(")
    exit()

if args.toggle:
    state = get_light()
    if not state:
        print("Couldn't get state :(")
        exit()
    if state["lights"][0]["on"]:
        res = set_light(on=0)
        if res:
            print_response(res)
        else:
            print("Couldn't toggle light for some reason.. Try again?")
    else:
        res = set_light(on=1)
        if res:
            print_response(res)
        else:
            print("Couldn't toggle light for some reason.. Try again?")
    exit()


if (b := args.brightness) and (t := args.color):
    if b < 3 or b > 100:
        print("Brightness value must be between 3 and 100 (inclusive)")
        exit()
    if t < 2900 or t > 7000:
        print("Temperature value must be between 2900 and 7000 (inclusive)")
        exit()
    t = translate_temperature(t)
    
else:
    state = get_light()
    if not state:
        print("Couldn't get current light state :(")
    light = state["lights"][0]
    t = translate_temperature(args.color) if args.color else light["temperature"]
    b = args.brightness if args.brightness else light["brightness"]

res = set_light(brightness=b, color_temp=t)
if res:
    print_response(res)
else:
    print("Couldn't set light for some reason.. Try again?")