import pyglet

from pyglet import shapes


window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

# image = pyglet.resource.image('kitten.jpg')

batch = pyglet.graphics.Batch()

circle = shapes.Circle(360, 240, 10, color=(100, 255, 0), batch= batch)
circle.opacity = 100
@window.event
def on_draw():
    window.clear()
    batch.draw()


def update():
    circle.position = (circle.position[0] +5, circle.position[1])

@window.event
def on_key_press(symbol, modifiers):
    print('A key is pressed')
    update()


pyglet.app.run()