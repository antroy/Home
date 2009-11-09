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
    

