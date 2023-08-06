import time
import sys
import datetime

rooting=False
sudoroot=False
nowsudo=False

def setting():
    a=input('Please set root password:')
    with open('settings.py','w') as c:
        c.write("rootpass='{0}'".format('a'))
    
def showinfo():
    print('Razo 1.0.0a5.')
    print('Type help for help.')
    print('Still testing,please know.')


h=(
'''
help:Show help.
su:Ask for superuser license.
shutdown:Shutdown razo.
info:Show info.
setting:Run setting.
time:Get time.
''')
def wai(a):
    global rooting
    if a=='help':
        print(h)
    elif a=='su':
        a=input('Please enter root password:')
        import settings
        if a==settings.rootpass:
            rooting=True
    elif a=='shutdown':
        if rooting:
            print('Shutting down.')
            time.sleep(5)
            sys.exit(0)
        else:
            print('Not able until root.')
    elif a=='info':
        showinfo()
    elif a=='setting':
        if rooting:
            setting()
            rooting=False
        else:
            print('Not able until root.')
    elif a=='time':
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print('No this command.')



try:
    import settings
    a=settings.rootpass
except ImportError as e:
    setting()


showinfo()
time.sleep(3)


while True:
    if rooting:
        a=input('[root]>>>')
    else:
        a=input('[user]>>>')
    wai(a)
