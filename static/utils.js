function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function postNews() {

    var data = {
    'title': document.getElementById('title').value,
    'author': document.getElementById('author').value,
    'tags': document.getElementById('tags').value,
    'body': document.getElementById('body').innerHTML
    }

    console.log(data);

    post('/save_news', data);


}


function httpGet(theUrl)
{
    var response;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, true ); //true == async
    xmlHttp.onreadystatechange=function() {
        if (xmlHttp.readyState==4 && xmlHttp.status==200) {
        response = xmlHttp.responseText;
        alert(response);
        } else if(xmlHttp.readyState==4 && xmlHttp.status!=200) {
        response = 'An error occured';
        alert(response);
        }
    }
    xmlHttp.send(null);
}

var hidden = true;
function hideComments() {
    //httpGet('/logout');
    if (hidden) {
        $('.comments').show();
        $('.btn-hide-comments').text('HIDE COMMENTS');
    } else {
        $('.comments').hide();
        $('.btn-hide-comments').text('SHOW COMMENTS');
    }
    hidden = !hidden;
    console.log(hidden);
}

$(document).ready(function(){

console.log('document ready');


});