import cv2
import mediapipe as mp
import pyglet
from pyglet import shapes
import threading
from gameClasses import Dot
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles









class FingerObject(pyglet.window.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "Fingers")
        self.height = height
        self.width = width
        self.window = super()
        self.batch = pyglet.graphics.Batch()
        self.circle = shapes.Circle(360, 240, 10, color=(100, 255, 0), batch=self.batch)
        self.circle.opacity = 100
        self.webcam = cv2.VideoCapture(0)
        self.count = 0

        self.apple_list = list() #Todo replace with clever matrix
        print("inited")

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        for apple in self.apple_list:
            apple.draw()

    def update(self, delta_time):
        if cv2.waitKey(1) & 0xFF == 27:
            self.quit()

        self.check_collisions()
        if self.count == 30:
            self.apple_list.append(Dot(self.width, self.height))
            self.apple_list[-1].draw()
            self.count = 0
        frame = self.getFrame()
        if frame == -1:
            return
        frame.x = 1 - frame.x
        frame.y = 1 - frame.y
        self.circle.position = (frame.x * self.width, frame.y * self.height)

        self.count += 1
        print(self.count)

    def quit(self):

        self.webcam.release()
        cv2.destroyAllWindows()

    def check_collisions(self):
        for apple in self.apple_list:
            if apple.collision(self.circle.position, self.circle.radius):
                self.apple_list.remove(apple)
                self.circle.radius += 5

    def getFrame(self):

        pointer  = -1
        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.3,
                min_tracking_confidence=0.5) as hands:
            success, image = self.webcam.read()

            if not success:
                print("Try reading again")
                return pointer

            image.flags.writeable = False
            results = hands.process(image)

            image.flags.writeable = True

            if results.multi_hand_landmarks:
                pointer = results.multi_hand_landmarks[0].landmark[8]
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))



            return pointer




# def vision(finger):
#     with mp_hands.Hands(
#             static_image_mode=False,
#             max_num_hands=2,
#             min_detection_confidence=0.2,
#             min_tracking_confidence=0.5) as hands:
#
#         while webcam.isOpened():
#             success, image = webcam.read()
#             if not success:
#                 print("Ignoring empty frame")
#                 continue
#
#             image.flags.writeable = False
#             results = hands.process(image)
#
#             image.flags.writeable = True
#
#             if results.multi_hand_landmarks:
#                 x = results.multi_hand_landmarks[0].landmark[8]
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     mp_drawing.draw_landmarks(
#                         image,
#                         hand_landmarks,
#                         mp_hands.HAND_CONNECTIONS,
#                         mp_drawing_styles.get_default_hand_landmarks_style(),
#                         mp_drawing_styles.get_default_hand_connections_style())
#
#                 finger.update(x.x, x.y)
#
#             cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
#
#             if cv2.waitKey(1) & 0xFF == 27:
#                 break
#
#         webcam.release()
#         cv2.destroyAllWindows()

if __name__ == "__main__":
    fingy = FingerObject(720, 480)

    pyglet.clock.schedule_interval(fingy.update, 1/30)
    pyglet.app.run()