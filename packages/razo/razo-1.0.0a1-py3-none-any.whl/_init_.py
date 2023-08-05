import time
import setting
import showinfo
import sys

rooting=False
sudoroot=False
nowsudo=False

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
        do('showinfo')
    else:
        print('No this command.')

def do(m):
    exec('{0}.{0}()'.format(m))

try:
    import settings
    a=settings.rootpass
except ImportError as e:
    do('setting')


do('showinfo')



while True:
    if rooting:
        a=input('[root]>>>')
    else:
        a=input('[user]>>>')
    wai(a)
