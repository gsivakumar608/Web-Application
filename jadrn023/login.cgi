#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

##---------------------------- MAIN ---------------------------------------

my $q;
if(authenticate_user()) {
    send_to_main();   
    }
else {
    send_to_login_error();
    }    
###########################################################################

###########################################################################
sub authenticate_user {
    $q = new CGI;
    my $user = $q->param("user");
    my $password = $q->param("password");    
    open DATA, "</srv/www/cgi-bin/jadrn023/passwords.dat" 
        or die "Cannot open file.";
    @file_lines = <DATA>;
    close DATA;

    $OK = 0; #not authorized

    foreach $line (@file_lines) {
        chomp $line;
        ($stored_user, $stored_pass) = split /=/, $line;    
        if($stored_user eq $user && Crypt::SaltedHash->validate($stored_pass, $password)) {
            $OK = 1;
            last;
            }
        }
    return $OK;
    }
###########################################################################

###########################################################################
sub send_to_login_error {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn023/proj1/error.html" />
</head><body></body>
</html>

END
    }  
    
###########################################################################
      
###########################################################################
sub send_to_main {
# args are DRIVER, CGI OBJECT, SESSION LOCATION
# default for undef is FILE, NEW SESSION, /TMP 
# for login.html, don't look for any existing session.
# Always start a new one.  Send a cookie to the browser.
# Default expiration is when the browser is closed.
# WATCH YOUR COOKIE NAMES! USE JADRNXXX_SID  
    my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
    $session->expires('+1d');
    my $cookie = $q->cookie(jadrn000SID => $session->id);
    print $q->header( -cookie=>$cookie ); #send cookie with session ID to browser    
    my $sid = $session->id;
    print <<END;
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>Cameras</title>
	<meta http-equiv="content-type" 
		content="text/html;charset=utf-8" />
		
 <link rel="stylesheet" type="text/css" href="/~jadrn023/proj1/css/style.css" />   
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script type="text/javascript" src="/~jadrn023/proj1/js/ajax_healper.js"></script>
<script type="text/javascript" src="/~jadrn023/proj1/js/validation.js"></script>
</head>

<body>
<h1> Cameras </h1>
<div class="progressTextDiv"> Submitting Form...</div>
<div class="successCenter" id ="confirmation"></div>

    <form  	  id="addProductForm"
              name="Validate"
              action="http://jadran.sdsu.edu/perl/jadrn023/proj1/confirm.cgi"
              method="post"
              enctype="multipart/form-data">
      
<div id="menu">
<ul>
<li><a class="selected" href="/~jadrn023/proj1/newInventory.html">New Inventory</a></li>
<li><a href="/~jadrn023/proj1/editInventory.html">Edit Inventory</a></li>
<li><a href="/~jadrn023/proj1/deleteInventory.html">Delete Inventory</a></li>
</ul>
</div>

<!-- <div id= "content"> -->

<ul class="inlineobjects">
			<li><label class="title">SKU:<span class="astric">*</span></label></li>
            <li><input type="text" name="sku" id="sku" size="25" maxlength="6"/></li>
</ul> 
<ul class="inlineobjects">            
             <li><label class="title">Category:<span class="astric">*</span></label></li>    
            <li><input type="text" name="category" id="category" size="25" /></li>
</ul> 
<ul class="inlineobjects"> 
			<li><label class="title">Vender:<span class="astric">*</span></label></li> 
    		<li><input type="text" name="vender" id="vender" size="25" /></li>
</ul> 
<ul class="inlineobjects"> 
            <li><label class="title">Manufacturer's Identifier:<span class="astric">*</span></label></li> 
            <li><input type="text" name="manufacturersidentifier" id="manufacturersidentifier" size="25" /></li>
</ul> 
<ul class="inlineobjects">           
        	<li><label class="title">Description:<span class="astric">*</span></label></li> 
			<li><textarea rows="4" cols="50" name="description" id="description" ></textarea></li>
</ul> 
<ul class="inlineobjects">  
        	<li><label class="title">Product Features:<span class="astric">*</span></label></li> 
            <li><textarea rows="4" cols="50" name="productfeatures" id="productfeatures" ></textarea></li>
</ul>
<ul class="inlineobjects">         
            <li><label class="title">Cost:<span class="astric">*</span></label></li> 
          $ <li><input type="text" name="cost" id="cost" size="25" /></li>
</ul> 
<ul class="inlineobjects">         
            <li><label class="title">Retail:<span class="astric">*</span></label></li> 
          $ <li><input type="text" name="retail" id="retail" size="25" /></li>
</ul> 
<ul class="inlineobjects"> 
         	<li><label class="title">Product Image:<span class="astric">*</span></label></li> 
            <li><input type="file" name="productimage" id="productimage" /></li>
</ul>

<div id="error_message"> 
</div>   

 <div id="button">  
        <input type="submit" value="Submit" name="submit" class="formbutton" />
        <input type="reset" value="Clear" name="reset" class="formbutton" />
        </div> 

</form>
</body>
</html>

END
}
###########################################################################    
    





