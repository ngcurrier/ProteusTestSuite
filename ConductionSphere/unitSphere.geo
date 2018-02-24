// Gmsh project created on Fri Feb 23 17:48:38 2018
//+
SetFactory("OpenCASCADE");
Sphere(1) = {0, 0, 0, 0.5, -Pi/2, Pi/2, 2*Pi};
//+
Physical Surface("Surface") = {1};
//+
Physical Volume("Sphere") = {1};
