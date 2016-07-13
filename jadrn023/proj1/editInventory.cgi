#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

my $q = new CGI;
my $cookie_sid = $q->cookie('jadrn023SID');
my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});   
my $sid = $session->id;

if($cookie_sid ne $sid) {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn023/proj1/error.html" />
</head><body></body>
</html>

END
return;
}

print <<END;
Content-type: text/html

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

      
<div id="menu">
<ul>
<li><a class="selected" href="/perl/jadrn023/proj1/newInventory.cgi">New Inventory</a></li>
<li><a href="/perl/jadrn023/proj1/editInventory.cgi">Edit Inventory</a></li>
<li><a href="/perl/jadrn023/proj1/deleteInventory.cgi">Delete Inventory</a></li>
</ul>
</div>

<div id= "sku_form">
<form  	  id="fetchProductForm"
              method="post"
              enctype="multipart/form-data">
              
<input type="text" name="sku_search" id="sku_search" size="6" />
<input type="submit" value="Submit" name="submit" class="formbutton" />
</form>
</div>
    <form  
              name="Validate"
              id="editProductForm"
              action="http://jadran.sdsu.edu/perl/jadrn023/proj1/confirm.cgi"
              method="post"
              enctype="multipart/form-data">


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
          \$\ <li><input type="text" name="cost" id="cost" size="25" /></li>
</ul> 
<ul class="inlineobjects">         
            <li><label class="title">Retail:<span class="astric">*</span></label></li> 
          \$\ <li><input type="text" name="retail" id="retail" size="25" /></li>
</ul> 
<ul class="inlineobjects"> 
         	<li><label class="title">Product Image:<span class="astric">*</span></label></li> 
            <li><input type="file" name="productimage" id="productimage" /></li>
             <li><img id="prodImageView" src="" alt="product image" height="65" width="65"></li>
</ul>

<div id="error_message"> 
</div>   

 <div id="button">  
        <input type="submit" value="Update" name="submit" class="formbutton" />
        <input type="reset" value="Clear" name="reset" class="formbutton" />
        </div> 

<table>
    <tr>
        <td>The current session ID is</td>
        <td>$sid</td>
    </tr>
    <tr>
        <td>The cookie session ID is</td>
        <td>$cookie_sid</td>
    </tr>
</table>

<a href="/perl/jadrn023/logout.cgi">Logout Now</a>

</form>
</body>
</html>
END
