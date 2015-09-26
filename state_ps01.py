"""
state_ps01.py: Get and set vehicle state, parameter and channel-override information. Modified vehicle_state.py
-removed arming code

It also demonstrates how to observe vehicle attribute (state) changes.

Full documentation is provided at http://python.dronekit.io/examples/vehicle_state.html
"""

from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

# First get an instance of the API endpoint
api = local_connect()
# Get the connected vehicle (currently only one vehicle can be returned).
vehicle = api.get_vehicles()[0]

# Get all vehicle attributes (state)
print "\nGet all vehicle attribute values:"
print " Location: %s" % vehicle.location
print " Attitude: %s" % vehicle.attitude
print " Velocity: %s" % vehicle.velocity
print " GPS: %s" % vehicle.gps_0
print " Groundspeed: %s" % vehicle.groundspeed
print " Airspeed: %s" % vehicle.airspeed
print " Mount status: %s" % vehicle.mount_status
print " Battery: %s" % vehicle.battery
print " Rangefinder: %s" % vehicle.rangefinder
print " Rangefinder distance: %s" % vehicle.rangefinder.distance
print " Rangefinder voltage: %s" % vehicle.rangefinder.voltage
print " Mode: %s" % vehicle.mode.name    # settable
print " Armed: %s" % vehicle.armed    # settable


# Set vehicle mode and armed attributes (the only settable attributes)
print "Set Vehicle.mode=GUIDED (currently: %s)" % vehicle.mode.name
vehicle.mode = VehicleMode("GUIDED")
vehicle.flush()  # Flush to guarantee that previous writes to the vehicle have taken place
while not vehicle.mode.name=='GUIDED' and not api.exit:  #Wait until mode has changed
    print " Waiting for mode change ..."
    time.sleep(1)

# Show how to add and remove and attribute observer callbacks (using mode as example)
def mode_callback(attribute):
    print " CALLBACK: Mode changed to: ", vehicle.mode.name

print "\nAdd mode attribute observer for Vehicle.mode"
vehicle.add_attribute_observer('mode', mode_callback)

print " Set mode=STABILIZE (currently: %s)" % vehicle.mode.name
vehicle.mode = VehicleMode("STABILIZE")
vehicle.flush()

print " Wait 2s so callback invoked before observer removed"
time.sleep(2)

# Remove observer - specifying the attribute and previously registered callback function
vehicle.remove_attribute_observer('mode', mode_callback)


# Get Vehicle Home location ((0 index in Vehicle.commands)
print "\nGet home location"
cmds = vehicle.commands
cmds.download()
cmds.wait_valid()
print " Home WP: %s" % cmds[0]


# Get/Set Vehicle Parameters
print "\nRead vehicle param 'THR_MIN': %s" % vehicle.parameters['THR_MIN']
print "Write vehicle param 'THR_MIN' : 10"
vehicle.parameters['THR_MIN']=10
vehicle.flush()
print "Read new value of param 'THR_MIN': %s" % vehicle.parameters['THR_MIN']


# Demo callback handler for raw MAVLink messages
def mavrx_debug_handler(message):
    print "Raw MAVLink message: ", message

print "\nSet MAVLink callback handler (start receiving all MAVLink messages)"
vehicle.set_mavlink_callback(mavrx_debug_handler)

print "Wait 1s so mavrx_debug_handler has a chance to be called before it is removed"
time.sleep(1)

print "Remove the MAVLink callback handler (stop getting messages)"
vehicle.unset_mavlink_callback()


## Reset variables to sensible values.
print "\nReset vehicle attributes/parameters and exit"
vehicle.mode = VehicleMode("STABILIZE")
vehicle.armed = False
vehicle.parameters['THR_MIN']=130
vehicle.flush()
