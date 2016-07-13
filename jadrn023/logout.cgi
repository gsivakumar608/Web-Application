#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $q = new CGI;
my $sid = $q->cookie("jadrn023SID") || undef;
$session = new CGI::Session(undef, $sid, {Directory => '/tmp'});
    $session->param("my_name", "parmar");
    my $name = $session->param("my_name");
$session->delete();
$session->flush();
my $cookie = $q->cookie(jadrn023SID => '');

print $q->header( -cookie=>$cookie ); #send cookie with session ID to browser  


print <<END;    
    
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn023/error.html" />
</head><body></body>
</html>

END
