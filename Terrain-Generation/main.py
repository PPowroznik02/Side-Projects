import numpy as np
import matplotlib.pyplot as plt

class TerrainGeneration:
    def __init__(self, N, seed=None):
        self.N = N
        self.rng = np.random.default_rng(seed)
        self.terrain = self.generate_diamond_square()
        self.display_2d()
    
    def generate_diamond_square(self):
        def declare_init_state(N):
            terrain = np.zeros((N, N), dtype=float)
            terrain[0, 0] = self.rng.random()
            terrain[N-1, 0] = self.rng.random()
            terrain[0, N-1] = self.rng.random()
            terrain[N-1, N-1] = self.rng.random()
            return terrain

        def diamond_step(step, half, terrain, amp):
            for i in range(half, self.N, step):
                for j in range(half, self.N, step):
                    total = (terrain[i-half, j-half] + terrain[i-half, j+half] +
                             terrain[i+half, j-half] + terrain[i+half, j+half])
                    terrain[i, j] = total / 4 + self.rng.uniform(-amp, amp)
            return terrain

        def square_step(step, half, terrain, amp):
            for i in range(0, self.N, half):
                for j in range((i+half)%step, self.N, step):
                    total = 0
                    count = 0
                    for dx, dy in [(-half,0),(half,0),(0,-half),(0,half)]:
                        x, y = i+dx, j+dy
                        if 0 <= x < self.N and 0 <= y < self.N:
                            total += terrain[x, y]
                            count += 1
                    terrain[i, j] = total / count + self.rng.uniform(-amp, amp)
            return terrain

        terrain = declare_init_state(self.N)
        step = self.N - 1
        amp = 0.5
        decay = 0.5

        while step > 1:
            half = step // 2
            terrain = diamond_step(step, half, terrain, amp)
            terrain = square_step(step, half, terrain, amp)
            step //= 2
            amp *= decay

        terrain -= terrain.min()
        terrain /= terrain.max()
        return terrain

    def display_2d(self):
        plt.imshow(self.terrain, cmap='viridis')
        plt.title("Generated Terrain")
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    TerrainGeneration(N=1025, seed=None)
