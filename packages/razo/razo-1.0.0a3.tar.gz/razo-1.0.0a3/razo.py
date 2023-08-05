import time
import sys

rooting=False
sudoroot=False
nowsudo=False

def setting():
    a=input('Please set root password:')
    with open('settings.py','w') as c:
        c.write("rootpass='{0}'".format('a'))
    
def showinfo():
    print('Razo 1.0.0a3.')
    print('Type help for help.')
    print('Still testing,please know.')


h=(
'''
help:Show help.
su:Ask for superuser license.
shutdown:Shutdown razo.
info:Show info.
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
            sys.exit(0)
    elif a=='info':
        showinfo()
    else:
        print('No this command.')



try:
    import settings
    a=settings.rootpass
except ImportError as e:
    setting()


do('showinfo')



while True:
    if rooting:
        a=input('[root]>>>')
    else:
        a=input('[user]>>>')
    wai(a)
