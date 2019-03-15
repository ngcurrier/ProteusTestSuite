NoseRadius = 0.579;
h = 0.3;
hfar = 5.0;


NoseInflowStandoff = NoseRadius*20.0;
TailOutletStandoff = NoseRadius*100.0;
RadialStandoff = 50.0*NoseRadius;

// compute the x,y tangent line nose intercept
Cone1AngDeg = 12.84;
Cone1AngRad = Cone1AngDeg*Pi/180.0;
ComplCone1AngRad = Pi*0.5 - Cone1AngRad;
xint = NoseRadius - Cos(ComplCone1AngRad)*NoseRadius;
yint = Sin(ComplCone1AngRad)*NoseRadius;

//+ Create the nose geometry
Point(1) = {0, 0, 0, h};
Point(2) = {xint, yint, 0, h};
Point(3) = {NoseRadius, 0, 0, h};
Circle(1) = {1, 3, 2};


//+ Create first conic section
// Distance from end of nose radius to stop of first conic
Dist1 = 18.017*NoseRadius - xint;
Point(4) = {xint + Dist1, yint + Dist1*Tan(Cone1AngRad), 0, h};
Line(2) = {2, 4};

//+ Create second conic section
Cone2AngDeg = 7.0;
Cone2AngRad = Cone2AngDeg*Pi/180.0;
// Distance from end of first conic to stop of second conic
Dist2 = 31.67*NoseRadius - xint - Dist1;
TailX = xint + Dist1 + Dist2;
Point(5) = {TailX, yint + Dist1*Tan(Cone1AngRad) + Dist2*Tan(Cone2AngRad), 0, h}; 
Line(3) = {4, 5};


Point(6) = {xint + Dist1 + Dist2, 0, 0, h};
Line(4) = {5,6};

//+ Extrude surface rotation in 4 steps to prevent degeneracy
Extrude {{1, 0, 0}, {0, 0, 0}, Pi/2} {
  Curve{1}; Curve{2}; Curve{3}; Curve{4}; 
}
Extrude {{1, 0, 0}, {0, 0, 0}, Pi/2} {
  Curve{5}; Curve{8}; Curve{12}; Curve{16};
}
Extrude {{1, 0, 0}, {0, 0, 0}, Pi/2} {
  Curve{19}; Curve{22}; Curve{26}; Curve{30};
}
Extrude {{1, 0, 0}, {0, 0, 0}, Pi/2} {
  Curve{33}; Curve{36}; Curve{40}; Curve{44};
}

//+ Create a named surface from all current faces
Physical Surface("BiConic") = {21, 35, 7, 49, 25, 39, 11, 53, 29, 32, 43, 15, 18, 46, 57, 60};

//+ Create bounding box
Point(61) = {-NoseInflowStandoff, RadialStandoff, RadialStandoff, hfar};
Point(62) = {-NoseInflowStandoff, RadialStandoff, -RadialStandoff, hfar};
Point(63) = {-NoseInflowStandoff, -RadialStandoff, RadialStandoff, hfar};
Point(64) = {-NoseInflowStandoff, -RadialStandoff,-RadialStandoff, hfar};
Line(65) = {61,63};
Line(66) = {63,64};
Line(67) = {64,62};
Line(68) = {62,61};


//+ Create walls
Extrude {(TailOutletStandoff + TailX), 0, 0} {
  Curve{68}; Curve{65}; Curve{66}; Curve{67}; 
}
Physical Surface("Walls") = {80, 76, 72, 84};

//+ Create inlet and outlet surfaces
Curve Loop(1) = {67, 68, 65, 66};
Plane Surface(85) = {1};
Curve Loop(2) = {69, 73, 77, 81};
Plane Surface(86) = {2};

Physical Surface("Inlet") = {85};
Physical Surface("Outlet") = {86};


//+ Create interior volume
Surface Loop(1) = {84, 85, 72, 76, 80, 86, 43, 29, 15, 57, 60, 18, 32, 46, 53, 39, 25, 11, 7, 49, 35, 21};
Volume(1) = {1};
Physical Volume("Volume") = {1};
