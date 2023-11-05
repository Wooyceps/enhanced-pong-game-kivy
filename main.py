from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball, stat_tracker):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 4)
            bounced = Vector(-1 * vx, vy)
            if abs(bounced.x) < 35:
                print(bounced.x)
                bounced *= 1.1
            ball.velocity = bounced.x, bounced.y + offset


class StatTracker(Widget):
    current_exchange = NumericProperty(0)
    best_exchange = NumericProperty(0)


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    stat_tracker = ObjectProperty(None)

    current_exchange = NumericProperty(0)
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        # bounce off paddles
        self.player1.bounce_ball(self.ball, self.stat_tracker)
        self.player2.bounce_ball(self.ball, self.stat_tracker)

        self.ball.move()

        self.player2.center_y = self.ball.y

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off to a side to score point?
        if self.ball.x < self.x:
            print(self.ball.velocity)
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            print(self.ball.velocity)
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y



class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()