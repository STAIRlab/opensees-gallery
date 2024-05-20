from math import cos,sin,sqrt,pi
import opensees.openseespy as ops
#######################################################################
#
#  Excavation of cohesionless soil supported by a cantilevered sheet
#  pile wall.  2D Plane Strain analysis.  Beam elements define the
#  wall, and beam-contact elements are used to create a frictional
#  soil-pile interface. Initial state analysis is used to create
#  an initial state of stress and strain due to gravity without the
#  corresponding displacements.
#
#   Created by:  Chris McGann
#                Pedro Arduino
#              --University of Washington--
#
# ---> Basic units are kN and m
#
#######################################################################


# outDir = ./out/
# file, 'mkdir', outDir
#-----------------------------------------------------------------------------------------
#  1. CREATE SOIL NODES AND FIXITIES
#-----------------------------------------------------------------------------------------
model = ops.Model( ndm=2,  ndf=2)

# define soil nodes
model.node(       1,     -5.250, 0.000)
model.node(       2,     -5.250, 0.500)
model.node(       3,     -4.750, 0.000)
model.node(       4,     -4.750, 0.500)
model.node(       5,     -4.250, 0.000)
model.node(       6,     -5.250, 1.000)
model.node(       7,     -4.750, 1.000)
model.node(       8,     -4.250, 0.500)
model.node(       9,     -4.250, 1.000)
model.node(      10,     -5.250, 1.500)
model.node(      11,     -3.750, 0.000)
model.node(      12,     -4.750, 1.500)
model.node(      13,     -3.750, 0.500)
model.node(      14,     -3.750, 1.000)
model.node(      15,     -4.250, 1.500)
model.node(      16,     -3.250, 0.000)
model.node(      17,     -5.250, 2.000)
model.node(      18,     -4.750, 2.000)
model.node(      19,     -3.250, 0.500)
model.node(      20,     -3.750, 1.500)
model.node(      21,     -3.250, 1.000)
model.node(      22,     -4.250, 2.000)
model.node(      23,     -5.250, 2.500)
model.node(      24,     -2.750, 0.000)
model.node(      25,     -3.250, 1.500)
model.node(      26,     -3.750, 2.000)
model.node(      27,     -4.750, 2.500)
model.node(      28,     -2.750, 0.500)
model.node(      29,     -4.250, 2.500)
model.node(      30,     -2.750, 1.000)
model.node(      31,     -3.250, 2.000)
model.node(      32,     -3.750, 2.500)
model.node(      33,     -2.750, 1.500)
model.node(      34,     -5.250, 3.000)
model.node(      35,     -2.250, 0.000)
model.node(      36,     -4.750, 3.000)
model.node(      37,     -2.250, 0.500)
model.node(      38,     -4.250, 3.000)
model.node(      39,     -2.250, 1.000)
model.node(      40,     -3.250, 2.500)
model.node(      41,     -2.750, 2.000)
model.node(      42,     -3.750, 3.000)
model.node(      43,     -2.250, 1.500)
model.node(      44,     -5.250, 3.500)
model.node(      45,     -1.750, 0.000)
model.node(      46,     -2.750, 2.500)
model.node(      47,     -4.750, 3.500)
model.node(      48,     -1.750, 0.500)
model.node(      49,     -2.250, 2.000)
model.node(      50,     -3.250, 3.000)
model.node(      51,     -1.750, 1.000)
model.node(      52,     -4.250, 3.500)
model.node(      53,     -3.750, 3.500)
model.node(      54,     -1.750, 1.500)
model.node(      55,     -2.250, 2.500)
model.node(      56,     -2.750, 3.000)
model.node(      57,     -5.250, 4.000)
model.node(      58,     -1.250, 0.000)
model.node(      59,     -1.250, 0.500)
model.node(      60,     -4.750, 4.000)
model.node(      61,     -1.750, 2.000)
model.node(      62,     -3.250, 3.500)
model.node(      63,     -4.250, 4.000)
model.node(      64,     -1.250, 1.000)
model.node(      65,     -2.250, 3.000)
model.node(      66,     -3.750, 4.000)
model.node(      67,     -1.250, 1.500)
model.node(      68,     -1.750, 2.500)
model.node(      69,     -2.750, 3.500)
model.node(      70,     -1.250, 2.000)
model.node(      71,     -3.250, 4.000)
model.node(      72,     -0.750, 0.000)
model.node(      73,     -5.250, 4.500)
model.node(      74,     -4.750, 4.500)
model.node(      75,     -0.750, 0.500)
model.node(      76,     -4.250, 4.500)
model.node(      77,     -1.750, 3.000)
model.node(      78,     -2.250, 3.500)
model.node(      79,     -0.750, 1.000)
model.node(      80,     -1.250, 2.500)
model.node(      81,     -2.750, 4.000)
model.node(      82,     -3.750, 4.500)
model.node(      83,     -0.750, 1.500)
model.node(      84,     -0.750, 2.000)
model.node(      85,     -3.250, 4.500)
model.node(      86,     -1.750, 3.500)
model.node(      87,     -5.250, 5.000)
model.node(      88,     -0.250, 0.000)
model.node(      89,     -1.250, 3.000)
model.node(      90,     -2.250, 4.000)
model.node(      91,     -4.750, 5.000)
model.node(      92,     -0.250, 0.500)
model.node(      93,     -0.250, 1.000)
model.node(      94,     -4.250, 5.000)
model.node(      95,     -0.750, 2.500)
model.node(      96,     -2.750, 4.500)
model.node(      97,     -3.750, 5.000)
model.node(      98,     -0.250, 1.500)
model.node(     102,     -1.750, 4.000)
model.node(     103,     -1.250, 3.500)
model.node(     104,     -3.250, 5.000)
model.node(     105,     -0.250, 2.000)
model.node(     107,     -0.750, 3.000)
model.node(     108,     -2.250, 4.500)
model.node(     109,      0.250, 0.000)
model.node(     110,     -5.250, 5.500)
model.node(     111,     -4.750, 5.500)
model.node(     112, 0.250, 0.500)
model.node(     114,     -2.750, 5.000)
model.node(     115,     -0.250, 2.500)
model.node(     116, 0.250, 1.000)
model.node(     117,     -4.250, 5.500)
model.node(     118,     -1.250, 4.000)
model.node(     119, 0.250, 1.500)
model.node(     120,     -3.750, 5.500)
model.node(     121,     -1.750, 4.500)
model.node(     122,     -0.750, 3.500)
model.node(     124,     -2.250, 5.000)
model.node(     125,     -0.250, 3.000)
model.node(     126,      0.250, 2.000)
model.node(     127,     -3.250, 5.500)
model.node(     129,     -5.250, 6.000)
model.node(     130,      0.750, 0.000)
model.node(     131,      0.750, 0.500)
model.node(     132,     -1.250, 4.500)
model.node(     133,     -4.750, 6.000)
model.node(     134,     -0.750, 4.000)
model.node(     135, 0.250, 2.500)
model.node(     136,     -2.750, 5.500)
model.node(     137,     -4.250, 6.000)
model.node(     138, 0.750, 1.000)
model.node(     139,     -0.250, 3.500)
model.node(     140,     -1.750, 5.000)
model.node(     142,     -3.750, 6.000)
model.node(     143, 0.750, 1.500)
model.node(     144, 0.250, 3.000)
model.node(     145,     -2.250, 5.500)
model.node(     146, 0.750, 2.000)
model.node(     147,     -3.250, 6.000)
model.node(     148,     -0.750, 4.500)
model.node(     149,     -1.250, 5.000)
model.node(     150,     -0.250, 4.000)
model.node(     152, 1.250, 0.000)
model.node(     153, 0.750, 2.500)
model.node(     154,     -5.250, 6.500)
model.node(     155,     -2.750, 6.000)
model.node(     156,     -4.750, 6.500)
model.node(     157, 1.250, 0.500)
model.node(     158, 0.250, 3.500)
model.node(     159,     -1.750, 5.500)
model.node(     160,     -4.250, 6.500)
model.node(     161, 1.250, 1.000)
model.node(     162, 1.250, 1.500)
model.node(     163,     -3.750, 6.500)
model.node(     164, 0.750, 3.000)
model.node(     165,     -2.250, 6.000)
model.node(     166,     -0.250, 4.500)
model.node(     167,     -0.750, 5.000)
model.node(     169,     -3.250, 6.500)
model.node(     170, 1.250, 2.000)
model.node(     171, 0.250, 4.000)
model.node(     172,     -1.250, 5.500)
model.node(     173, 0.750, 3.500)
model.node(     174,     -1.750, 6.000)
model.node(     175,     -2.750, 6.500)
model.node(     176, 1.250, 2.500)
model.node(     177,     -5.250, 7.000)
model.node(     178, 1.750, 0.000)
model.node(     179,     -4.750, 7.000)
model.node(     180, 1.750, 0.500)
model.node(     181, 1.750, 1.000)
model.node(     182,     -0.250, 5.000)
model.node(     183,     -4.250, 7.000)
model.node(     185, 0.250, 4.500)
model.node(     186,     -0.750, 5.500)
model.node(     187, 1.750, 1.500)
model.node(     188,     -2.250, 6.500)
model.node(     189, 1.250, 3.000)
model.node(     190,     -3.750, 7.000)
model.node(     191, 0.750, 4.000)
model.node(     192,     -1.250, 6.000)
model.node(     193, 1.750, 2.000)
model.node(     194,     -3.250, 7.000)
model.node(     195,     -1.750, 6.500)
model.node(     196, 1.250, 3.500)
model.node(     198, 1.750, 2.500)
model.node(     199,     -0.250, 5.500)
model.node(     200, 0.250, 5.000)
model.node(     201,     -2.750, 7.000)
model.node(     202,     -0.750, 6.000)
model.node(     203, 0.750, 4.500)
model.node(     204,     -5.250, 7.500)
model.node(     205, 2.250, 0.000)
model.node(     206,     -4.750, 7.500)
model.node(     207, 2.250, 0.500)
model.node(     208,     -4.250, 7.500)
model.node(     209, 2.250, 1.000)
model.node(     210, 1.750, 3.000)
model.node(     211,     -2.250, 7.000)
model.node(     212, 1.250, 4.000)
model.node(     213,     -1.250, 6.500)
model.node(     214, 2.250, 1.500)
model.node(     215,     -3.750, 7.500)
model.node(     216,     -3.250, 7.500)
model.node(     217, 2.250, 2.000)
model.node(     218, 0.250, 5.500)
model.node(     220, 0.750, 5.000)
model.node(     221,     -0.250, 6.000)
model.node(     222,     -1.750, 7.000)
model.node(     223, 1.750, 3.500)
model.node(     224,     -0.750, 6.500)
model.node(     225, 1.250, 4.500)
model.node(     226,     -2.750, 7.500)
model.node(     227, 2.250, 2.500)
model.node(     228,     -5.250, 8.000)
model.node(     229, 2.750, 0.000)
model.node(     230,     -4.750, 8.000)
model.node(     231, 2.750, 0.500)
model.node(     232,     -4.250, 8.000)
model.node(     233, 2.750, 1.000)
model.node(     234, 1.750, 4.000)
model.node(     235,     -1.250, 7.000)
model.node(     236,     -2.250, 7.500)
model.node(     237, 2.250, 3.000)
model.node(     238,     -3.750, 8.000)
model.node(     239, 0.750, 5.500)
model.node(     240, 2.750, 1.500)
model.node(     241, 0.250, 6.000)
model.node(     243, 1.250, 5.000)
model.node(     244,     -0.250, 6.500)
model.node(     245, 2.750, 2.000)
model.node(     246,     -3.250, 8.000)
model.node(     247,     -1.750, 7.500)
model.node(     248, 2.250, 3.500)
model.node(     249,     -0.750, 7.000)
model.node(     250, 1.750, 4.500)
model.node(     251,     -2.750, 8.000)
model.node(     252, 2.750, 2.500)
model.node(     253, 0.750, 6.000)
model.node(     254, 2.250, 4.000)
model.node(     255,     -5.250, 8.500)
model.node(     256, 3.250, 0.000)
model.node(     257,     -1.250, 7.500)
model.node(     258,     -4.750, 8.500)
model.node(     259, 1.250, 5.500)
model.node(     260, 0.250, 6.500)
model.node(     261, 3.250, 0.500)
model.node(     262,     -2.250, 8.000)
model.node(     263, 2.750, 3.000)
model.node(     265,     -4.250, 8.500)
model.node(     266, 3.250, 1.000)
model.node(     267,     -0.250, 7.000)
model.node(     268, 1.750, 5.000)
model.node(     269,     -3.750, 8.500)
model.node(     270, 3.250, 1.500)
model.node(     271,     -3.250, 8.500)
model.node(     272,     -1.750, 8.000)
model.node(     273, 3.250, 2.000)
model.node(     274, 2.750, 3.500)
model.node(     275, 2.250, 4.500)
model.node(     276,     -0.750, 7.500)
model.node(     277, 1.250, 6.000)
model.node(     278, 0.750, 6.500)
model.node(     279,     -2.750, 8.500)
model.node(     280, 3.250, 2.500)
model.node(     281, 0.250, 7.000)
model.node(     282, 1.750, 5.500)
model.node(     283,     -1.250, 8.000)
model.node(     284, 2.750, 4.000)
model.node(     286, 3.750, 0.000)
model.node(     287,     -5.250, 9.000)
model.node(     288,     -4.750, 9.000)
model.node(     289,     -2.250, 8.500)
model.node(     290, 2.250, 5.000)
model.node(     291,     -0.250, 7.500)
model.node(     292, 3.250, 3.000)
model.node(     293, 3.750, 0.500)
model.node(     294,     -4.250, 9.000)
model.node(     295, 3.750, 1.000)
model.node(     296,     -3.750, 9.000)
model.node(     297, 3.750, 1.500)
model.node(     298,     -0.750, 8.000)
model.node(     299, 2.750, 4.500)
model.node(     300,     -1.750, 8.500)
model.node(     301, 3.250, 3.500)
model.node(     302, 1.250, 6.500)
model.node(     303, 3.750, 2.000)
model.node(     304, 0.750, 7.000)
model.node(     305,     -3.250, 9.000)
model.node(     306, 1.750, 6.000)
model.node(     307, 2.250, 5.500)
model.node(     308, 0.250, 7.500)
model.node(     309, 3.750, 2.500)
model.node(     310,     -2.750, 9.000)
model.node(     312, 3.250, 4.000)
model.node(     313,     -1.250, 8.500)
model.node(     314, 2.750, 5.000)
model.node(     315,     -0.250, 8.000)
model.node(     316, 3.750, 3.000)
model.node(     317,     -2.250, 9.000)
model.node(     318,     -5.250, 9.500)
model.node(     319, 4.250, 0.000)
model.node(     320,     -4.750, 9.500)
model.node(     321, 4.250, 0.500)
model.node(     322, 1.250, 7.000)
model.node(     323,     -4.250, 9.500)
model.node(     324, 4.250, 1.000)
model.node(     325, 1.750, 6.500)
model.node(     326, 0.750, 7.500)
model.node(     327, 2.250, 6.000)
model.node(     328,     -0.750, 8.500)
model.node(     329, 3.250, 4.500)
model.node(     330, 4.250, 1.500)
model.node(     331,     -3.750, 9.500)
model.node(     332,     -1.750, 9.000)
model.node(     333, 3.750, 3.500)
model.node(     334, 4.250, 2.000)
model.node(     335, 2.750, 5.500)
model.node(     336, 0.250, 8.000)
model.node(     337,     -3.250, 9.500)
model.node(     339, 4.250, 2.500)
model.node(     340,     -2.750, 9.500)
model.node(     341, 3.750, 4.000)
model.node(     342,     -1.250, 9.000)
model.node(     343, 3.250, 5.000)
model.node(     344,     -0.250, 8.500)
model.node(     345, 1.750, 7.000)
model.node(     346, 2.250, 6.500)
model.node(     347, 1.250, 7.500)
model.node(     348, 4.250, 3.000)
model.node(     349,     -2.250, 9.500)
model.node(     350, 2.750, 6.000)
model.node(     351,     -5.250, 10.000)
model.node(     352, 4.750, 0.000)
model.node(     353, 0.750, 8.000)
model.node(     354,     -4.750, 10.000)
model.node(     355, 4.750, 0.500)
model.node(     356, 4.750, 1.000)
model.node(     357,     -4.250, 10.000)
model.node(     358, 3.750, 4.500)
model.node(     359,     -0.750, 9.000)
model.node(     360,     -3.750, 10.000)
model.node(     361, 4.750, 1.500)
model.node(     362, 4.250, 3.500)
model.node(     363, 0.250, 8.500)
model.node(     364, 3.250, 5.500)
model.node(     365,     -1.750, 9.500)
model.node(     366,     -3.250, 10.000)
model.node(     367, 4.750, 2.000)
model.node(     369, 1.750, 7.500)
model.node(     370, 2.250, 7.000)
model.node(     371, 3.750, 5.000)
model.node(     372,     -0.250, 9.000)
model.node(     373, 4.750, 2.500)
model.node(     374, 2.750, 6.500)
model.node(     375,     -1.250, 9.500)
model.node(     376,     -2.750, 10.000)
model.node(     377, 4.250, 4.000)
model.node(     378, 1.250, 8.000)
model.node(     379, 3.250, 6.000)
model.node(     380, 0.750, 8.500)
model.node(     381, 4.750, 3.000)
model.node(     382,     -2.250, 10.000)
model.node(     383, 5.250, 0.000)
model.node(     384, 4.250, 4.500)
model.node(     385, 5.250, 0.500)
model.node(     386,     -0.750, 9.500)
model.node(     387, 0.250, 9.000)
model.node(     388, 5.250, 1.000)
model.node(     389, 3.750, 5.500)
model.node(     390, 4.750, 3.500)
model.node(     391,     -1.750, 10.000)
model.node(     392, 2.250, 7.500)
model.node(     393, 5.250, 1.500)
model.node(     394, 2.750, 7.000)
model.node(     395, 1.750, 8.000)
model.node(     397, 5.250, 2.000)
model.node(     398, 1.250, 8.500)
model.node(     399, 3.250, 6.500)
model.node(     400,     -0.250, 9.500)
model.node(     401, 4.250, 5.000)
model.node(     402,     -1.250, 10.000)
model.node(     403, 4.750, 4.000)
model.node(     404, 5.250, 2.500)
model.node(     405, 0.750, 9.000)
model.node(     406, 3.750, 6.000)
model.node(     407, 5.250, 3.000)
model.node(     408, 2.750, 7.500)
model.node(     409, 4.750, 4.500)
model.node(     410,     -0.750, 10.000)
model.node(     411, 2.250, 8.000)
model.node(     412, 0.250, 9.500)
model.node(     413, 4.250, 5.500)
model.node(     414, 1.750, 8.500)
model.node(     415, 3.250, 7.000)
model.node(     416, 5.250, 3.500)
model.node(     418, 1.250, 9.000)
model.node(     419, 3.750, 6.500)
model.node(     420, 4.750, 5.000)
model.node(     421,     -0.250, 10.000)
model.node(     422, 4.250, 6.000)
model.node(     423, 5.250, 4.000)
model.node(     424, 0.750, 9.500)
model.node(     425, 2.750, 8.000)
model.node(     426, 3.250, 7.500)
model.node(     427, 2.250, 8.500)
model.node(     428, 3.750, 7.000)
model.node(     429, 1.750, 9.000)
model.node(     430, 0.250, 10.000)
model.node(     431, 4.750, 5.500)
model.node(     432, 5.250, 4.500)
model.node(     433, 1.250, 9.500)
model.node(     434, 4.250, 6.500)
model.node(     436, 5.250, 5.000)
model.node(     437, 0.750, 10.000)
model.node(     438, 4.750, 6.000)
model.node(     439, 2.750, 8.500)
model.node(     440, 3.250, 8.000)
model.node(     441, 3.750, 7.500)
model.node(     442, 2.250, 9.000)
model.node(     443, 4.250, 7.000)
model.node(     444, 1.750, 9.500)
model.node(     445, 5.250, 5.500)
model.node(     446, 1.250, 10.000)
model.node(     447, 4.750, 6.500)
model.node(     448, 3.250, 8.500)
model.node(     449, 3.750, 8.000)
model.node(     450, 2.750, 9.000)
model.node(     451, 5.250, 6.000)
model.node(     452, 4.250, 7.500)
model.node(     453, 2.250, 9.500)
model.node(     454, 4.750, 7.000)
model.node(     455, 1.750, 10.000)
model.node(     456, 5.250, 6.500)
model.node(     457, 3.750, 8.500)
model.node(     458, 3.250, 9.000)
model.node(     459, 4.250, 8.000)
model.node(     460, 2.750, 9.500)
model.node(     461, 2.250, 10.000)
model.node(     462, 4.750, 7.500)
model.node(     463, 5.250, 7.000)
model.node(     464, 3.750, 9.000)
model.node(     465, 4.250, 8.500)
model.node(     466, 3.250, 9.500)
model.node(     467, 4.750, 8.000)
model.node(     468, 2.750, 10.000)
model.node(     469, 5.250, 7.500)
model.node(     470, 4.250, 9.000)
model.node(     471, 3.750, 9.500)
model.node(     472, 4.750, 8.500)
model.node(     473, 3.250, 10.000)
model.node(     474, 5.250, 8.000)
model.node(     475, 4.250, 9.500)
model.node(     476, 3.750, 10.000)
model.node(     477, 4.750, 9.000)
model.node(     478, 5.250, 8.500)
model.node(     479, 4.750, 9.500)
model.node(     480, 4.250, 10.000)
model.node(     481, 5.250, 9.000)
model.node(     482, 4.750, 10.000)
model.node(     483, 5.250, 9.500)
model.node(     484, 5.250, 10.000)
print("Finished creating all -ndf 2 soil nodes...")

# define fixities for soil nodes
model.fix(    1, 1,  1)
model.fix(    2, 1,  0)
model.fix(    3, 0,  1)
model.fix(    5, 0,  1)
model.fix(    6, 1,  0)
model.fix(   10, 1,  0)
model.fix(   11, 0,  1)
model.fix(   16, 0,  1)
model.fix(   17, 1,  0)
model.fix(   23, 1,  0)
model.fix(   24, 0,  1)
model.fix(   34, 1,  0)
model.fix(   35, 0,  1)
model.fix(   44, 1,  0)
model.fix(   45, 0,  1)
model.fix(   57, 1,  0)
model.fix(   58, 0,  1)
model.fix(   72, 0,  1)
model.fix(   73, 1,  0)
model.fix(   87, 1,  0)
model.fix(   88, 0,  1)
model.fix(  109, 0,  1)
model.fix(  110, 1,  0)
model.fix(  129, 1,  0)
model.fix(  130, 0,  1)
model.fix(  152, 0,  1)
model.fix(  154, 1,  0)
model.fix(  177, 1,  0)
model.fix(  178, 0,  1)
model.fix(  204, 1,  0)
model.fix(  205, 0,  1)
model.fix(  228, 1,  0)
model.fix(  229, 0,  1)
model.fix(  255, 1,  0)
model.fix(  256, 0,  1)
model.fix(  286, 0,  1)
model.fix(  287, 1,  0)
model.fix(  318, 1,  0)
model.fix(  319, 0,  1)
model.fix(  351, 1,  0)
model.fix(  352, 0,  1)
model.fix(  383, 1,  1)
model.fix(  385, 1,  0)
model.fix(  388, 1,  0)
model.fix(  393, 1,  0)
model.fix(  397, 1,  0)
model.fix(  404, 1,  0)
model.fix(  407, 1,  0)
model.fix(  416, 1,  0)
model.fix(  423, 1,  0)
model.fix(  432, 1,  0)
model.fix(  436, 1,  0)
model.fix(  445, 1,  0)
model.fix(  451, 1,  0)
model.fix(  456, 1,  0)
model.fix(  463, 1,  0)
model.fix(  469, 1,  0)
model.fix(  474, 1,  0)
model.fix(  478, 1,  0)
model.fix(  481, 1,  0)
model.fix(  483, 1,  0)
model.fix(  484, 1,  0)
print("Finished creating all -ndf 2 boundary conditions...")

#-----------------------------------------------------------------------------------------
#  2. DESIGNATE LIST OF PERMANENT NODES (NEVER REMOVED) FOR RECORDERS
#-----------------------------------------------------------------------------------------

mNodeInfo = [open, outDir/NodesInfoPerm.dat, 'w]'
puts mNodeInfo "       1      -5.250      0.000"
puts mNodeInfo "       2      -5.250      0.500"
puts mNodeInfo "       3      -4.750      0.000"
puts mNodeInfo "       4      -4.750      0.500"
puts mNodeInfo "       5      -4.250      0.000"
puts mNodeInfo "       6      -5.250      1.000"
puts mNodeInfo "       7      -4.750      1.000"
puts mNodeInfo "       8      -4.250      0.500"
puts mNodeInfo "       9      -4.250      1.000"
puts mNodeInfo "      10      -5.250      1.500"
puts mNodeInfo "      11      -3.750      0.000"
puts mNodeInfo "      12      -4.750      1.500"
puts mNodeInfo "      13      -3.750      0.500"
puts mNodeInfo "      14      -3.750      1.000"
puts mNodeInfo "      15      -4.250      1.500"
puts mNodeInfo "      16      -3.250      0.000"
puts mNodeInfo "      17      -5.250      2.000"
puts mNodeInfo "      18      -4.750      2.000"
puts mNodeInfo "      19      -3.250      0.500"
puts mNodeInfo "      20      -3.750      1.500"
puts mNodeInfo "      21      -3.250      1.000"
puts mNodeInfo "      22      -4.250      2.000"
puts mNodeInfo "      23      -5.250      2.500"
puts mNodeInfo "      24      -2.750      0.000"
puts mNodeInfo "      25      -3.250      1.500"
puts mNodeInfo "      26      -3.750      2.000"
puts mNodeInfo "      27      -4.750      2.500"
puts mNodeInfo "      28      -2.750      0.500"
puts mNodeInfo "      29      -4.250      2.500"
puts mNodeInfo "      30      -2.750      1.000"
puts mNodeInfo "      31      -3.250      2.000"
puts mNodeInfo "      32      -3.750      2.500"
puts mNodeInfo "      33      -2.750      1.500"
puts mNodeInfo "      34      -5.250      3.000"
puts mNodeInfo "      35      -2.250      0.000"
puts mNodeInfo "      36      -4.750      3.000"
puts mNodeInfo "      37      -2.250      0.500"
puts mNodeInfo "      38      -4.250      3.000"
puts mNodeInfo "      39      -2.250      1.000"
puts mNodeInfo "      40      -3.250      2.500"
puts mNodeInfo "      41      -2.750      2.000"
puts mNodeInfo "      42      -3.750      3.000"
puts mNodeInfo "      43      -2.250      1.500"
puts mNodeInfo "      44      -5.250      3.500"
puts mNodeInfo "      45      -1.750      0.000"
puts mNodeInfo "      46      -2.750      2.500"
puts mNodeInfo "      47      -4.750      3.500"
puts mNodeInfo "      48      -1.750      0.500"
puts mNodeInfo "      49      -2.250      2.000"
puts mNodeInfo "      50      -3.250      3.000"
puts mNodeInfo "      51      -1.750      1.000"
puts mNodeInfo "      52      -4.250      3.500"
puts mNodeInfo "      53      -3.750      3.500"
puts mNodeInfo "      54      -1.750      1.500"
puts mNodeInfo "      55      -2.250      2.500"
puts mNodeInfo "      56      -2.750      3.000"
puts mNodeInfo "      57      -5.250      4.000"
puts mNodeInfo "      58      -1.250      0.000"
puts mNodeInfo "      59      -1.250      0.500"
puts mNodeInfo "      60      -4.750      4.000"
puts mNodeInfo "      61      -1.750      2.000"
puts mNodeInfo "      62      -3.250      3.500"
puts mNodeInfo "      63      -4.250      4.000"
puts mNodeInfo "      64      -1.250      1.000"
puts mNodeInfo "      65      -2.250      3.000"
puts mNodeInfo "      66      -3.750      4.000"
puts mNodeInfo "      67      -1.250      1.500"
puts mNodeInfo "      68      -1.750      2.500"
puts mNodeInfo "      69      -2.750      3.500"
puts mNodeInfo "      70      -1.250      2.000"
puts mNodeInfo "      71      -3.250      4.000"
puts mNodeInfo "      72      -0.750      0.000"
puts mNodeInfo "      73      -5.250      4.500"
puts mNodeInfo "      74      -4.750      4.500"
puts mNodeInfo "      75      -0.750      0.500"
puts mNodeInfo "      76      -4.250      4.500"
puts mNodeInfo "      77      -1.750      3.000"
puts mNodeInfo "      78      -2.250      3.500"
puts mNodeInfo "      79      -0.750      1.000"
puts mNodeInfo "      80      -1.250      2.500"
puts mNodeInfo "      81      -2.750      4.000"
puts mNodeInfo "      82      -3.750      4.500"
puts mNodeInfo "      83      -0.750      1.500"
puts mNodeInfo "      84      -0.750      2.000"
puts mNodeInfo "      85      -3.250      4.500"
puts mNodeInfo "      86      -1.750      3.500"
puts mNodeInfo "      87      -5.250      5.000"
puts mNodeInfo "      88      -0.250      0.000"
puts mNodeInfo "      89      -1.250      3.000"
puts mNodeInfo "      90      -2.250      4.000"
puts mNodeInfo "      91      -4.750      5.000"
puts mNodeInfo "      92      -0.250      0.500"
puts mNodeInfo "      93      -0.250      1.000"
puts mNodeInfo "      94      -4.250      5.000"
puts mNodeInfo "      95      -0.750      2.500"
puts mNodeInfo "      96      -2.750      4.500"
puts mNodeInfo "      97      -3.750      5.000"
puts mNodeInfo "      98      -0.250      1.500"
puts mNodeInfo "      99       0.000      0.250"
puts mNodeInfo "     100       0.000     -0.250"
puts mNodeInfo "     101       0.000      0.750"
puts mNodeInfo "     102      -1.750      4.000"
puts mNodeInfo "     103      -1.250      3.500"
puts mNodeInfo "     104      -3.250      5.000"
puts mNodeInfo "     105      -0.250      2.000"
puts mNodeInfo "     106       0.000      1.250"
puts mNodeInfo "     107      -0.750      3.000"
puts mNodeInfo "     108      -2.250      4.500"
puts mNodeInfo "     109       0.250      0.000"
puts mNodeInfo "     110      -5.250      5.500"
puts mNodeInfo "     111      -4.750      5.500"
puts mNodeInfo "     112       0.250      0.500"
puts mNodeInfo "     113       0.000      1.750"
puts mNodeInfo "     114      -2.750      5.000"
puts mNodeInfo "     115      -0.250      2.500"
puts mNodeInfo "     116       0.250      1.000"
puts mNodeInfo "     117      -4.250      5.500"
puts mNodeInfo "     118      -1.250      4.000"
puts mNodeInfo "     119       0.250      1.500"
puts mNodeInfo "     120      -3.750      5.500"
puts mNodeInfo "     121      -1.750      4.500"
puts mNodeInfo "     122      -0.750      3.500"
puts mNodeInfo "     123       0.000      2.250"
puts mNodeInfo "     124      -2.250      5.000"
puts mNodeInfo "     125      -0.250      3.000"
puts mNodeInfo "     126       0.250      2.000"
puts mNodeInfo "     127      -3.250      5.500"
puts mNodeInfo "     128       0.000      2.750"
puts mNodeInfo "     129      -5.250      6.000"
puts mNodeInfo "     130       0.750      0.000"
puts mNodeInfo "     131       0.750      0.500"
puts mNodeInfo "     132      -1.250      4.500"
puts mNodeInfo "     133      -4.750      6.000"
puts mNodeInfo "     134      -0.750      4.000"
puts mNodeInfo "     135       0.250      2.500"
puts mNodeInfo "     136      -2.750      5.500"
puts mNodeInfo "     137      -4.250      6.000"
puts mNodeInfo "     138       0.750      1.000"
puts mNodeInfo "     139      -0.250      3.500"
puts mNodeInfo "     140      -1.750      5.000"
puts mNodeInfo "     141       0.000      3.250"
puts mNodeInfo "     142      -3.750      6.000"
puts mNodeInfo "     143       0.750      1.500"
puts mNodeInfo "     144       0.250      3.000"
puts mNodeInfo "     145      -2.250      5.500"
puts mNodeInfo "     146       0.750      2.000"
puts mNodeInfo "     147      -3.250      6.000"
puts mNodeInfo "     148      -0.750      4.500"
puts mNodeInfo "     149      -1.250      5.000"
puts mNodeInfo "     150      -0.250      4.000"
puts mNodeInfo "     151       0.000      3.750"
puts mNodeInfo "     152       1.250      0.000"
puts mNodeInfo "     153       0.750      2.500"
puts mNodeInfo "     154      -5.250      6.500"
puts mNodeInfo "     155      -2.750      6.000"
puts mNodeInfo "     156      -4.750      6.500"
puts mNodeInfo "     157       1.250      0.500"
puts mNodeInfo "     158       0.250      3.500"
puts mNodeInfo "     159      -1.750      5.500"
puts mNodeInfo "     160      -4.250      6.500"
puts mNodeInfo "     161       1.250      1.000"
puts mNodeInfo "     162       1.250      1.500"
puts mNodeInfo "     163      -3.750      6.500"
puts mNodeInfo "     164       0.750      3.000"
puts mNodeInfo "     165      -2.250      6.000"
puts mNodeInfo "     166      -0.250      4.500"
puts mNodeInfo "     167      -0.750      5.000"
puts mNodeInfo "     168       0.000      4.250"
puts mNodeInfo "     169      -3.250      6.500"
puts mNodeInfo "     170       1.250      2.000"
puts mNodeInfo "     171       0.250      4.000"
puts mNodeInfo "     172      -1.250      5.500"
puts mNodeInfo "     173       0.750      3.500"
puts mNodeInfo "     174      -1.750      6.000"
puts mNodeInfo "     175      -2.750      6.500"
puts mNodeInfo "     176       1.250      2.500"
puts mNodeInfo "     177      -5.250      7.000"
puts mNodeInfo "     178       1.750      0.000"
puts mNodeInfo "     179      -4.750      7.000"
puts mNodeInfo "     180       1.750      0.500"
puts mNodeInfo "     181       1.750      1.000"
puts mNodeInfo "     182      -0.250      5.000"
puts mNodeInfo "     183      -4.250      7.000"
puts mNodeInfo "     184       0.000      4.750"
puts mNodeInfo "     185       0.250      4.500"
puts mNodeInfo "     186      -0.750      5.500"
puts mNodeInfo "     187       1.750      1.500"
puts mNodeInfo "     188      -2.250      6.500"
puts mNodeInfo "     189       1.250      3.000"
puts mNodeInfo "     190      -3.750      7.000"
puts mNodeInfo "     191       0.750      4.000"
puts mNodeInfo "     192      -1.250      6.000"
puts mNodeInfo "     193       1.750      2.000"
puts mNodeInfo "     194      -3.250      7.000"
puts mNodeInfo "     195      -1.750      6.500"
puts mNodeInfo "     196       1.250      3.500"
puts mNodeInfo "     197       0.000      5.250"
puts mNodeInfo "     198       1.750      2.500"
puts mNodeInfo "     199      -0.250      5.500"
puts mNodeInfo "     200       0.250      5.000"
puts mNodeInfo "     201      -2.750      7.000"
puts mNodeInfo "     202      -0.750      6.000"
puts mNodeInfo "     203       0.750      4.500"
puts mNodeInfo "     204      -5.250      7.500"
puts mNodeInfo "     205       2.250      0.000"
puts mNodeInfo "     206      -4.750      7.500"
puts mNodeInfo "     207       2.250      0.500"
puts mNodeInfo "     208      -4.250      7.500"
puts mNodeInfo "     209       2.250      1.000"
puts mNodeInfo "     210       1.750      3.000"
puts mNodeInfo "     211      -2.250      7.000"
puts mNodeInfo "     212       1.250      4.000"
puts mNodeInfo "     213      -1.250      6.500"
puts mNodeInfo "     214       2.250      1.500"
puts mNodeInfo "     215      -3.750      7.500"
puts mNodeInfo "     216      -3.250      7.500"
puts mNodeInfo "     217       2.250      2.000"
puts mNodeInfo "     219       0.000      5.750"
puts mNodeInfo "     220       0.750      5.000"
puts mNodeInfo "     221      -0.250      6.000"
puts mNodeInfo "     222      -1.750      7.000"
puts mNodeInfo "     223       1.750      3.500"
puts mNodeInfo "     224      -0.750      6.500"
puts mNodeInfo "     225       1.250      4.500"
puts mNodeInfo "     226      -2.750      7.500"
puts mNodeInfo "     227       2.250      2.500"
puts mNodeInfo "     228      -5.250      8.000"
puts mNodeInfo "     229       2.750      0.000"
puts mNodeInfo "     230      -4.750      8.000"
puts mNodeInfo "     231       2.750      0.500"
puts mNodeInfo "     232      -4.250      8.000"
puts mNodeInfo "     233       2.750      1.000"
puts mNodeInfo "     234       1.750      4.000"
puts mNodeInfo "     235      -1.250      7.000"
puts mNodeInfo "     236      -2.250      7.500"
puts mNodeInfo "     237       2.250      3.000"
puts mNodeInfo "     238      -3.750      8.000"
puts mNodeInfo "     240       2.750      1.500"
puts mNodeInfo "     242       0.000      6.250"
puts mNodeInfo "     243       1.250      5.000"
puts mNodeInfo "     244      -0.250      6.500"
puts mNodeInfo "     245       2.750      2.000"
puts mNodeInfo "     246      -3.250      8.000"
puts mNodeInfo "     247      -1.750      7.500"
puts mNodeInfo "     248       2.250      3.500"
puts mNodeInfo "     249      -0.750      7.000"
puts mNodeInfo "     250       1.750      4.500"
puts mNodeInfo "     251      -2.750      8.000"
puts mNodeInfo "     252       2.750      2.500"
puts mNodeInfo "     254       2.250      4.000"
puts mNodeInfo "     255      -5.250      8.500"
puts mNodeInfo "     256       3.250      0.000"
puts mNodeInfo "     257      -1.250      7.500"
puts mNodeInfo "     258      -4.750      8.500"
puts mNodeInfo "     261       3.250      0.500"
puts mNodeInfo "     262      -2.250      8.000"
puts mNodeInfo "     263       2.750      3.000"
puts mNodeInfo "     265      -4.250      8.500"
puts mNodeInfo "     264       0.000      6.750"
puts mNodeInfo "     266       3.250      1.000"
puts mNodeInfo "     267      -0.250      7.000"
puts mNodeInfo "     268       1.750      5.000"
puts mNodeInfo "     269      -3.750      8.500"
puts mNodeInfo "     270       3.250      1.500"
puts mNodeInfo "     271      -3.250      8.500"
puts mNodeInfo "     272      -1.750      8.000"
puts mNodeInfo "     273       3.250      2.000"
puts mNodeInfo "     274       2.750      3.500"
puts mNodeInfo "     275       2.250      4.500"
puts mNodeInfo "     276      -0.750      7.500"
puts mNodeInfo "     279      -2.750      8.500"
puts mNodeInfo "     280       3.250      2.500"
puts mNodeInfo "     283      -1.250      8.000"
puts mNodeInfo "     284       2.750      4.000"
puts mNodeInfo "     285       0.000      7.250"
puts mNodeInfo "     286       3.750      0.000"
puts mNodeInfo "     287      -5.250      9.000"
puts mNodeInfo "     288      -4.750      9.000"
puts mNodeInfo "     289      -2.250      8.500"
puts mNodeInfo "     290       2.250      5.000"
puts mNodeInfo "     291      -0.250      7.500"
puts mNodeInfo "     292       3.250      3.000"
puts mNodeInfo "     293       3.750      0.500"
puts mNodeInfo "     294      -4.250      9.000"
puts mNodeInfo "     295       3.750      1.000"
puts mNodeInfo "     296      -3.750      9.000"
puts mNodeInfo "     297       3.750      1.500"
puts mNodeInfo "     298      -0.750      8.000"
puts mNodeInfo "     299       2.750      4.500"
puts mNodeInfo "     300      -1.750      8.500"
puts mNodeInfo "     301       3.250      3.500"
puts mNodeInfo "     303       3.750      2.000"
puts mNodeInfo "     305      -3.250      9.000"
puts mNodeInfo "     309       3.750      2.500"
puts mNodeInfo "     310      -2.750      9.000"
puts mNodeInfo "     311       0.000      7.750"
puts mNodeInfo "     312       3.250      4.000"
puts mNodeInfo "     313      -1.250      8.500"
puts mNodeInfo "     314       2.750      5.000"
puts mNodeInfo "     315      -0.250      8.000"
puts mNodeInfo "     316       3.750      3.000"
puts mNodeInfo "     317      -2.250      9.000"
puts mNodeInfo "     318      -5.250      9.500"
puts mNodeInfo "     319       4.250      0.000"
puts mNodeInfo "     320      -4.750      9.500"
puts mNodeInfo "     321       4.250      0.500"
puts mNodeInfo "     323      -4.250      9.500"
puts mNodeInfo "     324       4.250      1.000"
puts mNodeInfo "     328      -0.750      8.500"
puts mNodeInfo "     329       3.250      4.500"
puts mNodeInfo "     330       4.250      1.500"
puts mNodeInfo "     331      -3.750      9.500"
puts mNodeInfo "     332      -1.750      9.000"
puts mNodeInfo "     333       3.750      3.500"
puts mNodeInfo "     334       4.250      2.000"
puts mNodeInfo "     337      -3.250      9.500"
puts mNodeInfo "     338       0.000      8.250"
puts mNodeInfo "     339       4.250      2.500"
puts mNodeInfo "     340      -2.750      9.500"
puts mNodeInfo "     341       3.750      4.000"
puts mNodeInfo "     342      -1.250      9.000"
puts mNodeInfo "     343       3.250      5.000"
puts mNodeInfo "     344      -0.250      8.500"
puts mNodeInfo "     348       4.250      3.000"
puts mNodeInfo "     349      -2.250      9.500"
puts mNodeInfo "     351      -5.250     10.000"
puts mNodeInfo "     352       4.750      0.000"
puts mNodeInfo "     354      -4.750     10.000"
puts mNodeInfo "     355       4.750      0.500"
puts mNodeInfo "     356       4.750      1.000"
puts mNodeInfo "     357      -4.250     10.000"
puts mNodeInfo "     358       3.750      4.500"
puts mNodeInfo "     359      -0.750      9.000"
puts mNodeInfo "     360      -3.750     10.000"
puts mNodeInfo "     361       4.750      1.500"
puts mNodeInfo "     362       4.250      3.500"
puts mNodeInfo "     365      -1.750      9.500"
puts mNodeInfo "     366      -3.250     10.000"
puts mNodeInfo "     367       4.750      2.000"
puts mNodeInfo "     368       0.000      8.750"
puts mNodeInfo "     371       3.750      5.000"
puts mNodeInfo "     372      -0.250      9.000"
puts mNodeInfo "     373       4.750      2.500"
puts mNodeInfo "     375      -1.250      9.500"
puts mNodeInfo "     376      -2.750     10.000"
puts mNodeInfo "     377       4.250      4.000"
puts mNodeInfo "     381       4.750      3.000"
puts mNodeInfo "     382      -2.250     10.000"
puts mNodeInfo "     383       5.250      0.000"
puts mNodeInfo "     384       4.250      4.500"
puts mNodeInfo "     385       5.250      0.500"
puts mNodeInfo "     386      -0.750      9.500"
puts mNodeInfo "     388       5.250      1.000"
puts mNodeInfo "     390       4.750      3.500"
puts mNodeInfo "     391      -1.750     10.000"
puts mNodeInfo "     393       5.250      1.500"
puts mNodeInfo "     396       0.000      9.250"
puts mNodeInfo "     397       5.250      2.000"
puts mNodeInfo "     400      -0.250      9.500"
puts mNodeInfo "     401       4.250      5.000"
puts mNodeInfo "     402      -1.250     10.000"
puts mNodeInfo "     403       4.750      4.000"
puts mNodeInfo "     404       5.250      2.500"
puts mNodeInfo "     407       5.250      3.000"
puts mNodeInfo "     409       4.750      4.500"
puts mNodeInfo "     410      -0.750     10.000"
puts mNodeInfo "     416       5.250      3.500"
puts mNodeInfo "     417       0.000      9.750"
puts mNodeInfo "     420       4.750      5.000"
puts mNodeInfo "     421      -0.250     10.000"
puts mNodeInfo "     423       5.250      4.000"
puts mNodeInfo "     432       5.250      4.500"
puts mNodeInfo "     435       0.000     10.250"
puts mNodeInfo "     436       5.250      5.000"
close, mNodeInfo

#-----------------------------------------------------------------------------------------
#  3. CREATE LAGRANGE MULTIPLIER NODES FOR BEAM CONTACT ELEMENTS
#-----------------------------------------------------------------------------------------

for k in range(1,43):
       model.node(1000+k,  0.00 0.00)

print("Finished creating all -ndf 2 nodes...")

#-----------------------------------------------------------------------------------------
#  4. CREATE SOIL MATERIALS
#-----------------------------------------------------------------------------------------

# define pressure depended material for soil
nDMaterial, 'PressureDependMultiYield02', 5, 2 1.8, 9.6e3, 2.7e4, 36, 0.1, \
                                      101.0 0.0 26 0.067 0.23 0.06 \
                                      0.27 20 5.0 3.0 1.0 \
                                      0.0 0.77 0.9 0.02 0.7 101.0
# element thickness
thick1 = 1.0
# body force in x-direction
xWgt1 =  0.00
# body force in y-direction
yWgt1 =  [expr -9.81*1.8]

# create wrapper material for initial state analysis
nDMaterial, 'InitialStateAnalysisWrapper', 1, 5 2

print("Finished creating all soil materials...")

#-----------------------------------------------------------------------------------------
#  5. CREATE SOIL ELEMENTS
#-----------------------------------------------------------------------------------------

model.element('quad',   1, 109, 130, 131, 112, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   2, 130, 152, 157, 131, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   3, 152, 178, 180, 157, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   4, 178, 205, 207, 180, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   5, 205, 229, 231, 207, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   6, 229, 256, 261, 231, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   7, 256, 286, 293, 261, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   8, 286, 319, 321, 293, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',   9, 319, 352, 355, 321, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  10, 352, 383, 385, 355, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  11, 112, 131, 138, 116, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  12, 131, 157, 161, 138, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  13, 157, 180, 181, 161, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  14, 180, 207, 209, 181, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  15, 207, 231, 233, 209, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  16, 231, 261, 266, 233, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  17, 261, 293, 295, 266, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  18, 293, 321, 324, 295, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  19, 321, 355, 356, 324, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  20, 355, 385, 388, 356, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  21, 116, 138, 143, 119, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  22, 138, 161, 162, 143, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  23, 161, 181, 187, 162, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  24, 181, 209, 214, 187, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  25, 209, 233, 240, 214, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  26, 233, 266, 270, 240, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  27, 266, 295, 297, 270, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  28, 295, 324, 330, 297, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  29, 324, 356, 361, 330, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  30, 356, 388, 393, 361, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  31, 119, 143, 146, 126, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  32, 143, 162, 170, 146, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  33, 162, 187, 193, 170, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  34, 187, 214, 217, 193, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  35, 214, 240, 245, 217, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  36, 240, 270, 273, 245, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  37, 270, 297, 303, 273, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  38, 297, 330, 334, 303, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  39, 330, 361, 367, 334, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  40, 361, 393, 397, 367, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  41, 126, 146, 153, 135, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  42, 146, 170, 176, 153, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  43, 170, 193, 198, 176, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  44, 193, 217, 227, 198, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  45, 217, 245, 252, 227, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  46, 245, 273, 280, 252, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  47, 273, 303, 309, 280, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  48, 303, 334, 339, 309, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  49, 334, 367, 373, 339, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  50, 367, 397, 404, 373, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  51, 135, 153, 164, 144, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  52, 153, 176, 189, 164, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  53, 176, 198, 210, 189, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  54, 198, 227, 237, 210, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  55, 227, 252, 263, 237, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  56, 252, 280, 292, 263, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  57, 280, 309, 316, 292, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  58, 309, 339, 348, 316, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  59, 339, 373, 381, 348, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  60, 373, 404, 407, 381, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  61, 144, 164, 173, 158, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  62, 164, 189, 196, 173, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  63, 189, 210, 223, 196, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  64, 210, 237, 248, 223, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  65, 237, 263, 274, 248, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  66, 263, 292, 301, 274, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  67, 292, 316, 333, 301, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  68, 316, 348, 362, 333, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  69, 348, 381, 390, 362, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  70, 381, 407, 416, 390, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  71, 158, 173, 191, 171, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  72, 173, 196, 212, 191, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  73, 196, 223, 234, 212, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  74, 223, 248, 254, 234, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  75, 248, 274, 284, 254, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  76, 274, 301, 312, 284, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  77, 301, 333, 341, 312, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  78, 333, 362, 377, 341, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  79, 362, 390, 403, 377, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  80, 390, 416, 423, 403, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  81, 171, 191, 203, 185, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  82, 191, 212, 225, 203, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  83, 212, 234, 250, 225, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  84, 234, 254, 275, 250, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  85, 254, 284, 299, 275, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  86, 284, 312, 329, 299, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  87, 312, 341, 358, 329, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  88, 341, 377, 384, 358, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  89, 377, 403, 409, 384, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  90, 403, 423, 432, 409, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  91, 185, 203, 220, 200, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  92, 203, 225, 243, 220, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  93, 225, 250, 268, 243, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  94, 250, 275, 290, 268, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  95, 275, 299, 314, 290, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  96, 299, 329, 343, 314, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  97, 329, 358, 371, 343, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  98, 358, 384, 401, 371, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad',  99, 384, 409, 420, 401, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 100, 409, 432, 436, 420, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 101, 200, 220, 239, 218, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 102, 220, 243, 259, 239, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 103, 243, 268, 282, 259, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 104, 268, 290, 307, 282, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 105, 290, 314, 335, 307, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 106, 314, 343, 364, 335, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 107, 343, 371, 389, 364, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 108, 371, 401, 413, 389, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 109, 401, 420, 431, 413, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 110, 420, 436, 445, 431, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 111, 218, 239, 253, 241, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 112, 239, 259, 277, 253, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 113, 259, 282, 306, 277, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 114, 282, 307, 327, 306, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 115, 307, 335, 350, 327, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 116, 335, 364, 379, 350, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 117, 364, 389, 406, 379, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 118, 389, 413, 422, 406, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 119, 413, 431, 438, 422, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 120, 431, 445, 451, 438, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 121, 241, 253, 278, 260, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 122, 253, 277, 302, 278, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 123, 277, 306, 325, 302, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 124, 306, 327, 346, 325, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 125, 327, 350, 374, 346, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 126, 350, 379, 399, 374, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 127, 379, 406, 419, 399, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 128, 406, 422, 434, 419, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 129, 422, 438, 447, 434, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 130, 438, 451, 456, 447, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 131, 260, 278, 304, 281, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 132, 278, 302, 322, 304, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 133, 302, 325, 345, 322, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 134, 325, 346, 370, 345, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 135, 346, 374, 394, 370, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 136, 374, 399, 415, 394, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 137, 399, 419, 428, 415, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 138, 419, 434, 443, 428, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 139, 434, 447, 454, 443, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 140, 447, 456, 463, 454, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 141, 281, 304, 326, 308, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 142, 304, 322, 347, 326, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 143, 322, 345, 369, 347, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 144, 345, 370, 392, 369, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 145, 370, 394, 408, 392, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 146, 394, 415, 426, 408, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 147, 415, 428, 441, 426, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 148, 428, 443, 452, 441, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 149, 443, 454, 462, 452, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 150, 454, 463, 469, 462, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 151, 308, 326, 353, 336, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 152, 326, 347, 378, 353, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 153, 347, 369, 395, 378, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 154, 369, 392, 411, 395, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 155, 392, 408, 425, 411, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 156, 408, 426, 440, 425, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 157, 426, 441, 449, 440, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 158, 441, 452, 459, 449, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 159, 452, 462, 467, 459, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 160, 462, 469, 474, 467, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 161, 336, 353, 380, 363, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 162, 353, 378, 398, 380, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 163, 378, 395, 414, 398, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 164, 395, 411, 427, 414, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 165, 411, 425, 439, 427, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 166, 425, 440, 448, 439, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 167, 440, 449, 457, 448, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 168, 449, 459, 465, 457, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 169, 459, 467, 472, 465, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 170, 467, 474, 478, 472, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 171, 363, 380, 405, 387, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 172, 380, 398, 418, 405, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 173, 398, 414, 429, 418, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 174, 414, 427, 442, 429, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 175, 427, 439, 450, 442, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 176, 439, 448, 458, 450, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 177, 448, 457, 464, 458, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 178, 457, 465, 470, 464, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 179, 465, 472, 477, 470, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 180, 472, 478, 481, 477, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 181, 387, 405, 424, 412, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 182, 405, 418, 433, 424, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 183, 418, 429, 444, 433, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 184, 429, 442, 453, 444, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 185, 442, 450, 460, 453, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 186, 450, 458, 466, 460, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 187, 458, 464, 471, 466, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 188, 464, 470, 475, 471, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 189, 470, 477, 479, 475, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 190, 477, 481, 483, 479, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 191, 412, 424, 437, 430, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 192, 424, 433, 446, 437, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 193, 433, 444, 455, 446, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 194, 444, 453, 461, 455, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 195, 453, 460, 468, 461, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 196, 460, 466, 473, 468, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 197, 466, 471, 476, 473, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 198, 471, 475, 480, 476, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 199, 475, 479, 482, 480, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 200, 479, 483, 484, 482, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 201,  88,  92,  75,  72, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 202,  92,  93,  79,  75, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 203,  93,  98,  83,  79, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 204,  98, 105,  84,  83, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 205, 105, 115,  95,  84, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 206, 115, 125, 107,  95, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 207, 125, 139, 122, 107, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 208, 139, 150, 134, 122, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 209, 150, 166, 148, 134, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 210, 166, 182, 167, 148, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 211, 182, 199, 186, 167, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 212, 199, 221, 202, 186, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 213, 221, 244, 224, 202, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 214, 244, 267, 249, 224, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 215, 267, 291, 276, 249, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 216, 291, 315, 298, 276, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 217, 315, 344, 328, 298, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 218, 344, 372, 359, 328, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 219, 372, 400, 386, 359, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 220, 400, 421, 410, 386, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 221, 72, 75, 59, 58, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 222, 75, 79, 64, 59, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 223, 79, 83, 67, 64, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 224, 83, 84, 70, 67, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 225, 84, 95, 80, 70, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 226, 95, 107, 89, 80, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 227, 107, 122, 103, 89, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 228, 122, 134, 118, 103, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 229, 134, 148, 132, 118, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 230, 148, 167, 149, 132, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 231, 167, 186, 172, 149, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 232, 186, 202, 192, 172, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 233, 202, 224, 213, 192, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 234, 224, 249, 235, 213, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 235, 249, 276, 257, 235, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 236, 276, 298, 283, 257, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 237, 298, 328, 313, 283, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 238, 328, 359, 342, 313, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 239, 359, 386, 375, 342, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 240, 386, 410, 402, 375, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 241, 58, 59, 48, 45, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 242, 59, 64, 51, 48, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 243, 64, 67, 54, 51, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 244, 67, 70, 61, 54, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 245, 70, 80, 68, 61, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 246, 80, 89, 77, 68, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 247, 89, 103, 86, 77, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 248, 103, 118, 102, 86, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 249, 118, 132, 121, 102, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 250, 132, 149, 140, 121, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 251, 149, 172, 159, 140, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 252, 172, 192, 174, 159, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 253, 192, 213, 195, 174, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 254, 213, 235, 222, 195, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 255, 235, 257, 247, 222, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 256, 257, 283, 272, 247, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 257, 283, 313, 300, 272, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 258, 313, 342, 332, 300, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 259, 342, 375, 365, 332, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 260, 375, 402, 391, 365, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 261, 45, 48, 37, 35, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 262, 48, 51, 39, 37, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 263, 51, 54, 43, 39, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 264, 54, 61, 49, 43, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 265, 61, 68, 55, 49, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 266, 68, 77, 65, 55, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 267, 77, 86, 78, 65, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 268, 86, 102, 90, 78, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 269, 102, 121, 108, 90, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 270, 121, 140, 124, 108, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 271, 140, 159, 145, 124, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 272, 159, 174, 165, 145, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 273, 174, 195, 188, 165, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 274, 195, 222, 211, 188, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 275, 222, 247, 236, 211, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 276, 247, 272, 262, 236, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 277, 272, 300, 289, 262, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 278, 300, 332, 317, 289, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 279, 332, 365, 349, 317, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 280, 365, 391, 382, 349, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 281, 35, 37, 28, 24, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 282, 37, 39, 30, 28, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 283, 39, 43, 33, 30, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 284, 43, 49, 41, 33, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 285, 49, 55, 46, 41, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 286, 55, 65, 56, 46, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 287, 65, 78, 69, 56, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 288, 78, 90, 81, 69, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 289, 90, 108, 96, 81, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 290, 108, 124, 114, 96, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 291, 124, 145, 136, 114, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 292, 145, 165, 155, 136, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 293, 165, 188, 175, 155, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 294, 188, 211, 201, 175, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 295, 211, 236, 226, 201, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 296, 236, 262, 251, 226, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 297, 262, 289, 279, 251, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 298, 289, 317, 310, 279, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 299, 317, 349, 340, 310, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 300, 349, 382, 376, 340, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 301, 24, 28, 19, 16, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 302, 28, 30, 21, 19, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 303, 30, 33, 25, 21, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 304, 33, 41, 31, 25, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 305, 41, 46, 40, 31, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 306, 46, 56, 50, 40, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 307, 56, 69, 62, 50, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 308, 69, 81, 71, 62, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 309, 81, 96, 85, 71, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 310, 96, 114, 104, 85, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 311, 114, 136, 127, 104, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 312, 136, 155, 147, 127, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 313, 155, 175, 169, 147, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 314, 175, 201, 194, 169, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 315, 201, 226, 216, 194, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 316, 226, 251, 246, 216, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 317, 251, 279, 271, 246, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 318, 279, 310, 305, 271, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 319, 310, 340, 337, 305, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 320, 340, 376, 366, 337, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 321, 16, 19, 13, 11, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 322, 19, 21, 14, 13, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 323, 21, 25, 20, 14, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 324, 25, 31, 26, 20, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 325, 31, 40, 32, 26, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 326, 40, 50, 42, 32, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 327, 50, 62, 53, 42, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 328, 62, 71, 66, 53, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 329, 71, 85, 82, 66, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 330, 85, 104, 97, 82, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 331, 104, 127, 120, 97, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 332, 127, 147, 142, 120, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 333, 147, 169, 163, 142, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 334, 169, 194, 190, 163, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 335, 194, 216, 215, 190, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 336, 216, 246, 238, 215, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 337, 246, 271, 269, 238, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 338, 271, 305, 296, 269, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 339, 305, 337, 331, 296, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 340, 337, 366, 360, 331, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 341, 11, 13, 8 5, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 342, 13, 14, 9 8, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 343, 14, 20, 15, 9  thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 344, 20, 26, 22, 15, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 345, 26, 32, 29, 22, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 346, 32, 42, 38, 29, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 347, 42, 53, 52, 38, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 348, 53, 66, 63, 52, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 349, 66, 82, 76, 63, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 350, 82, 97, 94, 76, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 351, 97, 120, 117, 94, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 352, 120, 142, 137, 117, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 353, 142, 163, 160, 137, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 354, 163, 190, 183, 160, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 355, 190, 215, 208, 183, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 356, 215, 238, 232, 208, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 357, 238, 269, 265, 232, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 358, 269, 296, 294, 265, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 359, 296, 331, 323, 294, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 360, 331, 360, 357, 323, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 361, 5 8, 4 3, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 362, 8 9, 7 4, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 363, 9 15, 12, 7  thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 364, 15, 22, 18, 12, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 365, 22, 29, 27, 18, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 366, 29, 38, 36, 27, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 367, 38, 52, 47, 36, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 368, 52, 63, 60, 47, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 369, 63, 76, 74, 60, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 370, 76, 94, 91, 74, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 371, 94, 117, 111, 91, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 372, 117, 137, 133, 111, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 373, 137, 160, 156, 133, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 374, 160, 183, 179, 156, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 375, 183, 208, 206, 179, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 376, 208, 232, 230, 206, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 377, 232, 265, 258, 230, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 378, 265, 294, 288, 258, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 379, 294, 323, 320, 288, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 380, 323, 357, 354, 320, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 381, 3 4, 2 1, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 382, 4 7, 6 2, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 383, 7 12, 10, 6  thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 384, 12, 18, 17, 10, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 385, 18, 27, 23, 17, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 386, 27, 36, 34, 23, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 387, 36, 47, 44, 34, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 388, 47, 60, 57, 44, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 389, 60, 74, 73, 57, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 390, 74, 91, 87, 73, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 391, 91, 111, 110, 87, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 392, 111, 133, 129, 110, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 393, 133, 156, 154, 129, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 394, 156, 179, 177, 154, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 395, 179, 206, 204, 177, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 396, 206, 230, 228, 204, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 397, 230, 258, 255, 228, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 398, 258, 288, 287, 255, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 399, 288, 320, 318, 287, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
model.element('quad', 400, 320, 354, 351, 318, thick1, "PlaneStrain", 1 0.0, 0.0, xWgt1, yWgt1)
print("Finished creating all soil elements...")

# create list of permanent elements with connectivities for post-processing
eleFile = [open, outDir/SolidElementInfo.dat, 'w]'
puts eleFile "       1       109       130       131       112"
puts eleFile "       2       130       152       157       131"
puts eleFile "       3       152       178       180       157"
puts eleFile "       4       178       205       207       180"
puts eleFile "       5       205       229       231       207"
puts eleFile "       6       229       256       261       231"
puts eleFile "       7       256       286       293       261"
puts eleFile "       8       286       319       321       293"
puts eleFile "       9       319       352       355       321"
puts eleFile "      10       352       383       385       355"
puts eleFile "      11       112       131       138       116"
puts eleFile "      12       131       157       161       138"
puts eleFile "      13       157       180       181       161"
puts eleFile "      14       180       207       209       181"
puts eleFile "      15       207       231       233       209"
puts eleFile "      16       231       261       266       233"
puts eleFile "      17       261       293       295       266"
puts eleFile "      18       293       321       324       295"
puts eleFile "      19       321       355       356       324"
puts eleFile "      20       355       385       388       356"
puts eleFile "      21       116       138       143       119"
puts eleFile "      22       138       161       162       143"
puts eleFile "      23       161       181       187       162"
puts eleFile "      24       181       209       214       187"
puts eleFile "      25       209       233       240       214"
puts eleFile "      26       233       266       270       240"
puts eleFile "      27       266       295       297       270"
puts eleFile "      28       295       324       330       297"
puts eleFile "      29       324       356       361       330"
puts eleFile "      30       356       388       393       361"
puts eleFile "      31       119       143       146       126"
puts eleFile "      32       143       162       170       146"
puts eleFile "      33       162       187       193       170"
puts eleFile "      34       187       214       217       193"
puts eleFile "      35       214       240       245       217"
puts eleFile "      36       240       270       273       245"
puts eleFile "      37       270       297       303       273"
puts eleFile "      38       297       330       334       303"
puts eleFile "      39       330       361       367       334"
puts eleFile "      40       361       393       397       367"
puts eleFile "      41       126       146       153       135"
puts eleFile "      42       146       170       176       153"
puts eleFile "      43       170       193       198       176"
puts eleFile "      44       193       217       227       198"
puts eleFile "      45       217       245       252       227"
puts eleFile "      46       245       273       280       252"
puts eleFile "      47       273       303       309       280"
puts eleFile "      48       303       334       339       309"
puts eleFile "      49       334       367       373       339"
puts eleFile "      50       367       397       404       373"
puts eleFile "      51       135       153       164       144"
puts eleFile "      52       153       176       189       164"
puts eleFile "      53       176       198       210       189"
puts eleFile "      54       198       227       237       210"
puts eleFile "      55       227       252       263       237"
puts eleFile "      56       252       280       292       263"
puts eleFile "      57       280       309       316       292"
puts eleFile "      58       309       339       348       316"
puts eleFile "      59       339       373       381       348"
puts eleFile "      60       373       404       407       381"
puts eleFile "      61       144       164       173       158"
puts eleFile "      62       164       189       196       173"
puts eleFile "      63       189       210       223       196"
puts eleFile "      64       210       237       248       223"
puts eleFile "      65       237       263       274       248"
puts eleFile "      66       263       292       301       274"
puts eleFile "      67       292       316       333       301"
puts eleFile "      68       316       348       362       333"
puts eleFile "      69       348       381       390       362"
puts eleFile "      70       381       407       416       390"
puts eleFile "      71       158       173       191       171"
puts eleFile "      72       173       196       212       191"
puts eleFile "      73       196       223       234       212"
puts eleFile "      74       223       248       254       234"
puts eleFile "      75       248       274       284       254"
puts eleFile "      76       274       301       312       284"
puts eleFile "      77       301       333       341       312"
puts eleFile "      78       333       362       377       341"
puts eleFile "      79       362       390       403       377"
puts eleFile "      80       390       416       423       403"
puts eleFile "      81       171       191       203       185"
puts eleFile "      82       191       212       225       203"
puts eleFile "      83       212       234       250       225"
puts eleFile "      84       234       254       275       250"
puts eleFile "      85       254       284       299       275"
puts eleFile "      86       284       312       329       299"
puts eleFile "      87       312       341       358       329"
puts eleFile "      88       341       377       384       358"
puts eleFile "      89       377       403       409       384"
puts eleFile "      90       403       423       432       409"
puts eleFile "      91       185       203       220       200"
puts eleFile "      92       203       225       243       220"
puts eleFile "      93       225       250       268       243"
puts eleFile "      94       250       275       290       268"
puts eleFile "      95       275       299       314       290"
puts eleFile "      96       299       329       343       314"
puts eleFile "      97       329       358       371       343"
puts eleFile "      98       358       384       401       371"
puts eleFile "      99       384       409       420       401"
puts eleFile "     100       409       432       436       420"
puts eleFile "     201        88        92        75        72"
puts eleFile "     202        92        93        79        75"
puts eleFile "     203        93        98        83        79"
puts eleFile "     204        98       105        84        83"
puts eleFile "     205       105       115        95        84"
puts eleFile "     206       115       125       107        95"
puts eleFile "     207       125       139       122       107"
puts eleFile "     208       139       150       134       122"
puts eleFile "     209       150       166       148       134"
puts eleFile "     210       166       182       167       148"
puts eleFile "     211       182       199       186       167"
puts eleFile "     212       199       221       202       186"
puts eleFile "     213       221       244       224       202"
puts eleFile "     214       244       267       249       224"
puts eleFile "     215       267       291       276       249"
puts eleFile "     216       291       315       298       276"
puts eleFile "     217       315       344       328       298"
puts eleFile "     218       344       372       359       328"
puts eleFile "     219       372       400       386       359"
puts eleFile "     220       400       421       410       386"
puts eleFile "     221        72        75        59        58"
puts eleFile "     222        75        79        64        59"
puts eleFile "     223        79        83        67        64"
puts eleFile "     224        83        84        70        67"
puts eleFile "     225        84        95        80        70"
puts eleFile "     226        95       107        89        80"
puts eleFile "     227       107       122       103        89"
puts eleFile "     228       122       134       118       103"
puts eleFile "     229       134       148       132       118"
puts eleFile "     230       148       167       149       132"
puts eleFile "     231       167       186       172       149"
puts eleFile "     232       186       202       192       172"
puts eleFile "     233       202       224       213       192"
puts eleFile "     234       224       249       235       213"
puts eleFile "     235       249       276       257       235"
puts eleFile "     236       276       298       283       257"
puts eleFile "     237       298       328       313       283"
puts eleFile "     238       328       359       342       313"
puts eleFile "     239       359       386       375       342"
puts eleFile "     240       386       410       402       375"
puts eleFile "     241        58        59        48        45"
puts eleFile "     242        59        64        51        48"
puts eleFile "     243        64        67        54        51"
puts eleFile "     244        67        70        61        54"
puts eleFile "     245        70        80        68        61"
puts eleFile "     246        80        89        77        68"
puts eleFile "     247        89       103        86        77"
puts eleFile "     248       103       118       102        86"
puts eleFile "     249       118       132       121       102"
puts eleFile "     250       132       149       140       121"
puts eleFile "     251       149       172       159       140"
puts eleFile "     252       172       192       174       159"
puts eleFile "     253       192       213       195       174"
puts eleFile "     254       213       235       222       195"
puts eleFile "     255       235       257       247       222"
puts eleFile "     256       257       283       272       247"
puts eleFile "     257       283       313       300       272"
puts eleFile "     258       313       342       332       300"
puts eleFile "     259       342       375       365       332"
puts eleFile "     260       375       402       391       365"
puts eleFile "     261        45        48        37        35"
puts eleFile "     262        48        51        39        37"
puts eleFile "     263        51        54        43        39"
puts eleFile "     264        54        61        49        43"
puts eleFile "     265        61        68        55        49"
puts eleFile "     266        68        77        65        55"
puts eleFile "     267        77        86        78        65"
puts eleFile "     268        86       102        90        78"
puts eleFile "     269       102       121       108        90"
puts eleFile "     270       121       140       124       108"
puts eleFile "     271       140       159       145       124"
puts eleFile "     272       159       174       165       145"
puts eleFile "     273       174       195       188       165"
puts eleFile "     274       195       222       211       188"
puts eleFile "     275       222       247       236       211"
puts eleFile "     276       247       272       262       236"
puts eleFile "     277       272       300       289       262"
puts eleFile "     278       300       332       317       289"
puts eleFile "     279       332       365       349       317"
puts eleFile "     280       365       391       382       349"
puts eleFile "     281        35        37        28        24"
puts eleFile "     282        37        39        30        28"
puts eleFile "     283        39        43        33        30"
puts eleFile "     284        43        49        41        33"
puts eleFile "     285        49        55        46        41"
puts eleFile "     286        55        65        56        46"
puts eleFile "     287        65        78        69        56"
puts eleFile "     288        78        90        81        69"
puts eleFile "     289        90       108        96        81"
puts eleFile "     290       108       124       114        96"
puts eleFile "     291       124       145       136       114"
puts eleFile "     292       145       165       155       136"
puts eleFile "     293       165       188       175       155"
puts eleFile "     294       188       211       201       175"
puts eleFile "     295       211       236       226       201"
puts eleFile "     296       236       262       251       226"
puts eleFile "     297       262       289       279       251"
puts eleFile "     298       289       317       310       279"
puts eleFile "     299       317       349       340       310"
puts eleFile "     300       349       382       376       340"
puts eleFile "     301        24        28        19        16"
puts eleFile "     302        28        30        21        19"
puts eleFile "     303        30        33        25        21"
puts eleFile "     304        33        41        31        25"
puts eleFile "     305        41        46        40        31"
puts eleFile "     306        46        56        50        40"
puts eleFile "     307        56        69        62        50"
puts eleFile "     308        69        81        71        62"
puts eleFile "     309        81        96        85        71"
puts eleFile "     310        96       114       104        85"
puts eleFile "     311       114       136       127       104"
puts eleFile "     312       136       155       147       127"
puts eleFile "     313       155       175       169       147"
puts eleFile "     314       175       201       194       169"
puts eleFile "     315       201       226       216       194"
puts eleFile "     316       226       251       246       216"
puts eleFile "     317       251       279       271       246"
puts eleFile "     318       279       310       305       271"
puts eleFile "     319       310       340       337       305"
puts eleFile "     320       340       376       366       337"
puts eleFile "     321        16        19        13        11"
puts eleFile "     322        19        21        14        13"
puts eleFile "     323        21        25        20        14"
puts eleFile "     324        25        31        26        20"
puts eleFile "     325        31        40        32        26"
puts eleFile "     326        40        50        42        32"
puts eleFile "     327        50        62        53        42"
puts eleFile "     328        62        71        66        53"
puts eleFile "     329        71        85        82        66"
puts eleFile "     330        85       104        97        82"
puts eleFile "     331       104       127       120        97"
puts eleFile "     332       127       147       142       120"
puts eleFile "     333       147       169       163       142"
puts eleFile "     334       169       194       190       163"
puts eleFile "     335       194       216       215       190"
puts eleFile "     336       216       246       238       215"
puts eleFile "     337       246       271       269       238"
puts eleFile "     338       271       305       296       269"
puts eleFile "     339       305       337       331       296"
puts eleFile "     340       337       366       360       331"
puts eleFile "     341        11        13         8         5"
puts eleFile "     342        13        14         9         8"
puts eleFile "     343        14        20        15         9"
puts eleFile "     344        20        26        22        15"
puts eleFile "     345        26        32        29        22"
puts eleFile "     346        32        42        38        29"
puts eleFile "     347        42        53        52        38"
puts eleFile "     348        53        66        63        52"
puts eleFile "     349        66        82        76        63"
puts eleFile "     350        82        97        94        76"
puts eleFile "     351        97       120       117        94"
puts eleFile "     352       120       142       137       117"
puts eleFile "     353       142       163       160       137"
puts eleFile "     354       163       190       183       160"
puts eleFile "     355       190       215       208       183"
puts eleFile "     356       215       238       232       208"
puts eleFile "     357       238       269       265       232"
puts eleFile "     358       269       296       294       265"
puts eleFile "     359       296       331       323       294"
puts eleFile "     360       331       360       357       323"
puts eleFile "     361         5         8         4         3"
puts eleFile "     362         8         9         7         4"
puts eleFile "     363         9        15        12         7"
puts eleFile "     364        15        22        18        12"
puts eleFile "     365        22        29        27        18"
puts eleFile "     366        29        38        36        27"
puts eleFile "     367        38        52        47        36"
puts eleFile "     368        52        63        60        47"
puts eleFile "     369        63        76        74        60"
puts eleFile "     370        76        94        91        74"
puts eleFile "     371        94       117       111        91"
puts eleFile "     372       117       137       133       111"
puts eleFile "     373       137       160       156       133"
puts eleFile "     374       160       183       179       156"
puts eleFile "     375       183       208       206       179"
puts eleFile "     376       208       232       230       206"
puts eleFile "     377       232       265       258       230"
puts eleFile "     378       265       294       288       258"
puts eleFile "     379       294       323       320       288"
puts eleFile "     380       323       357       354       320"
puts eleFile "     381         3         4         2         1"
puts eleFile "     382         4         7         6         2"
puts eleFile "     383         7        12        10         6"
puts eleFile "     384        12        18        17        10"
puts eleFile "     385        18        27        23        17"
puts eleFile "     386        27        36        34        23"
puts eleFile "     387        36        47        44        34"
puts eleFile "     388        47        60        57        44"
puts eleFile "     389        60        74        73        57"
puts eleFile "     390        74        91        87        73"
puts eleFile "     391        91       111       110        87"
puts eleFile "     392       111       133       129       110"
puts eleFile "     393       133       156       154       129"
puts eleFile "     394       156       179       177       154"
puts eleFile "     395       179       206       204       177"
puts eleFile "     396       206       230       228       204"
puts eleFile "     397       230       258       255       228"
puts eleFile "     398       258       288       287       255"
puts eleFile "     399       288       320       318       287"
puts eleFile "     400       320       354       351       318"
close, eleFile

#-----------------------------------------------------------------------------------------
#  6. CREATE BEAM NODES AND FIXITIES
#-----------------------------------------------------------------------------------------
model, 'BasicBuilder', ndm=2,  ndf=3, 

# define beam nodes
model.node(      99, 0.000, 0.250)
model.node(     100, 0.000     -0.250)
model.node(     101, 0.000, 0.750)
model.node(     106, 0.000, 1.250)
model.node(     113, 0.000, 1.750)
model.node(     123, 0.000, 2.250)
model.node(     128, 0.000, 2.750)
model.node(     141, 0.000, 3.250)
model.node(     151, 0.000, 3.750)
model.node(     168, 0.000, 4.250)
model.node(     184, 0.000, 4.750)
model.node(     197, 0.000, 5.250)
model.node(     219, 0.000, 5.750)
model.node(     242, 0.000, 6.250)
model.node(     264, 0.000, 6.750)
model.node(     285, 0.000, 7.250)
model.node(     311, 0.000, 7.750)
model.node(     338, 0.000, 8.250)
model.node(     368, 0.000, 8.750)
model.node(     396, 0.000, 9.250)
model.node(     417, 0.000, 9.750)
model.node(     435, 0.000, 10.250)
print("Finished creating all -ndf 3 beam nodes...")

# create list of beam nodes and locations for post-processing
bNodeInfo = [open, outDir/NodesInfo3.dat, 'w]'
puts bNodeInfo "      99       0.000      0.250"
puts bNodeInfo "     100       0.000     -0.250"
puts bNodeInfo "     101       0.000      0.750"
puts bNodeInfo "     106       0.000      1.250"
puts bNodeInfo "     113       0.000      1.750"
puts bNodeInfo "     123       0.000      2.250"
puts bNodeInfo "     128       0.000      2.750"
puts bNodeInfo "     141       0.000      3.250"
puts bNodeInfo "     151       0.000      3.750"
puts bNodeInfo "     168       0.000      4.250"
puts bNodeInfo "     184       0.000      4.750"
puts bNodeInfo "     197       0.000      5.250"
puts bNodeInfo "     219       0.000      5.750"
puts bNodeInfo "     242       0.000      6.250"
puts bNodeInfo "     264       0.000      6.750"
puts bNodeInfo "     285       0.000      7.250"
puts bNodeInfo "     311       0.000      7.750"
puts bNodeInfo "     338       0.000      8.250"
puts bNodeInfo "     368       0.000      8.750"
puts bNodeInfo "     396       0.000      9.250"
puts bNodeInfo "     417       0.000      9.750"
puts bNodeInfo "     435       0.000     10.250"
close, bNodeInfo

# fix the base node of the sheetpile in the vertial direction
model.fix(  100, 0 1, 0)
print("Finished creating all -ndf 3 boundary conditions...")

#-----------------------------------------------------------------------------------------
#  7. CREATE BEAM MATERIALS
#-----------------------------------------------------------------------------------------

# beam properties
thick =      0.5
area =       0.5
I =          9.75e-4
beamE =      200000000
numIntPts =  3
transTag =   1
secTag =     1

# geometric transformation
model.geomTransf('Linear',  transTag)

# beam section
section, 'Elastic',  secTag, beamE, area, I

print("Finished creating all beam materials...")

#-----------------------------------------------------------------------------------------
#  8. CREATE BEAM ELEMENTS
#-----------------------------------------------------------------------------------------

model.element('dispBeamColumn', 401, 100, 99, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 402, 99, 101, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 403, 101, 106, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 404, 106, 113, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 405, 113, 123, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 406, 123, 128, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 407, 128, 141, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 408, 141, 151, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 409, 151, 168, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 410, 168, 184, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 411, 184, 197, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 412, 197, 219, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 413, 219, 242, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 414, 242, 264, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 415, 264, 285, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 416, 285, 311, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 417, 311, 338, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 418, 338, 368, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 419, 368, 396, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 420, 396, 417, numIntPts, secTag, transTag)
model.element('dispBeamColumn', 421, 417, 435, numIntPts, secTag, transTag)
print("Finished creating all beam elements...")

# create list of beam elements with connectivities for post-processing
beamInfo = [open, outDir/beamElementInfo.dat, 'w]'
puts beamInfo " 401 100 99 "
puts beamInfo " 402 99 101 "
puts beamInfo " 403 101 106 "
puts beamInfo " 404 106 113 "
puts beamInfo " 405 113 123 "
puts beamInfo " 406 123 128 "
puts beamInfo " 407 128 141 "
puts beamInfo " 408 141 151 "
puts beamInfo " 409 151 168 "
puts beamInfo " 410 168 184 "
puts beamInfo " 411 184 197 "
puts beamInfo " 412 197 219 "
puts beamInfo " 413 219 242 "
puts beamInfo " 414 242 264 "
puts beamInfo " 415 264 285 "
puts beamInfo " 416 285 311 "
puts beamInfo " 417 311 338 "
puts beamInfo " 418 338 368 "
puts beamInfo " 419 368 396 "
puts beamInfo " 420 396 417 "
puts beamInfo " 421 417 435 "
close, beamInfo

#-----------------------------------------------------------------------------------------
#  9. CREATE CONTACT MATERIAL FOR BEAM CONTACT ELEMENTS 
#-----------------------------------------------------------------------------------------

# two-dimensional contact material
nDMaterial, 'ContactMaterial2D',  2, 0.1, 1000.0, 0.0, 0.0

print("Finished creating all contact materials...")

#-----------------------------------------------------------------------------------------
#  10. CREATE BEAM CONTACT ELEMENTS
#-----------------------------------------------------------------------------------------

# gap = and force tolerances for beam contact elements
gapTol =    1.0e-10
forceTol =  1.0e-10

# define beam contact elements
model.element('BeamContact2D', 1001, 100, 99, 88, 1001, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1002, 100, 99, 109, 1002, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1003, 99, 101, 92, 1003, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1004, 99, 101, 112, 1004, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1005, 101, 106, 93, 1005, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1006, 101, 106, 116, 1006, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1007, 106, 113, 98, 1007, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1008, 106, 113, 119, 1008, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1009, 113, 123, 105, 1009, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1010, 113, 123, 126, 1010, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1011, 123, 128, 115, 1011, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1012, 123, 128, 135, 1012, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1013, 128, 141, 125, 1013, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1014, 128, 141, 144, 1014, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1015, 141, 151, 139, 1015, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1016, 141, 151, 158, 1016, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1017, 151, 168, 150, 1017, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1018, 151, 168, 171, 1018, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1019, 168, 184, 166, 1019, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1020, 168, 184, 185, 1020, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1021, 184, 197, 182, 1021, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1022, 184, 197, 200, 1022, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1023, 197, 219, 199, 1023, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1024, 197, 219, 218, 1024, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1025, 219, 242, 221, 1025, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1026, 219, 242, 241, 1026, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1027, 242, 264, 244, 1027, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1028, 242, 264, 260, 1028, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1029, 264, 285, 267, 1029, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1030, 264, 285, 281, 1030, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1031, 285, 311, 291, 1031, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1032, 285, 311, 308, 1032, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1033, 311, 338, 315, 1033, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1034, 311, 338, 336, 1034, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1035, 338, 368, 344, 1035, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1036, 338, 368, 363, 1036, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1037, 368, 396, 372, 1037, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1038, 368, 396, 387, 1038, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1039, 396, 417, 400, 1039, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1040, 396, 417, 412, 1040, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1041, 417, 435, 421, 1041, 2 thick, gapTol, forceTol)
model.element('BeamContact2D', 1042, 417, 435, 430, 1042, 2 thick, gapTol, forceTol)
print("Finished creating all beam-contact elements...")

# create list of permanent beam contact elements with connectivities for post-process
beamContactInfo = [open, outDir/beamContactInfo.dat, 'w]'
puts beamContactInfo "1001  100  99  88 1001  "
puts beamContactInfo "1002  100  99 109 1002  "
puts beamContactInfo "1003   99 101  92 1003  "
puts beamContactInfo "1004   99 101 112 1004  "
puts beamContactInfo "1005  101 106  93 1005  "
puts beamContactInfo "1006  101 106 116 1006  "
puts beamContactInfo "1007  106 113  98 1007  "
puts beamContactInfo "1008  106 113 119 1008  "
puts beamContactInfo "1009  113 123 105 1009  "
puts beamContactInfo "1010  113 123 126 1010  "
puts beamContactInfo "1011  123 128 115 1011  "
puts beamContactInfo "1012  123 128 135 1012  "
puts beamContactInfo "1013  128 141 125 1013  "
puts beamContactInfo "1014  128 141 144 1014  "
puts beamContactInfo "1015  141 151 139 1015  "
puts beamContactInfo "1016  141 151 158 1016  "
puts beamContactInfo "1017  151 168 150 1017  "
puts beamContactInfo "1018  151 168 171 1018  "
puts beamContactInfo "1019  168 184 166 1019  "
puts beamContactInfo "1020  168 184 185 1020  "
puts beamContactInfo "1021  184 197 182 1021  "
puts beamContactInfo "1022  184 197 200 1022  "
puts beamContactInfo "1023  197 219 199 1023  "
puts beamContactInfo "1025  219 242 221 1025  "
puts beamContactInfo "1027  242 264 244 1027  "
puts beamContactInfo "1029  264 285 267 1029  "
puts beamContactInfo "1031  285 311 291 1031  "
puts beamContactInfo "1033  311 338 315 1033  "
puts beamContactInfo "1035  338 368 344 1035  "
puts beamContactInfo "1037  368 396 372 1037  "
puts beamContactInfo "1039  396 417 400 1039  "
puts beamContactInfo "1041  417 435 421 1041  "
close, beamContactInfo

#-----------------------------------------------------------------------------------------
#  11. CREATE RECORDER LISTS USING PREVIOUSLY DEFINED NODAL/ELEMENTAL DATA
#-----------------------------------------------------------------------------------------

# permanent soil node list
nodeListPerm = {}
channel = [open "outDir/NodesInfoPerm.dat" r]
ctr = 0;
foreach, 'line', [split, '[read', nonewline=channel],  '\n]', {
ctr0 = ctr+1
lineData = (ctr) line
nodeNumber = [lindex, lineData(ctr) 0]
nodeListPerm.append(nodeNumber)

close, channel

# permanent soil element list
solidElementList = {}
channel = [open "outDir/SolidElementInfo.dat" r]
ctr = 0;
foreach, 'line', [split, '[read', nonewline=channel],  '\n]', {
ctr0 = ctr+1
lineData = (ctr) line
elementNumber = [lindex, lineData(ctr) 0]
solidElementList.append(elementNumber        )

close, channel

# beam element list
BeamElementList = {}
channel = [open "outDir/beamElementInfo.dat" r]
ctr = 0;
foreach, 'line', [split, '[read', nonewline=channel],  '\n]', {
ctr0 = ctr+1
lineData = (ctr) line
elementNumber = [lindex, lineData(ctr) 0]
BeamElementList.append(elementNumber        )

close, channel

# permanent beam contact element list
BCElemList = {}
channel = [open "outDir/beamContactInfo.dat" r]
ctr = 0;
foreach, 'line', [split, '[read', nonewline=channel],  '\n]', {
ctr0 = ctr+1
lineData = (ctr) line
elementNumber = [lindex, lineData(ctr) 0]
BCElemList.append(elementNumber )

close, channel

#-----------------------------------------------------------------------------------------
#  13. CREATE RECORDERS
#-----------------------------------------------------------------------------------------

# PERMANENT RECORDERS---------------------------------------------------------------------
# record nodal displacments at permanent nodes
eval "recorder Node -file outDir/displacement.out -time -node nodeListPerm -dof 1 2  disp"
# record elemental stress in the soil at permanent elements
eval "recorder Element -file outDir/stress1.out   -time  -ele solidElementList  material 1 stress"
eval "recorder Element -file outDir/stress2.out   -time  -ele solidElementList  material 2 stress"
eval "recorder Element -file outDir/stress3.out   -time  -ele solidElementList  material 3 stress"
eval "recorder Element -file outDir/stress4.out   -time  -ele solidElementList  material 4 stress"
# record permanent contact element information
eval "recorder Element  -file outDir/slaveForce.out  -time  -ele BCElemList  forces"
eval "recorder Element  -file outDir/frictForce.out  -time  -ele BCElemList  frictionforces"
eval "recorder Element  -file outDir/contForce.out   -time  -ele BCElemList  forcescalars"
eval "recorder Element  -file outDir/mastForce.out   -time  -ele BCElemList  masterforces"
# record beam response
eval "recorder Element -file outDir/globalForces.out -time -ele BeamElementList globalForce"

# RECORDERS FOR EXCAVATED MATERIAL (TO BE REMOVED)---------------------------------------
file, 'mkdir', ./lift1
file, 'mkdir', ./lift2
file, 'mkdir', ./lift3
file, 'mkdir', ./lift4
file, 'mkdir', ./lift5
file, 'mkdir', ./lift6
file, 'mkdir', ./lift7
file, 'mkdir', ./lift8
file, 'mkdir', ./lift9
file, 'mkdir', ./lift10
# excavation lift 1
model.recorder('Node', file='lift1)/disp.out', time=True, node=430,  437, 446, 455, 461, 468, 473, 476, 480, 482, 484, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift1)/stress1.out', time=True, eleRange=191,  200, "material", 1, "stress")
model.recorder('Element', file='lift1)/stress2.out', time=True, eleRange=191,  200, "material", 2, "stress")
model.recorder('Element', file='lift1)/stress3.out', time=True, eleRange=191,  200, "material", 3, "stress")
model.recorder('Element', file='lift1)/stress4.out', time=True, eleRange=191,  200, "material", 4, "stress")
model.recorder('Element', file='lift1)/slaveForce.out', time=True, ele=1042,  "forces")
model.recorder('Element', file='lift1)/frictForce.out', time=True, ele=1042,  "frictionforces")
model.recorder('Element', file='lift1)/contForce.out',  time=True, ele=1042,  "forcescalars")
model.recorder('Element', file='lift1)/mastForce.out',  time=True, ele=1042,  "masterforces")
# excavation lift 2
model.recorder('Node', file='lift2)/disp.out', time=True, node=412,  424, 433, 444, 453, 460, 466, 471, 475, 479, 483, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift2)/stress1.out', time=True, eleRange=181,  190, "material", 1, "stress")
model.recorder('Element', file='lift2)/stress2.out', time=True, eleRange=181,  190, "material", 2, "stress")
model.recorder('Element', file='lift2)/stress3.out', time=True, eleRange=181,  190, "material", 3, "stress")
model.recorder('Element', file='lift2)/stress4.out', time=True, eleRange=181,  190, "material", 4, "stress")
model.recorder('Element', file='lift2)/slaveForce.out', time=True, ele=1040,  "forces")
model.recorder('Element', file='lift2)/frictForce.out', time=True, ele=1040,  "frictionforces")
model.recorder('Element', file='lift2)/contForce.out',  time=True, ele=1040,  "forcescalars")
model.recorder('Element', file='lift2)/mastForce.out',  time=True, ele=1040,  "masterforces")
# excavation lift 3
model.recorder('Node', file='lift3)/disp.out', time=True, node=387,  405, 418, 429, 442, 450, 458, 464, 470, 477, 481, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift3)/stress1.out', time=True, eleRange=171,  180, "material", 1, "stress")
model.recorder('Element', file='lift3)/stress2.out', time=True, eleRange=171,  180, "material", 2, "stress")
model.recorder('Element', file='lift3)/stress3.out', time=True, eleRange=171,  180, "material", 3, "stress")
model.recorder('Element', file='lift3)/stress4.out', time=True, eleRange=171,  180, "material", 4, "stress")
model.recorder('Element', file='lift3)/slaveForce.out', time=True, ele=1038,  "forces")
model.recorder('Element', file='lift3)/frictForce.out', time=True, ele=1038,  "frictionforces")
model.recorder('Element', file='lift3)/contForce.out',  time=True, ele=1038,  "forcescalars")
model.recorder('Element', file='lift3)/mastForce.out',  time=True, ele=1038,  "masterforces")
# excavation lift 4
model.recorder('Node', file='lift4)/disp.out', time=True, node=363,  380, 398, 414, 427, 439, 448, 457, 465, 472, 478, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift4)/stress1.out', time=True, eleRange=161,  170, "material", 1, "stress")
model.recorder('Element', file='lift4)/stress2.out', time=True, eleRange=161,  170, "material", 2, "stress")
model.recorder('Element', file='lift4)/stress3.out', time=True, eleRange=161,  170, "material", 3, "stress")
model.recorder('Element', file='lift4)/stress4.out', time=True, eleRange=161,  170, "material", 4, "stress")
model.recorder('Element', file='lift4)/slaveForce.out', time=True, ele=1036,  "forces")
model.recorder('Element', file='lift4)/frictForce.out', time=True, ele=1036,  "frictionforces")
model.recorder('Element', file='lift4)/contForce.out',  time=True, ele=1036,  "forcescalars")
model.recorder('Element', file='lift4)/mastForce.out',  time=True, ele=1036,  "masterforces")
# excavation lift 5
model.recorder('Node', file='lift5)/disp.out', time=True, node=336,  353, 378, 395, 411, 425, 440, 449, 459, 467, 474, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift5)/stress1.out', time=True, eleRange=151,  160, "material", 1, "stress")
model.recorder('Element', file='lift5)/stress2.out', time=True, eleRange=151,  160, "material", 2, "stress")
model.recorder('Element', file='lift5)/stress3.out', time=True, eleRange=151,  160, "material", 3, "stress")
model.recorder('Element', file='lift5)/stress4.out', time=True, eleRange=151,  160, "material", 4, "stress")
model.recorder('Element', file='lift5)/slaveForce.out', time=True, ele=1034,  "forces")
model.recorder('Element', file='lift5)/frictForce.out', time=True, ele=1034,  "frictionforces")
model.recorder('Element', file='lift5)/contForce.out',  time=True, ele=1034,  "forcescalars")
model.recorder('Element', file='lift5)/mastForce.out',  time=True, ele=1034,  "masterforces")
# excavation lift 6
model.recorder('Node', file='lift6)/disp.out', time=True, node=308,  326, 347, 369, 392, 408, 426, 441, 452, 462, 469, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift6)/stress1.out', time=True, eleRange=141,  150, "material", 1, "stress")
model.recorder('Element', file='lift6)/stress2.out', time=True, eleRange=141,  150, "material", 2, "stress")
model.recorder('Element', file='lift6)/stress3.out', time=True, eleRange=141,  150, "material", 3, "stress")
model.recorder('Element', file='lift6)/stress4.out', time=True, eleRange=141,  150, "material", 4, "stress")
model.recorder('Element', file='lift6)/slaveForce.out', time=True, ele=1032,  "forces")
model.recorder('Element', file='lift6)/frictForce.out', time=True, ele=1032,  "frictionforces")
model.recorder('Element', file='lift6)/contForce.out',  time=True, ele=1032,  "forcescalars")
model.recorder('Element', file='lift6)/mastForce.out',  time=True, ele=1032,  "masterforces")
# excavation lift 7
model.recorder('Node', file='lift7)/disp.out', time=True, node=281,  304, 322, 345, 370, 394, 415, 428, 443, 454, 463, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift7)/stress1.out', time=True, eleRange=131,  140, "material", 1, "stress")
model.recorder('Element', file='lift7)/stress2.out', time=True, eleRange=131,  140, "material", 2, "stress")
model.recorder('Element', file='lift7)/stress3.out', time=True, eleRange=131,  140, "material", 3, "stress")
model.recorder('Element', file='lift7)/stress4.out', time=True, eleRange=131,  140, "material", 4, "stress")
model.recorder('Element', file='lift7)/slaveForce.out', time=True, ele=1030,  "forces")
model.recorder('Element', file='lift7)/frictForce.out', time=True, ele=1030,  "frictionforces")
model.recorder('Element', file='lift7)/contForce.out',  time=True, ele=1030,  "forcescalars")
model.recorder('Element', file='lift7)/mastForce.out',  time=True, ele=1030,  "masterforces")
# excavation lift 8
model.recorder('Node', file='lift8)/disp.out', time=True, node=260,  278, 302, 325, 346, 374, 399, 419, 434, 447, 456, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift8)/stress1.out', time=True, eleRange=121,  130, "material", 1, "stress")
model.recorder('Element', file='lift8)/stress2.out', time=True, eleRange=121,  130, "material", 2, "stress")
model.recorder('Element', file='lift8)/stress3.out', time=True, eleRange=121,  130, "material", 3, "stress")
model.recorder('Element', file='lift8)/stress4.out', time=True, eleRange=121,  130, "material", 4, "stress")
model.recorder('Element', file='lift8)/slaveForce.out', time=True, ele=1028,  "forces")
model.recorder('Element', file='lift8)/frictForce.out', time=True, ele=1028,  "frictionforces")
model.recorder('Element', file='lift8)/contForce.out',  time=True, ele=1028,  "forcescalars")
model.recorder('Element', file='lift8)/mastForce.out',  time=True, ele=1028,  "masterforces")
# excavation lift 9
model.recorder('Node', file='lift9)/disp.out', time=True, node=241,  253, 277, 306, 327, 350, 379, 406, 422, 438, 451, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift9)/stress1.out', time=True, eleRange=111,  120, "material", 1, "stress")
model.recorder('Element', file='lift9)/stress2.out', time=True, eleRange=111,  120, "material", 2, "stress")
model.recorder('Element', file='lift9)/stress3.out', time=True, eleRange=111,  120, "material", 3, "stress")
model.recorder('Element', file='lift9)/stress4.out', time=True, eleRange=111,  120, "material", 4, "stress")
model.recorder('Element', file='lift9)/slaveForce.out', time=True, ele=1026,  "forces")
model.recorder('Element', file='lift9)/frictForce.out', time=True, ele=1026,  "frictionforces")
model.recorder('Element', file='lift9)/contForce.out',  time=True, ele=1026,  "forcescalars")
model.recorder('Element', file='lift9)/mastForce.out',  time=True, ele=1026,  "masterforces")
# excavation lift 10
model.recorder('Node', file='lift10)/disp.out', time=True, node=218,  239, 259, 282, 307, 335, 364, 389, 413, 431, 445, dof=[1, 2 ], "disp")
model.recorder('Element', file='lift10/stress1.out',    time=True, eleRange=[101,  110], "material", 1, "stress")
model.recorder('Element', file='lift10/stress2.out',    time=True, eleRange=[101,  110], "material", 2, "stress")
model.recorder('Element', file='lift10/stress3.out',    time=True, eleRange=[101,  110], "material", 3, "stress")
model.recorder('Element', file='lift10/stress4.out',    time=True, eleRange=[101,  110], "material", 4, "stress")
model.recorder('Element', file='lift10/slaveForce.out', time=True, ele=1024,  "forces")
model.recorder('Element', file='lift10/frictForce.out', time=True, ele=1024,  "frictionforces")
model.recorder('Element', file='lift10/contForce.out',  time=True, ele=1024,  "forcescalars")
model.recorder('Element', file='lift10/mastForce.out',  time=True, ele=1024,  "masterforces")

print("Finished creating recorders...")

#-----------------------------------------------------------------------------------------
#  12. GRAVITY ANALYSIS (w/ INITIAL STATE ANALYSIS TO RESET DISPLACEMENTS)
#-----------------------------------------------------------------------------------------

# define analysis parameters for gravity phase
model.constraints('Transformation')
model.test(       NormDispIncr, 1e-5, 15, 1)
model.algorithm(  Newton)
model.numberer(   RCM)
model.system(     SparseGeneral)
model.integrator( LoadControl, 1)
model.analysis(   Static)

# turn on initial state analysis feature
InitialStateAnalysis, 'on'

# ensure soil material intially considers linear elastic behavior
updateMaterialStage( material=1,  stage=0)

# contact = elements to be frictionless for gravity analysis
Parameter = value=0,  eleRange=1001,  1042, friction

startT =  [clock, 'seconds]'
model.analyze(    4)

# update soil material to consider elastoplastic behavior and analyze a few more steps
updateMaterialStage, material=1,  stage=1)

model.analyze(4)

# designate end of initial state analysis (zeros displacements, keeps state variables)
InitialStateAnalysis, 'off'

# turn on frictional behavior for beam contact elements
Parameter = value=1,  eleRange=1001,  1042, friction

#-----------------------------------------------------------------------------------------
#  14. REMOVE ELEMENTS TO SIMULATE EXCAVATION
#-----------------------------------------------------------------------------------------

# define analysis parameters for excavation phase
model.constraints('Transformation')
model.test(       NormDispIncr, 1e-4, 60, 1)
model.algorithm(  KrylovNewton)
model.numberer(   RCM)
model.system(     SparseGeneral)
model.integrator( LoadControl, 1)
model.analysis(   Static)

# remove objects associated with lift 1-----------------------------------
# recorders
recCount = 10
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 190+k)

# contact element
model.remove('element', 1042)
# lagrange multiplier node
model.remove('node', 1042)
# soil nodes
model.remove('node', 430 )
model.remove('node', 437 )
model.remove('node', 446 )
model.remove('node', 455 )
model.remove('node', 461 )
model.remove('node', 468 )
model.remove('node', 473 )
model.remove('node', 476 )
model.remove('node', 480 )
model.remove('node', 482 )
model.remove('node', 484)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 2-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 180+k)

# contact element
model.remove('element', 1040)
# lagrange multiplier node
model.remove('node', 1040)
# soil nodes
model.remove('node', 412 )
model.remove('node', 424 )
model.remove('node', 433 )
model.remove('node', 444 )
model.remove('node', 453 )
model.remove('node', 460 )
model.remove('node', 466 )
model.remove('node', 471 )
model.remove('node', 475 )
model.remove('node', 479 )
model.remove('node', 483)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 3-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 170+k)

# contact element
model.remove('element', 1038)
# lagrange multiplier node
model.remove('node', 1038)
# soil nodes
model.remove('node', 387 )
model.remove('node', 405 )
model.remove('node', 418 )
model.remove('node', 429 )
model.remove('node', 442 )
model.remove('node', 450 )
model.remove('node', 458 )
model.remove('node', 464 )
model.remove('node', 470 )
model.remove('node', 477 )
model.remove('node', 481)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 4-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 160+k)

# contact element
model.remove('element', 1036)
# lagrange multiplier node
model.remove('node', 1036)
# soil nodes
model.remove('node', 363 )
model.remove('node', 380 )
model.remove('node', 398 )
model.remove('node', 414 )
model.remove('node', 427 )
model.remove('node', 439 )
model.remove('node', 448 )
model.remove('node', 457 )
model.remove('node', 465 )
model.remove('node', 472 )
model.remove('node', 478)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 5-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 150+k)

# contact element
model.remove('element', 1034)
# lagrange multiplier node
model.remove('node', 1034)
# soil nodes
model.remove('node', 336 )
model.remove('node', 353 )
model.remove('node', 378 )
model.remove('node', 395 )
model.remove('node', 411 )
model.remove('node', 425 )
model.remove('node', 440 )
model.remove('node', 449 )
model.remove('node', 459 )
model.remove('node', 467 )
model.remove('node', 474)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 6-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 140+k)

# contact element
model.remove('element', 1032)
# lagrange multiplier node
model.remove('node', 1032)
# soil nodes
model.remove('node', 308 )
model.remove('node', 326 )
model.remove('node', 347 )
model.remove('node', 369 )
model.remove('node', 392 )
model.remove('node', 408 )
model.remove('node', 426 )
model.remove('node', 441 )
model.remove('node', 452 )
model.remove('node', 462 )
model.remove('node', 469)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 7-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 130+k)

# contact element
model.remove('element', 1030)
# lagrange multiplier node
model.remove('node', 1030)
# soil nodes
model.remove('node', 281 )
model.remove('node', 304 )
model.remove('node', 322 )
model.remove('node', 345 )
model.remove('node', 370 )
model.remove('node', 394 )
model.remove('node', 415 )
model.remove('node', 428 )
model.remove('node', 443 )
model.remove('node', 454 )
model.remove('node', 463)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 8-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
       model.remove('element', 120+k)

# contact element
model.remove('element', 1028)
# lagrange multiplier node
model.remove('node', 1028)
# soil nodes
model.remove('node', 260 )
model.remove('node', 278 )
model.remove('node', 302 )
model.remove('node', 325 )
model.remove('node', 346 )
model.remove('node', 374 )
model.remove('node', 399 )
model.remove('node', 419 )
model.remove('node', 434 )
model.remove('node', 447 )
model.remove('node', 456)

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 9-----------------------------------
# recorders
for k in range(0, 8+1):
       model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1,11):
       model.remove('element', 110+k)

# contact element
model.remove('element', 1026)
# lagrange multiplier node
model.remove('node', 1026)
# soil nodes
model.remove('node', 241 )
model.remove('node', 253 )
model.remove('node', 277 )
model.remove('node', 306 )
model.remove('node', 327 )
model.remove('node', 350 )
model.remove('node', 379 )
model.remove('node', 406 )
model.remove('node', 422 )
model.remove('node', 438 )
model.remove('node', 451 )

# run analysis after object removal
model.analyze(4)

# remove objects associated with lift 10----------------------------------
# recorders
for k in range(0, 8+1):
    model.remove('recorder', recCount + k)

recCount = (recCount + k)
# soil elements
for k in range(1, 10+1):
    model.remove('element', 100+k)

# contact element
model.remove('element', 1024)
# lagrange multiplier node
model.remove('node', 1024)
# soil nodes
model.remove('node', 218 )
model.remove('node', 239 )
model.remove('node', 259 )
model.remove('node', 282 )
model.remove('node', 307 )
model.remove('node', 335 )
model.remove('node', 364 )
model.remove('node', 389 )
model.remove('node', 413 )
model.remove('node', 431 )
model.remove('node', 445 )

# run analysis after object removal
model.analyze(4)

# excavation analysis complete
#endT =    [clock, 'seconds]'
print("Analysis execution time:, (endT-startT) seconds")

