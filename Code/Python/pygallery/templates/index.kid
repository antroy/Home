  <html xmlns:py="http://purl.org/kid/ns#">
    <head>
     <title py:content="info['title']">Photo's and Stuff.</title>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
     <link href="${context}/index.css" rel="stylesheet" type="text/css"/>
     <script language="javascript" type="text/javascript">
     img_arr = <span py:replace="imagearray">[]</span>;
     
     var i = 0;
     var image = new Image();

     for (i = 0; img_arr.length > i ; i++){
        image.src = img_arr[i];
     }
     
     function swap(new_src){
        document.previewImage.src = new_src
     }
     </script>
    </head>
   
    <body>
	<div id="menu">
     <div id="menu_heading">Other Albums</div>
    <span py:for="i, folder in enumerate(folders)" py:strip="True">
	<a href="${folder['dir']}" class="${('odd', 'even')[i%2]}"><span py:replace="folder['name']">Folder Name</span></a>
	</span>
	<div py:strip="True" py:if="parent_name">
        <hr/>
        <a href="${parent}" class="parent_link"><span>Back to</span> ${parent_name}</a>
    </div>
    <div py:strip="True" py:if="admin_url">
        <span class="divider">
            <a href="${admin_url}">Back to Admin Page</a>
        </span>
    </div>
	</div>
    
	<div id="preview">
	    <img name="previewImage" alt="Photograph Preview" 
            title="Photograph Preview" src="${initialimage}" py:if="initialimage"/>
        </div>
   <div id="content">
     <h1 py:content="info['title']">Kids Photos and Movies</h1>
      <div id="description">
        <p py:for="para in info['description']" py:content="para">
	  Description here.
	</p>
	</div>

      <div id="photos" py:if="len(image_triples) > 0" >
      <h2>Photos</h2>
      
      <ul>
         <li py:for="triple in image_triples">
	     <a href="${triple['imageurl']}" onmouseover="swap('${triple['thumburl']}')">
	       <span py:replace="triple['description']">Description here</span>
	     </a>
	 </li>
      </ul>
      </div>

      <div id="movies" py:if="len(movies) > 0" >
      <h2>Movies</h2>
      <ul>
         <li py:for="movie in movies">
	     <a href="${movie['url']}">
	       <span py:replace="movie['description']">Description here</span>
	     </a>
	 </li>
      </ul>
      </div>
    </div>
    </body>
  </html>
    

