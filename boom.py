import subprocess
exe_path = 'C:\\Users\\tyrep\\Documents\\untitled3\\cmake-build-debug\\untitled3.exe'
p = subprocess.Popen(exe_path,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
print(p)
while p.poll() is None:
    num = input()
    out = p.communicate(input=num.encode())[0]
    print('out : ', out)