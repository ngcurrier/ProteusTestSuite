h = 0.1;
//+
Point(1) = {-0.5, -0.5, 0, h};
Point(2) = {-0.5, 0.5, 0, h};
Point(3) = {0.5, 0.5, 0, h};
Point(4) = {0.5, -0.5, 0, h};
//+
Line(1) = {2, 3};
//+
Line(2) = {3, 4};
//+
Line(3) = {4, 1};
//+
Line(4) = {2, 1};
//+
Curve Loop(1) = {1, 2, 3, -4};
//+
Plane Surface(1) = {1};
//+
Extrude {0, 0, 4} {
  Surface{1}; Layers{300}; Recombine;
}
//+
Physical Surface("Walls") = {25, 13, 17, 21};
//+
Physical Surface("Outlet") = {26};
//+
Physical Surface("Inlet") = {1};
