import gcodeparser as gp
import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt

class G50Printer3D():
    lines = []
    cur_point = (0,0,0,0,0) # x,y,z,w,e
     
    def __init__(self,**kwargs):
        kwargs['width'] = 3.725
        kwargs['height'] = 1.330
        kwargs['depth'] = 2.500
        kwargs['nozzle_radius'] = 0.006

    def print(self,gcode):
        command = gp.GcodeParser(gcode,True)
        for line in command.lines: 
            if line.type == gp.Commands.COMMENT:
                continue

            print(line.type,line.command,line.params)
            if line.type == gp.Commands.OTHER:
                if line.command_str == 'G28':
                    self.move_quick(line.get_param('X'),
                            line.get_param('Y'),
                            line.get_param('Z'),
                            line.get_param('F'))
            elif line.type == gp.Commands.MOVE:
                if line.command_str == 'G0':
                    self.move_quick(line.get_param('X'),
                            line.get_param('Y'),
                            line.get_param('Z'),
                            line.get_param('F'))
                if line.command_str == 'G1':
                    self.move_linear(line.get_param('X'),
                                line.get_param('Y'),
                                line.get_param('Z'),
                                line.get_param('F'),
                                line.get_param('V'),
                                line.get_param('W'))    
        pass

    def set_extrusion_mode(self,mode): # M82，绝对挤出长度：absolute；M83，相对挤出长度：relative
        pass

    def set_steppers_power_off(self): # M84，停止轴电机
        pass

    def set_positioning_mode(self,mode): # G90，绝对移动位置：absolute；G91，相对移动位置：relative
        pass

    def set_fan_speed(self,value): # M106 S{value}，设置风扇速度，速度：0~255。
        pass

    def set_fan_power_off(self): # M107，风扇关闭
        pass

    def set_hotend_temperature(self,value): # M104 S{value}，设置热端温度，摄氏度
        pass

    def wait_hotend_temprature(self,value): # M109 S{value}，等待热端到指定温度，摄氏度
        pass

    def set_bed_temperature(self,value): # M140 S{value}，设置平台温度，摄氏度
        pass

    def wait_bed_temperatura(self,value): # M190 S{value}，等待平台到指定温度，摄氏度
        pass

    def reset_extrusion(value_in_mm): # G92 P{value}，挤出长度：毫米
        pass

    def set_auto_home(self,x,y,z): # G28 X{x} Y{y} Z{z}，回原点，位置：x,y,z
        pass

    def move_quick(self,x,y,z,speed): # G0 F{speed} X{x} Y{y} Z{z}，快速移动，位置：x,y,z；速度：mm/s
        if not x: x = self.cur_point[0]
        if not y: y = self.cur_point[1]
        if not z: z = self.cur_point[2]
        self.cur_point = x,y,z,self.cur_point[3],0
        pass

    def move_linear(self,x,y,z,speed,extrude,roller): # G1 F{speed} X{x} Y{y} Z{z} V{extrude} W{roller}，直线移动，位置：x,y,z；挤出长度：毫米；速度：mm/s
        line_begin = self.cur_point
        
        if not x: x = self.cur_point[0]
        if not y: y = self.cur_point[1]
        if not z: z = self.cur_point[2]
        if not extrude: extrude = self.cur_point[4]
        self.cur_point = x,y,z,roller,extrude
        line_end = self.cur_point

        self.lines.append((line_begin,line_end))
        pass

    def move_cycle(self,x,y,z,speed,extrude):
        pass
        
with open('C:/Users/SLTru/Desktop/长方体-G50_6_Ender-PLA_1h44m.gcode', 'r') as f:
    gcode = f.read()

printer = G50Printer3D()
printer.print(gcode)
print(len(printer.lines))

fig = plt.figure()

#创建3d绘图区域
ax = plt.axes(projection='3d')
plt.show(block=False)
plt.ion()

x = []
y = []
z = []
w = []
roller_x = []
roller_y = []
roller_z = []

roller_radius = 10 # mm
roller_velocity_in_second = 3.14 / 2.5


cursor_x = []
cursor_y = []
cursor_z = []

last_i = 0
for i in range(len(printer.lines)):
    for line in printer.lines[last_i:i]:
        begin,end = line
        x.append(begin[0])
        y.append(begin[1])
        z.append(begin[2])
        w.append(begin[3])

        x.append(end[0])
        y.append(end[1])
        z.append(end[2])
        w.append(end[3])

        tail = Rotation.from_euler('xyz',[0,0,end[3]],True).apply([0,-roller_radius,0])
        left = Rotation.from_euler('xyz',[0,0,end[3]],True).apply([-roller_radius,-roller_radius,0])
        right = Rotation.from_euler('xyz',[0,0,end[3]],True).apply([roller_radius,-roller_radius,0])

        # roller_x.append(end[0] + tail[0])
        # roller_y.append(end[1] + tail[1])
        # roller_z.append(end[2] + tail[2])
        # roller_velocity_in_second

        # roller_pos = end[0] + direction[0],end[1] + direction[1],end[2] + direction[2]

        cursor_x.extend([end[0],end[0]+left[0],end[0]+right[0],end[0],end[0]+tail[0]])
        cursor_y.extend([end[1],end[1]+left[1],end[1]+right[1],end[1],end[1]+tail[1]])
        cursor_z.extend([end[2],end[2]+left[2],end[2]+right[2],end[2],end[2]+tail[2]])

    last_i = i
    

    ax.cla()
    ax.scatter([-300,300,0],[300,-300,0],[0,0,200])
 
    ax.plot(x,y,z)
    ax.plot(cursor_x,cursor_y,cursor_z)
    cursor_x.clear()
    cursor_y.clear()
    cursor_z.clear()

    fig.canvas.draw()
    fig.canvas.flush_events()

plt.ioff()
plt.show(block=True)


