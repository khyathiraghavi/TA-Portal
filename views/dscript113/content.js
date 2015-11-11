// Copyright 2001-2003 Villario, villario@yahoo.com

<!-- hide JavaScript from non-JavaScript browsers
var agt=navigator.userAgent.toLowerCase();
var is_major = parseInt(navigator.appVersion);
var is_minor = parseFloat(navigator.appVersion);
var is_nav  = ((agt.indexOf('mozilla')!=-1) && (agt.indexOf('spoofer')==-1) && (agt.indexOf('compatible') == -1) && (agt.indexOf('opera')==-1) && (agt.indexOf('webtv')==-1));
var is_nav2 = (is_nav && (is_major == 2));
var is_nav3 = (is_nav && (is_major == 3));
var is_badnav4 = (is_nav && (parseFloat(navigator.appVersion) == 4.02));
var is_oldnav4 = (is_nav && (parseFloat(navigator.appVersion) < 4.06));
var is_nav4 = (is_nav && (is_major == 4));
var is_nav4up = (is_nav && (is_major >= 4));
var is_nav6 = (is_nav && (is_major == 5));
var is_nav6up = (is_nav && (is_major >= 5));
var is_ie   = (agt.indexOf("msie") != -1);
var is_ie3  = (is_ie && (is_major < 4));
var is_ie4  = (is_ie && (is_major == 4) && (agt.indexOf("msie 5.0")==-1));
var is_ie4up  = (is_ie  && (is_major >= 4));
var is_ie5  = (is_ie && (is_major == 4) && (agt.indexOf("msie 5.0")!=-1));
var is_ie5up  = (is_ie && !is_ie3 && !is_ie4);
var is_aol   = (agt.indexOf("aol") != -1);
var is_aol3  = (is_aol && is_ie3);
var is_aol4  = (is_aol && is_ie4);
var is_aol5up  = (is_aol && is_ie5up);
var is_opera = (agt.indexOf("opera") != -1);
var is_opera4 = (is_opera && (is_major == 4));
var is_opera5 = (is_opera && (is_major == 5));
var is_opera5up = (is_opera && (is_major >= 5));
var is_webtv = (agt.indexOf("webtv") != -1);
var is_domcom = ((is_nav6up)||(is_ie5up)||(is_opera5up))
var is_mac    = (agt.indexOf("mac")!=-1);
var is_mac68k = (is_mac && ((agt.indexOf("68k")!=-1) || (agt.indexOf("68000")!=-1)));
var is_macppc = (is_mac && ((agt.indexOf("ppc")!=-1) || (agt.indexOf("powerpc")!=-1)));
var dhtmlnav=0;
var dhtmlBrowser=0;
if ((is_nav4up)||(is_ie4up)) dhtmlBrowser=1;

var table_template_front_array1 = new Array();
var table_template_front_array2 = new Array();
var table_template_end_array = new Array();
var row_template_front_array = new Array();
var parent_layer_array = new Array();
var child_layer_array = new Array();
var last_button_name = "";
var last_parent_layer = "";
var last_child_layer = "";
var last_image_name = "";
var image_pointer = "";
var TimerID = "";
var TimerIDLink = "";
var table_width = 185; // Changes the width of all menu tables. Set to widest menu.
var IsLink = "NO";
var PrevLayer = "NO";
var WaitLink = 0;
var LinkLayer = "";
var TimeLinkOut = 800;
var TimeLayerOut = 800;

if (document.images) {
    var arrow = new Image();
    var blank = new Image();
    arrow.src = "dscript113/arrow.gif";
    blank.src = "dscript113/blank.gif";

    var I1on = new Image(); 
    I1on.src = "dscript113/button1_on.gif";
    var I1off = new Image();
    I1off.src = "dscript113/button1_off.gif";
    var I2on = new Image(); 
    I2on.src = "dscript113/button2_on.gif";
    var I2off = new Image();
    I2off.src = "dscript113/button2_off.gif";
    var I3on = new Image(); 
    I3on.src = "dscript113/button3_on.gif";
    var I3off = new Image();
    I3off.src = "dscript113/button3_off.gif";
    var I4on = new Image(); 
    I4on.src = "dscript113/button4_on.gif";
    var I4off = new Image();
    I4off.src = "dscript113/button4_off.gif";
    var I5on = new Image(); 
    I5on.src = "dscript113/button5_on.gif";
    var I5off = new Image();
    I5off.src = "dscript113/button5_off.gif";
}

function changeImages() {
  if (document.images) {
    for (var i=0; i<changeImages.arguments.length; i+=2) {
      document[changeImages.arguments[i]].src = eval(changeImages.arguments[i+1] + ".src");
    }
  }
}

function Layer(name, visibility, zindex, table_template, left, top) {
    this.name = name;
    this.left = left;
    this.top = top;
    this.width = table_width;
    this.visibility = visibility;
    this.zindex = zindex;
    this.table_template = table_template;
    this.ar = ar;
    this.fl = fl;

    if (this.table_template == 1) {
        this.left = this.left + this.width - 7;
    }

    if ((is_domcom)||(is_ie4)) {  
      if (is_mac) { //changed the navigator.appVersion.indexOf("Macintosh") to is_mac
            this.top += 7;
            this.left += 2;
        }
        this.layer_content = '<div id="' + this.name + '" style="position: absolute; left: ' + this.left + '; top: ' + this.top + '; width: ' + this.width + '; visibility: ' + (this.visibility ? 'visible' : 'hidden') + '; z-index: ' + this.zindex + ';">';
    } else if (is_nav4) { 
        this.layer_content = '<layer name="' + this.name + '" left=' + this.left + ' top=' + this.top + ' width=' + this.width + ' visibility=' + (this.visibility ? '"show"' : '"hide"') + ' z-index=' + this.zindex + '>';
    }
	   this.layer_content += table_template_front_array1[this.table_template];
	   this.layer_content += name
	   this.layer_content += table_template_front_array2[this.table_template];
		if (this.table_template == 0) { 
			parent_layer_array[parent_layer_array.length] = this.name;
		} else {
		child_layer_array[child_layer_array.length] = this.name;
	    }
}

function ar(row_template, row_content) {  
    this.layer_content += row_template_front_array[row_template] + row_content + row_end;
}

function fl() {  
    this.layer_content += table_template_end_array[this.table_template];
    if ((is_domcom)||(is_ie4)) {
      this.layer_content += '</div>'; 
    } else if (is_nav4) {
        this.layer_content += '</layer>';
        ;
    } document.write(this.layer_content)
}

function define_table(tw) {
    table_template_front_array1[0] = '<table width="' + tw + '" cellspacing="0" cellpadding="0" border="0" onmouseover="TableOver(\'';
    table_template_front_array2[0] = '\');" onmouseout="TableOut();"><tr><td colspan="2" width="7"><img src="dscript113/corner_ul.gif" width=7 height=8 border="0"></td><td width="' + (tw-7) + '" background="dscript113/line_top.gif"><img src="dscript113/blank.gif" width=' + (tw-7) + ' height=1 border="0"></td><td colspan="2" width="7"><img src="dscript113/corner_ur.gif" width=7 height=8 border="0"></td></tr><tr><td width="1" background="dscript113/vert_line.gif"><img src="dscript113/vert_line.gif" width=1 height=1 border="0"></td><td width="6" bgcolor="FFFFCE"><img src="dscript113/blank.gif" width=6 height=1 border="0"></td><td width="' + (tw-7) + '" valign="top" bgcolor="FFFFCE"><table width="' + (tw-7) + '" cellspacing="0" cellpadding="1" border="0">';
    table_template_end_array[0] = '</table></td><td width="6" bgcolor="FFFFCE"><img src="dscript113/blank.gif" width=6 height=1 border="0"></td><td width="1" background="dscript113/vert_line.gif"><img src="dscript113/vert_line.gif" width=1 height=1 border="0"></td></tr><tr><td colspan="2" width="7"><img src="dscript113/corner_ll.gif" width=7 height=8 border="0"></td><td width="' + (tw-7) + '" background="dscript113/line_bot.gif"><img src="dscript113/blank.gif" width=' + (tw-7) + ' height=1 border="0"></td><td colspan="2" width="7"><img src="dscript113/corner_lr.gif" width=7 height=8 border="0"></td></tr></table>';

    table_template_front_array1[1] = '<table width="' + tw + '" cellspacing="0" cellpadding="0" border="0" onmouseover="TableOver(\'';
    table_template_front_array2[1] = '\');" onmouseout="TableOut();"><tr><td colspan="2" width="7"><img src="dscript113/corner_ul.gif" width=7 height=8 border="0"></td><td width="' + (tw-14) + '" background="dscript113/line_top.gif"><img src="dscript113/blank.gif" width=' + (tw-14) + ' height=1 border="0"></td><td colspan="2" width="7"><img src="dscript113/corner_ur.gif" width=7 height=8 border="0"></td></tr><tr><td width="1" background="dscript113/vert_line.gif"><img src="dscript113/vert_line.gif" width=1 height=1 border="0"></td><td width="6" bgcolor="FFFFCE"><img src="dscript113/blank.gif" width=6 height=1 border="0"></td><td width="' + (tw-14) + '" valign="top" bgcolor="FFFFCE"><table width="' + (tw-14) + '" cellspacing="0" cellpadding="1" border="0">';
    table_template_end_array[1] = '</table></td><td width="6" bgcolor="FFFFCE"><img src="dscript113/blank.gif" width=6 height=1 border="0"></td><td width="1" background="dscript113/vert_line.gif"><img src="dscript113/vert_line.gif" width=1 height=1 border="0"></td></tr><tr><td colspan="2" width="7"><img src="dscript113/corner_ll.gif" width=7 height=8 border="0"></td><td width="' + (tw-14) + '" background="dscript113/line_bot.gif"><img src="dscript113/blank.gif" width=' + (tw-14) + ' height=1 border="0"></td><td colspan="2" width="7"><img src="dscript113/corner_lr.gif" width=7 height=8 border="0"></td></tr></table>';

    row_template_front_array[0] = '<tr><td width=11 valign="top"><img src="dscript113/bullet.gif" width=11 height=11 border="0"></td><td width=' + (tw-25) + '>';
    row_template_front_array[1] = '<tr><td width=' + (tw-14) + ' COLSPAN="2"><font face="Verdana, sans-serif" size=1>';
    row_template_front_array[2] = '<tr><td width=' + (tw-14) + ' ALIGN="right" COLSPAN="2"><font face="Verdana, sans-serif" size=1>';

    row_end = '</tr>';
}

define_table(table_width);

var l = new Layer("L01", 0, 4, 0, 260, 356);
l.ar(1, '<b><font class=MenuHead>PlanMagic Corporation</b></font>');
l.ar(0, '<a href="http://planmagic.com/company.html" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>About us</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/products.html" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>Our products</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/testimonials.html" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>Testimonials</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/affiliate.html" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>Affiliate program</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/directory/" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>Distributors & resellers</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/feedback.html" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>Feedback</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/contact.html" onmouseout="LinkOut(\'L01\');" onmouseover="LinkOver(\'L01-0\');" class="MenuLink"><font face=Verdana, sans-serif>Contact details</font></a></td>');
l.fl();

var l = new Layer("L02", 0, 4, 0, 260, 387);
l.ar(1, '<b><font class=MenuHead>PlanMagic software</b></font>');
l.ar(0, '<a href="http://planmagic.com/business_planning.html" onmouseout="LinkOut(\'L02\');" onmouseover="LinkOver(\'L02-1\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Business</font></a>&nbsp;<img src="dscript113/arrow.gif" name="Link"></td>');
l.ar(0, '<a href="http://planmagic.com/marketing_planning.html" onmouseout="LinkOut(\'L02\');" onmouseover="LinkOver(\'L02-2\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Marketing</font></a>&nbsp;<img src="dscript113/arrow.gif" name="Link"></td>');
l.ar(0, '<a href="http://planmagic.com/financial_planning.html" onmouseout="LinkOut(\'L02\');" onmouseover="LinkOver(\'L02-3\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Finance Pro</font></a>&nbsp;<img src="dscript113/arrow.gif" name="Link"></td>');
l.ar(0, '<a href="http://planmagic.com/business_plan/hotel_business_plan.html" onmouseout="LinkOut(\'L02\');" onmouseover="LinkOver(\'L02-0\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Hotel</font></a></td>');
l.ar(0, '<a href="http://plan-a-restaurant.com" onmouseout="LinkOut(\'L02\');" onmouseover="LinkOver(\'L02-0\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Restaurant</font></a></td>');
l.fl();

var l = new Layer("L02-1", 0, 5, 1, 275, 405);
l.ar(1, '<b><font class=MenuHead1>Business planning</b></font>');
l.ar(0, '<a href="http://planmagic.com/business_planning.html" onmouseover="TableOver(\'L02-1\');" class="MenuLink"><font face=Verdana, sans-serif>Features</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/tourbiz/tourbiz.htm" onmouseover="TableOver(\'L02-1\');" class="MenuLink"><font face=Verdana, sans-serif>Online demo</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/download.html" onmouseover="TableOver(\'L02-1\');" class="MenuLink"><font face=Verdana, sans-serif>Download demo</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/register.html" onmouseover="TableOver(\'L02-1\');" class="MenuLink"><font face=Verdana, sans-serif>How to order</font></a></td>');
l.fl();

var l = new Layer("L02-2", 0, 5, 1, 275, 420);
l.ar(1, '<b><font class=MenuHead1>Marketing planning</b></font>');
l.ar(0, '<a href="http://planmagic.com/marketing_planning.html" onmouseover="TableOver(\'L02-2\');" class="MenuLink"><font face=Verdana, sans-serif>Features</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/tourmar/tourmar.htm" onmouseover="TableOver(\'L02-2\');" class="MenuLink"><font face=Verdana, sans-serif>Online demo</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/download.html" onmouseover="TableOver(\'L02-2\');" class="MenuLink"><font face=Verdana, sans-serif>Download demo</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/register.html" onmouseover="TableOver(\'L02-2\');" class="MenuLink"><font face=Verdana, sans-serif>How to order</font></a></td>');
l.fl();

var l = new Layer("L02-3", 0, 5, 1, 275, 435);
l.ar(1, '<b><font class=MenuHead1>Financial planning</b></font>');
l.ar(0, '<a href="http://planmagic.com/financial_planning.html" onmouseover="TableOver(\'L02-3\');" class="MenuLink"><font face=Verdana, sans-serif>Features</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/download.html" onmouseover="TableOver(\'L02-3\');" class="MenuLink"><font face=Verdana, sans-serif>Download demo</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/register.html" onmouseover="TableOver(\'L02-3\');" class="MenuLink"><font face=Verdana, sans-serif>How to order</font></a></td>');
l.fl();

var l = new Layer("L03", 0, 4, 0, 260, 413);
l.ar(1, '<b><font class=MenuHead>Demo downloads</b></font>');
l.ar(0, '<a href="http://planmagic.com/download.html" onmouseover="TableOver(\'L03\');" class="MenuLink"><font face=Verdana, sans-serif>Business planning</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/download.html" onmouseover="TableOver(\'L03\');" class="MenuLink"><font face=Verdana, sans-serif>Marketing planning</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/download.html" onmouseover="TableOver(\'L03\');" class="MenuLink"><font face=Verdana, sans-serif>Financial planning</font></a></td>');
l.ar(0, '<a href="http://plan-a-restaurant.com" onmouseover="TableOver(\'L03\');" class="MenuLink"><font face=Verdana, sans-serif>Restaurant planning</font></a></td>');
l.fl();

var l = new Layer("L04", 0, 4, 0, 260, 437);
l.ar(1, '<b><font class=MenuHead>Available software</b></font>');
l.ar(0, '<a href="http://planmagic.com/business_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Business</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/marketing_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Marketing</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/financial_plannig.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Finance Pro</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/business_plan/bar_business_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Bar</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/business_plan/restaurant_business_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Restaurant</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/business_plan/bed_and_breakfast_business_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Bed & Breakfast</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/business_plan/hotel_business_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Hotel</font></a></td>');
l.ar(0, '<a href="http://planmagic.com/business_plan/resort_business_plan.html" onmouseover="TableOver(\'L04\');" class="MenuLink"><font face=Verdana, sans-serif>PlanMagic Resort</font></a></td>');
l.fl();

var numOfMenus = 4; // Number of the Main menus
var numOfImages = 5; // Number of rollover button images

layersList = new Array("L01","L02","L02-1","L02-2","L02-3","L03","L04");
var layerCount = 7; // Total number of the Main and the Sub menus

//--> end hide JavaScript