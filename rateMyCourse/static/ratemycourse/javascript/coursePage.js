'use strict'

var sNum = 3;

function setScores(scores) {
    var tables = document.getElementsByClassName("rating");
    for (var i = 0; i < sNum; i++) {
        var lis = tables[i].getElementsByTagName("i");
        for (var j = 0; j < scores[i]; j++) {
            lis[j].setAttribute("class", "fa fa-star");
        }
    }
}

function generateGrid(imageUrls, text, headline) {
        var ScreenGridHtml = `
            <tr>
                <td><img></td>
                <td>
                    <table>
                        <tr><h1></tr>
                        <tr><p></tr>
                        <tr>
                            <div>
                                <img>
                                <img>
                                <img>
                            </div>
                        </tr>
                    </table>
                </td>
            </tr>
        `;
        // create div
        var commentGrid = document.createElement("table");
        commentGrid.id = "commentGrid";
        commentGrid.innerHTML = ScreenGridHtml;
        //insert user image
        var imageTag = commentGrid.getElementsByTagName("img");
        imageTag[0].src = imageUrls;
        imageTag[0].width = "150";
        imageTag[0].setAttribute("class", "img-fluid d-block mb-5 m-5");
        // insert headLine
        var headlineTag = commentGrid.getElementsByTagName("h1");
        var node1 = document.createTextNode(headline);
        headlineTag[0].appendChild(node1);
        headlineTag[0].setAttribute("class", "display-5 mb-4 text-dark");
        //insert text
        var textTag = commentGrid.getElementsByTagName("p");
        var node = document.createTextNode(text);
        textTag[0].appendChild(node);
        textTag[0].setAttribute("class", "lead mb-5 text-dark");
        // insert icons
        imageTag[1].src = "../../static/ratemycourse/images/store.png";
        imageTag[2].src = "../../static/ratemycourse/images/feedback.png";
        imageTag[3].src = "../../static/ratemycourse/images/more.png";

        var trTags = commentGrid.getElementsByTagName("tr");
        trTags[0].setAttribute("class", "commentTr");
        trTags[0].setAttribute("style", "background:#FFF; color:#FFF");
       
        var tdTags = commentGrid.getElementsByTagName("div");
       // tdTags[2].align = "right";
        //tdTags[3].align = "right";
    //tdTags[4].align = "right";
        tdTags[0].setAttribute("style", "float:right");
        
        return commentGrid;
}

function setComments(){//get comments list from service
	$.ajax('/getComment', {
		dataType: 'json',
		data: {'course_number': $('#courseNumber').text()},
	}).done(function(data){
    	var imgurl = "../../static/ratemycourse/images/user.png";
    	var headLine = "Image and gradient intro";
    	var text = "Get a fluid web page working on all devices with the Bootstrap 4 grid system.";
    	var parents = document.getElementById("commentDiv");
    	var comment = document.getElementById("commentGrid");
    	if (comment) {
    	    parents.removeChild(comment);
    	}
    	for(var i = 0; i < data.comments.length; i++){
    	    //generate a new row
    	    var Grid=generateGrid(imgurl, data.comments[i].content, data.comments[i].username);
    	    //insert this new row
    	    parents.appendChild(Grid);
    	    var br = document.createElement("br");
    	    parents.appendChild(br);
    	}
	})
}


$(document).ready(function(){
	//var scores = {{score_list|safe}};
	$.ajax('/getOverAllRate', {dataType: 'json', data: {'course_number': $('#courseNumber').text()}, }).done(function(data){
		setScores(data.rate)
	})
	//var userimg = {{userimg_list}};
	//var text = {{text_list}};
	//var headLine = {{headLine_list}};
	setComments();
	document.getElementById("toComment").onclick = function () { console.log("cliked");; }// turn to the page of grading
})