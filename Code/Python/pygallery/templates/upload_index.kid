<html xmlns:py="http://purl.org/kid/ns#">
   
    <head>
     <title>Gallery Administration Page.</title>
     <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
     <link href="${gallery_context}/upload.css" rel="stylesheet" type="text/css"/>
    </head>
   
    <body>
    <div id="top">
    <h2>Gallery Administration Page.</h2>
    <p>
    Hi <span py:replace="user"></span>!
    </p>
    <p>
    The list below shows your gallery folder tree - add new subfolders and view galleries using the links next to the folders. Upload and delete photos and update folder information by clicking on the Edit link.
    </p>
    
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
    </div>
    
      <ul py:def="display_tree(node)" class="treeList">
         <li>
         <span class="edit_folder_link">${node.path}</span>
            (<a href="${node.contextpath}">Edit</a> | 
            <a href="${gallery_context}/${node.fullpath}?admin_url=${admin_context}/index.html">View</a> | 
            <a href="${node.contextpath}/_">New Subfolder</a>)
         <div py:for="child in node.children" py:replace="display_tree(child)" />
         </li>
      </ul>
          
      <div id="treepanel" class="inner" py:content="display_tree(root_node)">
         Key/Value Table replaces this text
      </div>
        
    </body>
  </html>
    

