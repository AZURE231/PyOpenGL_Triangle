import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader


class App:

    def __init__(self) -> None:
        pg.init()
        # set window size and using OpenGL in that window
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()                                # set FPS
        # initialize opengl
        glClearColor(0.1, 0.2, 0.2, 1)  # back ground color
        self.shader = self.createShader(
            "RGB_Triangle/shaders/vertex.txt", "RGB_Triangle/shaders/fragment.txt")
        glUseProgram(self.shader)
        self.triangle = Triangle()
        self.mainLoop()

    def createShader(self, vertexFilepath, fragmentFilepath):
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()
        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        running = True
        while (running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)
            pg.display.flip()

            # timming
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Triangle:

    def __init__(self) -> None:
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3
        # allocate some number of vertex array object names for use (para: Specifies the number of vertex array object names to generate)
        self.vao = glGenVertexArrays(1)
        # after create vao, bind it
        glBindVertexArray(self.vao)
        # vertex buffer object, create name, 1 object
        self.vbo = glGenBuffers(1)
        # after create, bind it
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # load data into a buffer object
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)  # 0 is position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)  # 1 is color
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                              24, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    myApp = App()
