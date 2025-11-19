import viz
import vizact
import vizcam
import vizshape
import math
import time

# === setup ===

viz.go()

viz.window.setSize([1920, 1080])
viz.mouse.setVisible(False)
viz.mouse.setTrap(True)
viz.mouse.setOverride(viz.ON)
viz.window.setName("kruks")


floor = vizshape.addPlane(size=(50,50), axis=vizshape.AXIS_Y, cullFace=False)
floor.setPosition(0, 0, 0)
floor.color(viz.RED)

viz.MainView.setPosition([0, 1.8, 0])

viz.setOption('ambient', 0.12)
viz.MainScene.fogColor(0,0,0)
viz.MainScene.fog(0, 30)

light = viz.addLight()
light.enable()
light.color(1,1,1)
light.spread(25)
light.intensity(3.5)
light.spotexponent(40)

def update_flashlight():
	pos = viz.MainView.getPosition()
	yaw, pitch, roll = viz.MainView.getEuler()
	yaw = math.radians(yaw)
	pitch = math.radians(pitch)
	
	dx = math.sin(yaw)
	dy = -math.sin(pitch)
	dz = math.cos(yaw)
	
	light.position(pos[0], pos[1], pos[2])
	light.direction(dx, dy, dz)

vizact.ontimer(0, update_flashlight)

# === keyboard ===

KEY_W = False
KEY_A = False
KEY_S = False
KEY_D = False

def OnKeyDown(e):
	global KEY_W, KEY_A, KEY_S, KEY_D
	
	key = e.lower()
	if key == "w":
		KEY_W = True
	if key == "a":
		KEY_A = True
	if key == "s":
		KEY_S = True
	if key == "d":
		KEY_D = True
		
def OnKeyUp(e):
	global KEY_W, KEY_A, KEY_S, KEY_D
	
	key = e.lower()
	if key == "w":
		KEY_W = False
	if key == "a":
		KEY_A = False
	if key == "s":
		KEY_S = False
	if key == "d":
		KEY_D = False
		
		
viz.callback(viz.KEYDOWN_EVENT, OnKeyDown)
viz.callback(viz.KEYUP_EVENT, OnKeyUp)

# === mouse 

SENSITIVITY = 0.1
yaw = 0.0
pitch = 0.0

def OnMouseMove(e):
	global yaw, pitch
		
	yaw += e.dx * SENSITIVITY
	pitch -= e.dy * SENSITIVITY
	pitch = max(-89.0, min(89.0, pitch))
	viz.MainView.setEuler([yaw, pitch, 0])
	
viz.callback(viz.MOUSE_MOVE_EVENT, OnMouseMove)


# === game ===

SPEED = 0.1

def MovementHandler():
	global yaw
	
	pos = viz.MainView.getPosition()
	yaw_rad = math.radians(yaw)
	move_x = 0
	move_z = 0
	
	if KEY_W:
		move_x += math.sin(yaw_rad) * SPEED
		move_z += math.cos(yaw_rad) * SPEED
	if KEY_S:
		move_x -= math.sin(yaw_rad) * SPEED
		move_z -= math.cos(yaw_rad) * SPEED
	if KEY_A:
		move_x -= math.cos(yaw_rad) * SPEED
		move_z += math.sin(yaw_rad) * SPEED
	if KEY_D:
		move_x += math.cos(yaw_rad) * SPEED
		move_z -= math.sin(yaw_rad) * SPEED
		
	new_x = pos[0] + move_x
	new_z = pos[2] + move_z
	viz.MainView.setPosition([new_x, pos[1], new_z])
		
def MainLoop():
	while True:
		MovementHandler()
		time.sleep(0.01)
		
viz.director(MainLoop)


	
	
	