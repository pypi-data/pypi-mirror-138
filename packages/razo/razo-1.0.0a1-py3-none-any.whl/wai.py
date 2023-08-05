h=(
'''
help:Show help.
su:Ask for superuser license.
shutdown:Shutdown razo.
''')
def wai(a):
    global 
    if a=='help':
        print(h)
    if a=='su':
        a=input
