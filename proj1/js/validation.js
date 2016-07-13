var sku;
var category;
var vender;
var manufacturersIdentifier;
var description;
var productFeatures;
var cost;
var retail;
var productImage;
var infoArray;
var userName;
var password;

var inputType = 
    {
    	IDENTICODE:0, TEXT:1,  NUMBER:2, IMAGE:3, AMOUNT:4
     };
     
//error message divs
var ErrorMessage = "error_message";

 $(document).ready(function()
 { 
 			
 		var url = window.location.href; 
//  		console.log(url);
         var isSubmitForm = false;
         var isError = false;
         var formData;
         var currentPage;
         

         
         $('#fetchProductForm').submit(function(e){
            //e.preventDefault();
            fetchProductString();
            return false;         
  });
 		
        $('#addProductForm').submit(function(e){
            //e.preventDefault();
            submitFormData("new");
            return false;         
  });
  
    $('#editProductForm').submit(function(e){
            //e.preventDefault();
            submitFormData("edit");
            return false;         
  });
  
  $('#deleteProductForm').submit(function(e){
            //e.preventDefault();
            submitFormData("delete");
            return false;         
  });
  
  
  
   function submitFormData(formType)
   {
              if(isSubmitForm == true) 
              {
              return true;
              }
              if(validateform() != false) 
              {
               handleAnswer("OK", formType);
               //updateProgressText(true);
               //send_file();
              return isSubmitForm;
              } 
              else 
              {
              return false;
              }
  
  }
  
  function fetchProductString()
  {
  var request = new HttpRequest(
        "http://jadran.sdsu.edu/perl/jadrn023/proj1/ajax_string/fetch_string.cgi?sku="+document.getElementById("sku_search").value, handle_string_data);   
    request.send();
  }
  
  function handle_string_data(response)
  {
  console.log(response);
  if(response) {
   var fields = new Array();
   fields = response.split("|");
   if(fields.length > 0) {
   //$("#sku_form").hide();
   console.log(fields[0]);
   
   	document.getElementById("sku").value = fields[0];
	document.getElementById("category").value = fields[1];
	document.getElementById("vender").value = fields[2];
	document.getElementById("manufacturersidentifier").value = fields[3];
	document.getElementById("description").value = fields[4];
	document.getElementById("productfeatures").value = fields[5];
	document.getElementById("cost").value = fields[6];
	document.getElementById("retail").value = fields[7];
	
	document.getElementById("prodImageView").src = "/~jadrn023/proj1/images/u_load_images/"+fields[8];
	
	

   } 
   }
  }
  

         // function send_file() 
        //{     
//         var form_data = new FormData($('form')[0]);       
//         form_data.append("image", document.getElementById("productimage").files[0]);
//         
//         $.ajax({
//             url: "/perl/jadrn023/proj1/upload.cgi",
//             type: "post",
//             data: form_data,
//             processData: false,
//             contentType: false,
//             success: function(response) 
//             {
//               if(response != '') 
//               {
//               console.log("upload successful"+response);
//               var responseArray = response.split(':');
//               
//               if(responseArray.length > 1 && responseArray[0].trim() == 'error') 
//               {
//               isError=true;
//               $('#error_message').html(responseArray[1]);
//               updateProgressText(false);
//               return false;
//               } 
//         }
//             if(isError == false) 
//             {
//             // $('form').hide(10, function(){
// //             document.getElementById('confirmation').innerHTML = response;
// //             $('#confirmation').show();
// //             $('.enrollbutton').click(function(){
// //             $('#confirmation').html('');
// //             $('#confirmation').hide();
// //             resetChildInfo();
// //             $('form').show();
// //             $("#programselection").focus();
// //   });
// //             });
//             } 
// 			//updateProgressText(false);
//             },
//             error: function(response) {
//             $('#error_message').html(response);
//  			//updateProgressText(false);
//             }
//         });
//     }
        
    function handleAnswer(answer, formType) 
    {
        if($.trim(answer) == "OK")  
        {
        
        var form_data = new FormData($('form')[0]);  
        if(formType == "delete") {
        form_data.append("sku", document.getElementById("sku").value);
        form_data.append("category", document.getElementById("category").value);
        form_data.append("vender", document.getElementById("vender").value);
        form_data.append("formType", formType);
        } else {
           //  var params = $('form').serialize();
//             $.post('/perl/jadrn023/proj1/confirm.cgi', params, handleAjaxPost);
          
         
        form_data.append("sku", document.getElementById("sku").value);
        form_data.append("category", document.getElementById("category").value);
        form_data.append("vender", document.getElementById("vender").value);
        form_data.append("manufacturersidentifier", document.getElementById("manufacturersidentifier").value);
        form_data.append("description", document.getElementById("description").value);
        form_data.append("productfeatures", document.getElementById("productfeatures").value);
        form_data.append("cost", document.getElementById("cost").value);
        form_data.append("retail", document.getElementById("retail").value);
        form_data.append("productimage", document.getElementById("productimage").files[0]);
        form_data.append("formType", formType);
        }
        
        
        $.ajax({
            url: "/perl/jadrn023/proj1/confirm.cgi",
            type: "post",
            data: form_data,
            processData: false,
            contentType: false,
            async:false,
            success: function(response) 
            {
             if(response =='deleted') {
             resetFormInfo();
             isError=false;
              		isSubmitForm = true;
              		$('#error_message').html("record is deleted");
             } else if(response =='ok') {
             
              		isError=false;
              		isSubmitForm = true;
              		$('#error_message').html("result is ok");
              	
             }else 
              {
              		isError=true;
              		$('#error_message').html(response);
              	} 
              	
            },
            error: function(response) {
            $('#error_message').html(response);
 			
            }
        });
            
            }
        else if ($.trim(answer) == "DUP")
            $('#status').html("ERROR, Duplicate");
        else
            $('#status').html("Database error");        
    }
        
    function handleAjaxPost(returnResult) 
    {
              if(returnResult !='ok') 
              {
              	
              	
              		isError=true;
              		$('#error_message').html(returnResult);
              	} 
              	else 
              	{
              		isError=false;
              		isSubmitForm = true;
              	}       
    }  
  
 $("#sku").focus();  
  }); 
              
    function resetFormInfo() 
    {
    
    $('#sku_search').val('');
    $('#sku').val('');
    $('#category').val('');
    $('#vender').val('');
    $('#manufacturersidentifier').val('');
    $('#description').val('');
    $('#productfeatures').val('');
 	$('#cost').val('');
 	$('#retail').val('');
 	$('#productimage').val('');
    }
    
function initVariables() {

      sku = {
        ID:"sku", TYPE:inputType.IDENTICODE, ERROR:"Please enter valid SKU.", ERROR_DIV_ID:"error_message", NAME:"sku"
     }
      
    category={
         ID:"category", TYPE:inputType.TEXT, ERROR:"Please enter valid category.", ERROR_DIV_ID:"error_message", NAME:"category"
    }
     
     vender={
         ID:"vender", TYPE:inputType.TEXT, ERROR:"Please enter valid vender.", ERROR_DIV_ID:"error_message", NAME:"vender"
    }  
     
      manufacturersIdentifier = {
          ID:"manufacturersidentifier", TYPE:inputType.TEXT, ERROR:"Please enter manufacturers identifier.", ERROR_DIV_ID:"error_message", NAME:"manufacturers identifier"
     }
     
     description = {
          ID:"description", TYPE:inputType.TEXT, ERROR:"Please enter valid description.", ERROR_DIV_ID:"error_message", NAME:"description"
     }
     
     productFeatures={ 
          ID:"productfeatures", TYPE:inputType.TEXT, ERROR:"Please enter valid product features.", ERROR_DIV_ID:"error_message", NAME:"product features"
     }
     
     cost={
         ID:"cost", TYPE:inputType.AMOUNT, ERROR:"Please enter valid cost price.", ERROR_DIV_ID:"error_message", NAME:"cost"
     }
     
    retail={
         ID:"retail", TYPE:inputType.AMOUNT, ERROR:"Please enter valid retail price.", ERROR_DIV_ID:"error_message", NAME:"retail"
     }
    
    productImage={
     ID:"productimage", TYPE:inputType.PHOTO, ERROR:"Please upload product image.", ERROR_DIV_ID:"error_message", NAME:"product image"
    }
     
    infoArray = [sku, category, vender, manufacturersIdentifier, description, productFeatures, cost, retail, productImage];
    
    function getBlurFunction(obj) {
        return function() {
        validateOnBlur(obj);
            }
    }
}

function validateOnBlur(obj) {
if(checkEmptyValue(obj, false) == false) {
return false;
}
if(validateInput(obj, false) == false) {
    return false;
}
    clearError(obj);
}

function validateInput(obj, isShowError) {


switch(obj.TYPE) 
    { 
        case inputType.IDENTICODE:
                if(validateSKU(obj, isShowError) == false) 
                {
                    return false;
                }
                break;
                                  
        case inputType.AMOUNT:
                if(validateAmount(obj, isShowError) == false) 
                {
                    return false;
                }
                break;

        case inputType.PHOTO:
                if(validatePhoto(obj, isShowError) == false) 
                {
                    return false;
                }
                break;

             }
}  

function checkEmptyValue(obj, isShowError) 
{
             var value = getValueFromId(obj.ID);
             if(isEmpty(value)) 
             {
                 if(isShowError) 
                 {
                 showErrorDiv(obj, true);
                 }
                return false;
            }
        return true;
}

function validateform()
 {
     if(!infoArray) 
     {
     initVariables();
     }
     clearAllErrorMessages();
     
     //check input types and show error message if input is empty or invalid
    for(var i= 0; i<infoArray.length; i++) 
    {
        if(checkEmptyValue(infoArray[i], true) == false) {
        return false;
        }
        if(validateInput(infoArray[i], true) == false) {
           
           return false;
           }
    }    
 }
  
// function validateAddress(obj, isShowError)
// {
//     var value = getValueFromId(obj.ID);
//     if(isAddress(value))
//     {
//         return true;  
//     }  
//     else  
//     {  
//         if(isShowError) {
//         showErrorDiv(obj, false);
//         }
//         return false;  
//     } 
// }
     

function validatePhoto(obj, isShowError)
{
     var value = getValueFromId(obj.ID);
     if(isEmpty(value)) 
     {   if(isShowError) {
        showErrorDiv(obj, true);
     }
        return false;
     }
     var fileUpload = value;
     var extension = fileUpload.substring(fileUpload.lastIndexOf('.') + 1);
     //checking below extentions for photos
     if(extension == "gif" || extension == "GIF" || extension == "png" || extension == "PNG" || extension == "JPEG" || extension == "jpeg" || extension == "jpg" || extension == "JPG")
     {
         return true;
     } 
    else
    {
        if(isShowError) {
        document.getElementById(obj.ERROR_DIV_ID).innerHTML = "Please upload valid Image. Only JPEG/JPG/PNG/GIF file is allowed ";
        document.getElementById(obj.ID).style.borderColor="red";
        document.getElementById(obj.ID).focus();
        }
         return false;
     }         
}
   
function validateusernamepassword(obj, isShowError)
{
if(isEmpty(document.getElementById(obj.ID).value.trim()) == false)
    {
         return true;  
    }  
    else  
    {  
         if(isShowError) {
        showErrorDiv(obj, true);
        }
        return false;  
    } 
}

function validateAmount(obj, isShowError)
{
//window.alert("validate number inside");
     var value = getValueFromId(obj.ID);
     console.log(value);
    if(isValidAmount(value))
    {
        return true;  
    }  
    else  
    {  
    console.log("inside else".value);
        if(isShowError) {
        showErrorDiv(obj, false);
        }
        return false;  
    }  
}

function validateSKU(obj, isShowError)
{
  var value = getValueFromId(obj.ID);
     console.log(value);
     if(value.length == 6)
     {
     
    if(isSKU(value))
    {
        return true;  
    }  
    else  
    {
        if(isShowError) {
        showErrorDiv(obj, false);
        }
        return false;  
    }
    }
    else
    {
    if(isShowError) {
        showErrorDiv(obj, false);
        }
        return false;  
    }  
}



     /*Helper Functions*/ 
function isEmpty(value)
{
    if(value !="")
    {
        return false;
    }
    else 
    {
       return true;
    }
    }

function isValidAmount(value)
{
    var amountExpression = /^\d*[.]?\d+$/;
    return value.match(amountExpression); 
}  

function isNumber(value)
{
    var numberExpression = /^[0-9]+$/;
    return value.match(numberExpression); 
}  
 
     
function isText(value)
{
    var textExpression=/^[a-zA-Z]+$/;
    return value.match(textExpression);
}

function isSKU(value)
{
    var SKUExpression= /^[a-zA-Z]{3}[0-9]{3}$/;
    return value.match(SKUExpression);
}
     
    //clear all red borders and error messages.
function clearAllErrorMessages() 
{
    clearAllErrors();
    clearAllErrorBorder();
}
     
function clearAllErrorBorder() 
{
     for(var i=0; i<infoArray.length; i++) 
     {
        clearError(infoArray[i]);
    }
}
     
function clearError(obj) 
{
clearAllErrors();
var id = obj.ID;
        if(id == "inlineDiv") 
        {
            document.getElementById(obj.ID).style.borderColor="#ffffff";
        } 
        else 
        {
            document.getElementById(obj.ID).style.borderColor="#dddddd";
        }
}

function clearAllErrors() 
{
document.getElementById("error_message").innerHTML = "";
}
       
function getValueFromId(id) 
{
    return document.getElementById(id).value.trim();
}
     
function showErrorDiv(obj, isEmpty)
{
    if(isEmpty) 
    {
        if(obj.TYPE == inputType.PHOTO) 
        {
            document.getElementById(obj.ERROR_DIV_ID).innerHTML = obj.ERROR;
        } 
        else 
        {
            document.getElementById(obj.ERROR_DIV_ID).innerHTML = 'Please enter ' + obj.NAME;
        }
    } 
    else 
    { 
        document.getElementById(obj.ERROR_DIV_ID).innerHTML = obj.ERROR; 
    }
    document.getElementById(obj.ID).style.borderColor="red";
    document.getElementById(obj.ID).focus();
}
    
    