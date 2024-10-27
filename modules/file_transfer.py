import config

def upload(user_input):
    '''
        Upload process 
        adb push <pc_folder_file> <sd_card_folder>
        (where th <sd_card_folder> is the SD Card folder identified using utility function)
        
        adb shell
        > su root
        > mv <sd_card_folder>/<folder_file> <desired_folder>
        > exit
    '''
    pass

def download(user_input):
    '''
        Download process
        adp pull <mobile_file_folder> <pc_folder>
    '''
    pass
