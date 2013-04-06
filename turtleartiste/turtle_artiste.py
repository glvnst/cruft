#!/usr/bin/python
"""
Make 360 Art d' Turtle pieces
"""
import turtle

TURTLE = turtle.Turtle()
SCREEN = TURTLE.getscreen()
SCREEN.setup(width=500, height=500)
SCREEN.mode("logo")
SCREEN.tracer(0, 0)

TURTLE.speed(0)


def protect_state(decorated_function):
    """
    Decorate a function so pen position, heading, up/down state, color are
    restored, requires argument 0 to be a turtle object
    """
    def wrapped_function(protected_turtle, *args):
        """ Save pen state, call decorated function, restore pen state """
        starting_position = protected_turtle.position()
        starting_heading = protected_turtle.heading()
        starting_color = protected_turtle.color()
        was_down = protected_turtle.isdown()
        decorated_function(protected_turtle, *args)
        protected_turtle.penup()
        protected_turtle.goto(starting_position)
        protected_turtle.setheading(starting_heading)
        protected_turtle.color(starting_color[0], starting_color[1])
        if was_down:
            protected_turtle.pendown()
    return wrapped_function    


@protect_state
def write_label(label_turtle, label_text):
    """ Write an image label and return the turtle to the previous state """    
    label_turtle.penup()
    label_turtle.goto(-245, 175)
    label_turtle.write(label_text, font=("Caracteres L1", 74, "normal"))
    

@protect_state
def draw_background(background_turtle, background_screen):
    """
    Draw and fill a box that fills the background. this is a workaround for
    use with PDF export
    """
    background_turtle.penup()
    background_turtle.goto(-251, 251)
    background_turtle.color(background_screen.bgcolor(),
                            background_screen.bgcolor())
    background_turtle.fill(True)
    background_turtle.pendown()
    for _ in range(4):
        background_turtle.right(90)
        background_turtle.forward(500)
    background_turtle.fill(False)
    background_turtle.penup()




for angle in range(0, 360):
    caption = "{}".format(angle)

    SCREEN.bgcolor('#EBEBEB')
    draw_background(TURTLE, SCREEN)
    SCREEN.title(caption)

    TURTLE.hideturtle()

    for distance in range(0, 180):
        for color in ['red', 'green', 'yellow', 'blue']:
            TURTLE.color(color)
            TURTLE.forward(distance)
            TURTLE.right(angle)

    TURTLE.penup()
    TURTLE.color("#D6D6D6")
    write_label(TURTLE, caption)
    SCREEN.update()
    SCREEN.getcanvas().postscript(file="turtle-{:03d}.ps".format(angle),
                                  colormode='color')
    TURTLE.reset()

