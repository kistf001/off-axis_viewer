from pyrr import Vector3, vector, vector3, matrix44
import pyrr 
from math import sin, cos, radians

class Figure:

    def __init__(self):
        self.r_x, self.r_y, self.r_z = 0,0,0
        self.t_x, self.t_y, self.t_z = 0,0,0

    def get_figure_matrix(self):
        
        asdsad = (
            pyrr.Matrix44.from_translation(
                pyrr.Vector3([self.t_x, self.t_y, self.t_z])
            )*
            pyrr.Matrix44.from_x_rotation(self.r_x) *
            pyrr.Matrix44.from_y_rotation(self.r_y) *
            pyrr.Matrix44.from_z_rotation(self.r_z) 
        )

        #return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
        return asdsad

    # Camera method for the WASD movement
    def process_keyboard(self, direction):
        if direction == "FORWARD":
            self.t_y += 0.06                  #
        if direction == "BACKWARD":
            self.t_y -= 0.06                  #
        if direction == "RIGHT":
            self.t_x += 0.06                  #
        if direction == "LEFT":
            self.t_x -= 0.06                  #
        if direction == "SSSSS":
            self.t_z += 0.06                  #
        if direction == "ZZZZZ":
            self.t_z -= 0.06                  #


        if direction == "rFORWARD":
            self.r_x += 0.04                 #
        if direction == "rBACKWARD":
            self.r_x -= 0.04                 #
        if direction == "rLEFT":
            self.r_y -= 0.04                 #
        if direction == "rRIGHT":
            self.r_y += 0.04                 #
            










