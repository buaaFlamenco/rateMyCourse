'use strict'
function ccomments(node,j){
    console.log(node.id);
    var c =  node.getElementsByTagName("ul");
    if(c.length!=0){
        node.removeChild(c[0]);
        if(j==1) return;
    }
    var ulnode = document.createElement("ul");
    node.appendChild(ulnode);
    ulnode.setAttribute("class","list-group");
    ulnode.setAttribute("style","margin-top:32px");
    var lnode1 = document.createElement("li");
    ulnode.appendChild(lnode1);
    lnode1.setAttribute("class","list-group-item");
    var divnode = document.createElement("div");
    lnode1.appendChild(divnode);
    divnode.setAttribute("style","width:100%");
    //textarea
    var inputnode = document.createElement("textarea");
    divnode.appendChild(inputnode);
    inputnode.setAttribute("class", "texta");
    //submit
    var cfmnode = document.createElement("button");
    divnode.appendChild(cfmnode);
    cfmnode.setAttribute("class", "cfmbutton");
    var btnnode = document.createTextNode("发送");
    cfmnode.setAttribute("onclick", "cfmclick(this)");
    cfmnode.appendChild(btnnode);
    $.ajax('/getDiscuss', {
        dataType: 'json',
        data: {'iId': node.id},
    }).done(function(data){
        for(var i=0; i< data.discusses.length; i++){
            var dis = data.discusses[i];
            var lnode1 = document.createElement("li");
            //time
            var tdivnode = document.createElement("div");
            lnode1.appendChild(tdivnode);
            tdivnode.setAttribute("style", "float:right");
            var tNode = document.createTextNode(dis.time);
            tdivnode.appendChild(tNode);
            //username
            var ndivnode = document.createElement("div");
            lnode1.appendChild(ndivnode);
            ndivnode.setAttribute("style", "float:left;margin-right:16px");
            var nNode = document.createTextNode(dis.userName);
            ndivnode.appendChild(nNode);
            //text
            var cdivnode = document.createElement("div");
            lnode1.appendChild(cdivnode);
            cdivnode.setAttribute("style", "float:left");
            var cNode = document.createTextNode(dis.text);
            cdivnode.appendChild(cNode);

            ulnode.appendChild(lnode1);
            lnode1.setAttribute("class","list-group-item");
        }
    })
}
function cfmclick(node){
  if($.cookie('username') == undefined){
    alert("please log in first!");
    return false;
  }
  var id = $(node).parents(".commentGrid").attr("id");
  var text = $(node).prev().val();
  if(text==null){
    alert("please enter words!");
    return false;
  }
  $.ajax("/submitDiscuss/", {
    dataType: 'json',
    type: 'POST',
    traditional: true,
    data: {
      'username': $.cookie('username'),
      'discuss': text,
      'comment_id': id,
    }
  }).done(function (data) {
    if(data.statCode == 0){
      alert("your comment submited succesfully!");
      ccomments($(node).parents(".commentGrid")[0], 0);
    }
    else {
      alert(data.errormessage);

    }
  });
}
function generateGrid(imageUrls, userName, iTerm, iTeacher, iToal, text, time, commentid) {
    var ScreenGridHtml = `
        <div>
            <img>
            <p>
        </div>
            <table>
                <tr>
                    <td><p></td>
                    <td><p></td>
                    <td><p></td>
                </tr>
                <tr>
                    <td><p></td>
                    <td><p></td>
                    <td><p></td>
                </tr>
            <table>
        <div>
            <p>
        </div>
        <div>
            <a>
            <a>
            <a>
            <a>
            <a>
            <p>
        </div>
        <div>
        <br/>
        <br/>
        <br/>
        `;

        // create div
        var commentGrid = document.createElement("div");
        commentGrid.setAttribute("class", "commentGrid");
        commentGrid.id = commentid;
        commentGrid.innerHTML = ScreenGridHtml;
        //insert user image and name
        var imageTag = commentGrid.getElementsByTagName("img");
        imageTag[0].src = imageUrls;
        imageTag[0].width = "86";
        imageTag[0].height = "86";
        imageTag[0].setAttribute("style", "margin-bottom:16px;margin-top:16px");

        var pTags = commentGrid.getElementsByTagName("p");
        var userNameNode = document.createTextNode(userName);
        pTags[0].appendChild(userNameNode);
        pTags[0].setAttribute("class", "userName");

        // insert information
        var term = document.createTextNode("学期");
        var teacher = document.createTextNode("上课老师");
        var total = document.createTextNode("总评");
        var vTerm = document.createTextNode(iTerm);
        var vTeacher = document.createTextNode(iTeacher);
        var vTotal = document.createTextNode(iToal.toFixed(1));
        pTags[1].appendChild(term);
        pTags[2].appendChild(teacher);
        pTags[3].appendChild(total);
        pTags[4].appendChild(vTerm);
        pTags[5].appendChild(vTeacher);
        pTags[6].appendChild(vTotal);

        //insert text
        pTags[7].innerHTML = text;
        pTags[7].setAttribute("style", "margin-top:16px;text-align:left; width:70%")
        //inset time
        var timenode = document.createTextNode(time);
        pTags[8].appendChild(timenode);
        pTags[8].setAttribute("style", "float:left;text-align:left;margin-top:32px")
        //ccomment
        var aTags =  commentGrid.getElementsByTagName("a");
        var cnode = document.createTextNode("评论");
        aTags[0].appendChild(cnode);
        aTags[0].setAttribute("style", "float:right;text-align:right;margin-top:32px;margin-right:16px;");
        aTags[0].setAttribute("class", "comments");
        aTags[0].setAttribute("href", "#");
        aTags[0].setAttribute("onclick", "ccomments(this.parentElement.parentElement, 1)");
        var dnode = document.createTextNode("删除");
        aTags[1].appendChild(dnode);
        aTags[1].setAttribute("href", "#");
        aTags[1].setAttribute("style", "float:right;text-align:right;margin-top:32px;margin-right:16px; display:none");
        aTags[1].setAttribute("class", "delete");
        aTags[1].setAttribute("onclick", "del(this)");

        var chnode = document.createTextNode("修改");
        aTags[2].appendChild(chnode);
        aTags[2].setAttribute("href", "#");
        aTags[2].setAttribute("style", "float:right;text-align:right;margin-top:32px;margin-right:16px; display:none");
        aTags[2].setAttribute("class", "change");
        aTags[2].setAttribute("onclick", "changeclick(this)");

        var anode = document.createElement("i");
        anode.setAttribute("class", "fa fa-thumbs-o-up");
        aTags[3].appendChild(anode);
        aTags[3].setAttribute("style", "float:right;margin-top:32px;margin-right:16px;");
        aTags[3].setAttribute("class", "good");
        aTags[3].setAttribute("onclick", "gclick(this)");
        

        //css
        var divTags = commentGrid.getElementsByTagName("div");
        divTags[0].setAttribute("class", "row text-center");
        divTags[1].setAttribute("class", "row text-center");
        divTags[2].setAttribute("class", "text-center");
        divTags[0].setAttribute("style", "width:70%;border-bottom:1px #e4e4e4 solid;");
        divTags[3].setAttribute("style", "width:100%;border-bottom:1px #e4e4e4 solid;");
        var tableTag = commentGrid.getElementsByTagName("table");
        tableTag[0].setAttribute("style", "width:70%; margin-top:16px;border-bottom:1px #e4e4e4 solid");
        return commentGrid;
}

function setComments() {//get comments list from service
    if($.cookie('username') == undefined){
        $.ajax('/getComment', {
            dataType: 'json',
            data: {
                'course_number': window.location.pathname.split('/')[2]
            },
        }).done(function(data){
            var imgurl = "../../static/ratemycourse/images/user.png";
            var parents = document.getElementById("commentDiv");
            var child = parents.children;
            if(child.length!=0){
               $("#commentDiv").empty();
            }
            for(var i=0; i<data.comments.length; i++){
                //generate a new row
                var cmt = data.comments[i]
                var Grid = generateGrid(imgurl, cmt.userName, cmt.iTerm, cmt.iTeacher, cmt.iTotal, cmt.text, cmt.time, cmt.iId);
                //insert this new row
                parents.appendChild(Grid);
            }
        })
    }else{
        $.ajax('/getComment', {
            dataType: 'json',
            data: {
                'course_number': window.location.pathname.split('/')[2],
                'username': $.cookie('username'),
            },
        }).done(function(data){
            var imgurl = "../../static/ratemycourse/images/user.png";
            var parents = document.getElementById("commentDiv");
            var child = parents.children;
            if(child.length!=0){
               $("#commentDiv").empty();
            }
            for(var i=0; i<data.comments.length; i++){
                //generate a new row
                var cmt = data.comments[i]
                var Grid = generateGrid(imgurl, cmt.userName, cmt.iTerm, cmt.iTeacher, cmt.iTotal, cmt.text, cmt.time, cmt.iId);
                //insert this new row
                parents.appendChild(Grid);
                //show delete
                if(cmt.isSelf==1){
                    Grid.getElementsByClassName('delete')[0].style.display='block';
                    Grid.getElementsByClassName('change')[0].style.display='block';
                }
            }
        })
    }

}
function del(node){
   var id = node.parentElement.parentElement.id;
   console.log(id);

   $.ajax("/delComment/", {
    dataType: 'json',
    type: 'POST',
    traditional: true,
    data: {
      'comment_id': id,
      'password':$.cookie('password'),
    }
  }).done(function (data) {
    if(data.statCode == 0){
     setComments();
    }
    else {
      alert(data.errormessage)
    }
  })
  }
 function changeclick(node){
   var id = node.parentElement.parentElement.id;
   console.log(id);
   window.location.href="/addComment/"+id;
  }
 function gclick(node){
  var id = node.parentElement.parentElement.id;
  $.ajax('/changeSupport/', {
            dataType: 'json',
            type: 'POST',
            traditional: true,
            data: {
                'comment_id': id,
                'username':$.cookie('username'),
                'password':$.cookie('password')
            },
   }).done(function(data){
        $("i").animate({
            //height:'+=16px',
            //width:'+=16px'
            fontSize:'+=8px'
        },"fast");
        $("i").animate({
           // height:'-=16px',
            //width:'-=16px'
            fontSize:'-=8px'
        },"fast");
   })
}
$(document).ready(function () {
    // Form validation for Sign in / Sign up forms
    validateSignUp()
    validateSignIn()

    // Login widget set according to cookie
    setCookie()

  ////////// csrf set up //////////
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
          }
      }
  });
  /////////////////////////////////


    // $.ajax('/getOverAllRate', {
    // 	dataType: 'json',
    // 	data: {
    // 		'course_number': $('#courseNumber').text()
    // 		 },
    // 	}).done(function (data) {
    //     setScores(data.rate)
    // })
    setComments();
})
