#import unittest
#from gradescope_utils.autograder_utils.decorators import weight, visibility, number

def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''


    global cur_hedons, cur_health    #health and hedon values
    cur_hedons = 0
    cur_health = 0
    
    global cur_star, cur_star_activity #amount of stars and appliable activities
    cur_star = 0
    cur_star_activity = None
    
    global bored_with_stars #effectiveness of stars
    bored_with_stars = False
    
    global last_activity,last_activity_duration #
    last_activity = None
    last_activity_duration = 0

    global last_running, last_textbook #last activity time = current time, if current time - last activity < 120, tired
    last_running = 0
    last_textbook = 0
    
    global cur_time, last_finished
    cur_time = 0
    last_finished = -1000

    global running_time, resting_time, textbook_time #consecutive time for activity, reset once switch activity
    running_time=0 
    resting_time=0
    textbook_time=0

    global tired
    tired = False

    global last_star_1, last_star_2
    last_star_1 = 0
    last_star_2 = 0
    

            

def star_can_be_taken(activity):
    global running_time, resting_time, textbook_time, cur_health, cur_hedons, last_activity
    global tired, cur_time, last_running, last_textbook
    global cur_star_activity, bored_with_stars
    global last_star_1, last_star_2

    if bored_with_stars == True:
        return False
    else:
        if cur_star_activity == activity:
            return True
        else:
            return False


    
def perform_activity(activity, duration):
    global running_time, resting_time, textbook_time, cur_health, cur_hedons, last_activity
    global tired, cur_time, last_running, last_textbook
    global cur_star_activity


    #tired value
    if last_textbook > 0 or last_running > 0:
        if cur_time - max(last_textbook, last_running) < 120:
            tired = True
        else:
            tired = False

    
    if activity == "running":
        #health segment
        #not tired portion
        if running_time <=180:
            if running_time + duration > 180:
                cur_health += (180-running_time)*3 + duration-(180-running_time)
            else:
                cur_health += duration * 3
        else:
            cur_health += duration #3 hours of running times 3 plus one every minute over 180
        running_time+=duration
        resting_time=0
        textbook_time=0
        last_activity="running"
        cur_time += duration
        last_running = cur_time
        
        #hedon portion

        if tired == True:
            if cur_star_activity != "running":
                cur_hedons += duration*(-2)
            else:
                if duration >= 10:
                    cur_hedons += 10 + (duration - 10)*(-2)
                else:
                    cur_hedons += duration
        else:
            if cur_star_activity == "running":
                if duration >= 10:
                    cur_hedons += 10*5 + (duration - 10)*(-2)
                else:
                    cur_hedons += 5*duration
            else:
                if duration >= 10:
                    cur_hedons += 10*2 + (duration - 10)*(-2)
                else:
                    cur_hedons += duration*2

        cur_star_activity = None
        tired = True


    #textbook segment
    elif activity == "textbooks":
        #health segment
        cur_health += duration*2

        textbook_time+=duration
        resting_time=0
        running_time=0
        last_activity="textbooks"
        cur_time += duration
        last_textbook = cur_time
        
        #hedon portion

        if tired == True:
            if cur_star_activity != "textbooks":
                cur_hedons += duration*(-2)
            else:
                if duration >= 10:
                    cur_hedons += 10 + (duration - 10)*(-2)
                else:
                    cur_hedons += duration
        else:
            if cur_star_activity == "textbooks":
                if duration >= 10:
                    if duration >= 20:
                        cur_hedons += 10*4 + 10*1 + (duration-20)*(-1)
                    else:
                        cur_hedons += 10*4 + (duration - 10)
                else:
                    cur_hedons += 4*duration
            else:
                if duration >= 20:
                    cur_hedons += 20*1 + (duration - 20)*(-1)
                else:
                    cur_hedons += duration*1
        cur_star_activity = None
        tired = True

    elif activity == "resting":
        textbook_time=0
        resting_time += duration
        running_time=0
        last_activity="resting"
        cur_time += duration

                
        #hedon segment
        #if running_time < 120 or textbook_time < 120: #if ran or carried textbooks less than two hours before, user is tired
            #if
        #elif a == "textbooks":
        #health += b * 2
        
        #hedon segment


def get_cur_hedons():
    global cur_hedons
    return cur_hedons
    
def get_cur_health():
    global cur_health
    return cur_health
    
def offer_star(activity):
    global running_time, resting_time, textbook_time, cur_health, cur_hedons, last_activity
    global tired, cur_time, last_running, last_textbook
    global cur_star_activity, bored_with_stars
    global last_star_1, last_star_2

    if bored_with_stars == False:
        
        if last_star_2 > 0:
            if cur_time - last_star_2 < 120:
                bored_with_stars = True
                #stop function here
            else:
                cur_star_activity = activity

                last_star_2 = last_star_1
                last_star_1 = cur_time
        else:
            cur_star_activity = activity

            last_star_2 = last_star_1
            last_star_1 = cur_time
    else:
        cur_star_activity = None


        
def most_fun_activity_minute():
    global running_time, resting_time, textbook_time, cur_health, cur_hedons, last_activity
    global tired, cur_time, last_running, last_textbook
    global cur_star_activity, bored_with_stars
    global last_star_1, last_star_2
    if bored_with_stars == False:
        if tired == True:
            if cur_star_activity == None:
                return "resting"
            else:
                return cur_star_activity
        else:
            if cur_star_activity == None:
                return "running"
            else:
                return cur_star_activity
    else:
        if tired == True:
            return "resting"
        else:
            return "running"

        
    
################################################################################
#These functions are not required, but we recommend that you use them anyway
#as helper functions

def get_effective_minutes_left_hedons(activity):
    '''Return the number of minutes during which the user will get the full
    amount of hedons for activity activity'''
    pass
    
def get_effective_minutes_left_health(activity):
    pass    

def estimate_hedons_delta(activity, duration):
    '''Return the amount of hedons the user would get for performing activity
    activity for duration minutes'''
    pass
            

def estimate_health_delta(activity, duration):
    pass
        
################################################################################

#@weight(1)
#@visibility("visible")
#def test_function_names(self):
    # gamify.get_cur_hedons()
    # gamify.get_cur_health()
    # gamify.offer_star("running")
    # gamify.perform_activity("running", 10)
    # gamify.star_can_be_taken("running")
    # gamify.most_fun_activity_minute()
        
if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)    
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health())            # 90 = 30 * 3                          # Test 2           		
    print(most_fun_activity_minute())  # resting                              # Test 3
    perform_activity("resting", 30)    
    offer_star("running")              
    print(most_fun_activity_minute())  # running                              # Test 4
    perform_activity("textbooks", 30)  
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons())            # -80 = -20 + 30 * (-2)                # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons())            # -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons())            # -430 = -90 + 170 * (-2)              # Test 10
    
  


    