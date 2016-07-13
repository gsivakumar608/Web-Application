#!/usr/bin/perl

use DBI;
use CGI;

my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "jadrn023";
my $username = "jadrn023";
my $password = "briefcase";
my $database_source = "dbi:mysql:$database:$host:$port";
my $response = "";


my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

my $q = new CGI;
my $sku = $q->param("sku");
print $sku;

my $query = "select product.sku, jadrn023.category.name, jadrn023.vendor.name,
 product.vendorModel, product.description, product.features, product.cost, product.retail,
  product.image from jadrn023.vendor, jadrn023.category, product where product.sku='$sku'
   and product.venID=jadrn023.vendor.vendorID and product.catID = jadrn023.category.categoryID;";
            
my $sth = $dbh->prepare($query);
$sth->execute();

while(my @row=$sth->fetchrow_array()) {
    foreach $item (@row) {    
        $response .= $item."|"; #field separator
        }
    $response = substr $response, 0, (length($response)-1);  
    $response .= "||";  #record separator
    } 
    $response = substr $response, 0, (length($response)-2);     
unless($response) {
    $response = "invalid";
    }    
$sth->finish();
$dbh->disconnect();
    
print "Content-type: text/html\n\n";
print $response;               
