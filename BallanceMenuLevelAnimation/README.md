# README

This folder contains the animation data of Ballance MenuLevel stone ball.

The animation is split into 3 files, position, rotation and scale. The coordinate system of these file is Virtools based. Please do convertion before using it in another 3D software. Position and scale are axis based value and rotation is quaternions.

These animation are stored as binary file because it consume less memory and can exactly reflect underlying data because there must be precision bias if converting data to corresponding ASCII representation. But ASCII, or a CSV file is easy to read and view so we create an assistant Python script to help you convert them into equvalent CSV files. At the same time, the layout of these binary also is presented by this convertion script.
