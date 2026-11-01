import os, glob
cands=[]
for root in [r'E:\envolution', r'C:\Users\10552', r'D:\\', r'C:\Python*', r'C:\Users\10552\miniconda*', r'C:\Users\10552\anaconda*', r'C:\Users\10552\.conda']:
    pass
# faster: common paths
paths=[
 r'E:\envolution\.venv\Scripts\python.exe',
 r'E:\envolution\venv\Scripts\python.exe',
 r'E:\envolution\.conda\python.exe',
 r'C:\Users\10552\miniconda3\python.exe',
 r'C:\Users\10552\anaconda3\python.exe',
 r'C:\Users\10552\AppData\Local\Programs\Python\Python311\python.exe',
 r'C:\Users\10552\AppData\Local\Programs\Python\Python312\python.exe',
 r'C:\Users\10552\AppData\Local\Programs\Python\Python310\python.exe',
]
import pathlib
for p in paths:
    if pathlib.Path(p).exists():
        print('exists', p)
# search torch in site-packages under user
for p in pathlib.Path(r'C:\Users\10552').glob('**/torch/__init__.py'):
    print('torch', p)
    if len(list(pathlib.Path(r'C:\Users\10552').glob('**/torch/__init__.py')))>20:
        break
