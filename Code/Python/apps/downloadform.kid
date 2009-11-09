<html xmlns:py="http://purl.org/kid/ns#">
<head>
     <title></title>
</head>
<body>
     <h1>Download Manager</h1>
     The following url's are scheduled for download (in order of priority):<br/>
    <br/>
        <form method="post" action="/apps/downloadqueue/delete_url" name="download_form">
    <ol>
        <li py:for="data in url_list">
            <input name="url" value="${data[0]}" type="checkbox"/>
            <span py:replace="'%s (%s)' % data "> URL (status)</span>
        </li>
    </ol>
    <br/>
    <input name="delete" value="Delete Selected" type="submit"/></form>
    <form method="post" action="/apps/downloadqueue/add_url" name="add_url_form"><input name="new_url"/><br/>
    <input name="add" value="Add URL" type="submit"/></form>
  </body>
</html>
                        
