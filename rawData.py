import matplotlib.pyplot as plt

xList = [-3.5, -3.4, -3.3, -3.1999999999999997, -3.0999999999999996, -2.9999999999999996, -2.8999999999999995, -2.7999999999999994, -2.6999999999999993, -2.599999999999999, -2.499999999999999, -2.399999999999999, -2.299999999999999, -2.199999999999999, -2.0999999999999988, -1.9999999999999987, -1.8999999999999986, -1.7999999999999985, -1.6999999999999984, -1.5999999999999983, -1.4999999999999982, -1.3999999999999981, -1.299999999999998, -1.199999999999998, -1.0999999999999979, -0.9999999999999979, -0.8999999999999979, -0.7999999999999979, -0.699999999999998, -0.599999999999998, -0.499999999999998, -0.399999999999998, -0.29999999999999805, -0.19999999999999804, -0.09999999999999803, 1.970645868709653e-15, 0.10000000000000198, 0.20000000000000198, 0.300000000000002, 0.400000000000002, 0.500000000000002, 0.600000000000002, 0.700000000000002, 0.8000000000000019, 0.9000000000000019, 1.000000000000002, 1.100000000000002, 1.2000000000000022, 1.3000000000000023, 1.4000000000000024, 1.5000000000000024, 1.6000000000000025, 1.7000000000000026, 1.8000000000000027, 1.9000000000000028, 2.0000000000000027, 2.1000000000000028, 2.200000000000003, 2.300000000000003, 2.400000000000003, 2.500000000000003, 2.600000000000003, 2.7000000000000033, 2.8000000000000034, 2.9000000000000035, 3.0000000000000036, 3.1000000000000036, 3.2000000000000037, 3.300000000000004, 3.400000000000004]
aVal_list = [0.0007982065, 0.0007944998, 0.0008052713, 0.000801827, 0.0008029099, 0.000804094, 0.0008052809, 0.0007996966, 0.0008078785, 0.0008065318, 0.0008011294, 0.0007986922, 0.0007976418, 0.0007983074, 0.0007979283, 0.0007963077, 0.0007972988, 0.000807215, 0.0007931232, 0.0007916194, 0.0007913882, 0.0007875065, 0.0007866217, 0.0007829634, 0.000777659, 0.0007744584, 0.0007677755, 0.0007602712, 0.0007497389, 0.0007384339, 0.0007220712, 0.0007071155, 0.0006884291, 0.000673364, 0.0006627413, 0.0006624921, 0.0006629852, 0.0006719725, 0.0006877714, 0.0007058415, 0.0007227586, 0.0007392224, 0.0007490116, 0.0007596588, 0.0007670092, 0.0007735765, 0.0007778823, 0.0007824456, 0.0007865771, 0.0007885762, 0.0007906911, 0.0007926944, 0.0007929006, 0.0007945779, 0.0007991202, 0.000799492, 0.0007993782, 0.0007960336, 0.000798921, 0.0008021397, 0.0007988505, 0.0007975588, 0.0008022248, 0.0008029265, 0.0008018495, 0.0008027861, 0.0008021296, 0.0008012615, 0.000799832, 0.000800957]
bVal_list = [0.2899151, 0.288454, 0.2888715, 0.2891491, 0.2893396, 0.2890938, 0.2888781, 0.2895317, 0.2888798, 0.2889646, 0.2896689, 0.2895167, 0.2899643, 0.2894856, 0.2897084, 0.28986, 0.2895189, 0.2889335, 0.2899653, 0.2897053, 0.2902421, 0.2898562, 0.2901402, 0.2900849, 0.2898644, 0.2901378, 0.289862, 0.2897793, 0.2897594, 0.2900132, 0.2899364, 0.2903609, 0.2899842, 0.2899753, 0.2899414, 0.2893751, 0.2892896, 0.2899761, 0.2898412, 0.2899612, 0.2898656, 0.2902333, 0.2902308, 0.2898667, 0.289821, 0.2900159, 0.2898803, 0.2901536, 0.2902014, 0.2902257, 0.2897442, 0.2901668, 0.2897422, 0.2898371, 0.28947, 0.2896285, 0.289579, 0.2899698, 0.2896247, 0.28942, 0.2898113, 0.289883, 0.2896092, 0.2894202, 0.2893302, 0.2897005, 0.2894169, 0.2890747, 0.289435, 0.2892867]
amplitude_list = [0.2899161988258446, 0.28845509415840137, 0.2888726224032257, 0.2891502117539393, 0.2893407140249493, 0.28909491826319056, 0.2888792224043431, 0.28953280439277007, 0.28888092965045437, 0.28896572555703626, 0.28967000782878016, 0.2895178016774104, 0.2899653970854645, 0.28948670073436, 0.2897094988434655, 0.28986109381211045, 0.2895199978284514, 0.28893462758607913, 0.28996638468708813, 0.2897063815475325, 0.2902431789167372, 0.2898572697810554, 0.2901412663337274, 0.2900859566399169, 0.28986544316437635, 0.2901388336204813, 0.2898630168255661, 0.2897802973302146, 0.28976036995555166, 0.29001414010159005, 0.2899372991385859, 0.29036176101742517, 0.2899850171720355, 0.2899760818225643, 0.2899421574383255, 0.2893758583499884, 0.2892903597037679, 0.2899768785925022, 0.28984201601379095, 0.28996205910026074, 0.28986650107136197, 0.29023424139588816, 0.29023176650225063, 0.2898676954239337, 0.289822014940399, 0.2900169317012566, 0.28988134370628726, 0.2901546549929485, 0.290202465987962, 0.2902267713235862, 0.2897452788675868, 0.29016788276212063, 0.2897432849130442, 0.28983818915120413, 0.28947110303637225, 0.28962960345881095, 0.2895801033332688, 0.2899708926453349, 0.2896258018976456, 0.2894211115798195, 0.2898124009938349, 0.28988409716477975, 0.2896103110893494, 0.2894213137607602, 0.2893313111204189, 0.28970161229405056, 0.28941801156373315, 0.28907581047206526, 0.2894361051358801, 0.2892878088150378]
distance_list = [0.0, 0.0014611047018009591, 0.0010436239128148578, 0.00076600855610119199, 0.0005755192194632318, 0.00082132110203999968, 0.0010370241304498492, 0.00038340289565676639, 0.0010353451779884426, 0.00095053645938492234, 0.00024621734980378069, 0.00039840029606472746, 4.9203240605600937e-05, 0.00042950001185190388, 0.00020670018721627152, 5.5132707546765765e-05, 0.00039620103977558723, 0.0009816413362691049, 5.045671351653836e-05, 0.00020990338226527591, 0.00032707107670184503, 5.986401256177874e-05, 0.00022539790946469562, 0.00017048282053511794, 5.4705481957897567e-05, 0.00022396263584272032, 6.1201762727858532e-05, 0.00014099903186220872, 0.00016306930505080973, 0.0001148754704485205, 7.9058673819449376e-05, 0.00045501121995066961, 0.00012971463892239038, 0.00013859902527164919, 0.00013799460283301602, 0.00055679295825948063, 0.00063994925578024649, 0.00014019993850214081, 0.00013288010126427549, 0.00010323034062231608, 9.0236553648773848e-05, 0.00032362071017294215, 0.00031950998135587069, 6.1874753941251265e-05, 9.9136681038288461e-05, 0.00010376548992802193, 4.0300286669453174e-05, 0.0002390201999179661, 0.00028653609361539392, 0.00031074926014085116, 0.00017106516663877269, 0.00025176034883678716, 0.00017298139372430102, 7.8084356550815287e-05, 0.00044510093781935427, 0.00028660288294124492, 0.00033610204236346724, 5.4743141071846046e-05, 0.00029040087897634138, 0.00049511562292277832, 0.00010380199774569539, 3.210653384108405e-05, 0.00030592639104018421, 0.00049492250746956861, 0.00058491134494810342, 0.00021464885915406152, 0.00049821544608092414, 0.00084040555270948713, 0.00048010275176282212, 0.00062840601942551174]

xList2 = [-4, -3.95, -3.9000000000000004, -3.8500000000000005, -3.8000000000000007, -3.750000000000001, -3.700000000000001, -3.6500000000000012, -3.6000000000000014, -3.5500000000000016, -3.5000000000000018, -3.450000000000002, -3.400000000000002, -3.3500000000000023, -3.3000000000000025, -3.2500000000000027, -3.200000000000003, -3.150000000000003, -3.100000000000003, -3.0500000000000034, -3.0000000000000036, -2.9500000000000037, -2.900000000000004, -2.850000000000004, -2.8000000000000043, -2.7500000000000044, -2.7000000000000046, -2.650000000000005, -2.600000000000005, -2.550000000000005, -2.5000000000000053, -2.4500000000000055, -2.4000000000000057, -2.350000000000006, -2.300000000000006, -2.250000000000006, -2.2000000000000064, -2.1500000000000066, -2.1000000000000068, -2.050000000000007, -2.000000000000007, -1.950000000000007, -1.900000000000007, -1.850000000000007, -1.800000000000007, -1.7500000000000069, -1.7000000000000068, -1.6500000000000068, -1.6000000000000068, -1.5500000000000067, -1.5000000000000067, -1.4500000000000066, -1.4000000000000066, -1.3500000000000065, -1.3000000000000065, -1.2500000000000064, -1.2000000000000064, -1.1500000000000064, -1.1000000000000063, -1.0500000000000063, -1.0000000000000062, -0.9500000000000062, -0.9000000000000061, -0.8500000000000061, -0.800000000000006, -0.750000000000006, -0.700000000000006, -0.6500000000000059, -0.6000000000000059, -0.5500000000000058, -0.5000000000000058, -0.4500000000000058, -0.4000000000000058, -0.3500000000000058, -0.3000000000000058, -0.25000000000000583, -0.20000000000000584, -0.15000000000000585, -0.10000000000000585, -0.050000000000005845, -5.842548667089886e-15, 0.04999999999999416, 0.09999999999999416, 0.14999999999999417, 0.19999999999999418, 0.24999999999999417, 0.29999999999999416, 0.34999999999999415, 0.39999999999999414, 0.4499999999999941, 0.4999999999999941, 0.5499999999999942, 0.5999999999999942, 0.6499999999999942, 0.6999999999999943, 0.7499999999999943, 0.7999999999999944, 0.8499999999999944, 0.8999999999999945, 0.9499999999999945, 0.9999999999999946, 1.0499999999999945, 1.0999999999999945, 1.1499999999999946, 1.1999999999999946, 1.2499999999999947, 1.2999999999999947, 1.3499999999999948, 1.3999999999999948, 1.4499999999999948, 1.499999999999995, 1.549999999999995, 1.599999999999995, 1.649999999999995, 1.699999999999995, 1.7499999999999951, 1.7999999999999952, 1.8499999999999952, 1.8999999999999952, 1.9499999999999953, 1.9999999999999953, 2.0499999999999954, 2.099999999999995, 2.149999999999995, 2.199999999999995, 2.2499999999999947, 2.2999999999999945, 2.3499999999999943, 2.399999999999994, 2.449999999999994, 2.499999999999994, 2.5499999999999936, 2.5999999999999934, 2.6499999999999932, 2.699999999999993, 2.749999999999993, 2.7999999999999927, 2.8499999999999925, 2.8999999999999924, 2.949999999999992, 2.999999999999992, 3.049999999999992, 3.0999999999999917, 3.1499999999999915, 3.1999999999999913, 3.249999999999991, 3.299999999999991, 3.3499999999999908, 3.3999999999999906, 3.4499999999999904, 3.4999999999999902, 3.54999999999999, 3.59999999999999, 3.6499999999999897, 3.6999999999999895, 3.7499999999999893, 3.799999999999989, 3.849999999999989, 3.899999999999989, 3.9499999999999886, 3.9999999999999885]
aVal_list2 = [0.0008071834, 0.0008003846, 0.0008000624, 0.0007970453, 0.0007959169, 0.0007843704, 0.0007954881, 0.0007987378, 0.0007954037, 0.0007943824, 0.0007997179, 0.0007946824, 0.0007941328, 0.0007948923, 0.0007934272, 0.0007932189, 0.0007928769, 0.0007897743, 0.0007894842, 0.0007899327, 0.0007878028, 0.0007861465, 0.0007874526, 0.0007867273, 0.0007846172, 0.000784502, 0.0007819607, 0.0007801832, 0.000778071, 0.0007761683, 0.0007744037, 0.0007730592, 0.0007717388, 0.0007666927, 0.0007652647, 0.000761772, 0.0007578609, 0.0007546563, 0.0007508529, 0.0007462709, 0.0007419509, 0.0007359335, 0.0007315543, 0.0007255853, 0.0007202632, 0.0007152666, 0.0007101384, 0.0007065908, 0.0007020375, 0.0007004049, 0.0006991267, 0.0006967161, 0.000698322, 0.0006986382, 0.0006987716, 0.0006997838, 0.000698103, 0.0006978624, 0.0006964165, 0.0006940494, 0.0006921571, 0.0006912509, 0.000686876, 0.0006849068, 0.0006822593, 0.0006798668, 0.000676932, 0.0006719344, 0.0006738139, 0.000670919, 0.0006685395, 0.0006651158, 0.0006659059, 0.0006636125, 0.0006624281, 0.0006612371, 0.0006606856, 0.0006580983, 0.0006601611, 0.0006599134, 0.0006624921, 0.0006603939, 0.0006612081, 0.0006602106, 0.0006610259, 0.0006617317, 0.0006634005, 0.0006638011, 0.0006656506, 0.0006666037, 0.0006683256, 0.0006695068, 0.0006725027, 0.0006744867, 0.0006764842, 0.0006804577, 0.0006808829, 0.0006850681, 0.0006870403, 0.0006898436, 0.0006920269, 0.0006939597, 0.0006962252, 0.0006979767, 0.0006986046, 0.0006984313, 0.0006973336, 0.0006997939, 0.0006995506, 0.0006985954, 0.0006989601, 0.0006994958, 0.0007025983, 0.0007055314, 0.0007096583, 0.000714459, 0.0007196498, 0.0007264283, 0.0007320516, 0.0007362178, 0.0007423356, 0.0007469206, 0.0007512762, 0.000755774, 0.0007584923, 0.0007616037, 0.0007655211, 0.0007675098, 0.0007695151, 0.0007724246, 0.000776083, 0.0007773648, 0.0007795733, 0.0007808548, 0.0007833698, 0.0007846329, 0.0007848329, 0.000785586, 0.0007882664, 0.0007896666, 0.0007906092, 0.0007898806, 0.0007908199, 0.0007909834, 0.0007931856, 0.0007930052, 0.0007922448, 0.0007937328, 0.0007961644, 0.0007976952, 0.0007936356, 0.0007957114, 0.0007970071, 0.0007956622, 0.000796764, 0.0007903868, 0.000797495, 0.00079884, 0.0007990821, 0.0007975733, 0.0007959758]
bVal_list2 = [0.2882823, 0.2897745, 0.2896029, 0.2898147, 0.289938, 0.288234, 0.289699, 0.2893724, 0.2897202, 0.2897409, 0.2894167, 0.2897943, 0.2898814, 0.290026, 0.2899525, 0.2898401, 0.2897735, 0.2897408, 0.2897368, 0.2899525, 0.289705, 0.2897134, 0.2900662, 0.2899725, 0.2898837, 0.2902293, 0.2898017, 0.2898435, 0.2899703, 0.2899173, 0.2897791, 0.2898243, 0.2902714, 0.2898611, 0.2902705, 0.2902018, 0.2899039, 0.2900152, 0.2901607, 0.2900441, 0.2899984, 0.2899945, 0.2902637, 0.290227, 0.2900946, 0.2901442, 0.2903463, 0.290154, 0.290125, 0.2902711, 0.2903943, 0.2899324, 0.2903202, 0.2901826, 0.2899244, 0.2903032, 0.2899668, 0.2903003, 0.2899489, 0.2898191, 0.290171, 0.2901987, 0.2899958, 0.2899447, 0.2903506, 0.2901494, 0.28996, 0.2888153, 0.2898407, 0.2900406, 0.2898872, 0.2898051, 0.2899882, 0.2899931, 0.2903134, 0.2901392, 0.2899447, 0.2889927, 0.2899017, 0.289983, 0.2893751, 0.2903337, 0.2902791, 0.2901505, 0.2900713, 0.2898753, 0.2899546, 0.2903742, 0.2900266, 0.2902721, 0.2902402, 0.289878, 0.2899699, 0.2901981, 0.2899113, 0.2900586, 0.2892877, 0.2904907, 0.2900385, 0.2903508, 0.290008, 0.2899025, 0.2900137, 0.2902257, 0.2902875, 0.2903241, 0.29006, 0.2901722, 0.2902662, 0.2899819, 0.2901268, 0.2901237, 0.2903366, 0.2902344, 0.2901003, 0.2900676, 0.2898314, 0.2900157, 0.2902297, 0.2900325, 0.2903235, 0.2899959, 0.2903347, 0.2902633, 0.290338, 0.2903736, 0.2903601, 0.2899985, 0.2897007, 0.2899087, 0.2902656, 0.2900246, 0.2898776, 0.2901661, 0.2902758, 0.2903373, 0.2901638, 0.2897145, 0.2898138, 0.2902831, 0.2896527, 0.2897637, 0.2896081, 0.2894636, 0.2896432, 0.289866, 0.2896782, 0.2899558, 0.2898014, 0.2895873, 0.2896742, 0.2898577, 0.2901782, 0.2903245, 0.290337, 0.2889572, 0.2902358, 0.2897488, 0.2898909, 0.289843, 0.2898365]
amplitude_list2 = [0.28828343004468926, 0.2897756053669079, 0.2896040051315829, 0.28981579601067337, 0.28993909244479554, 0.2882350672505419, 0.2897000921682926, 0.2893735023526396, 0.28972129185664963, 0.28974198897675746, 0.2894178048904552, 0.28979538959860435, 0.2898824877650667, 0.2900270893033418, 0.289953585566676, 0.2898411854175202, 0.2897745847310087, 0.2897418763797959, 0.2897378756040398, 0.28995357602540534, 0.28970607114496527, 0.2897144666147679, 0.29006726886023737, 0.2899735672369028, 0.28988476184484163, 0.2902303602690077, 0.28980275496521135, 0.28984455002306936, 0.28997134388861784, 0.28991833897930624, 0.2897801347537484, 0.2898253310030314, 0.290272425901489, 0.2898621139626671, 0.29027150876431373, 0.29020279981388875, 0.2899048905906103, 0.2900161818539978, 0.290161671494647, 0.29004506005975383, 0.2899993491263351, 0.2899954338060626, 0.2902646218700857, 0.2902279070024583, 0.2900954941536274, 0.29014508164011515, 0.2903471684384698, 0.29015486035315463, 0.29012584938548897, 0.29027194501404013, 0.2903951415754621, 0.2899332371134499, 0.29032103985356567, 0.29018344101291255, 0.28992524208338427, 0.29030404342276517, 0.2899676403498132, 0.29030113880592917, 0.2899497363460631, 0.2898199310423278, 0.290171825514558, 0.2901995232757916, 0.2899966134565702, 0.2899455089416194, 0.2903514015776615, 0.29015019651764107, 0.2899607901715896, 0.28881608163315264, 0.28984148323119974, 0.2900413759805048, 0.2898879708937628, 0.2898058632344028, 0.2899889645657359, 0.2899938592956067, 0.2903141557529492, 0.2901399534899363, 0.2899454527381867, 0.28899344931444804, 0.2899024516549799, 0.2899837508804511, 0.2893758583499884, 0.29033445106599587, 0.29027985306073434, 0.29015125112307605, 0.29007205318494655, 0.2898760553045608, 0.28995535891130453, 0.29037495873015695, 0.29002736387844735, 0.2902728654195959, 0.29024096946356076, 0.28987877315070043, 0.2899706798383097, 0.29019888382955317, 0.28991208925907663, 0.29005939815258786, 0.28928850127997396, 0.2904915078015046, 0.2900393137259565, 0.2903516194975197, 0.290008825667824, 0.2899033305885174, 0.29001453569988367, 0.29022653929639813, 0.2902883406281367, 0.2903249401052049, 0.2900608382290682, 0.29017304382788983, 0.29026704296816397, 0.2899827414918738, 0.29012764194998963, 0.29012454325007425, 0.2903374501230097, 0.29023525753759893, 0.29010116800004915, 0.29006847988263507, 0.2898322934419052, 0.290016609773587, 0.29023062323199983, 0.29003343440524065, 0.29032444904691207, 0.2899968618919741, 0.2903356720074519, 0.2902642839228228, 0.290338990758336, 0.29037459878087796, 0.29036110912889923, 0.28999951564363535, 0.28970172200727273, 0.28990972901138157, 0.2902666375045243, 0.2900256417994662, 0.2898786482586982, 0.29016715066221516, 0.2902768570414864, 0.29033836022833387, 0.2901648614031701, 0.2897155650903372, 0.28981487200341766, 0.2902841740759375, 0.2896537789848376, 0.2897647765844777, 0.2896091797262722, 0.2894646807119982, 0.28964428606419296, 0.28986708473582723, 0.2896792833584465, 0.28995688639071465, 0.28980249363956795, 0.2895883986607925, 0.28967528718050073, 0.289858792183232, 0.29017929453280683, 0.2903255902923242, 0.29033809326692167, 0.28895828097345405, 0.29023689565579874, 0.28974990120237415, 0.28989200132982723, 0.289844097356094, 0.2898375929891155]
distance_list2 = [0.0, 0.0014922154883532865, 0.0013206191989521482, 0.001532433535613071, 0.0016557383319903514, 5.3416504649781312e-05, 0.0014167482733506577, 0.0010901327158467093, 0.0014379482505751265, 0.001458656171138728, 0.0011344245650065632, 0.0015120516773579665, 0.0015991532534939932, 0.0017437433185934395, 0.0016702566488532458, 0.0015578625893384319, 0.001491268626352183, 0.0014586038964581492, 0.0014546076830818382, 0.0016702890847546496, 0.0014228319990977, 0.0014312546108787433, 0.0017840091127762374, 0.0016903237831928275, 0.0016015589884180157, 0.0019471321079747221, 0.0015196093394669902, 0.001561433460253748, 0.0016882510274937898, 0.0016352941437025946, 0.0014971588922796908, 0.0015423775351792448, 0.0019894157759677198, 0.0015793191370924568, 0.0019886418524736101, 0.0019200370947588567, 0.0016223499218745174, 0.001733695909389633, 0.0018792444453104708, 0.0017628526803611174, 0.0017173393633921757, 0.001713681822349178, 0.0019828428381409601, 0.0019464111435983132, 0.0018143832040580623, 0.0018641674571031278, 0.0020662801678439065, 0.0018744011740219537, 0.0018456974156905899, 0.0019916644014648403, 0.0021147624572076412, 0.0016537935283369716, 0.0020408055307671734, 0.0019033975282223945, 0.0016456747942346797, 0.0020237518336199546, 0.0016880280754964568, 0.0020209589508550342, 0.0016702768830752794, 0.0015409586438175473, 0.0018921994450088418, 0.0019199034623012146, 0.0017177182890377798, 0.0016668909163192376, 0.0020720692364785747, 0.0018714357928167342, 0.0016827485603030459, 0.00054989207304798093, 0.0015640965390698548, 0.0017635721920883551, 0.0016108774444405368, 0.0015294126464004841, 0.0017117400918381827, 0.001716813689171557, 0.002036251778852046, 0.0018626266218659255, 0.0016688425226500155, 0.00072587500786430845, 0.0016260602438708312, 0.0017070644225980454, 0.0011023372497995796, 0.0020566451121450616, 0.0020021286242921988, 0.0018739723167485131, 0.0017949604493710152, 0.001599626580497125, 0.0016784697829667539, 0.0020968080727509228, 0.0017500325778327533, 0.0019947598081102485, 0.0019628178465208859, 0.0016016283389687089, 0.0016929656378534468, 0.0019203900786535476, 0.0016342347692056404, 0.0017808147273202003, 0.0010133020163308811, 0.002211773656252847, 0.0017603047476154687, 0.0020718254942596295, 0.0017295379468205484, 0.0016241513618630939, 0.0017349517809285707, 0.0019464659419894373, 0.002008137544046567, 0.002044694172548633, 0.001781090752477261, 0.0018929486297071692, 0.0019868175632492711, 0.0017030653286776991, 0.0018476721929668661, 0.0018445461716080013, 0.002056960508406043, 0.0019547448782652041, 0.0018206139473073253, 0.001787706324974917, 0.0015515711202291175, 0.0017352800771564217, 0.0019488487748851098, 0.0017516381351133808, 0.0020422298296628922, 0.001714659314576449, 0.0020531613124671623, 0.0019816669564809326, 0.0020562765653528185, 0.0020917966438093751, 0.0020782176467447695, 0.0017166585084218012, 0.0014189000883870757, 0.0016267713835009302, 0.0019835438298359438, 0.0017425551465896465, 0.0015955389082131714, 0.0018839839795438617, 0.0019936422290734329, 0.0020551237249981738, 0.0018816327470711136, 0.0014323628338122798, 0.0015316168263926385, 0.0020008766774297559, 0.0013705002240443536, 0.0014815010451862342, 0.0013259009782529835, 0.0011814110757902988, 0.0013609719866348592, 0.0015837634644590419, 0.0013959799324381333, 0.0016735540530978799, 0.0015191399633875037, 0.0013050344922411979, 0.0013919659309353963, 0.0015754417687696407, 0.0018959273106007289, 0.002042232498529346, 0.0020547264182602131, 0.00067510898066283024, 0.0019535240247037016, 0.001466523733978931, 0.0016086203999271364, 0.0015607295870912717, 0.0015542404094276334]

plt.figure(1)
plt.title('Impdance change for Perpendicular to hole')
plt.plot(xList,aVal_list,'r-')
#plt.plot(aVal_list,bVal_list,'ro')
plt.xlabel("x_var")
plt.ylabel("real")

plt.figure(2)
plt.title('Impdance change for Parallel to hole')
plt.plot(xList2,aVal_list2,'b-')
#plt.plot(aVal_list2,bVal_list2,'bo')
plt.xlabel("x_var")
plt.ylabel("real")

plt.show()