# importing setup from setup tools
from setuptools import setup

setup(
   name='cvpackage',
   packages=['cvpackage'],
   version='0.0.2',
   license='MIT',
   description='An helper library for openCv developer.',
   author='Kartik Panchal',
   author_email='clickshare07@gmail.com',
   url='https://github.com/MrBucks07/CvPack',
   keywords=['MediaPipe', 'FaceMesh', 'FaceDetection', 'HandTracking', 'HandModule', 'FaceModule'],
   install_requires=[
      'opencv-python',
      'mediapipe'
   ],
   classifiers=[
      'License :: OSI Approved :: MIT License',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
      'Operating System :: OS Independent'
    ],
)
