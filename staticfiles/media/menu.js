//UDMv3.8

//*** DO NOT EDIT **************************************************************************
var tempEl;
function getRealLeft(imgElem) {
    if (ns4) {
        xPos = imgElem.x;
    } else if (!exclude) {
        xPos = eval(imgElem).offsetLeft;
        tempEl = eval(imgElem).offsetParent;
        while (tempEl != null) {
            xPos += tempEl.offsetLeft;
            tempEl = tempEl.offsetParent;
        }
    }
    if (mac && ie5) {
        xPos += parseInt(document.body.leftMargin);
    }
    return xPos;
}
;
function getRealTop(imgElem) {
    if (ns4) {
        yPos = imgElem.y;
    } else if (!exclude) {
        yPos = eval(imgElem).offsetTop;
        tempEl = eval(imgElem).offsetParent;
        while (tempEl != null) {
            yPos += tempEl.offsetTop;
            tempEl = tempEl.offsetParent;
        }
    }
    if (mac && ie5) {
        yPos += parseInt(document.body.topMargin);
    }
    return yPos;
}
;
/*get offset position based on a function from http://www.webreference.com/js/column33/image.html*/

var xPos = 0;
var yPos = 0;
var rImg;
var rPosition = new Array;
if (typeof document.images['anchor'] != "undefined" && typeof document.images['anchor'] != null) {
    rImg = document.images['anchor'];
}
;var fAry = new Array;
var fj = 0;
var fImgs = document.images;
var faryl = 0;
if (!exclude) {
    faryl = fImgs.length;
}

for (var i = 0; i < faryl; i++) {
    if (fImgs[i].name == "freeanchor") {
        fAry[fj] = fImgs[i];
        fj++;
    }
}
;
var usingR = 0;
var usingRF = 0;
if (!exclude && rImg) {
    usingR = 1;
    if ((mac && ie4) || kde) {
        ie4 = 0;
        ie = 0;
        kde = 0;
        exclude = 1;
    } else if (ns4) {
        xPos = getRealLeft(rImg);
        yPos = getRealTop(rImg);
        if (menuALIGN != "free") {
            menuALIGN = "left";
        }
        absLEFT = xPos;
        absTOP = yPos;
    } else {
        xPos = getRealLeft(rImg);
        yPos = getRealTop(rImg);
        if (menuALIGN != "free") {
            menuALIGN = "left";
        }
        absLEFT = xPos;
        absTOP = yPos;
    }
}

faryl = fAry.length;
if (faryl > 0 && menuALIGN == "free") {
    usingRF = 1;
    if ((mac && ie4) || kde) {
        ie4 = 0;
        ie = 0;
        kde = 0;
        exclude = 1;
    } else if (ns4) {
        for (i = 0; i < faryl; i++) {
            xPos = getRealLeft(fAry[i]);
            yPos = getRealTop(fAry[i]);
            if (typeof mI[i] != "undefined") {
                mI[i][7] = xPos;
                mI[i][6] = yPos;
            }
            absLEFT = 0;
            absTOP = 0;
        }
    } else {
        for (i = 0; i < faryl; i++) {
            xPos = getRealLeft(fAry[i]);
            yPos = getRealTop(fAry[i]);
            if (typeof mI[i] != "undefined") {
                mI[i][7] = xPos;
                mI[i][6] = yPos;
            }
            absLEFT = 0;
            absTOP = 0;
        }
    }
}
;
var brTok = "";
if (ie4 || (mac && ie5)) {
    brTok = "ie4";
} else if (ie5) {
    brTok = "ie5";
}
if (ns6 || op7 || kde) {
    brTok = "moz";
}
if (op6) {
    brTok = "op6";
}
if (op5) {
    brTok = "op5";
}
if (ns4) {
    brTok = "ns4";
}
if (!exclude) {
    document.write('<script language="javascript1.2" type="text/javascript" src="' + baseHREF + 'menu_' + brTok + '.js"></script>');
}
