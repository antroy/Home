index= '''  
<html>
    <head>
     <title>$info['title']</title>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
     <link href="${context}/index.css" rel="stylesheet" type="text/css"/>
     <script language="javascript" type="text/javascript">
     img_arr = $imagearray;
     
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
       #for $i, $folder in enumerate($folders)
	   <a href="${folder['dir']}" class="${('odd', 'even')[i%2]}">
         $folder['name']
       </a>
	   #end for
	#if $parent_name
        <hr/>
        <a href="${parent}" class="parent_link"><span>Back to</span> ${parent_name}</a>
    #end if
    #if $admin_url
        <span class="divider">
            <a href="${admin_url}">Back to Admin Page</a>
        </span>
    #end if
	</div>
    
	<div id="preview">
    #if $initialimage
	    <img name="previewImage" alt="Photograph Preview" 
            title="Photograph Preview" src="${initialimage}" />
    #end if
        </div>
   <div id="content">
     <h1>$info['title']</h1>
      <div id="description">
        #for $para in $info['description']
        <p>$para</p>
        #end for
	</div>
      #if $image_triples
      <div id="photos">
      <h2>Photos</h2>
      
      <ul>
        #for $triple in $image_triples
         <li>
	     <a href="${triple['imageurl']}" onmouseover="swap('${triple['thumburl']}')">
	       $triple['description']
	     </a>
         </li>
        #end for
      </ul>
      </div>
      #end if

      #if $movies
      <div id="movies">
      <h2>Movies</h2>
      <ul>
         #for $movie in $movies 
         <li>
	     <a href="$movie['url']">
	       $movie['description']
	     </a>
         </li>
         #end for
      </ul>
      </div>
      #end if
    </div>
    </body>
  </html>
'''    

slideshow= '''  
<html>
    <head>
     <title>$info['title']</title>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
     <link href="${context}/index.css" rel="stylesheet" type="text/css"/>
     <script language="javascript" type="text/javascript">
     img_arr = $imagearray;
     
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
	<div id="menu" style="top:5px!important" >
     <div id="menu_heading">Other Albums</div>
       #for $i, $folder in enumerate($folders)
	   <a href="${folder['dir']}" class="${('odd', 'even')[i%2]}">
         $folder['name']
       </a>
	   #end for
	#if $parent_name
        <hr/>
        <a href="${parent}" class="parent_link"><span>Back to</span> ${parent_name}</a>
    #end if
    #if $admin_url
        <span class="divider">
            <a href="${admin_url}">Back to Admin Page</a>
        </span>
    #end if
	</div>
    </div>

   <div id="content">
    <h3>${image_triples[$slide_no]['description']}</h3>
    <div id="photo_frame">
        <img src="${image_triples[$slide_no]['imageurl']}"/>
    </div>
    </div>
    
    </body>
  </html>
'''    

upload_template = '''
<html xmlns:py="http://purl.org/kid/ns#">
   
    <head>
     <title>Gallery Administration Page.</title>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
     <link href="${gallery_context}/upload.css" rel="stylesheet" type="text/css"/>
    </head>
   
    <body>
    <div id="top">
    <h2>Gallery Administration Page.</h2>
    <p>Hi ${user}!</p>
    <p>
    The list below shows your gallery folder tree - add new subfolders and view galleries using the links next to the folders. Upload and delete photos and update folder information by clicking on the Edit link.
    </p>
    #if $errors
    <div id="errors">
        <p>The following errors occurred:</p>
        #for $i, $error in enumerate($errors)
        <p class="error">${'%i) %s' % ($i + 1, $error)}</p>
    </div>
    #end if

    #if $messages
    <div id="messages">
        #for $i, $mssg in enumerate($messages)
        <p class="message">${'%i) %s' % ($i + 1, $mssg)}</p>
    </div>
    #end if
    </div>
    
    #def display_tree($node)
      <ul class="treeList">
         <li>
         <span class="edit_folder_link">${node.path}</span>
            (<a href="${node.contextpath}">Edit</a> | 
            <a href="${gallery_context}/${node.fullpath}?admin_url=${admin_context}/index.html">View</a> | 
            <a href="${node.contextpath}/_">New Subfolder</a>)
             #for $child in $node.children
                $display_tree($child)
             #end for
         </li>
      </ul>
    #end def
          
      <div id="treepanel" class="inner">
          $display_tree($root_node)
      </div>
        
    </body>
  </html>
'''
# TODO: Rework this as cheetah template.
edit_templ = '''

<html xmlns:py="http://purl.org/kid/ns#">
   
    <head>
     <title>Edit Folder "$folder".</title>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
     <link href="${gallery_context}/upload.css" rel="stylesheet" type="text/css"/>
     
     <script type="text/javascript">
     
        tabs = ['photo_add_delete_tab', 'details_tab'];
     
        function activate(tab) {
            node = document.getElementById(tab);
            node.style.display='block';
            
            for (i = 0; i &lt; tabs.length; i++) {
                if (tabs[i] != tab){
                    node = document.getElementById(tabs[i]);
                    node.style.display='none';
                }
            }
            
        }
     
     </script>
     
    </head>
   
    <body>
    <div id="header"><a href="index.html">Folder Index</a> | <a href="${gallery_context}/${folder}?admin_url=${admin_context}/${folder}">View Folder</a></div>
    
    <div id="errors" py:if="errors">
        <p>The following errors occurred:</p>
        <p class="error" py:for="i, error in enumerate(errors)" py:content="'%i) %s' % (i + 1, error)">
        Error message.
        </p>
    </div>
    
    <div id="messages" py:if="messages">
        <p class="message" py:for="i, mssg in enumerate(messages)" py:content="'%i) %s' % (i + 1, mssg)">
        Message.
        </p>
    </div>

    <div id="tab_panel">    
    
    <div id="tab_button_panel">
    <a href="javascript:activate('details_tab')">Edit Details</a>
    <a href="javascript:activate('photo_add_delete_tab')">Add/Delete Photos</a>
    <a href="javascript:activate('reorganise_tab')">Reorganise Album</a>
    </div>
    
    <div id="details_tab">
    <h3>Edit Folder Details</h3>
    <form name="edit_form" action="" method="post">

    <table>
    <tr>
        <td width="30%">Folder Name: </td><td><input class="text" type="text" name="folder_name" value="${folder_name}" /></td>
    </tr>
    <tr>
        <td>Page Title: </td><td><input class="text" type="text" name="title" value="${title}" /></td>
    </tr>
    <tr>
        <td colspan="2">Description:</td>
    </tr>
    <tr>
        <td colspan="2">
            <textarea name="description" py:content="description">
            Content Here.
            </textarea>
        </td>
    </tr>
    </table>
    
    <input type="hidden" name="action" value="update" />
    
<?python
update_button_text = "Update Details"
if not folder:
    update_button_text = "Add Folder"
?>
    
    <input type="submit" value="${update_button_text}"/>
    </form>
    </div>
    
    <div id="photo_add_delete_tab" py:if="is_empty != None">
    
    <div id="bottom_left_panel">
    <h3>Upload Photographs</h3>
    
    <form name="upload_form" action="" method="post" enctype="multipart/form-data">
    <input type="hidden" name="action" value="upload" />
    
    <input name="u" type="file"/><br/>
    <input name="u" type="file"/><br/>
    <input name="u" type="file"/><br/><br/>
    
    <input value="Upload Photo's" type="submit"/>
    </form>
    </div>
    
    <div id="bottom_right_panel">
    <div py:if="len(files) > 0">
    <h3>Delete Photographs</h3>
    <form name="delete_form" action="" method="post" py:if="len(files) > 0">
        <div id="file_list">
            <span py:strip="True" py:for="file in files">
            <input name="file" type="checkbox" value="${file}"/> ${file}<br />
            </span>
        </div>
        <input type="hidden" name="action" value="delete" />
        <br/>
        <input type="submit" value="Delete Selected" />
    </form>
    </div>
    </div>
    </div>
    
    <div id="reorganise_tab">
    Reorganise your albums.
    <div  py:if="is_empty and parent">
    <form name="delete_page_form" action="upload.html" method="post">
    <input type="hidden" name="action" value="delete_folder" />
    <input type="submit" value="Delete this folder"/>
    </form>
    </div>
    
    </div>
    
    </div>
    </body>
  </html>
'''
