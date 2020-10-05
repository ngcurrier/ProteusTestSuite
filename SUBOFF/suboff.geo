// This is the geometry for the SUBOFF body found here 
// https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/ADA210642.xhtml

cellSize = 0.01;
Rmax = 5.0/6.0;

// create points 0 to 100
// forebody equation 0 ft to 3.333333 ft
// r = Rmax*(1.126395101*x*(0.3*x-1)^4 + 0.442874707*x^2*(0.3*x-1)3 + 1-(0.3*x-1)^4*(1.2*x + 1))^(1/2.1)
For k In {0:100:1}
    step = 3.33333/100.0;
    x = k*3.333333/100.0;
    r = Rmax*(1.126395101*x*(0.3*x-1.0)^4.0 + 0.442874707*x^2.0*(0.3*x-1.0)^3.0 + 1.0-(0.3*x-1.0)^4*(1.2*x + 1.0))^(1.0/2.1); 
    Point(k) = {x,r,0,cellSize};
EndFor

// create point 101
// middlebody equation 3.333333 ft to 10.645833 ft
// r = Rmax
Point(101) = {10.645833, Rmax, 0.0, cellSize};


// create point 102 to 201
// afterbody equation 10.645833 ft to 13.979167 ft
rh = 0.1175;
K0 = 10;
K1 = 44.6244;
For k In {0.1:100:1}
    x = k*(13.979167-10.645833)/100.0 + 10.645833;
    E = (13.979167 - x)/3.333333;
    r = Rmax * (rh^2 + rh*K0*E^2 + (20.0 - 20.0*rh^2 - 4.0*rh*K0 - 1.0/3.0*K1)*E^3 + (-45.0 + 45.0*rh^2 + 6.0*rh*K0 + K1)*E^4 + (36.0 - 36.0*rh^2 - 4.0*rh*K0 - K1)*E^5 + (-10.0 + 10.0*rh^2 + rh*K0 + 1.0/3.0*K1)*E^6)^0.5;
    Point(k+102) = {x,r,0,cellSize};
EndFor

// create points 203 to 304
// afterbody cap 13.979167 ft to 14.291667 ft
// r = 0.1175 Rmax * (1.0 - (3.2*x - 44.733333)^2.0)^0.5
For k In{0:100:1}
    x = k*(14.291667 - 13.979167)/100.0 + 13.979167;
    r = 0.1175*Rmax*(1.0 - (3.2*x - 44.733333)^2)^0.5;
    Point(k+202) = {x,r,0,cellSize};
EndFor

Spline(501) = {0:100};
Spline(502) = {100:101};
Spline(503) = {101:201};
Spline(504) = {201:302};
//+
Extrude {{1, 0, 0}, {0, 0, 0}, Pi/2} {
  Curve{501}; 
}
