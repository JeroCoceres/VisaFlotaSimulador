//UDMv3.4.1.1b
//**DO NOT EDIT THIS *****
if (!exclude) { //********
    //************************
    
    ///////////////////////////////////////////////////////////////////////////
    //
    //  ULTIMATE DROPDOWN MENU VERSION 3.4.1b by Brothercake
    //  http://www.brothercake.com/dropdown/ 
    //
    //  Link-wrapping routine by Brendan Armstrong
    //  KDE modifications by David Joham
    //  Opera reload/resize routine by Michael Wallner
    //  http://www.wallner-software.com/
    //
    //  This script featured on Dynamic Drive (http://www.dynamicdrive.com)
    //
    ///////////////////////////////////////////////////////////////////////////
    
    // *** POSITIONING AND STYLES *********************************************
    
    var menuALIGN = "fixed";	// alignment
    var absLEFT = 	0;		// absolute left or right position (if menu is left or right aligned)
    var absTOP = 	63; 		// absolute top position
    
    var staticMENU = false;		// static positioning mode (ie5,ie6 and ns4 only)
    
    var stretchMENU = false;	// show empty cells
    var showBORDERS = false;	// show empty cell borders
    
    var baseHREF ;		// base path to .js files for the script (ie: resources/)
    var zORDER = 	1000;		// base z-order of nav structure (not ns4)
    
    var mCOLOR = 	"White";	// main nav cell color
    var rCOLOR = 	"#4A71A5";	// main nav cell rollover color
    var bSIZE = 	1;		// main nav border size
    var bCOLOR = 	"#B5BAC6"	// main nav border color
    var aLINK = 	"#4A71A5";	// main nav link color
    var aHOVER = 	"White";	// main nav link hover-color (dual purpose)
    var aDEC = 	"none";		// main nav link decoration
    var fFONT = 	"Verdana";	// main nav font face
    var fSIZE = 	9;		// main nav font size (pixels)
    var fWEIGHT = 	"bold"		// main nav font weight
    var tINDENT = 	7;		// main nav text indent (if text is left or right aligned)
    var vPADDING = 	1;		// main nav vertical cell padding
    var vtOFFSET = 	0;		// main nav vertical text offset (+/- pixels from middle)
    
    var keepLIT =	true;		// keep rollover color when browsing menu
    var vOFFSET = 	3;		// shift the submenus vertically
    var hOFFSET = 	-1;		// shift the submenus horizontally
    
    var smCOLOR = 	"#B5BAC6";	// submenu cell color
    
    var srCOLOR = 	"#868B9E";	// submenu cell rollover color
    var sbSIZE = 	1;		// submenu border size
    var sbCOLOR = 	"White"		// submenu border color
    var saLINK = 	"White";	// submenu link color
    var saHOVER = 	"";		// submenu link hover-color (dual purpose)
    var saDEC = 	"none";		// submenu link decoration
    var sfFONT = 	"Verdana";	// submenu font face
    var sfSIZE = 	9;		// submenu font size (pixels)
    var sfWEIGHT = 	"normal"	// submenu font weight
    var stINDENT = 	5;		// submenu text indent (if text is left or right aligned)
    var svPADDING = 0;		// submenu vertical cell padding
    var svtOFFSET = 3;		// submenu vertical text offset (+/- pixels from middle)
    
    var shSIZE =	0;		// submenu drop shadow size
    var shCOLOR =	"cccccc";	// submenu drop shadow color
    var shOPACITY = 75;		// submenu drop shadow opacity (not ie4,ns4 or opera)
    
    var keepSubLIT = true;		// keep submenu rollover color when browsing child menu
    var chvOFFSET = -12;		// shift the child menus vertically
    var chhOFFSET = 7;		// shift the child menus horizontally
    
    var closeTIMER = 330;		// menu closing delay time
    
    var cellCLICK = true;		// links activate on TD click
    var aCURSOR = "hand";		// cursor for active links (not ns4 or opera)
    
    var altDISPLAY = "";		// where to display alt text
    var allowRESIZE = true;		// allow resize/reload
    
    var redGRID = false;		// show a red grid
    var gridWIDTH = 0;		// override grid width
    var gridHEIGHT = 1;		// override grid height
    var documentWIDTH = 0;		// override document width
    
    var hideSELECT = true;		// auto-hide select boxes when menus open (ie only)
    var allowForSCALING = false;	// allow for text scaling in mozilla 5
    var ancho = new Array(92, 108, 135, 120, 80, 93, 103);
    
    }
    