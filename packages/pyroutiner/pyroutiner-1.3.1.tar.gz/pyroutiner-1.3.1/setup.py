from distutils.core import setup, Extension

routiner = Extension('pyroutiner',
                    sources = ['pyrt.c', 'pyrtr.c'],
                    )

setup (name = 'pyroutiner',
       version = '1.3.1',
       author='Shrishak Bhattarai',
       author_email='bshrishak9@gmail.com',
       url='https://github.com/bshrishak9/Routiner',
       description = 'Routine Generating Algorithm',
       classifiers=[
       "Programming Language :: Python :: Implementation :: CPython", 
       'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
       ],
       ext_modules = [routiner])
