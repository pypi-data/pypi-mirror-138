def setting():
    a=input('Please set root password:')
    with open('settings.py','w') as c:
        c.write("rootpass='{0}'".format('a'))
    
