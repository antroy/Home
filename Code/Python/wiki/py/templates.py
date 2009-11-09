import os.path as path, adapter
from Cheetah.Template import Template

main = """
<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <title>$title</title>
    <link rel="stylesheet" href="StyleSheet?action=raw" type="text/css" />
  </head>
  <body>
    <div id="header">
       <div id="trail">
         $trail
       </div>
       <div id="edit">
       <a  href="${title}?action=edit" accesskey="E">Edit</a> | 
       <a  href="${title}?action=history" accesskey="H">History</a>
       </div>
    </div>
    <div id="sidebar">
        <div>
            $sidebar
        </div>
        <br/>
        #if $version
          <a class="wikilink" href="${title}?action=rollback&#38;version=$version">Rollback</a>
          <br/>
          <a class="wikilink" href="${title}">Latest Version</a>
        #end if
    </div>

    <div id="main">
       <h1>$title</h1>
       <div id="content">$text_content</div>
       <div id="timestamp">Last update: $last_modified</div>
   </div>
  </body>
</html>                  
"""

edit = """
<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <title>Edit Page: $title </title>
    <link rel="stylesheet" href="StyleSheet?action=raw" type="text/css" />
</head>

<body onload="document.edit_form.new_details.focus()">
 <form name="edit_form" method="post" action="$title">
  <h2>Editing Page: $title </h2>
  <div>
   <input id="title" name="title" type="hidden" value="$title" />
   <textarea name="new_details"  rows="25" cols="70" tabindex="1">$text_content</textarea>
  </div>
  <div>
   <input type="submit" value="Save" accesskey="S" tabindex="2" />
  </div>
</form>
</body>
</html>
"""

history_templ = """
<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <title>Page History: $title</title>
    <link rel="stylesheet" href="StyleSheet?action=raw" type="text/css" />
</head>

<body>
<h1>Page History: $title</h1>
<table id="historytable">
<tr><th>Version</th><th>Date Created</th><th></th></tr>
#for $version in $versionlist
    <tr>
        <td>$version.version</td>
        <td>$version.date</td>
        <td><a class="historylink" 
            href="${title}?action=viewhistory&#38;version=$version.version">view</a>
        </td>
    </tr>
#end for
</table>
</body>
</html>
"""

def main_template(title, content, modified, trail="", sidebar="", version=""):
    main_template = Template(source=main)
    main_template.title = title
    main_template.text_content = content
    main_template.last_modified = modified
    main_template.trail = trail
    main_template.sidebar = sidebar
    main_template.version = version

    return str(main_template)

def view_history_template(title, content, date, version):
    return main_template(title, content, date, version=version)
    
def edit_template(title, content):
    edit_template = Template(source=edit)
    edit_template.text_content = content
    edit_template.title = title
    
    return str(edit_template)

def history_template(title, history):
    history_template = Template(source=history_templ)
    history_template.versionlist = history
    history_template.title = title
    
    return str(history_template)

