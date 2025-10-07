import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

from life_froms import LIFE_FORMS


class GameOfLife:
    def __init__(self, N, life_form_type=None):
        self.N = N
        self.grid = self.random_grid()
        self.running = True
        self.life_form_type = life_form_type
        
        self.grid_with_life_from()  

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        self.img = self.ax.imshow(self.grid, cmap='binary', animated=True)
        
        self.ani = animation.FuncAnimation(self.fig, 
                                           self.update_frame, 
                                           interval=100, 
                                           blit=True
                                           )

        ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
        self.button = Button(ax_button, 'Start/Stop')
        self.button.on_clicked(self.toggle_animation)
        

    # Generate random state grid
    def random_grid(self):
        grid = np.random.randint(2, size=(self.N, self.N))
        
        # Border conditions
        grid[0, :] = 0
        grid[:, 0] = 0
        grid[self.N-1, :] = 0
        grid[:, self.N-1] = 0
        
        return grid

    # Update life in grid
    def update_grid(self):
        # New grid of dead cells
        new_grid = np.zeros((self.N, self.N), dtype=int)
        
        for i in range(1, self.N-1):
            for j in range(1, self.N-1):
                # Calculate number of non-dead neighbours
                total_life_neighbours = self.grid[i-1, j-1] + self.grid[i-1, j] + self.grid[i-1, j+1] + self.grid[i, j-1] + self.grid[i, j+1] + self.grid[i+1, j-1] + self.grid[i+1, j] + self.grid[i+1, j+1]
                
                # Gridcell remains alive
                if self.grid[i, j] == 1:
                    if total_life_neighbours == 2 or total_life_neighbours == 3:
                        new_grid[i, j] = 1
                        
                # Gridcell is resurected
                else:
                    if total_life_neighbours == 3:
                        new_grid[i, j] = 1
                        
        self.grid = new_grid

    # Updates frames in animation
    def update_frame(self, frame):
        if self.running:
            self.update_grid()
            self.img.set_data(self.grid)
            
        return (self.img, )

    # Turns on and off animation
    def toggle_animation(self, event):
        self.running = not self.running

    # Runs animation
    def run(self):
        plt.show()
    
    # Generates grid with life form
    def grid_with_life_from(self):
        if self.life_form_type:
            self.grid = np.zeros((self.N, self.N), dtype=int)
            
            center = self.N // 2
            
            life_form = LIFE_FORMS[self.life_form_type]
            
            self.grid[center:center+life_form.shape[0], center:center+life_form.shape[1]] += life_form

if __name__ == '__main__':
    game = GameOfLife(N=150, life_form_type=None)
    game.run()
    