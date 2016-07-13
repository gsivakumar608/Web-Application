#!/usr/bin/perl
# Parmar, Urvashi    Account   jadrn033
# CS545, Fall 2014
# Project3

use CGI;
use DBI;
use CGI::Carp qw (fatalsToBrowser);
use File::Basename;

####################################################################
### constants
$CGI::POST_MAX = 1024 * 3000; # Limit file size to 3MB
my $upload_dir = '/home/jadrn023/public_html/proj1/images/u_load_images';
my $safe_filename_chars = "a-zA-Z0-9_.-";
####################################################################

my $q = new CGI;

my $category;
my $sku;
my $vendor;
my $vendorid;
my $categoryId;
my $result = "";
my ($key, $value);
my $host = "opatija.sdsu.edu";
my $port = "3306";
my $formType="";

my $username = "jadrn023";
my $password = "briefcase";

$database = "jadrn023";
$database_source = "dbi:mysql:$database:$host:$port";

my @key_arr = $q->param;

if(@key_arr < 2) 
{
	$result = "Please enter valid data.";
	print "Content-type: text/html\n\n";
    print $result;
   	exit;
} 
else 
{
for(my $i=0; $i<@key_arr; $i++) 
{
 my @value_ele = $q->param($key_arr[$i]);
 for(my $j=0; $j<@value_ele; $j++) 
 {
   if( $key_arr[$i] eq "category" ||
    $key_arr[$i] eq "vender" || $key_arr[$i] eq "manufacturersidentifier" ||
     $key_arr[$i] eq "description" || $key_arr[$i] eq "productfeatures" 
    || $key_arr[$i] eq "productimage")
  {

   if(isEmpty(trim($value_ele[$j]))) 
   {
   		$result = "$key_arr[$i] cannot be empty";
   		print "Content-type: text/html\n\n";
        print $result;
   		exit;
   }
  } elsif($key_arr[$i] eq "sku") {
  if(isSKU($value_ele[$j]) == 0){
  	
  	$result = "invalid $key_arr[$i]";
  	print "Content-type: text/html\n\n";
	print $result;
  	exit;
   }
   }elsif( $key_arr[$i] eq "cost" || $key_arr[$i] eq "retail") {
   if(isValidAmount($value_ele[$j]) == 0) {
   $result = "invalid $key_arr[$i]";
   print "Content-type: text/html\n\n";
   print $result;
   exit;
   }
   }
 	}
  }
$formType = trim($q->param("formType"));
$sku =  trim($q->param("sku"));
$category =  trim($q->param("category"));
$vendor =  trim($q->param("vender"));


my $dbh = DBI->connect($database_source, $username, $password) 
or die 'Cannot connect to db';

if($formType eq "delete") {
my $imth = $dbh->prepare("SELECT image FROM product WHERE sku='$sku'");
$imth->execute()
or die 'Cannot insert values to db';

my @imageRow=$imth->fetchrow_array();
if(@imageRow != 0){
my $imageFile = "$upload_dir/$imageRow[0]";
if (unlink($imageFile) == 0) {
    print "File deleted successfully.";
} else {
    print "File was not deleted.";
}
}

my $wth = $dbh->prepare("DELETE FROM product WHERE sku='$sku'");
 $wth->execute()
or die 'Cannot insert values to db';
$wth->finish();
$dbh->disconnect();
deleteCategoryIfAbsent($category, $dbh);
deleteVendorIfAbsent($vendor, $dbh);
  
   $result = "deleted";
   print "Content-type: text/html\n\n";
   print $result;
   exit;

} else {

my $venderModel = trim($q->param("manufacturersidentifier"));
my $description = trim($q->param("description"));
my $features= trim($q->param("productfeatures"));
my $cost = trim($q->param("cost"));
my $retail = trim($q->param("retail"));
my $image = trim($q->param("productimage"));
my $filename = trim($q->param("productimage"));

unless($filename) {
    die "There was a problem uploading the image; ";        
    }
    
    
    
    
    
    
    
    
#     
# $childPhoto = $_FILES['photo']['name'];
# 
# if($_FILES['photo']['error'] > 0) 
# {
#     $err = $_FILES['photo']['error'];	
#     
#         
# 	if($err == 1) {
# 		echoError("The file was too big to upload, the limit is 2MB<br />");
#         exit;
#     } else if($err == 4) {
#     	echoError("Photo is missing. Please upload photo.");
#     	exit;
#     
#     } else if($err != 0) {
#     echoError("Error while uploading photo.");
#     exit;
#     }
#     	
#     }
#     
#          
#     else if($childPhoto !="" && $childPhoto != null) 
#     {
#     
#     $extension = pathinfo($childPhoto, PATHINFO_EXTENSION);
#     
#     
#       if($extension == "gif" || $extension == "GIF" || $extension == "png" || $extension == "PNG" || $extension == "JPEG" || $extension == "jpeg" || $extension == "jpg" || $extension == "JPG")
#      {
#      //valid file
#      
#      } else 
#      {
#        echoError('Invalid image file. Only jpeg/gif/png/jpg files are allowed');
#        exit;
#      }     
    
    
    
    
    
 my $filesize = -s $filename;
 if($filesize > $CGI::POST_MAX) {
    
   print "Content-type: text/html\n\n";
   print "image size too big";
   exit;
   }
    
    
    
    
my ($name, $path, $extension) = fileparse($filename, '/..*/');
$filename = $name.$extension;
$filename =~ s/ //; #remove any spaces
if($filename !~ /^([$safe_filename_chars]+)$/) {
    die "Sorry, invalid character in the filename.";
    }   

$filename = untaint($filename);
$filename = lc($filename);
# get a handle on the uploaded image     
my $filehandle = $q->upload("productimage"); 

unless($filehandle) { die "Invalid handle"; }

# save the file
open UPLOADFILE, ">$upload_dir/$filename" or die
    "Error, cannot save the file.";
binmode UPLOADFILE;
while(<$filehandle>) {
    print UPLOADFILE $_;
    }
close UPLOADFILE;
my ($ext) = $filename =~ /(\.[^.]+)$/;
#print "$ext\n";
my $newName = $sku.$ext;
rename("$upload_dir/$filename", "$upload_dir/$newName") || die ( "Error in renaming" );

my $sth = $dbh->prepare("SELECT vendorID FROM vendor WHERE name='$vendor'");
$sth->execute()
or die 'Cannot insert values to db';

my @row=$sth->fetchrow_array();
if(@row == 0){
$sth=$dbh->prepare("INSERT INTO vendor VALUES ('0', '$vendor')");
$sth->execute()
or die 'Cannot insert values to db';
$vendorid = $dbh->{'mysql_insertid'};
} else{
$vendorid = $row[0];
}
$sth->finish();


my $rth = $dbh->prepare("SELECT categoryID FROM category WHERE name='$category'");
$rth->execute()
or die 'Cannot insert values to db';

my @catRow=$rth->fetchrow_array();
if(@catRow == 0){
my $rth = $dbh->prepare("INSERT INTO category VALUES ('0', '$category')");
$rth->execute()
or die 'Cannot insert values to db';
$categoryId = $dbh->{'mysql_insertid'};
}else{
$categoryId = $catRow[0];
}
$rth->finish();
print $formType;
if($formType eq "new") {
my $tth = $dbh->prepare("INSERT INTO product VALUES ('$sku', '$categoryId', '$vendorid', '$venderModel',
 '$description', '$features', '$cost', '$retail', '$newName')");
 $tth->execute()
or die 'Cannot insert values to db';
$tth->finish();
 } elsif($formType eq "edit") {
 $uth = $dbh->prepare("UPDATE product SET catID='$categoryId', venID='$vendorid', vendorModel='$venderModel',
 description='$description', features='$features', cost='$cost', retail='$retail', image='$newName' WHERE sku='$sku'");
 $uth->execute()
or die 'Cannot insert values to db';
$uth->finish();
 }


$dbh->disconnect();
  
   $result = "ok";
   print "Content-type: text/html\n\n";
   print $result;
   exit;
   }
}
  
sub isEmpty {
 foreach $item (@_){
      if($item eq "") {
      	return 1;
      } 
      	return 0;
   }
return 0;
}

sub isSKU
{
	my @parms = @_;
	$length = length($parms[0]);
	if($length == 6) {
	
    return $parms[0] =~ /^[a-zA-Z]{3}[0-9]{3}$/; 
    } else {
    return 0;
    }
}

sub isValidAmount
{
	my @parms = @_;
    
    return $parms[0]=~ /^\d*[.]?\d+$/; 
}

sub untaint {
    if($filename =~ m/^(\w+)$/) { die "Tainted filename!"; }
    return $1;
    }
    
sub trim {
    my @out = @_;
    for (@out) {
        s/^\s+//;
        s/\s+$//;
    }
    return $out[0];
}

sub deleteCategoryIfAbsent {

my @parms = @_;
my $catToDel = @parms[0];
my $dbh = @parms[1];

my $rth = $dbh->prepare("SELECT categoryID FROM category WHERE name='$catToDel'");
$rth->execute()
or die 'Cannot insert values to db';

my @catRow=$rth->fetchrow_array();
if(@catRow != 0){
my $sth = $dbh->prepare("SELECT * FROM product WHERE catID='$catRow[0]'");
$sth->execute()
or die 'Cannot insert values to db';

my @prodRow=$sth->fetchrow_array();
if(@prodRow == 0){
my $wth = $dbh->prepare("DELETE FROM category WHERE name='$catToDel'");
 $wth->execute()
or die 'Cannot insert values to db';
$wth->finish();

}

$dbh->disconnect();


}
}

sub deleteVendorIfAbsent {

my @parms = @_;
my $vendorToDel = @parms[0];
my $dbh = @parms[1];

my $rth = $dbh->prepare("SELECT vendorID FROM vendor WHERE name='$vendorToDel'");
$rth->execute()
or die 'Cannot insert values to db';

my @vendorRow=$rth->fetchrow_array();
if(@vendorRow != 0){
my $sth = $dbh->prepare("SELECT * FROM product WHERE venID='$vendorRow[0]'");
$sth->execute()
or die 'Cannot insert values to db';

my @prodRow=$sth->fetchrow_array();
if(@prodRow == 0){
my $wth = $dbh->prepare("DELETE FROM vendor WHERE name='$vendorToDel'");
 $wth->execute()
or die 'Cannot insert values to db';
$wth->finish();

}

$dbh->disconnect();


}
}



