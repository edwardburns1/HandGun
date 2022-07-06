import cv2
import mediapipe as mp
import pyglet
from pyglet import shapes

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

webcam = cv2.VideoCapture(0)

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

batch = pyglet.graphics.Batch()

circle = shapes.Circle(360, 240, 10, color=(100, 255, 0), batch= batch)
circle.opacity = 100

@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(x, y):
    circle.position = (x, y)

@window.event
def on_key_press(symbol, modifiers):
    print('A key is pressed')



with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.2,
    min_tracking_confidence=0.5 ) as hands:

    while webcam.isOpened():
        success, image = webcam.read()
        if not success:
            print("Ignoring empty frame")
            continue

        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True

        if results.multi_hand_landmarks:
            x = results.multi_hand_landmarks[0].landmark[8]
            print(x.x)
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            print(x.x, x.y)
            update(x.x, x.y)

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == 27:
            break


    webcam.release()
    cv2.destroyAllWindows()

pyglet.app.run()