from flask import Flask, render_template, url_for, request, jsonify
from flask.helpers import send_from_directory
from flask.wrappers import Response
from flask_cors import CORS, cross_origin
from pycreate2 import Create2
import time

import pygame
pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True


class ControlledBot(Create2):

    def __init__(self, port = "/dev/ttyUSB0", baud = 115200, mode="full"):
        # init Create2 bot
        super().__init__(port, baud=baud)

        self.forward = True
        self.clean_status = False
        self.max_speed = 250
        self.right_motor_speed = 0
        self.left_motor_speed = 0
        
        self.start()

        if mode == "full":
            print(mode)
            self.full()
        elif mode == "safe":
            self.safe()
    
    def drive(self):
        # print(self.right_motor_speed, self.left_motor_speed)

        if self.forward:
            self.drive_direct(self.left_motor_speed, self.right_motor_speed)

        elif not self.forward:
            bot.drive_direct(-1 * self.left_motor_speed, -1 * self.right_motor_speed)

    def swap_direction(self):
        self.forward = not self.forward

    def turbo(self):
        if self.clean:
            self.max_speed = 250
        else:
            self.max_speed = (self.max_speed % 500) + 250

    def drive_controller(self, input_value, motor):
        if motor == "right":
            self.right_motor_speed =  self.__calc_speed(input_value)
        elif motor == "left":
            self.left_motor_speed =  self.__calc_speed(input_value)
    
    # set motor speed to zero and reset the roomba
    def safe_break(self):
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        self.reset()

    def swap_clean(self):
        self.clean_status = not self.clean_status
        self.clean(self.clean_status)

    def turn_right(self):
        self.right_motor_speed = -1 * self.max_speed
        self.left_motor_speed = self.max_speed

    def turn_left(self):
        self.left_motor_speed = -1 * self.max_speed
        self.right_motor_speed = self.max_speed

    def stop(self):
        self.left_motor_speed = 0
        self.right_motor_speed = 0

    # calculates the speed with given input
    def __calc_speed(self, controller_input):
        y = self.max_speed/2 * controller_input + self.max_speed/2
        return int(y)
            
    


def setup():

    for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
        joysticks[-1].init()
    # print a statement telling what the name of the controller is
        print ("Detected joystick "),joysticks[-1].get_name(),"'"

    return ControlledBot()


app = Flask(__name__)
cors = CORS(app)
# app.config['CORES_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    run()
    return render_template('index.html')

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/templates/js/<path:path>")
def send_js(path):
    print("Hi")
    return send_from_directory('templates/js', path)

@app.route("/command/", methods = ['GET', 'OPTIONS'])
@cross_origin()
def handleCommand():
    value = request.args.get('value')
    if value == 'w':
        bot.drive_direct(500, 500)
    if value == 'a':
        bot.drive_direct(100, -100)
    if value == 's':
        bot.drive_direct(-100, -100)
    if value == 'd':
        bot.drive_direct(-100, 100)
    if value == 'space':
        bot.drive_direct(0, 0)
    if value == 'c':
        if brush_status:
            bot.clean(False)
        else:
            bot.clean(True) 


    response = jsonify({"Hello Cors": "Nice"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def run():
    global bot
    bot = setup()

    while keepPlaying:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == 1536:
                if event.dict["axis"] == 5:
                    print(event.dict["value"])
                    bot.drive_controller(event.dict["value"], "right")

                if event.dict["axis"] == 4:
                    print(event.dict["value"])
                    bot.drive_controller(event.dict["value"], "left")

            if event.type == 1539:
                if event.dict["button"] == 3:
                    print("Button X pressed")
                    bot.swap_clean()

                if event.dict["button"] == 0:
                    print("Button A pressen")
                    bot.swap_direction()

                if event.dict["button"] == 1:
                    print("Button B pressed")
                    bot.safe_break()

                if event.dict["button"] == 4:
                    print("Button Y pressed")
                    bot.turbo()

                if event.dict["button"] == 6:
                    print("Right shoulder pressed")
                    bot.turn_right()
                if event.dict["button"] == 7:
                    print("Left shoulder pressed")
                    bot.turn_left()
            
            if event.type == 1540:
                if event.dict["button"] == 6:
                    print("Left shoulder pressed")
                    bot.stop()
                if event.dict["button"] == 7:
                    print("Right shoulder pressed")
                    bot.stop()

        bot.drive()



if __name__ == "__main__":
    run()
    # app.run(debug=True)