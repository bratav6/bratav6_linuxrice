from ctypes import *
user32 = windll.user32

if starting:
	# feature toggle
	vjoyaxis = True
	assists = False # auto throttle cut off & blip
	mouselock = True # locking mouse position for assetto corsa
	debouncing = True # prevent double shifting, set False to disable
	# assign vjoy device number
	v = vJoy[0]
	# vjoy axis range, do not modify
	a_max = 1 + v.axisMax
	a_min = -1 - v.axisMax
	# mouse steering
	m_sens = 16.0 # mouse sensitivity (higher faster)
	m_redu = 4 # center reduction sensitivity, acceptable range 1-50, set to 1 to disable
	steering = 0 # do not modify
	center_redu = 1 # center reduction; init value, do not modify
	# throttle
	th_axis = a_min
	th_inc = 240 # increase speed (higher faster)
	th_dec = 300 # decrease speed
	th_max = a_max # for throttle limit
	# brake
	br_axis = a_min
	br_inc = 240
	br_dec = 300
	br_max = a_max # for brake limit
	# handbrake
	ha_axis = a_min
	ha_inc = 300
	ha_dec = 600
	# clutch
	cl_axis = a_min
	cl_inc = 2000
	cl_dec = 600
	# auto blip
	blip_m = 0.4 # amount throttle applied on blip; range 0.0-1.0; 0.0=0% throttle, 1.0=100%
	a_blip = a_max * 2 * blip_m - a_max # calculation, do not modify
	# debouncing
	stimer = 0 # shifting timer
	t_upshift = 140 # minimum time required for next gear
	# throttle limit
	tlimit = 0.9 # throttle limited at 90%; range 0.0-1.0; useful for cars without traction control under low gears
	th_limit = a_max * 2 * tlimit - a_max # calculation, do not modify

#======== assign key here ========#
# toggle
toggle_vjoyaxis = keyboard.getPressed(Key.Grave) # axis calculation
toggle_mouselock = mouse.getPressed(2) # mouselock
key_assists_on = keyboard.getKeyDown(Key.NumberPad1) or mouse.wheelUp
key_assists_off = keyboard.getKeyDown(Key.NumberPad3) or mouse.wheelDown
# vehicle control
key_throttle = keyboard.getKeyDown(Key.W)
key_brake = keyboard.getKeyDown(Key.S)
key_handbrake = keyboard.getKeyDown(Key.Z)
key_clutch = keyboard.getKeyDown(Key.X)
key_centerx = mouse.getButton(2) # center steering (x-axis)
key_shiftup = keyboard.getKeyDown(Key.E)
key_shiftdown = keyboard.getKeyDown(Key.Q)
# brake limit
bl_70 = keyboard.getPressed(Key.NumberPad7)
bl_75 = keyboard.getPressed(Key.NumberPad4)
bl_80 = keyboard.getPressed(Key.NumberPad8)
bl_85 = keyboard.getPressed(Key.NumberPad5)
bl_90 = keyboard.getPressed(Key.NumberPad9)
bl_95 = keyboard.getPressed(Key.NumberPad6)
no_bl = keyboard.getPressed(Key.NumberPadPeriod)
# throttle limit
key_throttle_limit = mouse.getButton(0) # throttle limit is only applied while holding down assign key

#======== toggle ========#
if toggle_vjoyaxis:
	vjoyaxis = not vjoyaxis
if toggle_mouselock:
	mouselock = not mouselock
if key_assists_on: 
	assists = True
if key_assists_off:
	assists = False

#======== mouselock ========#
if (mouselock):
	user32.SetCursorPos(0 , 5000) # pixel coordinates (x, y)

#======== axis calculation ========#
if (vjoyaxis):
	# mouse steering
	if steering > 0:
		center_redu = m_redu ** (1 - (steering / a_max))
	elif steering < 0:
		center_redu = m_redu ** (1 - (steering / a_min))
	steering += (mouse.deltaX * m_sens) / center_redu
	if steering > a_max:
		steering = a_max
	elif steering < a_min:
		steering = a_min
	if key_centerx:
		steering = 0
	# throttle axis
	if key_throttle:
	    th_axis += th_inc
	else:
	    th_axis -= th_dec
	if th_axis > th_max:
	    th_axis = th_max
	elif th_axis < a_min:
	    th_axis = a_min
	# brake axis
	if key_brake:
	    br_axis += br_inc
	else:
	    br_axis -= br_dec
	if br_axis > br_max:
	    br_axis = br_max
	elif br_axis < a_min:
	    br_axis = a_min
	# handbrake axis
	if key_handbrake:
	    ha_axis += ha_inc
	else:
	    ha_axis -= ha_dec
	if ha_axis > a_max:
	    ha_axis = a_max
	elif ha_axis < a_min:
	    ha_axis = a_min
	# clutch axis
	if key_clutch:
	    cl_axis += cl_inc
	else:
	    cl_axis -= cl_dec
	if cl_axis > a_max:
	    cl_axis = a_max
	elif cl_axis < a_min:
	    cl_axis = a_min
	# assists switch
	if (assists):
		if key_shiftup:
			th_axis = a_min # throttle cut off while upshifting
		if key_shiftdown:
			th_axis = a_blip # throttle blip while downshifting
	# brake limit
	if bl_70:
		br_max = a_max * 0.4
	if bl_75:
		br_max = a_max * 0.5
	if bl_80:
		br_max = a_max * 0.6
	if bl_85:
		br_max = a_max * 0.7
	if bl_90:
		br_max = a_max * 0.8
	if bl_95:
		br_max = a_max * 0.9
	if no_bl:
		br_max = a_max
	if key_throttle_limit:
		th_max = th_limit
	else:
		th_max = a_max
else: # reset axis position
	steering = 0
	th_axis = a_min
	br_axis = a_min
	ha_axis = a_min
	cl_axis = a_min

#======== map vjoy axis & button ========#
v.x = int(round(steering))
v.y = th_axis
v.z = br_axis
v.ry = ha_axis
v.rx = cl_axis
v.setButton(1,key_shiftdown)
v.setButton(2,keyboard.getKeyDown(Key.Q))
v.setButton(3,keyboard.getKeyDown(Key.W)) # add new vjoy buttons below

#======== double shifting prevention ========#
if (debouncing):
	if key_shiftup:
		stimer = 0
	elif stimer < t_upshift: # end timer on reaching minimum time
		stimer += 1 # start timer on releasing shift button
		current = stimer
	if key_shiftup and (current >= t_upshift): 
		v.setButton(0,key_shiftup)
	else:
		v.setButton(0, False)
else:
	v.setButton(0,key_shiftup)

#======== diagnostics ========#
# important note: diagnostics has big impact on cpu usage (about 50-80% more)
# keep this section commented out, only uncomment for coding and testing
#diagnostics.watch(v.x)	# steering
#diagnostics.watch(v.y)	# throttle
#diagnostics.watch(v.z)	# brake
#diagnostics.watch(v.ry)	# handbrake
#diagnostics.watch(v.rx)	# clutch
#diagnostics.watch(v.axisMax)	# vjoy axis max range
#diagnostics.watch(stimer) # shifting timer

#======== reference & example ========#
# vjoy axis: x, y, z, rx, ry, rz, slider, dial
# keyboard assign: keyboard.getKeyDown(Key.A); keyboard.getPressed(Key.A)
# mouse button assign: mouse.getButton(0); mouse.getPressed(1)
# mouse button number: 0 = leftbutton; 1 = rightbutton; 2 = middlebutton; etc.
# to execute an action after pressed a key or clicked mouse button, use: keyboard.getPressed() or mouse.getPressed()
# to execute an action continuously while holding down a key or mouse button, use: keyboard.getKeyDown() or mouse.getButton()

#======== credits ========#
# most codes of "axis calculation" are borrowed from "Skagen", and others found in https://www.lfs.net/forum/post/1862759
# the codes for locking mouse are from https://bytes.com/topic/python/answers/21158-mouse-control-python
# misc codes and formating by threers
# last update: 2018-08-10