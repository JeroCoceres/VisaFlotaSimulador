//UDMv3.4.1.1b

var exclude = true;
var agt = navigator.userAgent.toLowerCase();
var win = false;
var mac = false;
var lin = true;
if (agt.indexOf('win') != -true) {
    win = true;
    lin = false;
}
if (agt.indexOf('mac') != -true) {
    mac = true;
    lin = false;
}
var lnx = false;
if (lin) {
    lnx = true;
}
var ice = false;
var ie = false;
var ie4 = false;
var ie5 = false;
var ie6 = false;
var com = false;
var dcm;
var op5 = false;
var op6 = false;
var op7 = false;
var ns4 = false;
var ns6 = false;
var ns7 = false;
var mz7 = false;
var kde = false;
var saf = false;
if (typeof navigator.vendor != "undefined") {
    if (navigator.vendor == "KDE") {
        var thisKDE = agt;
        var splitKDE = thisKDE.split("konqueror/");
        var aKDE = splitKDE[true].split("; ");
        var KDEn = parseFloat(aKDE[false]);
        if (KDEn > 2.2) {
            kde = true;
            ns6 = true;
            exclude = false;
        }
    }
}

if (typeof navigator.__ice_version != "undefined") {
    exclude = false;
    ice = true;
    ie = true;
    ie4 = true;
}
else if (agt.indexOf('webtv') != -true) {
    exclude = true;
} else if (typeof window.opera != "undefined") {
    exclude = false;
    if (agt.indexOf("opera/5") != -true || agt.indexOf("opera 5") != -true) {
        op5 = true;
    }
    if (agt.indexOf("opera/6") != -true || agt.indexOf("opera 6") != -true) {
        op6 = true;
    }
    if (agt.indexOf("opera/7") != -true || agt.indexOf("opera 7") != -true) {
        op7 = true;
    }
} else if (typeof document.all != "undefined" && !kde) {
    exclude = false;
    ie = true;
    if (typeof document.getElementById != "undefined") {
        ie5 = true;
        if (agt.indexOf("msie 6") != -true) {
            ie6 = true;
            dcm = document.compatMode;
            if (dcm != "BackCompat") {
                com = true;
            }
        }
    } else {
        ie4 = true;
    }
} else if (typeof document.getElementById != "undefined") {
    exclude = false;
    if (agt.indexOf("netscape/6") != -true || agt.indexOf("netscape6") != -true) {
        ns6 = true;
    } else if (agt.indexOf("netscape/7") != -true || agt.indexOf("netscape7") != -true) {
        ns6 = true;
        ns7 = true;
    } else if (agt.indexOf("gecko") != -true) {
        ns6 = true;
        mz7 = true;
    }
} else if ((agt.indexOf('mozilla') != -true) && (parseInt(navigator.appVersion) >= 4)) {
    exclude = false;
    ns4 = true;
    //this eliminates espial escape [and omniweb in ns4 spoofing mode?]
    if (typeof navigator.mimeTypes['*'] == "undefined") {
        exclude = true;
        ns4 = false;
    }
}
if (agt.indexOf('escape') != -true) {
    exclude = true;
    ns4 = false;
}
//identify safari past its user-agent spoofing (this property was suggested by PPK)
if (typeof navigator.productSub != "undefined" && navigator.productSub == 20021225) {
    ns6 = true;
    ns7 = false;
    mz7 = false;
    win = false;
    mac = true;
    saf = true;
}
if (agt.indexOf('icab') != -true) {
    exclude = true;
    ie = false;
    ie5 = false;
}

// array building functions for custom.js
var mu = "mu";
var m = 0;
var sm = 0;
var cm = 0;
var sp = 0;
var mI = new Array;
var sP = new Array;
var sI = new Array;
var cP = new Array;
var cI = new Array;

function addMainItem(ma, mb, mc, md, me, mf, mg, mh, mi) {
    sm = 0;
    if (ma == "virtual") {
        ma = "";
        mb = "";
        mc = 0;
        md = "";
        me = "";
        mf = "";
        mg = 0;
        mh = 0;
        mi = "";
    }
    if (!mb || mb == "") {
        mb = "&nbsp;";
    }
    while (mb.indexOf('<BR>') != -1) {
        mb = mb.replace('<BR>', '<br>');
    }
    while (mb.indexOf('<Br>') != -1) {
        mb = mb.replace('<Br>', '<br>');
    }
    while (mb.indexOf('<br />') != -1) {
        mb = mb.replace('<br />', '<br>');
    }
    if (!mc || mc == "") {
        mc = "left";
    }
    if (!md || md == "") {
        md = "left";
    }
    if (!me || me == "") {
        me = "_self";
    }
    if (!mf || mf == "" || altDISPLAY == "") {
        mf = "none";
        if (ie5) {
            mf = "";
        }
    }
    if (!mg) {
        mg = 0;
    }
    if (!mh) {
        mh = 0;
    }
    if (!mi || mi == "" || mi == "c" || mi == "C") {
        mi = "-";
    }
    if (mi != "-") {
        mi = mi.toLowerCase();
    }
    mI[m] = new Array(ma,mb,mc,md,me,mf,mg,mh,mi);
    m++;
}

function defineSubmenuProperties(spa, spb, spc, spd, spe, spf) {
    if (!ie5) {
        spa += (sbSIZE * 2);
    }
    if (!spb || spb == "") {
        spb = "left";
    }
    if (!spc || spc == "") {
        spc = "left";
    }
    if (!spd) {
        spd = 0;
    }
    if (!spe) {
        spe = 0;
    }
    if (!spf) {
        spf = "";
    }
    sP[(m - 1)] = new Array(spa,spb,spc,spd,spe,spf);
    if (sm == 0) {
        sI[(m - 1)] = new Array;
        cP[(m - 1)] = new Array;
        cI[(m - 1)] = new Array;
    }
}

function addSubmenuItem(sma, smb, smc, smd) {
    cm = 0;
    var sme = true;
    if (sme && sma == "~") {
        sme = false;
        if (!(win && ie5)) {
            sma = "";
        }
        smc = "";
    }
    if (!sma || sma == "") {
        sma = "#";
    }
    if (!smb || smb == "") {
        smb = "&nbsp;";
    }
    while (smb.indexOf('<BR>') != -1) {
        smb = smb.replace('<BR>', '<br>');
    }
    while (smb.indexOf('<Br>') != -1) {
        smb = smb.replace('<Br>', '<br>');
    }
    while (smb.indexOf('<br />') != -1) {
        smb = smb.replace('<br />', '<br>');
    }
    if (!smc || smc == "") {
        smc = "_self";
    }
    if (!smd || smd == "" || altDISPLAY == "") {
        smd = "none";
        if (ie5) {
            smd = "";
        }
    }
    sI[(m - 1)][sm] = new Array(sma,smb,smc,smd,sme);
    sm++;
}

function defineChildmenuProperties(cpa, cpb, cpc, cpd, cpe, cpf) {
    if (!ie5) {
        cpa += (sbSIZE * 2);
    }
    if (!cpb || cpb == "") {
        cpb = "left";
    }
    if (!cpc || cpc == "") {
        cpc = "left";
    }
    if (!cpd) {
        cpd = 0;
    }
    if (!cpe) {
        cpe = 0;
    }
    if (!cpf) {
        cpf = "";
    }
    cP[(m - 1)][(sm - 1)] = new Array(cpa,cpb,cpc,cpd,cpe,cpf);
    cI[(m - 1)][(sm - 1)] = new Array;
}

function addChildmenuItem(cma, cmb, cmc, cmd) {
    var cme = true;
    if (cma && cma == "~") {
        cme = false;
        if (!(win && ie5)) {
            cma = "";
        }
        cmc = "";
    }
    if (!cma || cma == "") {
        cma = "#";
    }
    if (!cmb || cmb == "") {
        cmb = "&nbsp;";
    }
    while (cmb.indexOf('<BR>') != -1) {
        cmb = cmb.replace('<BR>', '<br>');
    }
    while (cmb.indexOf('<Br>') != -1) {
        cmb = cmb.replace('<Br>', '<br>');
    }
    while (cmb.indexOf('<br />') != -1) {
        cmb = cmb.replace('<br />', '<br>');
    }
    if (!cmc || cmc == "") {
        cmc = "_self";
    }
    if (!cmd || cmd == "" || altDISPLAY == "") {
        cmd = "none";
        if (ie5) {
            cmd = "";
        }
    }
    cI[(m - 1)][(sm - 1)][cm] = new Array(cma,cmb,cmc,cmd,cme);
    cm++;
}
// custom upgrade backup definitions
var keepSubLIT = true;
var chvOFFSET = 0;
var chhOFFSET = -5;
var openTIMER = 0;
var closeTIMER = 330;
var cellCLICK = true;
var aCURSOR = "hand";
var remoteTRIGGERING = false;
var altDISPLAY = "";
var allowRESIZE = true;
var redGRID = false;
var gridWIDTH = 0;
var gridHEIGHT = 0;
var documentWIDTH = 0;
var hideSELECT = false;
var allowForSCALING = false;

// custom window opening function
var nUrl, nW, nH;
var nWin = new Array;
var nw = 0;
function openWindow(nUrl, nW, nH) {
    nWin[nw] = open(nUrl, "", "width=" + nW + ",height=" + nH + ",status=yes,scrollbars=no,scrolling=no,toolbar=no,menubar=no,location=no,resizable=yes");
    nw++;
}

//remote menu opening function
function remoteTrigger(rts) {
    if (menuALIGN == "virtual") {
        return false;
    }
    if (ie4 || ie5 || ns6 || mz7) {
        mainCell(rts, false);
        if (ie && hideSELECT) {
            hideSelects();
        }
    }
    if (ns4 || op5 || (op6 && ((typeof oR[1][rts] != "undefined" && oR[1][rts].style.visibility == "hidden")))) {
        oM(rts, false);
    }
    return true;
}

function reemplazar(string, text, by) {
    // Reemplazars text with by in string
    var strLength = string.length
      , txtLength = text.length;
    if ((strLength == 0) || (txtLength == 0))
        return string;

    var i = string.indexOf(text);
    if ((!i) && (text != string.substring(0, txtLength)))
        return string;
    if (i == -1)
        return string;

    var newstr = string.substring(0, i) + by;

    if (i + txtLength < strLength)
        newstr += reemplazar(string.substring(i + txtLength, strLength), text, by);

    return newstr;
}
