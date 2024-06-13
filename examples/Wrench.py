

#              OO+O+O                                                           
#             O+++OO                                                            
#             O+OO+O                                                            
#            O+O+O+O                                                            
#            OOO+OO                                                             
#            OO+O+O                                                             
#           O+O+OO                                                              
#           OO+O+O                                                              
#          O+O+O+O                                                              
#          OO+O+O                                                               
#         O+O+O+O                                                               
#         O+OO+O                                                                
#        O+O+OO                                                                 
#        OO+O+O                                                                 
#      OOOOOOO+O                                                                
#   O+O+OOO+OO+OO                                                               
# OOOOOOOOOOOOOO+OO                                                             
# OOOOOOOO+OOOO+OOO                                                             
# OOOOOO+OO+OOOOOOO                                                             
# OOOOO       OOOOO                                                             
#  O+OO       OOOO                                                              
#   OOO       OOO                                                               
#


title = "CST Sample Problem (Logan #8.22)"

material properties
steel  E=200000 A=0 Ix=0 Iy=0 Iz=0 J=0 G=0 nu=0.25 t=10 rho=0 kappa=0

constraints
free  tx=u ty=u tz=u rx=u ry=u rz=u
fixed  tx=c ty=c tz=u rx=u ry=u rz=u

forces
pushme  Fx=700 Fy=0 Fz=0 Mx=0 My=0 Mz=0


model.node(1, 0 y=50 z=0 constraint=free
model.node(2, 20 y=10 z=0
model.node(3, 40 y=0 z=0
model.node(4, 40 y=50 z=0 constraint=fixed
model.node(5, 55 y=70 z=0 constraint=free
model.node(6, 95 y=70 z=0
model.node(7, 115 y=50 z=0
model.node(8, 115 y=0 z=0 constraint=fixed
model.node(9, 135 y=10 z=0 constraint=free
model.node(10, 155 y=50 z=0
model.node(11, 155 y=90 z=0
model.node(12, 115 y=160 z=0
model.node(13, 170 y=404 z=0
model.node(14, 122 y=404 z=0 force=pushme
model.node(15, 67 y=160 z=0
model.node(16, 0 y=90 z=0
model.node(17, 26.2595 y=117.435 z=0
model.node(18, 30 y=50 z=0
model.node(19, 20 y=50 z=0
model.node(20, 10 y=50 z=0
model.node(21, 5 y=40 z=0
model.node(22, 10 y=30 z=0
model.node(23, 15 y=20 z=0
model.node(24, 30 y=5 z=0
model.node(25, 40 y=10 z=0
model.node(26, 40 y=20 z=0
model.node(27, 40 y=30 z=0
model.node(28, 40 y=40 z=0
model.node(29, 49.2519 y=79.4871 z=0
model.node(30, 43.5038 y=88.9741 z=0
model.node(31, 37.7557 y=98.4612 z=0
model.node(32, 32.0076 y=107.948 z=0
model.node(33, 19.6947 y=110.577 z=0
model.node(34, 13.1298 y=103.718 z=0
model.node(35, 6.56489 y=96.8588 z=0
model.node(36, 0 y=80 z=0
model.node(37, 0 y=70 z=0
model.node(38, 0 y=60 z=0
model.node(39, 47.5 y=60 z=0
model.node(40, 99 y=160 z=0
model.node(41, 83 y=160 z=0
model.node(42, 58.8519 y=151.487 z=0
model.node(43, 50.7038 y=142.974 z=0
model.node(44, 42.5557 y=134.461 z=0
model.node(45, 34.4076 y=125.948 z=0
model.node(46, 68.3333 y=70 z=0
model.node(47, 81.6667 y=70 z=0
model.node(48, 107 y=74 z=0
model.node(49, 119 y=78 z=0
model.node(50, 131 y=82 z=0
model.node(51, 143 y=86 z=0
model.node(52, 149.286 y=100 z=0
model.node(53, 143.571 y=110 z=0
model.node(54, 137.857 y=120 z=0
model.node(55, 132.143 y=130 z=0
model.node(56, 126.429 y=140 z=0
model.node(57, 120.714 y=150 z=0
model.node(58, 125 y=50 z=0
model.node(59, 135 y=50 z=0
model.node(60, 145 y=50 z=0
model.node(61, 155 y=63.3333 z=0
model.node(62, 155 y=76.6667 z=0
model.node(63, 105 y=60 z=0
model.node(64, 115 y=40 z=0
model.node(65, 115 y=30 z=0
model.node(66, 115 y=20 z=0
model.node(67, 115 y=10 z=0
model.node(68, 125 y=5 z=0
model.node(69, 140 y=20 z=0
model.node(70, 145 y=30 z=0
model.node(71, 150 y=40 z=0
model.node(72, 118.929 y=177.429 z=0
model.node(73, 122.857 y=194.857 z=0
model.node(74, 126.786 y=212.286 z=0
model.node(75, 130.714 y=229.714 z=0
model.node(76, 134.643 y=247.143 z=0
model.node(77, 138.571 y=264.571 z=0
model.node(78, 142.5 y=282 z=0
model.node(79, 146.429 y=299.429 z=0
model.node(80, 150.357 y=316.857 z=0
model.node(81, 154.286 y=334.286 z=0
model.node(82, 158.214 y=351.714 z=0
model.node(83, 162.143 y=369.143 z=0
model.node(84, 166.071 y=386.571 z=0
model.node(85, 154 y=404 z=0
model.node(86, 138 y=404 z=0
model.node(87, 118.071 y=386.571 z=0
model.node(88, 114.143 y=369.143 z=0
model.node(89, 110.214 y=351.714 z=0
model.node(90, 106.286 y=334.286 z=0
model.node(91, 102.357 y=316.857 z=0
model.node(92, 98.4286 y=299.429 z=0
model.node(93, 94.5 y=282 z=0
model.node(94, 90.5714 y=264.571 z=0
model.node(95, 86.6429 y=247.143 z=0
model.node(96, 82.7143 y=229.714 z=0
model.node(97, 78.7857 y=212.286 z=0
model.node(98, 74.8571 y=194.857 z=0
model.node(99, 70.9286 y=177.429 z=0
model.node(100, 15.8281 y=41.1347 z=0
model.node(101, 21.1837 y=32.5994 z=0
model.node(102, 29.506 y=38.2678 z=0
model.node(103, 23.4558 y=21.9638 z=0
model.node(104, 31.778 y=27.6323 z=0
model.node(105, 30.8991 y=14.8505 z=0
model.node(106, 24.9546 y=101.66 z=0
model.node(107, 14.9486 y=93.5215 z=0
model.node(108, 25.3499 y=89.7387 z=0
model.node(109, 35.7513 y=85.9558 z=0
model.node(110, 11.0391 y=83.1662 z=0
model.node(111, 21.4404 y=79.3834 z=0
model.node(112, 31.8418 y=75.6006 z=0
model.node(113, 42.2431 y=71.8177 z=0
model.node(114, 12.8673 y=70.7242 z=0
model.node(115, 23.2687 y=66.9414 z=0
model.node(116, 33.67 y=63.1585 z=0
model.node(117, 11.8878 y=59.3033 z=0
model.node(118, 40.8546 y=110.492 z=0
model.node(119, 43.2864 y=122.454 z=0
model.node(120, 50.9941 y=99.0945 z=0
model.node(121, 53.4259 y=111.057 z=0
model.node(122, 55.8578 y=123.019 z=0
model.node(123, 58.2896 y=134.981 z=0
model.node(124, 59.4604 y=79.4672 z=0
model.node(125, 61.8922 y=91.4292 z=0
model.node(126, 64.3241 y=103.391 z=0
model.node(127, 66.7559 y=115.353 z=0
model.node(128, 69.1878 y=127.316 z=0
model.node(129, 71.6196 y=139.278 z=0
model.node(130, 74.0514 y=151.24 z=0
model.node(131, 71.845 y=79.1137 z=0
model.node(132, 74.2769 y=91.0758 z=0
model.node(133, 76.7087 y=103.038 z=0
model.node(134, 79.1405 y=115 z=0
model.node(135, 81.5724 y=126.962 z=0
model.node(136, 84.0042 y=138.924 z=0
model.node(137, 86.4361 y=150.886 z=0
model.node(138, 84.3015 y=79.1137 z=0
model.node(139, 86.7333 y=91.0758 z=0
model.node(140, 89.1652 y=103.038 z=0
model.node(141, 91.597 y=115 z=0
model.node(142, 94.0289 y=126.962 z=0
model.node(143, 96.4607 y=138.924 z=0
model.node(144, 98.8925 y=150.886 z=0
model.node(145, 97.8941 y=84.7022 z=0
model.node(146, 100.326 y=96.6643 z=0
model.node(147, 102.758 y=108.626 z=0
model.node(148, 105.19 y=120.588 z=0
model.node(149, 107.621 y=132.551 z=0
model.node(150, 110.053 y=144.513 z=0
model.node(151, 110.385 y=84.8709 z=0
model.node(152, 112.817 y=96.833 z=0
model.node(153, 115.249 y=108.795 z=0
model.node(154, 117.68 y=120.757 z=0
model.node(155, 120.112 y=132.719 z=0
model.node(156, 124.092 y=91.0207 z=0
model.node(157, 126.523 y=102.983 z=0
model.node(158, 128.955 y=114.945 z=0
model.node(159, 137.798 y=97.1705 z=0
model.node(160, 146.214 y=77.4792 z=0
model.node(161, 135.111 y=72.1423 z=0
model.node(162, 138.975 y=60.5485 z=0
model.node(163, 124.805 y=64.4131 z=0
model.node(164, 111.384 y=66.0303 z=0
model.node(165, 139.172 y=41.1347 z=0
model.node(166, 125.494 y=38.2678 z=0
model.node(167, 133.816 y=32.5994 z=0
model.node(168, 123.222 y=27.6323 z=0
model.node(169, 131.544 y=21.9638 z=0
model.node(170, 124.101 y=14.8505 z=0
model.node(171, 149.305 y=390.219 z=0
model.node(172, 131.304 y=377.944 z=0
model.node(173, 147.729 y=372.527 z=0
model.node(174, 127.482 y=360.993 z=0
model.node(175, 143.908 y=355.575 z=0
model.node(176, 123.661 y=344.041 z=0
model.node(177, 140.087 y=338.623 z=0
model.node(178, 119.84 y=327.089 z=0
model.node(179, 136.265 y=321.671 z=0
model.node(180, 116.019 y=310.137 z=0
model.node(181, 132.444 y=304.719 z=0
model.node(182, 112.198 y=293.185 z=0
model.node(183, 128.623 y=287.767 z=0
model.node(184, 108.377 y=276.233 z=0
model.node(185, 124.802 y=270.815 z=0
model.node(186, 104.556 y=259.281 z=0
model.node(187, 120.981 y=253.863 z=0
model.node(188, 100.735 y=242.329 z=0
model.node(189, 117.16 y=236.911 z=0
model.node(190, 96.9134 y=225.377 z=0
model.node(191, 113.339 y=219.959 z=0
model.node(192, 93.0922 y=208.425 z=0
model.node(193, 109.518 y=203.007 z=0
model.node(194, 89.2711 y=191.473 z=0
model.node(195, 105.696 y=186.056 z=0
model.node(196, 87.6948 y=173.781 z=0

CSTPlaneStress elements
model.element("Tri",   1  nodes=[100,101,102]   material=steel    
model.element("Tri",   2  nodes=[101,103,104]   
model.element("Tri",   3  nodes=[102,101,104]   
model.element("Tri",   4  nodes=[104,103,105]   
model.element("Tri",   5  nodes=[20,100,19]   
model.element("Tri",   6  nodes=[1,21,20]   
model.element("Tri",   7  nodes=[21,100,20]   
model.element("Tri",   8  nodes=[22,100,21]   
model.element("Tri",   9  nodes=[22,101,100]   
model.element("Tri",  10  nodes=[23,101,22]   
model.element("Tri",  11  nodes=[23,103,101]   
model.element("Tri",  12  nodes=[2,103,23]   
model.element("Tri",  13  nodes=[2,105,103]   
model.element("Tri",  14  nodes=[24,105,2]   
model.element("Tri",  15  nodes=[3,25,24]   
model.element("Tri",  16  nodes=[25,105,24]   
model.element("Tri",  17  nodes=[26,105,25]   
model.element("Tri",  18  nodes=[26,104,105]   
model.element("Tri",  19  nodes=[27,104,26]   
model.element("Tri",  20  nodes=[27,102,104]   
model.element("Tri",  21  nodes=[28,102,27]   
model.element("Tri",  22  nodes=[4,18,28]   
model.element("Tri",  23  nodes=[18,102,28]   
model.element("Tri",  24  nodes=[19,102,18]   
model.element("Tri",  25  nodes=[19,100,102]   
model.element("Tri",  26  nodes=[106,107,108]   
model.element("Tri",  27  nodes=[107,110,111]   
model.element("Tri",  28  nodes=[108,107,111]   
model.element("Tri",  29  nodes=[108,111,112]   
model.element("Tri",  30  nodes=[109,108,112]   
model.element("Tri",  31  nodes=[109,112,113]   
model.element("Tri",  32  nodes=[111,110,114]   
model.element("Tri",  33  nodes=[111,114,115]   
model.element("Tri",  34  nodes=[112,111,115]   
model.element("Tri",  35  nodes=[112,115,116]   
model.element("Tri",  36  nodes=[113,112,116]   
model.element("Tri",  37  nodes=[115,114,117]   
model.element("Tri",  38  nodes=[17,33,32]   
model.element("Tri",  39  nodes=[33,106,32]   
model.element("Tri",  40  nodes=[34,106,33]   
model.element("Tri",  41  nodes=[34,107,106]   
model.element("Tri",  42  nodes=[35,107,34]   
model.element("Tri",  43  nodes=[35,110,107]   
model.element("Tri",  44  nodes=[16,110,35]   
model.element("Tri",  45  nodes=[36,110,16]   
model.element("Tri",  46  nodes=[36,114,110]   
model.element("Tri",  47  nodes=[37,114,36]   
model.element("Tri",  48  nodes=[37,117,114]   
model.element("Tri",  49  nodes=[38,117,37]   
model.element("Tri",  50  nodes=[1,20,38]   
model.element("Tri",  51  nodes=[20,117,38]   
model.element("Tri",  52  nodes=[19,117,20]   
model.element("Tri",  53  nodes=[19,115,117]   
model.element("Tri",  54  nodes=[18,115,19]   
model.element("Tri",  55  nodes=[18,116,115]   
model.element("Tri",  56  nodes=[4,116,18]   
model.element("Tri",  57  nodes=[39,116,4]   
model.element("Tri",  58  nodes=[39,113,116]   
model.element("Tri",  59  nodes=[5,113,39]   
model.element("Tri",  60  nodes=[29,113,5]   
model.element("Tri",  61  nodes=[29,109,113]   
model.element("Tri",  62  nodes=[30,109,29]   
model.element("Tri",  63  nodes=[31,109,30]   
model.element("Tri",  64  nodes=[31,108,109]   
model.element("Tri",  65  nodes=[31,106,108]   
model.element("Tri",  66  nodes=[32,106,31]   
model.element("Tri",  67  nodes=[118,120,121]   
model.element("Tri",  68  nodes=[119,118,121]   
model.element("Tri",  69  nodes=[119,121,122]   
model.element("Tri",  70  nodes=[120,125,126]   
model.element("Tri",  71  nodes=[121,120,126]   
model.element("Tri",  72  nodes=[121,126,127]   
model.element("Tri",  73  nodes=[122,121,127]   
model.element("Tri",  74  nodes=[122,127,128]   
model.element("Tri",  75  nodes=[123,122,128]   
model.element("Tri",  76  nodes=[123,128,129]   
model.element("Tri",  77  nodes=[125,124,131]   
model.element("Tri",  78  nodes=[125,131,132]   
model.element("Tri",  79  nodes=[126,125,132]   
model.element("Tri",  80  nodes=[126,132,133]   
model.element("Tri",  81  nodes=[127,126,133]   
model.element("Tri",  82  nodes=[127,133,134]   
model.element("Tri",  83  nodes=[128,127,134]   
model.element("Tri",  84  nodes=[128,134,135]   
model.element("Tri",  85  nodes=[129,128,135]   
model.element("Tri",  86  nodes=[129,135,136]   
model.element("Tri",  87  nodes=[130,129,136]   
model.element("Tri",  88  nodes=[130,136,137]   
model.element("Tri",  89  nodes=[132,131,138]   
model.element("Tri",  90  nodes=[132,138,139]   
model.element("Tri",  91  nodes=[133,132,139]   
model.element("Tri",  92  nodes=[133,139,140]   
model.element("Tri",  93  nodes=[134,133,140]   
model.element("Tri",  94  nodes=[134,140,141]   
model.element("Tri",  95  nodes=[135,134,141]   
model.element("Tri",  96  nodes=[135,141,142]   
model.element("Tri",  97  nodes=[136,135,142]   
model.element("Tri",  98  nodes=[136,142,143]   
model.element("Tri",  99  nodes=[137,136,143]   
model.element("Tri", 100  nodes=[137,143,144]   
model.element("Tri", 101  nodes=[139,138,145]   
model.element("Tri", 102  nodes=[139,145,146]   
model.element("Tri", 103  nodes=[140,139,146]   
model.element("Tri", 104  nodes=[140,146,147]   
model.element("Tri", 105  nodes=[141,140,147]   
model.element("Tri", 106  nodes=[141,147,148]   
model.element("Tri", 107  nodes=[142,141,148]   
model.element("Tri", 108  nodes=[142,148,149]   
model.element("Tri", 109  nodes=[143,142,149]   
model.element("Tri", 110  nodes=[143,149,150]   
model.element("Tri", 111  nodes=[144,143,150]   
model.element("Tri", 112  nodes=[146,145,151]   
model.element("Tri", 113  nodes=[146,151,152]   
model.element("Tri", 114  nodes=[147,146,152]   
model.element("Tri", 115  nodes=[147,152,153]   
model.element("Tri", 116  nodes=[148,147,153]   
model.element("Tri", 117  nodes=[148,153,154]   
model.element("Tri", 118  nodes=[149,148,154]   
model.element("Tri", 119  nodes=[149,154,155]   
model.element("Tri", 120  nodes=[150,149,155]   
model.element("Tri", 121  nodes=[152,151,156]   
model.element("Tri", 122  nodes=[152,156,157]   
model.element("Tri", 123  nodes=[153,152,157]   
model.element("Tri", 124  nodes=[153,157,158]   
model.element("Tri", 125  nodes=[154,153,158]   
model.element("Tri", 126  nodes=[157,156,159]   
model.element("Tri", 127  nodes=[31,118,32]   
model.element("Tri", 128  nodes=[31,120,118]   
model.element("Tri", 129  nodes=[30,120,31]   
model.element("Tri", 130  nodes=[30,125,120]   
model.element("Tri", 131  nodes=[29,125,30]   
model.element("Tri", 132  nodes=[29,124,125]   
model.element("Tri", 133  nodes=[5,124,29]   
model.element("Tri", 134  nodes=[46,124,5]   
model.element("Tri", 135  nodes=[46,131,124]   
model.element("Tri", 136  nodes=[47,131,46]   
model.element("Tri", 137  nodes=[47,138,131]   
model.element("Tri", 138  nodes=[6,138,47]   
model.element("Tri", 139  nodes=[6,145,138]   
model.element("Tri", 140  nodes=[48,145,6]   
model.element("Tri", 141  nodes=[48,151,145]   
model.element("Tri", 142  nodes=[49,151,48]   
model.element("Tri", 143  nodes=[49,156,151]   
model.element("Tri", 144  nodes=[50,156,49]   
model.element("Tri", 145  nodes=[50,159,156]   
model.element("Tri", 146  nodes=[51,159,50]   
model.element("Tri", 147  nodes=[11,52,51]   
model.element("Tri", 148  nodes=[52,159,51]   
model.element("Tri", 149  nodes=[53,159,52]   
model.element("Tri", 150  nodes=[53,157,159]   
model.element("Tri", 151  nodes=[53,158,157]   
model.element("Tri", 152  nodes=[54,158,53]   
model.element("Tri", 153  nodes=[55,158,54]   
model.element("Tri", 154  nodes=[55,154,158]   
model.element("Tri", 155  nodes=[55,155,154]   
model.element("Tri", 156  nodes=[56,155,55]   
model.element("Tri", 157  nodes=[56,150,155]   
model.element("Tri", 158  nodes=[57,150,56]   
model.element("Tri", 159  nodes=[12,150,57]   
model.element("Tri", 160  nodes=[12,144,150]   
model.element("Tri", 161  nodes=[40,144,12]   
model.element("Tri", 162  nodes=[40,137,144]   
model.element("Tri", 163  nodes=[41,137,40]   
model.element("Tri", 164  nodes=[41,130,137]   
model.element("Tri", 165  nodes=[15,130,41]   
model.element("Tri", 166  nodes=[42,130,15]   
model.element("Tri", 167  nodes=[42,129,130]   
model.element("Tri", 168  nodes=[42,123,129]   
model.element("Tri", 169  nodes=[43,123,42]   
model.element("Tri", 170  nodes=[44,123,43]   
model.element("Tri", 171  nodes=[44,122,123]   
model.element("Tri", 172  nodes=[44,119,122]   
model.element("Tri", 173  nodes=[45,119,44]   
model.element("Tri", 174  nodes=[45,118,119]   
model.element("Tri", 175  nodes=[17,118,45]   
model.element("Tri", 176  nodes=[32,118,17]   
model.element("Tri", 177  nodes=[162,161,163]   
model.element("Tri", 178  nodes=[11,160,62]   
model.element("Tri", 179  nodes=[51,160,11]   
model.element("Tri", 180  nodes=[50,160,51]   
model.element("Tri", 181  nodes=[50,161,160]   
model.element("Tri", 182  nodes=[49,161,50]   
model.element("Tri", 183  nodes=[49,163,161]   
model.element("Tri", 184  nodes=[49,164,163]   
model.element("Tri", 185  nodes=[48,164,49]   
model.element("Tri", 186  nodes=[6,63,48]   
model.element("Tri", 187  nodes=[63,164,48]   
model.element("Tri", 188  nodes=[7,164,63]   
model.element("Tri", 189  nodes=[7,163,164]   
model.element("Tri", 190  nodes=[58,163,7]   
model.element("Tri", 191  nodes=[59,163,58]   
model.element("Tri", 192  nodes=[59,162,163]   
model.element("Tri", 193  nodes=[60,162,59]   
model.element("Tri", 194  nodes=[10,61,60]   
model.element("Tri", 195  nodes=[61,162,60]   
model.element("Tri", 196  nodes=[61,160,162]   
model.element("Tri", 197  nodes=[162,160,161]   
model.element("Tri", 198  nodes=[62,160,61]   
model.element("Tri", 199  nodes=[165,166,167]   
model.element("Tri", 200  nodes=[167,166,168]   
model.element("Tri", 201  nodes=[167,168,169]   
model.element("Tri", 202  nodes=[169,168,170]   
model.element("Tri", 203  nodes=[59,166,165]   
model.element("Tri", 204  nodes=[58,166,59]   
model.element("Tri", 205  nodes=[7,64,58]   
model.element("Tri", 206  nodes=[64,166,58]   
model.element("Tri", 207  nodes=[65,166,64]   
model.element("Tri", 208  nodes=[65,168,166]   
model.element("Tri", 209  nodes=[66,168,65]   
model.element("Tri", 210  nodes=[66,170,168]   
model.element("Tri", 211  nodes=[67,170,66]   
model.element("Tri", 212  nodes=[8,68,67]   
model.element("Tri", 213  nodes=[68,170,67]   
model.element("Tri", 214  nodes=[9,170,68]   
model.element("Tri", 215  nodes=[9,169,170]   
model.element("Tri", 216  nodes=[69,169,9]   
model.element("Tri", 217  nodes=[69,167,169]   
model.element("Tri", 218  nodes=[70,167,69]   
model.element("Tri", 219  nodes=[70,165,167]   
model.element("Tri", 220  nodes=[71,165,70]   
model.element("Tri", 221  nodes=[10,60,71]   
model.element("Tri", 222  nodes=[60,165,71]   
model.element("Tri", 223  nodes=[59,165,60]   
model.element("Tri", 224  nodes=[171,172,173]   
model.element("Tri", 225  nodes=[173,172,174]   
model.element("Tri", 226  nodes=[173,174,175]   
model.element("Tri", 227  nodes=[175,174,176]   
model.element("Tri", 228  nodes=[175,176,177]   
model.element("Tri", 229  nodes=[177,176,178]   
model.element("Tri", 230  nodes=[177,178,179]   
model.element("Tri", 231  nodes=[179,178,180]   
model.element("Tri", 232  nodes=[179,180,181]   
model.element("Tri", 233  nodes=[181,180,182]   
model.element("Tri", 234  nodes=[181,182,183]   
model.element("Tri", 235  nodes=[183,182,184]   
model.element("Tri", 236  nodes=[183,184,185]   
model.element("Tri", 237  nodes=[185,184,186]   
model.element("Tri", 238  nodes=[185,186,187]   
model.element("Tri", 239  nodes=[187,186,188]   
model.element("Tri", 240  nodes=[187,188,189]   
model.element("Tri", 241  nodes=[189,188,190]   
model.element("Tri", 242  nodes=[189,190,191]   
model.element("Tri", 243  nodes=[191,190,192]   
model.element("Tri", 244  nodes=[191,192,193]   
model.element("Tri", 245  nodes=[193,192,194]   
model.element("Tri", 246  nodes=[193,194,195]   
model.element("Tri", 247  nodes=[195,194,196]   
model.element("Tri", 248  nodes=[86,171,85]   
model.element("Tri", 249  nodes=[86,172,171]   
model.element("Tri", 250  nodes=[14,87,86]   
model.element("Tri", 251  nodes=[87,172,86]   
model.element("Tri", 252  nodes=[88,172,87]   
model.element("Tri", 253  nodes=[88,174,172]   
model.element("Tri", 254  nodes=[89,174,88]   
model.element("Tri", 255  nodes=[89,176,174]   
model.element("Tri", 256  nodes=[90,176,89]   
model.element("Tri", 257  nodes=[90,178,176]   
model.element("Tri", 258  nodes=[91,178,90]   
model.element("Tri", 259  nodes=[91,180,178]   
model.element("Tri", 260  nodes=[92,180,91]   
model.element("Tri", 261  nodes=[92,182,180]   
model.element("Tri", 262  nodes=[93,182,92]   
model.element("Tri", 263  nodes=[93,184,182]   
model.element("Tri", 264  nodes=[94,184,93]   
model.element("Tri", 265  nodes=[94,186,184]   
model.element("Tri", 266  nodes=[95,186,94]   
model.element("Tri", 267  nodes=[95,188,186]   
model.element("Tri", 268  nodes=[96,188,95]   
model.element("Tri", 269  nodes=[96,190,188]   
model.element("Tri", 270  nodes=[97,190,96]   
model.element("Tri", 271  nodes=[97,192,190]   
model.element("Tri", 272  nodes=[98,192,97]   
model.element("Tri", 273  nodes=[98,194,192]   
model.element("Tri", 274  nodes=[99,194,98]   
model.element("Tri", 275  nodes=[99,196,194]   
model.element("Tri", 276  nodes=[15,41,99]   
model.element("Tri", 277  nodes=[41,196,99]   
model.element("Tri", 278  nodes=[40,196,41]   
model.element("Tri", 279  nodes=[40,195,196]   
model.element("Tri", 280  nodes=[12,72,40]   
model.element("Tri", 281  nodes=[72,195,40]   
model.element("Tri", 282  nodes=[73,195,72]   
model.element("Tri", 283  nodes=[73,193,195]   
model.element("Tri", 284  nodes=[74,193,73]   
model.element("Tri", 285  nodes=[74,191,193]   
model.element("Tri", 286  nodes=[75,191,74]   
model.element("Tri", 287  nodes=[75,189,191]   
model.element("Tri", 288  nodes=[76,189,75]   
model.element("Tri", 289  nodes=[76,187,189]   
model.element("Tri", 290  nodes=[77,187,76]   
model.element("Tri", 291  nodes=[77,185,187]   
model.element("Tri", 292  nodes=[78,185,77]   
model.element("Tri", 293  nodes=[78,183,185]   
model.element("Tri", 294  nodes=[79,183,78]   
model.element("Tri", 295  nodes=[79,181,183]   
model.element("Tri", 296  nodes=[80,181,79]   
model.element("Tri", 297  nodes=[80,179,181]   
model.element("Tri", 298  nodes=[81,179,80]   
model.element("Tri", 299  nodes=[81,177,179]   
model.element("Tri", 300  nodes=[82,177,81]   
model.element("Tri", 301  nodes=[82,175,177]   
model.element("Tri", 302  nodes=[83,175,82]   
model.element("Tri", 303  nodes=[83,173,175]   
model.element("Tri", 304  nodes=[84,173,83]   
model.element("Tri", 305  nodes=[84,171,173]   
model.element("Tri", 306  nodes=[13,85,84]   
model.element("Tri", 307  nodes=[85,171,84]   

