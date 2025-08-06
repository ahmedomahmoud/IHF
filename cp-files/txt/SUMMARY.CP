[Database]
databasename=teamsports

[Version]
def=301

[Print]
FormatFile=C76.FMT

[Definition]
competition=CompName;FirstDay;LastDay;Status;Round;UpdDate;UpdTime;LastGame;Gender;Event_ID;ListTyp;GMN
CrossHead=Round;Group;Mem;Team1;Nat1;Name1;Short1;Team2;Nat2;Name2;Short2;Team3;Nat3;Name3;Short3;Team4;Nat4;Name4;Short4;Team5;Nat5;Name5;Short5;Team6;Nat6;Name6;Short6;Team7;Nat7;Name7;Short7;Team8;Nat8;Name8;Short8;Status;SchState
CrossResult=Round;Group;Team;Nat;ID;TeamName;Name1;RA1;RB1;Result1;IA1;IB1;Game1;Date1;Time1;RA2;RB2;Result2;IA2;IB2;Game2;Date2;Time2;RA3;RB3;Result3;IA3;IB3;Game3;Date3;Time3;RA4;RB4;Result4;IA4;IB4;Game4;Date4;Time4;RA5;RB5;Result5;IA5;IB5;Game5;Date5;Time5;RA6;RB6;Result6;IA6;IB6;Game6;Date6;Time6;RA7;RB7;Result7;IA7;IB7;Game7;Date7;Time7;RA8;RB8;Result8;IA8;IB8;Game8;Date8;Time8
GroupRanking=Round;Gender;Group;Group2;Rnk;ERnk;DBS;Team;Nat;ID;Name;Games;Won;Tied;Lost;GFor;GA;GDiff;SFor;SA;SDiff;Points;NegPts;LastRnk
Games=Gender;Game;Group;Group2;TeamA;TeamNameA;NatA;TIDA;TeamB;TeamNameB;NatB;TIDB;STATUS;PLACE;RA;RB;RInfoA;RInfoB;RA1;RB1;RA2;RB2;RA3;RB3;RA4;RB4;RA5;RB5;nNormal;nExtra;LastPer;Min;Round;Date;Session;SiteCode;Site;Venue;StartTime;TimeType;EstTime;Spect;Capacity;PSpect;Win;SchState;StateTxt;GrpState;Comp_A;Comp_B;Apx;FedCode;Ref1Name;Ref1Nat;Ref1ID;Ref1Info;Ref2Name;Ref2Nat;Ref2ID;Ref2Info;Ref3Name;Ref3Nat;Ref3ID;Ref3Info;RSC;Medal;MedalCount;Result;AwayResult;ShortResult;ShortAwayResult
Teams=TC;Group;Team;Nat;ID;TeamName;Active;avgheight;avgheightft;avgweight;avgweightlbs;avgage;avgage_m;avgIntga;Shirt1;Short1;Socks1;GK_Shirt1;GK_Short1;Shirt2;Short2;Socks2;GK_Shirt2;GK_Short2;Shirt3;Short3;Socks3;GK_Shirt3;GK_Short3;DBS;Reason;Seed;FedCode
Overall=TC;Rnk;ERnk;DBS;Team;Nat;ID;Phase;Group;TeamName;Games;Won;Tied;Lost;GFor;GA;GDiff;SFor;SA;SDiff;CurRun_W;CurRun_L;Last2_W;Last2_L;M5_W;M5_L;M15_W;M15_L;GamesT;WonT;TiedT;LostT;PoolRank;Points;QRank
Finalranking=Gender;TC;Rnk;ERnk;Team;Nat;ID;TeamName;Games;Won;Tied;Lost;DBS;Reason;RnkPos
DsqNote=FinalStandings
Reportcode=RSC;Gender;Code;SubType;Version;Correction;Type;Note;GenDay;GenDate;GenTime;GenTimeMs;CPFile
Message=Text
config=Sport;SubSport;Event_Type
LegendHead=L_Titel;L_Columns
Legend=L_Txt1;L_Txt1Titel;L_Txt2;L_Txt2Titel;L_Txt3;L_Txt3Titel;L_Txt4;L_Txt4Titel;L_Txt5;L_Txt5Titel;L_Txt6;L_Txt6Titel
ReportProp=NoLegend;NoNote

[competition]
Handball;18/06/2025;29/06/2025;;;18/06/2025;22:56;116;M

[CrossHead]
V:A;4;POL;POL;Poland;Poland;SLO;SLO;Slovenia;Slovenia;NOR;NOR;Norway;Norway;URU;URU;Uruguay;Uruguay;;
V:B;4;AUT;AUT;Austria;Austria;HUN;HUN;Hungary;Hungary;BRA;BRA;Brazil;Brazil;ARG;ARG;Argentina;Argentina;;
V:C;4;SWE;SWE;Sweden;Sweden;JPN;JPN;Japan;Japan;USA;USA;USA;USA;KOR;KOR;Korea;Korea;;
V:D;4;CRO;CRO;Croatia;Croatia;POR;POR;Portugal;Portugal;ALG;ALG;Algeria;Algeria;CAN;CAN;Canada;Canada;;
V:E;4;FRA;FRA;France;France;DEN;DEN;Denmark;Denmark;MAR;MAR;Morocco;Morocco;MEX;MEX;Mexico;Mexico;;
V:F;4;FAR;FAR;Faroe Islands;Faroe Islands;ROU;ROU;Romania;Romania;ISL;ISL;Iceland;Iceland;MKD;MKD;North Macedonia;North Macedonia;;
V:G;4;SUI;SUI;Switzerland;Switzerland;GER;GER;Germany;Germany;SRB;SRB;Serbia;Serbia;TUN;TUN;Tunisia;Tunisia;;
V:H;4;ESP;ESP;Spain;Spain;EGY;EGY;Egypt;Egypt;KSA;KSA;Saudi Arabia;Saudi Arabia;BRN;BRN;Bahrain;Bahrain;;
V:MRI;0;;
V:MRII;0;;
V:MRIII;0;;
V:MRIV;0;;
V:PCI;0;;
V:PCII;0;;
V:PCIII;0;;
V:PCIV;0;;

[CrossResult]
V;A;POL;POL;POL;Poland;Poland;;;;;;;;;;;;;;28;20/06/2025;18:30;;;;;;36;21/06/2025;18:30;39;16;39 -  16;;;4;18/06/2025;18:30
V;A;SLO;SLO;SLO;Slovenia;Slovenia;;;;;;28;20/06/2025;18:30;;;;;;;;;33;33;33 -  33;;;3;18/06/2025;16:15;;;;;;35;21/06/2025;16:15
V;A;NOR;NOR;NOR;Norway;Norway;;;;;;36;21/06/2025;18:30;33;33;33 -  33;;;3;18/06/2025;16:15;;;;;;;;;;;;;;27;20/06/2025;16:15
V;A;URU;URU;URU;Uruguay;Uruguay;16;39;16 -  39;;;4;18/06/2025;18:30;;;;;;35;21/06/2025;16:15;;;;;;27;20/06/2025;16:15;;;;;;;;
V;B;AUT;AUT;AUT;Austria;Austria;;;;;;;;;;;;;;34;21/06/2025;14:00;;;;;;25;20/06/2025;11:45;29;23;29 -  23;;;1;18/06/2025;11:45
V;B;HUN;HUN;HUN;Hungary;Hungary;;;;;;34;21/06/2025;14:00;;;;;;;;;29;24;29 -  24;;;2;18/06/2025;14:00;;;;;;26;20/06/2025;14:00
V;B;BRA;BRA;BRA;Brazil;Brazil;;;;;;25;20/06/2025;11:45;24;29;24 -  29;;;2;18/06/2025;14:00;;;;;;;;;;;;;;33;21/06/2025;11:45
V;B;ARG;ARG;ARG;Argentina;Argentina;23;29;23 -  29;;;1;18/06/2025;11:45;;;;;;26;20/06/2025;14:00;;;;;;33;21/06/2025;11:45;;;;;;;;
V;C;SWE;SWE;SWE;Sweden;Sweden;;;;;;;;;;;;;;40;21/06/2025;18:30;;;;;;31;20/06/2025;16:15;42;31;42 -  31;;;7;18/06/2025;16:15
V;C;JPN;JPN;JPN;Japan;Japan;;;;;;40;21/06/2025;18:30;;;;;;;;;41;33;41 -  33;;;8;18/06/2025;18:30;;;;;;32;20/06/2025;18:30
V;C;USA;USA;USA;USA;USA;;;;;;31;20/06/2025;16:15;33;41;33 -  41;;;8;18/06/2025;18:30;;;;;;;;;;;;;;39;21/06/2025;16:15
V;C;KOR;KOR;KOR;Korea;Korea;31;42;31 -  42;;;7;18/06/2025;16:15;;;;;;32;20/06/2025;18:30;;;;;;39;21/06/2025;16:15;;;;;;;;
V;D;CRO;CRO;CRO;Croatia;Croatia;;;;;;;;;;;;;;38;21/06/2025;14:00;;;;;;30;20/06/2025;14:00;44;20;44 -  20;;;6;18/06/2025;14:00
V;D;POR;POR;POR;Portugal;Portugal;;;;;;38;21/06/2025;14:00;;;;;;;;;33;21;33 -  21;;;5;18/06/2025;11:45;;;;;;29;20/06/2025;11:45
V;D;ALG;ALG;ALG;Algeria;Algeria;;;;;;30;20/06/2025;14:00;21;33;21 -  33;;;5;18/06/2025;11:45;;;;;;;;;;;;;;37;21/06/2025;11:45
V;D;CAN;CAN;CAN;Canada;Canada;20;44;20 -  44;;;6;18/06/2025;14:00;;;;;;29;20/06/2025;11:45;;;;;;37;21/06/2025;11:45;;;;;;;;
V;E;FRA;FRA;FRA;France;France;;;;;;;;;;;;;;44;21/06/2025;18:30;;;;;;20;19/06/2025;18:30;46;17;46 -  17;;;12;18/06/2025;18:30
V;E;DEN;DEN;DEN;Denmark;Denmark;;;;;;44;21/06/2025;18:30;;;;;;;;;43;31;43 -  31;;;11;18/06/2025;16:15;;;;;;19;19/06/2025;16:15
V;E;MAR;MAR;MAR;Morocco;Morocco;;;;;;20;19/06/2025;18:30;31;43;31 -  43;;;11;18/06/2025;16:15;;;;;;;;;;;;;;43;21/06/2025;16:15
V;E;MEX;MEX;MEX;Mexico;Mexico;17;46;17 -  46;;;12;18/06/2025;18:30;;;;;;19;19/06/2025;16:15;;;;;;43;21/06/2025;16:15;;;;;;;;
V;F;FAR;FAR;FAR;Faroe Islands;Faroe Islands;;;;;;;;;;;;;;41;21/06/2025;11:45;;;;;;17;19/06/2025;11:45;33;28;33 -  28;;;10;18/06/2025;14:00
V;F;ROU;ROU;ROU;Romania;Romania;;;;;;41;21/06/2025;11:45;;;;;;;;;29;25;29 -  25;;;9;18/06/2025;11:45;;;;;;18;19/06/2025;14:00
V;F;ISL;ISL;ISL;Iceland;Iceland;;;;;;17;19/06/2025;11:45;25;29;25 -  29;;;9;18/06/2025;11:45;;;;;;;;;;;;;;42;21/06/2025;14:00
V;F;MKD;MKD;MKD;North Macedonia;North Macedonia;28;33;28 -  33;;;10;18/06/2025;14:00;;;;;;18;19/06/2025;14:00;;;;;;42;21/06/2025;14:00;;;;;;;;
V;G;SUI;SUI;SUI;Switzerland;Switzerland;;;;;;;;;;;;;;24;19/06/2025;21:00;;;;;;47;21/06/2025;18:45;41;31;41 -  31;;;15;18/06/2025;18:45
V;G;GER;GER;GER;Germany;Germany;;;;;;24;19/06/2025;21:00;;;;;;;;;30;29;30 -  29;;;16;18/06/2025;21:00;;;;;;48;21/06/2025;21:00
V;G;SRB;SRB;SRB;Serbia;Serbia;;;;;;47;21/06/2025;18:45;29;30;29 -  30;;;16;18/06/2025;21:00;;;;;;;;;;;;;;23;19/06/2025;18:45
V;G;TUN;TUN;TUN;Tunisia;Tunisia;31;41;31 -  41;;;15;18/06/2025;18:45;;;;;;48;21/06/2025;21:00;;;;;;23;19/06/2025;18:45;;;;;;;;
V;H;ESP;ESP;ESP;Spain;Spain;;;;;;;;;;;;;;46;21/06/2025;14:00;;;;;;21;19/06/2025;11:45;40;19;40 -  19;;;13;18/06/2025;11:45
V;H;EGY;EGY;EGY;Egypt;Egypt;;;;;;46;21/06/2025;14:00;;;;;;;;;35;30;35 -  30;;;14;18/06/2025;14:00;;;;;;22;19/06/2025;14:00
V;H;KSA;KSA;KSA;Saudi Arabia;Saudi Arabia;;;;;;21;19/06/2025;11:45;30;35;30 -  35;;;14;18/06/2025;14:00;;;;;;;;;;;;;;45;21/06/2025;11:45
V;H;BRN;BRN;BRN;Bahrain;Bahrain;19;40;19 -  40;;;13;18/06/2025;11:45;;;;;;22;19/06/2025;14:00;;;;;;45;21/06/2025;11:45;;;;;;;;

[GroupRanking]
V;M;A;;1;;;POL;POL;Poland;Poland;1;1;0;0;39;16;23;;;;2;;
V;M;A;;2;;;SLO;SLO;Slovenia;Slovenia;1;0;1;0;33;33;0;;;;1;;
V;M;A;;3;;;NOR;NOR;Norway;Norway;1;0;1;0;33;33;0;;;;1;;
V;M;A;;4;;;URU;URU;Uruguay;Uruguay;1;0;0;1;16;39;-23;;;;0;;
V;M;B;;1;;;AUT;AUT;Austria;Austria;1;1;0;0;29;23;6;;;;2;;
V;M;B;;2;;;HUN;HUN;Hungary;Hungary;1;1;0;0;29;24;5;;;;2;;
V;M;B;;3;;;BRA;BRA;Brazil;Brazil;1;0;0;1;24;29;-5;;;;0;;
V;M;B;;4;;;ARG;ARG;Argentina;Argentina;1;0;0;1;23;29;-6;;;;0;;
V;M;C;;1;;;SWE;SWE;Sweden;Sweden;1;1;0;0;42;31;11;;;;2;;
V;M;C;;2;;;JPN;JPN;Japan;Japan;1;1;0;0;41;33;8;;;;2;;
V;M;C;;3;;;USA;USA;USA;USA;1;0;0;1;33;41;-8;;;;0;;
V;M;C;;4;;;KOR;KOR;Korea;Korea;1;0;0;1;31;42;-11;;;;0;;
V;M;D;;1;;;CRO;CRO;Croatia;Croatia;1;1;0;0;44;20;24;;;;2;;
V;M;D;;2;;;POR;POR;Portugal;Portugal;1;1;0;0;33;21;12;;;;2;;
V;M;D;;3;;;ALG;ALG;Algeria;Algeria;1;0;0;1;21;33;-12;;;;0;;
V;M;D;;4;;;CAN;CAN;Canada;Canada;1;0;0;1;20;44;-24;;;;0;;
V;M;E;;1;;;FRA;FRA;France;France;1;1;0;0;46;17;29;;;;2;;
V;M;E;;2;;;DEN;DEN;Denmark;Denmark;1;1;0;0;43;31;12;;;;2;;
V;M;E;;3;;;MAR;MAR;Morocco;Morocco;1;0;0;1;31;43;-12;;;;0;;
V;M;E;;4;;;MEX;MEX;Mexico;Mexico;1;0;0;1;17;46;-29;;;;0;;
V;M;F;;1;;;FAR;FAR;Faroe Islands;Faroe Islands;1;1;0;0;33;28;5;;;;2;;
V;M;F;;2;;;ROU;ROU;Romania;Romania;1;1;0;0;29;25;4;;;;2;;
V;M;F;;3;;;ISL;ISL;Iceland;Iceland;1;0;0;1;25;29;-4;;;;0;;
V;M;F;;4;;;MKD;MKD;North Macedonia;North Macedonia;1;0;0;1;28;33;-5;;;;0;;
V;M;G;;1;;;SUI;SUI;Switzerland;Switzerland;1;1;0;0;41;31;10;;;;2;;
V;M;G;;2;;;GER;GER;Germany;Germany;1;1;0;0;30;29;1;;;;2;;
V;M;G;;3;;;SRB;SRB;Serbia;Serbia;1;0;0;1;29;30;-1;;;;0;;
V;M;G;;4;;;TUN;TUN;Tunisia;Tunisia;1;0;0;1;31;41;-10;;;;0;;
V;M;H;;1;;;ESP;ESP;Spain;Spain;1;1;0;0;40;19;21;;;;2;;
V;M;H;;2;;;EGY;EGY;Egypt;Egypt;1;1;0;0;35;30;5;;;;2;;
V;M;H;;3;;;KSA;KSA;Saudi Arabia;Saudi Arabia;1;0;0;1;30;35;-5;;;;0;;
V;M;H;;4;;;BRN;BRN;Bahrain;Bahrain;1;0;0;1;19;40;-21;;;;0;;

[Games]
M;1;inary Round - Group B;;AUT;Austria;AUT;AUT;ARG;Argentina;ARG;ARG;;;29;23;;;12;13;17;10;;;;;;;;;;;;18/06/2025;;;Plock;Orlen Arena;11:45;;;;;;1;;;;;;;;Yann Carmaux;FRA;;;Julien Mursch;FRA;;;;;;;;;;29 - 23;23 - 29;29 - 23;23 - 29
M;5;inary Round - Group D;;POR;Portugal;POR;POR;ALG;Algeria;ALG;ALG;;;33;21;;;18;11;15;10;;;;;;;;;;;;18/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;1;;;;;;;;Ioannis Fotakidis;GRE;;;Charalampos Kinatzidis;GRE;;;;;;;;;;33 - 21;21 - 33;33 - 21;21 - 33
M;9;inary Round - Group F;;ISL;Iceland;ISL;ISL;ROU;Romania;ROU;ROU;;;25;29;;;12;15;13;14;;;;;;;;;;;;18/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;2;;;;;;;;Novica Mitrovic;MNE;;;Miljan Vesovic;MNE;;;;;;;;;;25 - 29;29 - 25;25 - 29;29 - 25
M;13;inary Round - Group H;;ESP;Spain;ESP;ESP;BRN;Bahrain;BRN;BRN;;;40;19;;;21;12;19;7;;;;;;;;;;;;18/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;1;;;;;;;;Jacob Jaeger Pagh;DEN;;;Karl Johan Thygesen;DEN;;;;;;;;;;40 - 19;19 - 40;40 - 19;19 - 40
M;2;inary Round - Group B;;HUN;Hungary;HUN;HUN;BRA;Brazil;BRA;BRA;;;29;24;;;13;10;16;14;;;;;;;;;;;;18/06/2025;;;Plock;Orlen Arena;14:00;;;;;;1;;;;;;;;Vesna Balvan;BIH;;;Tatjana Prastalo;BIH;;;;;;;;;;29 - 24;24 - 29;29 - 24;24 - 29
M;6;inary Round - Group D;;CRO;Croatia;CRO;CRO;CAN;Canada;CAN;CAN;;;44;20;;;20;12;24;8;;;;;;;;;;;;18/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;1;;;;;;;;Miguel Soria Fabian;ESP;;;Jesus Alvarez Menendez;ESP;;;;;;;;;;44 - 20;20 - 44;44 - 20;20 - 44
M;10;inary Round - Group F;;MKD;North Macedonia;MKD;MKD;FAR;Faroe Islands;FAR;FAR;;;28;33;;;15;16;13;17;;;;;;;;;;;;18/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;2;;;;;;;;Kristof Altmar;HUN;;;Marton Horvath;HUN;;;;;;;;;;28 - 33;33 - 28;28 - 33;33 - 28
M;14;inary Round - Group H;;EGY;Egypt;EGY;EGY;KSA;Saudi Arabia;KSA;KSA;;;35;30;;;19;15;16;15;;;;;;;;;;;;18/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;1;;;;;;;;Danielo Bozhinovski;MKD;;;Viktor Nachevski;MKD;;;;;;;;;;35 - 30;30 - 35;35 - 30;30 - 35
M;3;inary Round - Group A;;NOR;Norway;NOR;NOR;SLO;Slovenia;SLO;SLO;;;33;33;;;17;12;16;21;;;;;;;;;;;;18/06/2025;;;Plock;Orlen Arena;16:15;;;;;;0;;;;;;;;Ramesh Thiyagarajah;GER;;;Suresh Thiyagarajah;GER;;;;;;;;;;33 - 33;33 - 33;33 - 33;33 - 33
M;7;inary Round - Group C;;SWE;Sweden;SWE;SWE;KOR;Korea;KOR;KOR;;;42;31;;;20;14;22;17;;;;;;;;;;;;18/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;1;;;;;;;;Mariana Garcia;ARG;;;Maria Ines Paolantoni;ARG;;;;;;;;;;42 - 31;31 - 42;42 - 31;31 - 42
M;11;inary Round - Group E;;DEN;Denmark;DEN;DEN;MAR;Morocco;MAR;MAR;;;43;31;;;21;18;22;13;;;;;;;;;;;;18/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;1;;;;;;;;William Weijmans;NED;;;Rick Wolbertus;NED;;;;;;;;;;43 - 31;31 - 43;43 - 31;31 - 43
M;4;inary Round - Group A;;POL;Poland;POL;POL;URU;Uruguay;URU;URU;;;39;16;;;19;8;20;8;;;;;;;;;;;;18/06/2025;;;Plock;Orlen Arena;18:30;;;;;;1;;;;;;;;Fadel Diop;SEN;;;Abdoulaye Faye;SEN;;;;;;;;;;39 - 16;16 - 39;39 - 16;16 - 39
M;8;inary Round - Group C;;JPN;Japan;JPN;JPN;USA;USA;USA;USA;;;41;33;;;20;10;21;23;;;;;;;;;;;;18/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;1;;;;;;;;Nichlas Nygaard;DEN;;;Jonas Primdahl;DEN;;;;;;;;;;41 - 33;33 - 41;41 - 33;33 - 41
M;12;inary Round - Group E;;FRA;France;FRA;FRA;MEX;Mexico;MEX;MEX;;;46;17;;;23;8;23;9;;;;;;;;;;;;18/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;1;;;;;;;;Hideki Furukawa;JPN;;;Murata Tetsuro;JPN;;;;;;;;;;46 - 17;17 - 46;46 - 17;17 - 46
M;15;inary Round - Group G;;TUN;Tunisia;TUN;TUN;SUI;Switzerland;SUI;SUI;;;31;41;;;17;21;14;20;;;;;;;;;;;;18/06/2025;;;Kielce;Hala Legionow;18:45;;;;;;2;;;;;;;;Amar Konjicanin;BIH;;;Dino Konjicanin;BIH;;;;;;;;;;31 - 41;41 - 31;31 - 41;41 - 31
M;16;inary Round - Group G;;GER;Germany;GER;GER;SRB;Serbia;SRB;SRB;;;30;29;;;14;12;16;17;;;;;;;;;;;;18/06/2025;;;Kielce;Hala Legionow;21:00;;;;;;1;;;;;;;;Mads Fremstad;NOR;;;Jorgen Jorstad;NOR;;;;;;;;;;30 - 29;29 - 30;30 - 29;29 - 30
M;17;inary Round - Group F;;FAR;Faroe Islands;FAR;FAR;ISL;Iceland;ISL;ISL;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;;;;;;;;;Cristian Lemes;URU;;;Mathias Sosa;URU;;;;;;;;;; - ; - ; - ; - 
M;21;inary Round - Group H;;KSA;Saudi Arabia;KSA;KSA;ESP;Spain;ESP;ESP;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;;;;;;;;;Mads Fremstad;NOR;;;Jorgen Jorstad;NOR;;;;;;;;;; - ; - ; - ; - 
M;18;inary Round - Group F;;MKD;North Macedonia;MKD;MKD;ROU;Romania;ROU;ROU;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;;;;;;;;;Michal Fabryczny;POL;;;Jakub Rawicki;POL;;;;;;;;;; - ; - ; - ; - 
M;22;inary Round - Group H;;EGY;Egypt;EGY;EGY;BRN;Bahrain;BRN;BRN;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;;;;;;;;;Andrej Budzak;SVK;;;Michal Zahradnik;SVK;;;;;;;;;; - ; - ; - ; - 
M;19;inary Round - Group E;;MEX;Mexico;MEX;MEX;DEN;Denmark;DEN;DEN;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;;;;;;;;;Novica Mitrovic;MNE;;;Miljan Vesovic;MNE;;;;;;;;;; - ; - ; - ; - 
M;20;inary Round - Group E;;FRA;France;FRA;FRA;MAR;Morocco;MAR;MAR;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;;;;;;;;;Zan Puksic;SLO;;;Miha Satler;SLO;;;;;;;;;; - ; - ; - ; - 
M;23;inary Round - Group G;;TUN;Tunisia;TUN;TUN;SRB;Serbia;SRB;SRB;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Kielce;Hala Legionow;18:45;;;;;;;;;;;;;;Jacob Jaeger Pagh;DEN;;;Karl Johan Thygesen;DEN;;;;;;;;;; - ; - ; - ; - 
M;24;inary Round - Group G;;SUI;Switzerland;SUI;SUI;GER;Germany;GER;GER;;;;;;;;;;;;;;;;;;;;;;19/06/2025;;;Kielce;Hala Legionow;21:00;;;;;;;;;;;;;;Danielo Bozhinovski;MKD;;;Viktor Nachevski;MKD;;;;;;;;;; - ; - ; - ; - 
M;25;inary Round - Group B;;BRA;Brazil;BRA;BRA;AUT;Austria;AUT;AUT;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Plock;Orlen Arena;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;29;inary Round - Group D;;CAN;Canada;CAN;CAN;POR;Portugal;POR;POR;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;26;inary Round - Group B;;HUN;Hungary;HUN;HUN;ARG;Argentina;ARG;ARG;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Plock;Orlen Arena;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;30;inary Round - Group D;;CRO;Croatia;CRO;CRO;ALG;Algeria;ALG;ALG;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;27;inary Round - Group A;;URU;Uruguay;URU;URU;NOR;Norway;NOR;NOR;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Plock;Orlen Arena;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;31;inary Round - Group C;;USA;USA;USA;USA;SWE;Sweden;SWE;SWE;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;28;inary Round - Group A;;POL;Poland;POL;POL;SLO;Slovenia;SLO;SLO;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Plock;Orlen Arena;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;32;inary Round - Group C;;JPN;Japan;JPN;JPN;KOR;Korea;KOR;KOR;;;;;;;;;;;;;;;;;;;;;;20/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;33;inary Round - Group B;;ARG;Argentina;ARG;ARG;BRA;Brazil;BRA;BRA;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Plock;Orlen Arena;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;37;inary Round - Group D;;ALG;Algeria;ALG;ALG;CAN;Canada;CAN;CAN;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;41;inary Round - Group F;;ROU;Romania;ROU;ROU;FAR;Faroe Islands;FAR;FAR;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;45;inary Round - Group H;;BRN;Bahrain;BRN;BRN;KSA;Saudi Arabia;KSA;KSA;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;34;inary Round - Group B;;AUT;Austria;AUT;AUT;HUN;Hungary;HUN;HUN;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Plock;Orlen Arena;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;38;inary Round - Group D;;POR;Portugal;POR;POR;CRO;Croatia;CRO;CRO;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;42;inary Round - Group F;;ISL;Iceland;ISL;ISL;MKD;North Macedonia;MKD;MKD;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;46;inary Round - Group H;;ESP;Spain;ESP;ESP;EGY;Egypt;EGY;EGY;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;35;inary Round - Group A;;SLO;Slovenia;SLO;SLO;URU;Uruguay;URU;URU;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Plock;Orlen Arena;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;39;inary Round - Group C;;KOR;Korea;KOR;KOR;USA;USA;USA;USA;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;43;inary Round - Group E;;MAR;Morocco;MAR;MAR;MEX;Mexico;MEX;MEX;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;36;inary Round - Group A;;NOR;Norway;NOR;NOR;POL;Poland;POL;POL;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Plock;Orlen Arena;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;40;inary Round - Group C;;SWE;Sweden;SWE;SWE;JPN;Japan;JPN;JPN;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;44;inary Round - Group E;;DEN;Denmark;DEN;DEN;FRA;France;FRA;FRA;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;47;inary Round - Group G;;SRB;Serbia;SRB;SRB;SUI;Switzerland;SUI;SUI;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Kielce;Hala Legionow;18:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;48;inary Round - Group G;;GER;Germany;GER;GER;TUN;Tunisia;TUN;TUN;;;;;;;;;;;;;;;;;;;;;;21/06/2025;;;Kielce;Hala Legionow;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;49;ent's Cup - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Plock;Orlen Arena;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;53;ent's Cup - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;57;ent's Cup - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;61;ent's Cup - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;50;ent's Cup - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Plock;Orlen Arena;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;54;ent's Cup - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;58;ent's Cup - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;62;ent's Cup - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;51;ound - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Plock;Orlen Arena;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;55;ound - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;59;ound - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;52;ound - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Plock;Orlen Arena;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;56;ound - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;60;ound - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;63;ound - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Kielce;Hala Legionow;18:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;64;ound - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23/06/2025;;;Kielce;Hala Legionow;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;65;ent's Cup - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Plock;Orlen Arena;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;69;ent's Cup - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;73;ent's Cup - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;77;ent's Cup - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;66;ent's Cup - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Plock;Orlen Arena;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;70;ent's Cup - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;74;ent's Cup - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;78;ent's Cup - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;67;ound - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Plock;Orlen Arena;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;71;ound - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;75;ound - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;68;ound - Group I;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Plock;Orlen Arena;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;72;ound - Group II;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;76;ound - Group III;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;79;ound - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Kielce;Hala Legionow;18:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;80;ound - Group IV;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;24/06/2025;;;Kielce;Hala Legionow;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;81;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;9-12. place;26/06/2025;;;Sosnowiec;Arena Sosnowiec;09:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;87;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;17-20. place;26/06/2025;;;Katowice;Arena Katowice;09:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;82;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;9-12. place;26/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;88;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;17-20. place;26/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;93;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;29-32. place;26/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;83;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;13-16. place;26/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;89;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;21-24. place;26/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;94;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;29-32. place;26/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;84;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;13-16. place;26/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;90;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;21-24. place;26/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;95;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;25-28. place;26/06/2025;;;Kielce;Hala Legionow;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;85;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Quarterfinals;26/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;91;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Quarterfinals;26/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;96;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;25-28. place;26/06/2025;;;Kielce;Hala Legionow;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;86;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Quarterfinals;26/06/2025;;;Sosnowiec;Arena Sosnowiec;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;92;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Quarterfinals;26/06/2025;;;Katowice;Arena Katowice;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;97;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;11-12. place;27/06/2025;;;Sosnowiec;Arena Sosnowiec;09:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;103;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;19-20. place;27/06/2025;;;Katowice;Arena Katowice;09:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;98;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;9-10. place;27/06/2025;;;Sosnowiec;Arena Sosnowiec;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;104;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;17-18. place;27/06/2025;;;Katowice;Arena Katowice;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;109;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;31-32. place;27/06/2025;;;Kielce;Hala Legionow;11:45;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;99;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;15-16. place;27/06/2025;;;Sosnowiec;Arena Sosnowiec;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;105;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;23-24. place;27/06/2025;;;Katowice;Arena Katowice;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;110;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;29-30. place;27/06/2025;;;Kielce;Hala Legionow;14:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;100;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;13-14. place;27/06/2025;;;Sosnowiec;Arena Sosnowiec;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;106;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;21-22. place;27/06/2025;;;Katowice;Arena Katowice;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;111;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;27-28. place;27/06/2025;;;Kielce;Hala Legionow;16:15;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;101;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;5-8. place;27/06/2025;;;Sosnowiec;Arena Sosnowiec;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;107;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;5-8. place;27/06/2025;;;Katowice;Arena Katowice;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;112;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;25-26. place;27/06/2025;;;Kielce;Hala Legionow;18:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;102;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Semifinals;27/06/2025;;;Sosnowiec;Arena Sosnowiec;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;108;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Semifinals;27/06/2025;;;Katowice;Arena Katowice;21:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;113;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;7-8. place;29/06/2025;;;Katowice;Arena Katowice;12:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;114;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;5-6. place;29/06/2025;;;Katowice;Arena Katowice;14:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;115;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;3-4. place;29/06/2025;;;Katowice;Arena Katowice;17:00;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 
M;116;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Finals;29/06/2025;;;Katowice;Arena Katowice;19:30;;;;;;;;;;;;;; ;;;; ;;;;;;;;;;; - ; - ; - ; - 

