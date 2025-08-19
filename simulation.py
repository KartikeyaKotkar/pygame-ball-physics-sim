import math
import random

import config
from ball import Ball


class Simulation:

    def __init__(self):
        self.balls = []
        self._create_balls()

    def _create_balls(self):
        for i in range(config.NUM_BALLS):
            while True:
                radius = config.BALL_RADIUS
                x = random.randint(radius, config.WIDTH - radius)
                y = random.randint(radius, config.HEIGHT - radius)
                vx = random.uniform(config.VELOCITY_RANGE[0], config.VELOCITY_RANGE[1])
                vy = random.uniform(config.VELOCITY_RANGE[0], config.VELOCITY_RANGE[1])
                color = config.BALL_COLORS[i % len(config.BALL_COLORS)]

                new_ball = Ball(x, y, vx, vy, radius, color)

                is_overlapping = False
                for existing_ball in self.balls:
                    dist = math.hypot(new_ball.x - existing_ball.x, new_ball.y - existing_ball.y)
                    if dist < new_ball.radius + existing_ball.radius:
                        is_overlapping = True
                        break

                if not is_overlapping:
                    self.balls.append(new_ball)
                    break

    def _handle_ball_collisions(self):
        num_balls = len(self.balls)
        for i in range(num_balls):
            for j in range(i + 1, num_balls):
                ball1 = self.balls[i]
                ball2 = self.balls[j]

                dx = ball2.x - ball1.x
                dy = ball2.y - ball1.y
                dist = math.hypot(dx, dy)

                if dist < ball1.radius + ball2.radius:
                    # Resolve overlap to prevent balls from sticking
                    overlap = (ball1.radius + ball2.radius) - dist
                    nx = dx / dist
                    ny = dy / dist
                    ball1.x -= overlap / 2 * nx
                    ball1.y -= overlap / 2 * ny
                    ball2.x += overlap / 2 * nx
                    ball2.y += overlap / 2 * ny

                    # Elastic collision response
                    # Normal vector (from ball1 to ball2) is (nx, ny)
                    # Tangent vector
                    tx, ty = -ny, nx

                    # Dot products for normal and tangent velocities
                    v1n = ball1.vx * nx + ball1.vy * ny
                    v1t = ball1.vx * tx + ball1.vy * ty
                    v2n = ball2.vx * nx + ball2.vy * ny
                    v2t = ball2.vx * tx + ball2.vy * ty

                    # Swap normal velocities (since masses are equal)
                    v1n_new, v2n_new = v2n, v1n

                    # Update velocities
                    ball1.vx = v1n_new * nx + v1t * tx
                    ball1.vy = v1n_new * ny + v1t * ty
                    ball2.vx = v2n_new * nx + v2t * tx
                    ball2.vy = v2n_new * ny + v2t * ty

    def update(self):
        for ball in self.balls:
            ball.move()
            ball.handle_wall_collision()
        self._handle_ball_collisions()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)
