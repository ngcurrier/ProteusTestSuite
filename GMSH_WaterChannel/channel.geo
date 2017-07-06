cl__1 = 1;
Point(1) = {0, 0, 0, 1};
Point(2) = {0, 1, 0, 1};
Point(3) = {0, 1, 1, 1};
Point(4) = {0, 0, 1, 1};
Point(5) = {10, 0, 0, 1};
Point(6) = {10, 1, 0, 1};
Point(7) = {10, 1, 1, 1};
Point(8) = {10, 0, 1, 1};
Line(1) = {3, 7};
Line(2) = {6, 2};
Line(3) = {1, 5};
Line(4) = {8, 4};
Line(5) = {4, 1};
Line(6) = {1, 2};
Line(7) = {2, 3};
Line(8) = {3, 4};
Line(9) = {8, 7};
Line(10) = {7, 6};
Line(11) = {6, 5};
Line(12) = {5, 8};
Line Loop(14) = {2, 7, 1, 10};
Plane Surface(14) = {14};
Line Loop(16) = {11, -3, 6, -2};
Plane Surface(16) = {16};
Line Loop(18) = {10, 11, 12, 9};
Plane Surface(18) = {18};
Line Loop(20) = {8, 5, 6, 7};
Plane Surface(20) = {20};
Line Loop(22) = {3, 12, 4, 5};
Plane Surface(22) = {22};
Line Loop(24) = {1, -9, 4, -8};
Plane Surface(24) = {24};
Surface Loop(29) = {16, 18, 14, 20, 24, 22};
Volume(30) = {29};
Coherence;

Physical Volume(31) = {30};
Physical Surface(32) = {14};
Physical Surface(33) = {24};
Physical Surface(34) = {16};
Physical Surface(35) = {22};
Physical Surface(36) = {20};
Physical Surface(37) = {18};
32 = DefineNumber[ 32, Name "Parameters/32" ];
Surf32 = DefineNumber[ 32, Name "Parameters/Surf32" ];