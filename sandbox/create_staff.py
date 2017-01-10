from charterclub.models import *

staff_list = [Staff(first_name="Steve", last_name="Moscow", position="Club Manager", order=0),
Staff(first_name="Thomas", last_name="Exgeniadis", position="Executive Chef", order=0),
Staff(first_name="Ramon", last_name="Quinones", position="Sous Chef", order=0),
Staff(first_name="Vera", last_name="Young", position="Bookkeeper", order=0),
Staff(first_name="Dana", last_name="Osterman", position="Maintenance", order=0),
Staff(first_name="Alexander", last_name="Reyes", position="Housekeeper", order=0),
Staff(first_name="Joy", last_name="Gillette", position="Dining Room Supervisor", order=0),
Staff(first_name="Hugo", last_name="Del Cid", position="Kitchen", order=0),
Staff(first_name="Lydia", last_name="Santiago", position="Sunday Chef", order=0),
Staff(first_name="Imelda", last_name="Castillo", position="Breakfast/Lunch", order=0),
Staff(first_name="Debra", last_name="Hudanish", position="Grill Cook", order=0),]

for i, staff in enumerate(staff_list):
    staff.order = i+1
    staff.save()
    
